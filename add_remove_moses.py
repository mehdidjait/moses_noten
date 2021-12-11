import pandas as pd


def add_remove(df):
    
    # copy the dataframe 
    df_moses = df.copy()
    
    while True:
        
        print('\nOptions: \n')
        print(' 1 --> add a student \n',
              '2 --> remove a student \n',
              '3 --> change the group of a student \n',
              '4 --> update the email of a student \n',
              '5 --> QUIT \n')
    
        try:
            option = int(input('option: '))
        except ValueError:
            print("invalid input for option")
            continue
        
        if option == 1:
            print('PLEASE enter the name from the the MOSES web page (VERY IMPORTANT!)')
            student = str(input('Name: ')).strip()
            prompt = input('Are you sure you entered the name from the MOSES web page (y/[n])? ')
            
            if prompt != 'y':
                print('\nPlease provide the name again\n')
                continue
                
            
            print('\nPLEASE provide the Email adress from the ISIS web page (VERY IMPORTANT!)')
            email = str(input('Email: ')).strip()
            
                       
            group = str(input('Gruppe: ')).strip()

            try:
                Matrikelnummer = int(input('Matrikelnummer: '))
            except ValueError:
                print("invalid input for Gruppe")
                continue
            
            new_student = {'Matrikelnummer': Matrikelnummer,
                           'Name': student, 
                           'Gruppe': group, 
                           'Email': email}
            
            df_moses = df_moses.append(new_student, ignore_index=True)
           
            print('\nthe following student will be added -->', student, 
                  '\nwith email -->', email,
                  '\nto the group -->', group)
            continue
            
        if option == 2:
            student = str(input('Name: ')).strip()
            if sum(df_moses.Name == student) < 1:
                print('the student', student, ' was not found')
                continue

            group = str(input('Gruppe: ')).strip()
            if not ((df_moses['Name'] == student) & 
                    (df_moses['Gruppe'] == group)).any():
                
                    print('the student', student,
                          'does not belong to group', 
                          group)
                    continue
            
            for i in df_moses.index:
                if df_moses.Name[i] == student and df_moses.Gruppe[i] == group:
                    df_moses = df_moses.drop([i])
                    print('the following student will be removed -->', student, 
                          'from group -->', group)
                    continue
            continue
                
        if option == 3:
            student = str(input('Name: ')).strip()
            if sum(df_moses.Name == student) < 1:
                print('the student', student, ' was not found')
                continue
            
            group = str(input('Neue Gruppe: ')).strip()
            for i in df_moses.index:
                if df_moses.Name[i] == student:
                  print('\nthe following student will be transferred -->', student, 
                        'from group -->', df_moses.Gruppe[i],
                        'to the group -->', group)
                  
                  df_moses.loc[i, 'Gruppe'] = group
                  print('\n', df_moses.Name[i], '--> Gruppe: ', 
                        df_moses.Gruppe[i], '\n')
                  continue
            continue
        
        if option == 4:
            
            student = str(input('Name: ')).strip()
            if sum(df_moses.Name == student) < 1:
                print('the student', student, ' was not found')
                continue 

            group = str(input('Gruppe: ')).strip()
            if not ((df_moses['Name'] == student) & 
                    (df_moses['Gruppe'] == group)).any():
                
                    print('the student', student,
                          'does not belong to group', 
                          group)
                    continue
                
            print('PLEASE provide the Email adress from the ISIS web page (VERY IMPORTANT!)')
            email = str(input('New email: '))
            
            for i in df_moses.index:
                if df_moses.Name[i] == student and df_moses.Gruppe[i] == group:
                    
                    print(f'\n{student}', 
                        '\nold email -->', df_moses.Email[i],
                        '\nnew email -->', email)
                    
                    df_moses.loc[i, 'Email'] = email
                    continue
            continue
                    
        if option == 5:
            # save and END
            print('\nthe changed student list will be saved to df_moses_final.csv\n')
            df_moses.to_pickle("./df_moses_final.pkl") 
            df_moses.to_csv("./df_moses_final.csv", index=False)  # CSV
            print('\n END \n')
        
        
        else:    
            print("\ninvalid input for option")
            continue
        
        return df_moses               


if __name__ == '__main__':
    df_moses_final = pd.read_pickle("./df_moses_final.pkl")
    df_moses_final_changed = add_remove(df_moses_final)
