import pandas as pd
import numpy as np


def initial_configuration_group(df, group):
    
    # copy the dataframe 
    df_moses = df.copy()
    
    # prepare the dataframe
    if 'Name' not in df_moses.columns:
        df_moses.rename(columns = {df_moses.columns[0]: "Matrikelnummer"}, inplace = True)
        df_moses.rename(columns = {df_moses.columns[1]: "Name"}, inplace = True) 
        df_moses.drop(columns = df_moses.columns[2], inplace = True)  # delete the third column
        
    # get the students with the same name
    duplicate = df_moses[df_moses.duplicated('Name')]
    duplicate_list = []
    for i in duplicate.Name:
        duplicate_list.append(i)
    
    # add the group column  
    if 'Gruppe' not in df_moses.columns:
        df_moses['Gruppe'] = "" 
        
    # assign group Number to students
    while True:
        
        Student = str(input('Name: '))
        if sum(df_moses.Name == Student) < 1 and Student != str(0):
            print('the student', Student, ' was not found')
            print('\nPLEASE enter the name from the HTML source code of the moses web page!')
            continue
        
        try:
            Gruppe = int(input('Gruppe: '))
        except ValueError:
            print("invalid input for Gruppe")
            continue
        
        # break the loop
        if Gruppe == 0 and Student == str(0):
            print('\n END \n')
            break
        
        if Student in duplicate_list:
           print('\nmore than one student has the following name -->', Student, 
                 '\n\nplease provide the Matrikelnummer')
           
           matrikelnummer = int(input('Matrikelnummer: '))
           
           for j in df_moses.index:
               if df_moses.Matrikelnummer[j] == matrikelnummer:
                  df_moses.loc[j, 'Gruppe'] = Gruppe
                  print('\n', df_moses.Name[j], matrikelnummer, 
                        '--> Gruppe: ', 
                        df_moses.Gruppe[j], '\n')
           continue
           
        # search the database for the provided name
        for i in df_moses.index:
            if df_moses.Name[i] == Student:
               df_moses.loc[i, 'Gruppe'] = Gruppe
               print('\n', df_moses.Name[i], '--> Gruppe: ', 
                     df_moses.Gruppe[i], '\n')
            
    # 2) Verification 
    # check if the number of students with a group & the total number of students is correct
    # init the total number of students with a group
    s1 = 0 
    
    j = 0
    while j < len(group):
        # total number of students in a given group
        s0 = 0  
        
        for i in df_moses.index:
            if df_moses.Gruppe[i] == group[j]:
                s0 += 1 
                s1 += 1
        print('group:', group[j], ' --> ', s0, 'students')
        j += 1
        
    print('\nthe total number of students with a group:', s1)
    
    # save 
    df_moses.to_pickle("./initial_conf_group.pkl")
     
    return df_moses


def initial_configuration_email(df, df_students):
    
    # copy the dataframe 
    df_moses = df.copy()
    
    # 1) preparing the dataframes
    df_students2 = df_students.Name + ", " + df_students.Vorname  # to match the df_moses 
    df_students2 = df_students2.to_frame()  
    df_students2.columns = ['Name']         
    df_students2['Email'] = df_students.iloc[:, [4]]  # get the Email adresses
    
    # add the Email column 
    if 'Email' not in df_moses.columns:
        df_moses['Email'] = ""   
    
    # 2) getting the Email adresses from df_students (only for students with a group)
    for i in df_students2.index:
        for j in df_moses.index:
            if df_students2.Name[i] == df_moses.Name[j] and df_moses.Gruppe[j] != '':
                df_moses.loc[j, 'Email'] = df_students2.Email[i]
                        
    # 3) manually input the Email adresses that cannot be found! 
    for i in df_moses.index:
        if df_moses.Email[i] == '' and df_moses.Gruppe[i] != '':
            print('The Email of the following student was not found: ', df_moses.Name[i])
            print('\nPLEASE provide the Email adress from the ISIS web page')
            Email = str(input("Email from ISIS: "))
            df_moses.loc[i, 'Email'] = Email
            print(df_moses.Name[i], '--> Email: ', df_moses.Email[i], '\n')
    
    # save 
    #df_moses.to_pickle("./Initial_Conf_Email.pkl")
    
    return df_moses


def final_configuration_email(df, HA):
    
    # copy the dataframes 
    df_moses = df.copy()
    df_HA = HA.copy()
    
    # Using HA0 --> reason: 2435 Versuche (the majority of the Email Adresses will be contained)
    df_HA = df_HA.drop([len(df_HA) - 1])  # delete the last row containing the Gesamtdurchschnitt
    
    # correct Email --> The same as the Email from ISIS (important to extract the online Hausaufgaben)
    Y = []  # list to contain the correct Emails
    
    for i in df_moses.index:
        for j in df_HA.index:
            if(df_moses.Gruppe[i] != ''):  # check only for students with a group
                if(df_moses.Email[i] == df_HA.iloc[j, 2]):
                    Y.append(df_moses.Name[i])

    for i in df_moses.index:
        if df_moses.Gruppe[i] != '':  # check only for students with a group
            if df_moses.Name[i] in Y:
                i += 1  # the Email is already correct 
            else:
                print('Email not found: ', df_moses.Name[i])
                print('PLEASE provide the Email adress from the ISIS web page')
                Email = str(input('Email from ISIS: '))
                print('\n', df_moses.Name[i], '--> old Email: ', df_moses.Email[i])
                df_moses.loc[i, 'Email'] = Email
                print('', df_moses.Name[i], '--> new Email: ', df_moses.Email[i], '\n')
    
    # save 
    print('\nA table with student, group, email will be saved to df_moses_final.csv\n')
    df_moses.to_pickle("./df_moses_final.pkl")  # Pandas Dataframe
    df_moses.to_csv("./df_moses_final.csv", index=False)  # CSV 
    
    return df_moses


if __name__ == "__main__":
    
    prompt = input('Are you sure you defined the groups correctly below in the code (y/[n])? ')
    if prompt != 'y':
        raise NotImplementedError
    
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
    
    df_students = pd.read_csv("students_list.csv")
    df_eintragungsliste = pd.read_csv("eintragungsliste.csv")
    # Using HA0 --> reason: 2435 Versuche (the majority of the Email Adresses will be contained)
    df_HA0 = pd.read_csv("HA0.csv")
    print('\nEnter 0 for Name & 0 for Gruppe when completed')
    
    df_moses_initial = initial_configuration_group(df_eintragungsliste, group)
    
    # for calling initial_configuration_group again (in case of an error in the first initial configuration)
    while True:  
        entry = input('Is the total number of students with a group correct (y/[n])? ')
        if entry == 'y':
            break
        df_moses_initial = initial_configuration_group(df_moses_initial, group)
    
    print('\nAlways enter the email adress FROM THE ISIS WEBSITE!\n')
    
    df_moses_initial = initial_configuration_email(df_moses_initial, df_students)
    df_moses_final = final_configuration_email(df_moses_initial, df_HA0)
    
 
     