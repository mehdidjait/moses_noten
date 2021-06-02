import pandas as pd
import numpy as np

# maybe save each new one with the f string method ! 
def enter_grades(df, df_HA, homework, group):
    
    # copy the dataframes
    df_moses_final = df.copy()
    df_HA = df_HA.copy()
    
    # delete the last row containing the Gesamtdurchschnitt
    df_HA = df_HA.drop([len(df_HA) - 1])
    
    # replacing the missing values and casting to float 
    df_HA = df_HA.replace({'-': np.nan})
    for col in list(df_HA.columns):
        if('/' in col):
            df_HA[col] = df_HA[col].astype(str).str.replace(',', '.').astype(float)
    
    if 'Gesamt' not in df_moses_final.columns:
        df_moses_final['Gesamt'] = ""
        df_moses_final['Schriftlich'] = ""
        df_moses_final['Online'] = ""
    
    while True:
        
        try:
            Gruppe = int(input('Gruppe: '))
            if (Gruppe not in group and Gruppe != 0):
                print(f'the group {Gruppe} was not found')
                continue
            
        except ValueError:
            print("invalid input for Gruppe")
            continue
        
        try:
            Note = float(input("Note:"))
        except ValueError:
            print("invalid input for Note")
            continue
        
        print("Gruppe:", Gruppe, "--> Note:", Note, "\n")
    
        if Gruppe == 0 and Note == 0:
            print('\n END \n')
            break
        
        else:
            for i in df_moses_final.index:
                if(df_moses_final.Gruppe[i] == Gruppe):
                    print(df_moses_final.Name[i])
                    df_moses_final.loc[i, 'Schriftlich'] = Note
                    
    for i in df_moses_final.index:
        for j in df_HA.index:
            if(df_moses_final.Gruppe[i] != ''):
                if(df_moses_final.Email[i] == df_HA.iloc[j, 2]):
                    df_moses_final.loc[i, 'Online'] = df_HA.iloc[j, 7]
                    
    df_moses_final["Online"] = pd.to_numeric(df_moses_final["Online"], downcast = "float")
    df_moses_final["Online"] = df_moses_final["Online"].fillna(0)
    
    df_moses_final["Schriftlich"] = pd.to_numeric(df_moses_final["Schriftlich"], downcast = "float") 
    df_moses_final["Schriftlich"] = df_moses_final["Schriftlich"].fillna(0)
    
    df_moses_final['Gesamt'] = df_moses_final['Schriftlich'] + df_moses_final['Online']
    df_moses_final['Gesamt'] = df_moses_final['Gesamt'].fillna(0)
    
    # no grade will be given to students with 0 for schriftlich and 0 for online
    for i in df_moses_final.index:
        if(df_moses_final.Gesamt[i] == 0):
            df_moses_final.loc[i, 'Gesamt'] = ''           
    
    #Print Javascript code for Moses
    
    
    for i in df_moses_final.index:
        if(df_moses_final.Gruppe[i] != ''):
            print("document.querySelector('input[title=\"", df_moses_final.Name[i], 
                  " : Hausaufgaben - ", homework, 
                  "\"]').value = '", df_moses_final.Gesamt[i], 
                  "'", sep = '')
            
            
    #############################################################################
    # for ANA2 tutors!
    # 1. COMMENT OUT lines 78 .. 83 by adding """ in line 77 and 84
    # 2. UNCOMMENT lines 92 .. 97 by deleting the """ from line 91 and 98
    #############################################################################
    """
     for i in df_moses_final.index:
        if(df_moses_final.Gruppe[i] != ''):
            print("document.querySelector('input[title=\"", df_moses_final.Name[i], 
                  " : Hausaufgaben - HA ", number_homework, 
                  "\"]').value = '", df_moses_final.Gesamt[i], 
                  "'", sep = '')
    """       
    #############################################################################
    # for ANA2 tutors!
    # 1. comment lines 78 .. 83 by adding """ in line 77 and 84
    # 2. uncomment lines 92 .. 97 by deleting the """ from line 91 and 98
    #############################################################################
    
    
    # save        
    df_moses_final.to_pickle(f'df_{homework}.pkl')  # Pandas Dataframe
    df_moses_final.to_csv(f'df_{homework}.csv', index=False)  # CSV 
    
    # Print the name + email adress of students with 0 points in the online HA 
    print('\n\n the following students have 0 points in the online homework !PLEASE VERIFY MANUALLY!\n')
    for i in df_moses_final.index:
        if(df_moses_final.Gruppe[i] != ''):
            if(not(df_HA.iloc[:, 2] == df_moses_final.Email[i]).any()):
                print(df_moses_final.Name[i], df_moses_final.Email[i])
                
    print('\n COMPARE the email adresses and UPDATE with add_remove_moses.py if needed\n')
    print(f'\nA complete csv table of the grades will be saved to df_{homework}.csv\n')
    return df_moses_final


if __name__ == "__main__":
    
    
    df_moses_final = pd.read_pickle("./df_moses_final.pkl")
    
    #############################################################################
    # Define the groups
    #############################################################################
    group = np.array((1,  3,  4,  6, 
                      10, 12, 13, 14,
                      15, 16, 17, 18, 
                      19, 20, 21, 22, 
                      25))
    #############################################################################
    # Define the groups
    #############################################################################
    
    while True:
        try:    
            number_homework = int(input('Enter homework number: '))
            homework = f'HA{number_homework}'  
            print(f'---> {homework}.csv')
            try:
                path = f"./{homework}.csv"
                df_online_HA = pd.read_csv(path)
                print(f'\nThe online homework {homework}.csv was successfully imported')
                break
            except FileNotFoundError:
                print(f'THE CSV FILE {homework}.csv WAS NOT FOUND!')
                continue
            
        except ValueError:
            print('Invalid input for homework number')
            continue
        
    print('\nEnter 0 for Gruppe & 0 for Note when finished')
    df_grades = enter_grades(df_moses_final, df_online_HA, homework, group)
    
