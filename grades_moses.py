import numpy as np
import os
import pandas as pd


def enter_grades(df_moses_final, homework_number, df_online_ha, online):
    """
    Parameters
    ----------
    df_moses_final : Pandas DataFrame
        dataframe containing the configured groups + emails.
    homework_number: int
        the number of the homework
    df_online_ha : Pandas DataFrame
        dataframe containg the online grades from the csv file downloaded from ISIS
    online: bool
        flag to indicate if the homeworks have an online part on ISIS 
    Returns
    -------
    df_moses_hausaufgabe : Pandas DataFrame
        dataframe containg the students + the homework grade + online homework grade + total
    """   
    
    
    df_moses_hausaufgabe = df_moses_final.copy()   
    if online:
        df_online_hausaufgabe = df_online_ha.copy()   
        # delete the last row containing the Gesamtdurchschnitt
        df_online_hausaufgabe = df_online_hausaufgabe.drop([len(df_online_hausaufgabe) - 1])
        df_online_hausaufgabe = df_online_hausaufgabe.replace({'-': np.nan})
        # cast the Bewertung column (containing the online note) to float 
        for column in df_online_hausaufgabe.columns:
            if 'Bewertung' in column:
                df_online_hausaufgabe[column] = df_online_hausaufgabe[column].astype(str).str.replace(',', '.').astype(float)
                df_online_hausaufgabe.rename(columns={column: 'Online'}, inplace=True)
            
    # adding columns to df_moses_hausaufgabe
    if 'Gesamt' not in df_moses_hausaufgabe.columns:
        df_moses_hausaufgabe['Gesamt'] = ''
        df_moses_hausaufgabe['Schriftlich'] = ''
        df_moses_hausaufgabe['Online'] = ''
    
    groups_without_grade = list(set(df_moses_hausaufgabe['Gruppe']))
    if '' in groups_without_grade:
        groups_without_grade.remove('')
    
    groups = groups_without_grade.copy()
    while True:
        print('__________________________________________________________________________\n'
              'Type quit to exit\n'
              'Type show to show the groups with the associated grade\n'
              'Type showng to show the groups still without a grade\n')
            
        group_input = str(input('Gruppe: ')).strip()
        if not group_input:
            print('No group was selected!')
            continue

        if group_input == 'quit':
            prompt = input('Quit enter grades. Proceed (y/[n])? ').strip()
            if prompt == 'y':
                break
        
            continue
        
        if group_input == 'show':
            for group in list(set(groups) - set(groups_without_grade)):
                grade = df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Gruppe'] == group, 'Schriftlich'].values[0]
                print(f'Gruppe: {group} -> Note: {grade}')
            
            continue

        if group_input == 'showng':
            print(f'groups without grade -> {groups_without_grade}')
            continue
        
        if group_input not in df_moses_hausaufgabe['Gruppe'].values:
            print(f'the group {group_input} was not found!')
            continue

        # extract the names and emails of students from the selected group
        if group_input in groups_without_grade:
            groups_without_grade.remove(group_input)
        
        else:
            print(f'\nWARNING! the group {group_input} already recieved a grade!\n'
                  'The old grade will be overwritten!')
            
        names_emails_selected = df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Gruppe'] == group_input, ['Name', 'Email']]
        print(f'\nGruppe: {group_input} --> {names_emails_selected.Name.values}')        
        try:
            note_input = float(input('Note: '))
            
        except ValueError:
            print('invalid input for Note!')
            continue
        
        df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Gruppe'] == group_input, 'Schriftlich'] = note_input
        if online:
            # extract the online note of students from the selected group and put it in the Online column of df_moses_hausaufgabe
            for ind, email in enumerate(names_emails_selected['Email']):
                online_note = df_online_hausaufgabe.loc[df_online_hausaufgabe['E-Mail-Adresse'] == email, 'Online'].values
                if online_note.size:
                    df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Email'] == email, 'Online'] = online_note[0]
                    print(f'{names_emails_selected.Name.values[ind]} --> online Note: {online_note[0]}')
                
                else:
                    # the online note of the student was not found! 
                    df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Email'] == email, 'Online'] = 0.0        
                    name_student = names_emails_selected['Name'].values[ind]
                    email_student = names_emails_selected['Email'].values[ind]
                    print(f'\n\nName: {name_student}\nEmail: {email_student}\n--> online Note: 0 -> !!! NOT FOUND -> '
                          f'PLEASE VERIFY THE GRADE AND EMAIL MANUALLY in HA{homework_number}.csv !!!\n'
                          '--> Update the email with add_remove_moses.py later if necessary!)\n')
                    
                    if 'tu-berlin' not in email_student:
                        print(f'!!! WARNING !!!\n The email "{email_student}" is not an official TU Berlin address '
                              f'and may need a change!!!\n Look carefully for "{name_student}" in HA{homework_number}.csv \n')
                        
                        while True:
                            prompt = str(input(f'\nWas the student "{name_student}" found (y/[n])? ')).strip()
                            if prompt == 'y':
                                print(f'{name_student}, Old Email: {email_student}')
                                new_email = str(input('New Email: ')).strip()
                                df_moses_final.loc[df_moses_final['Email'] == email_student, 'Email'] = new_email
                                online_note = df_online_hausaufgabe.loc[df_online_hausaufgabe['E-Mail-Adresse'] == new_email, 'Online'].values
                                df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Email'] == email, 'Online'] = online_note[0]
                                print(f'{names_emails_selected.Name.values[ind]} --> online Note: {online_note[0]}')
                                df_moses_final.to_pickle("./df_moses_final.pkl")  # Pandas Dataframe that can be exported to python 
                                df_moses_final.to_csv("./df_moses_final.csv", index=False)
                                break
                            
                            if prompt == 'n':
                                break
                            
                            print('Invalid input!')
                            continue
                
    # gesamt = online + schriftlich 
    columns = ['Gesamt', 'Schriftlich', 'Online']
    df_moses_hausaufgabe[columns] = df_moses_hausaufgabe[columns].apply(pd.to_numeric, errors='coerce', axis=1).fillna(0)
    df_moses_hausaufgabe['Gesamt'] = df_moses_hausaufgabe['Schriftlich'] + df_moses_hausaufgabe['Online']
    df_moses_hausaufgabe['Gruppe'].fillna('', inplace=True)
    while True:
        print('\n\nThe grades belong to which subject?\n\n'
              '1 --> Analysis I und Lineare Algebra\n2 --> Analysis II\n')
        
        try:
            subject_input = int(input('Subject: '))
            if subject_input == 1:
                homework = f'HA{homework_number}'
                break

            if subject_input == 2:
                homework = f'HA {homework_number}'
                break
        
            if subject_input not in [1, 2]:
                print('invalid input for subject!')
                continue

        except ValueError:
            print('invalid input for subject!')
            continue
        
    print('__________________________________________________________________________\n')
    for ind, name in enumerate(df_moses_hausaufgabe['Name']):
        if df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Name'] == name, 'Gruppe'].values[0]: 
            print("document.querySelector('input[title=\"", name, 
                  f' : Hausaufgaben - {homework}', "\"]').value = '",
                  df_moses_hausaufgabe.loc[ind, 'Gesamt'], "'", sep='')
    
    print('\n__________________________________________________________________________'
          f'\nFinished.\n\nTo upload the grades:\n'
          '1. Copy all the code starting with document.querySelector\n'
          f'2. Open the moses page for entering the grades of the Hausaufgabe {homework}\n'
          '3. right click anywhere in the page --> inspect --> console\n'
          '4. Paste the code into the console\n'
          '5. Press ENTER (the first time you will be asked for permission. Read the'
          ' message to give the necessary permission)\n'
          '__________________________________________________________________________\n\n'
          f'All the grades will be saved in the file --> HA{homework_number}_graded.csv '
          f'inside the directory --> HA{homework_number}_graded\n'
          '__________________________________________________________________________\n')
 
    if not os.path.isdir(f'./HA{homework_number}_graded/'):
        os.mkdir(f'./HA{homework_number}_graded/')
   
    df_moses_hausaufgabe.to_pickle(f'./HA{homework_number}_graded/HA{homework_number}_graded.pkl')  # Pandas Dataframe
    df_moses_hausaufgabe.to_csv(f'./HA{homework_number}_graded/HA{homework_number}_graded.csv', index=False)  # CSV 
    
    return df_moses_hausaufgabe


if __name__ == "__main__":
    if not os.path.isfile('./df_moses_final.csv'):
        print('\nThe file df_moses_final.csv was not found in the current directory!\n')
        raise NotImplementedError
    
    df_moses_final = pd.read_pickle("./df_moses_final.pkl")    
    while True:   
        try:    
            input_number_homework = int(input('Enter homework number: '))
            homework = 'HA' + str(input_number_homework)
             
        except ValueError:
            print('\nInvalid input for homework number!')
            continue
    
        prompt = str(input(f'Include online grades from {homework}.csv (y/[n])? ')).strip()
        if prompt == 'y':
            if not os.path.isfile(f'./{homework}.csv'):
                print(f'\nThe file {homework}.csv was not found in the current directory!\n')
                continue
                        
            df_online_ha = pd.read_csv(f'./{homework}.csv')
            print(f'\nThe online homework file {homework}.csv was successfully imported')
            df_hausaufgabe_grades = enter_grades(df_moses_final, input_number_homework, df_online_ha, online=True)
            break
                    
        if prompt == 'n':
            df_hausaufgabe_grades = enter_grades(df_moses_final, input_number_homework, None, online=False)
            break
        
        else:
            print('invalid input!')
            continue
        
