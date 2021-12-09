import numpy as np
import os
import pandas as pd


def enter_grades(df_moses_final, homework, df_online_ha, online):
    """,
    Parameters
    ----------
    df_moses_final : TYPE
        DESCRIPTION.
    df_online_ha : TYPE
        DESCRIPTION.
    homework : TYPE
        DESCRIPTION.

    Returns
    -------
    df_moses_hausaufgabe : TYPE
        DESCRIPTION.

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
    groups_without_grade.remove('')
    while True:
        print('__________________________________________________________________________'
              '\nType quit to exit'
              '\nType show to show the groups still without a grade')
            
        group_input = str(input('Gruppe: ')).strip()
        if group_input == 'quit':
            prompt = input('Quit enter grades. Proceed (y/[n])? ').strip()
            if prompt == 'y':
                break
        
            continue
        
        if group_input == 'show':
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
        print(f'\nGruppe {group_input} --> {names_emails_selected.Name.values}')        
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
                    print(f'{names_emails_selected.Name.values[ind]} --> online Note: 0 (NOT FOUND -> '
                          'PLEASE VERIFY MANUALLY in ISIS!)')
            
    # gesamt = online + schriftlich 
    columns = ['Gesamt', 'Schriftlich', 'Online']
    df_moses_hausaufgabe[columns] = df_moses_hausaufgabe[columns].apply(pd.to_numeric, errors='coerce', axis=1).fillna(0)
    df_moses_hausaufgabe['Gesamt'] = df_moses_hausaufgabe['Schriftlich'] + df_moses_hausaufgabe['Online']
    df_moses_hausaufgabe['Gruppe'].fillna('', inplace=True)
    print('__________________________________________________________________________\n')
    for ind, name in enumerate(df_moses_hausaufgabe['Name']):
        if df_moses_hausaufgabe.loc[df_moses_hausaufgabe['Name'] == name, 'Gruppe'].values[0]: 
            print("document.querySelector('input[title=\"", name, 
                  " : Hausaufgaben - ", homework, 
                  "\"]').value = '", df_moses_hausaufgabe.loc[ind, 'Gesamt'], 
                  "'", sep='')
    
    print('\n__________________________________________________________________________'
          f'\nFinished.\n\nTo upload the grades:\n'
          '1. Copy all the code starting with document.querySelector\n'
          f'2. Open the moses page for entering the grades of the Hausaufgabe {homework}\n'
          '3. right click anywhere in the page --> inspect --> console\n'
          '4. Paste the code into the console and press ENTER\n'
          '__________________________________________________________________________\n\n'
          f'All the grades will be saved in the file --> {homework}_graded.csv '
          f'inside the directory --> {homework}_graded')
    
    if not os.path.isdir(f'./{homework}_graded/'):
        os.mkdir(f'./{homework}_graded/')
   
    df_moses_hausaufgabe.to_pickle(f'./{homework}_graded/{homework}_graded.pkl')  # Pandas Dataframe
    df_moses_hausaufgabe.to_csv(f'./{homework}_graded/{homework}_graded.csv', index=False)  # CSV 
    
    return df_moses_hausaufgabe


if __name__ == "__main__":
    if not os.path.isfile('./df_moses_final.csv'):
        print('\nThe file df_moses_final.csv was not found in the current directory!\n')
        raise NotImplementedError
    
    df_moses_final = pd.read_pickle("./df_moses_final.pkl")    
    while True:   
        try:    
            input_number_homework = int(input('Enter homework number: '))
            homework = f'HA{input_number_homework}'
            prompt = str(input(f'Include online grades from {homework}.csv (y/[n])? ')).strip()
            if prompt == 'y':
                try:
                    df_online_ha = pd.read_csv(f'./{homework}.csv')
                    print(f'\nThe online homework file {homework}.csv was successfully imported')
                    df_hausaufgabe_grades = enter_grades(df_moses_final, homework, df_online_ha, online=True)
                    break
               
                except FileNotFoundError:
                    print(f'\nTHE ONLINE HOMEWORK FILE {homework}.csv WAS NOT FOUND!')
                    continue
                
            df_hausaufgabe_grades = enter_grades(df_moses_final, homework, None, online=False)
            break
        
        except ValueError:
            print('\nInvalid input for homework number!')
            continue
