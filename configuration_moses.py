import os
import pandas as pd 


def initial_import_eintragungsliste():
    """
    Returns
    -------
    df_moses : TYPE
        DESCRIPTION.

    """
    
    
    df_moses = pd.read_csv("eintragungsliste.csv")
    print('eintragungsliste.csv was successfully imported')
    df_moses.rename(columns={df_moses.columns[0]: "Matrikelnummer"}, inplace=True)
    df_moses.rename(columns={df_moses.columns[1]: "Name"}, inplace=True) 
    df_moses.drop(columns=df_moses.columns[2], inplace=True)  # delete the third column
    
    # add the group column  
    if 'Gruppe' not in df_moses.columns:
        df_moses['Gruppe'] = ""
    
    return df_moses
    

def configuration_groups():
    """
    Returns
    -------
    df_moses : TYPE
        DESCRIPTION.

    """
    
    
    if os.path.isfile('./df_moses_initial.csv'):
        prompt = input('df_moses_initial.csv was found!'
                       '\n-->An intial configuration of the groups was already performed.'
                       '\nProceed with the same file (y/[n])? ').strip()
        
        if prompt == 'y':       
            df_moses = pd.read_csv('df_moses_initial.csv')
            print('df_moses_initial.csv was successfully imported')
            df_moses.Gruppe.fillna('', inplace=True)
        
        else:
            df_moses = initial_import_eintragungsliste()
            
    else:
        df_moses = initial_import_eintragungsliste()
    
    while True:        
        print('__________________________________________________________________________\n\n'
              '                 :Assign groups to students:\n\n\n'
              'Every student can be chosen by the index shown left\n'
              '  -> example: 12 --> Nachname_12, Vorname_12\n'
              '              23 --> Nachname_23, Vorname_23\n'
              '              58 --> Nachname_58, Vorname_58\n\n'
              'Mutiple students can be chosen at once to form a group using + as seperator\n'
              '  -> example: 12+23+58\n\nFor groups with one student: give a single index as input\n'
              '  -> example: 58\n\nType quit to exit the configuration'
              '\n\n__________________________________________________________________________') 
            
        prompt = input('Continue (y/[n])? ').strip()
        if prompt == 'y':
            break
        
        continue
    
    for index, name in zip(df_moses.index, df_moses.Name):
        print(f'{index} --> {name}')               

    while True:
        print('__________________________________________________________________________\n')
        students_with_group = (df_moses.Gruppe != '').sum()
        print('Type quit to exit the configuration\n'
              f'Type show to show the groups with associated students\n'
              'Type showng to show students without a group\n\n'
              f'Total numbers of students with a group --> {students_with_group}\n')

        index_input = str(input('Select: ')).strip()        
        if '+' in index_input:
            selected_combination = list(filter(None, index_input.split('+')))
            if any(not index.isdecimal() or int(index) not in df_moses.index for index in selected_combination):
                print('\nInvalid combination! Please use the index shown '
                      'to the left of the student')
                    
                continue
            
            if len(selected_combination) != len(set(selected_combination)):
                print('\nA student was selected more than once!')
                continue 
            
            selected_students = [df_moses.loc[int(index), 'Name'] for index in selected_combination]
            print(f'\nselected_students --> {selected_students}'
                  '\n\nType back to go back to students selection')
            group_input = str(input('Gruppe: ')).strip()
            if group_input == 'back':
                continue
            
            if not group_input:
                print('WARNING! No group was selected')
                continue
            
            for index in selected_combination:
                df_moses.loc[int(index), 'Gruppe'] = group_input
            
            print(f'\n{selected_students} --> Gruppe: {group_input}'
                  '\n\nthe change will be saved in the file df_moses_initial.csv') 
                
            df_moses.to_csv("./df_moses_initial.csv", index=False) 
            continue
        
        if index_input.isdecimal():
            if int(index_input) not in df_moses.index:
                print('\nindex not found!\n')
                continue 
            
            print(f'\nselected student --> {df_moses.iloc[int(index_input), 1]}'
                  '\nType back to go back to students selection')
                
            group_input = str(input('Gruppe: ')).strip()
            if group_input == 'back':
                continue

            if not group_input:
                print('\nWARNING! No group was selected')
                continue
           
            df_moses.loc[int(index_input), 'Gruppe'] = group_input
            print(f'\n{df_moses.iloc[int(index_input), 1]} --> Gruppe: {group_input}'
                  '\n\nthe change will be saved in the file df_moses_initial.csv')
                
            continue
                
        if index_input == 'quit':
            prompt = input('Quit the configuration. Proceed (y/[n])? ').strip()
            if prompt == 'y':
                print('Configuration is finished\nAll the changes will be saved '
                      'in the file df_moses_initial.csv')
                    
                df_moses.to_csv("./df_moses_initial.csv", index=False) 
                return df_moses
                
            continue
        
        if index_input == 'show':
            for group in list(set(df_moses['Gruppe'])): 
                if group:
                    names_group = df_moses.loc[df_moses['Gruppe'] == group, 'Name'].values
                    print(f'Gruppe {group} --> {names_group}')
            
            continue
        
        if index_input == 'showng':
             for index, name in zip(df_moses.index, df_moses.Name):
                 if not df_moses.loc[df_moses['Name'] == name, 'Gruppe'].values[0]:
                    print(f'{index} --> {name}')
            
             continue
        
        else:
            print("\ninvalid input for select!")
            continue


def configuration_emails(df_moses):  
    """
    Parameters
    ----------
    df_moses : TYPE
        DESCRIPTION.

    Returns
    -------
    df_moses : TYPE
        DESCRIPTION.

    """
    
    
    df_isis_raw = pd.read_csv("Teilnehmerliste.csv")
    print('Teilnehmerliste.csv was successfully imported')
    df_isis = pd.DataFrame(columns=['Name', 'Email'])
    df_isis['Name'] = df_isis_raw.Nachname + ', ' + df_isis_raw.Vorname
    df_isis['Email'] = df_isis_raw['E-Mail-Adresse']
    
    if 'Email' not in df_moses.columns:
        df_moses['Email'] = ""   
    
    for ind, name_moses in enumerate(df_moses.Name):
        # check just for students with a group
        if df_moses.loc[df_moses['Name'] == name_moses, 'Gruppe'].values[0]:        
            found_email = df_isis[df_isis['Name'] == name_moses]['Email']
            
            if not found_email.empty:
                df_moses.loc[ind, 'Email'] = found_email.values[0]
                # print(f'{name_moses} --> email: {found_email.values[0]}')
                
            else:
                print('__________________________________________________________________________\n'
                      f'\nPLEASE provide the Email address of [{name_moses}] from the Teilnehmer/innen ISIS '
                      'web page (VERY IMPORTANT!)')
                    
                email_input = str(input("Email from ISIS Teilnehmer/innen: ")).strip()
                df_moses.loc[ind, 'Email'] = email_input
                print(f'\n{name_moses} --> email: {email_input}'
                      '\n__________________________________________________________________________')
                
    print('\nThe table with student, group, email will be saved to df_moses_final.csv\n')
    df_moses.to_pickle("./df_moses_final.pkl")  # Pandas Dataframe that can be exported to python 
    df_moses.to_csv("./df_moses_final.csv", index=False)
    
    return df_moses            


if __name__ == "__main__":
    if not os.path.isfile('./eintragungsliste.csv'):                    
        print('\nThe file eintragungsliste.csv was not found in the current directory!\n')
        raise NotImplementedError 
    
    df_moses = configuration_groups()
    if not os.path.isfile('./Teilnehmerliste.csv'):
        print('\nThe file Teilnehmerliste.csv was not found in the current directory!\n')
        raise NotImplementedError
            
    df_moses_final = configuration_emails(df_moses)  
