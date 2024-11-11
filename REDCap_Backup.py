import json
import requests
import os
import sys
import csv
import re
import time
from itertools import islice
from datetime import date, datetime



# Define the Base Folder in this case my base folder is 'D:\\Work\\MNTD\\Backup\\' 
base_folder = 'D:\\Work\\MNTD\\Backup\\'


# fetch the url of REDCap from text file
# Example: https://redcaps...........




redcap_url = ''
with open('url.txt', 'r') as file:
    redcap_url = file.read()
redcap_url = redcap_url.split("\n")[0]

# fetch the api of REDCap from json file
# Example Api
# {  "project_1": ["api_key1", "api_key2"] 
# "project2": ["api_key1"]
# "project3": ["api_key1"],
# }

with open("api_keys.json", mode='r') as jsonfile:
    api_dictionary = json.load(jsonfile)
api_dictionary




class Exporter:
    def __init__(self, filepaths):
        self.filepaths = filepaths
    # This function will export raw CSV
    def csv_data_raw(self):
        count = 0

        print(f'\nCSV Raw Data Started!\n')
        with requests.Session() as session:
            for token, file_path in self.file_paths.items():
                print(file_path)
                #The base name of a path is the last component of the path
                file_name = os.path.basename(file_path)
                file_path = os.path.join(file_path, 'CSV Data Raw')
                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                file_path = os.path.join(file_path, file_name)[:215] + '.csv'

                if not os.path.exists(file_path):
                    data = {
                        'token': token,
                        'content': 'record',
                        'action': 'export',
                        'format': 'csv',
                        'type': 'flat',
                        'csvDelimiter': '',
                        'rawOrLabel': 'raw',
                        'rawOrLabelHeaders': 'raw',
                        'exportCheckboxLabel': 'false',
                        'exportSurveyFields': 'false',
                        'exportDataAccessGroups': 'false', 
                        'returnFormat': 'json'
                    }
                    csv_data = ''
                    try:
                        csv_data = session.post(redcap_url,data=data)
                    except Exception as e:
                        print(f'An error has occured: Project category: {project_category} API token: {token} Index: {index} REDCap Project name not found, may check your API code')
                        Error = 'REDCap Project name may not found, please check your API code'
                        backup_log(datetime.now(), '', project_category, token, index, Error)
                        exit_input = input("Enter any key to exit")
                        if exit_input:
                            sys.exit(1)
                        else:
                            time.sleep(1000)


                    if csv_data.status_code == 200:   
                        with open(file_path, mode='wb') as file:
                            file.write(csv_data.content)
                            count += 1
                        print(f'{file_name}         Saved!')
                    else:
                        print(f'CSV Data Raw : {count} files Saved! \n But Something Wrong with Loading {file_name}')
                        backup_log('csv_data_raw', file_name)


            
                    
        print(f'CSV Data Raw: {count} files saved successfully')
        return count


    # This function will export Labeled CSV
    def csv_data_label(self):
        count = 0
        print(f'\nCSV Labeled Data Started!\n')
        try:
            with requests.Session() as session:
                for token, file_path in self.file_paths.items():
                    #The base name of a path is the last component of the path
                    file_name = os.path.basename(file_path)
                    file_path = os.path.join(file_path, 'CSV Data Label')
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)

                    file_path = os.path.join(file_path, file_name)[:215] + '.csv'
                    if not os.path.exists(file_path):
                        data = {
                            'token': token,
                            'content': 'record',
                            'action': 'export',
                            'format': 'csv',
                            'type': 'flat',
                            'csvDelimiter': '',
                            'rawOrLabel': 'label',
                            'rawOrLabelHeaders': 'raw',
                            'exportCheckboxLabel': 'false',
                            'exportSurveyFields': 'false',
                            'exportDataAccessGroups': 'false', 
                            'returnFormat': 'json'
                        }
                        csv_data = ''
                        try:
                            csv_data = session.post(redcap_url,data=data)
                        except Exception as e:
                            print(f'An error has occured: Project category: {project_category} API token: {token} Index: {index} REDCap Project name not found, may check your API code')
                            Error = 'REDCap Project name may not found, please check your API code'
                            backup_log(datetime.now(), '', project_category, token, index, Error)
                            exit_input = input("Enter any key to exit")
                            if exit_input:
                                sys.exit(1)
                            else:
                                time.sleep(1000)

                        if csv_data.status_code == 200: 
                            with open(file_path, mode='wb') as file:
                                file.write(csv_data.content)
                                count += 1
                            print(f'{file_name}         Saved!')

                        else:
                            print(f'CSV Data Label: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                            backup_log('csv_data_label', file_name)
        except Exception as e:
            print(f'An error has occured: {e}')
            backup_log('csv_data_label', file_name)
                    
        print(f'CSV Data Label: {count} files saved successfully')
        return count

    def csv_data_dictionary(self):
        count = 0
        print(f'\nCSV Data Dictionary Started!\n')
        try:
            with requests.Session() as session:
                for token, file_path in self.file_paths.items():
                    #The base name of a path is the last component of the path
                    file_name = os.path.basename(file_path)
                    file_path = os.path.join(file_path, 'CSV Data Dictionary')
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)

                    file_path = os.path.join(file_path, file_name)[:215] + '.csv'
                    if not os.path.exists(file_path):
                        data = {
                            'token': token,
                            'content': 'metadata',
                            'format': 'csv',
                            'returnFormat': 'csv'
                        }
                        csv_data = ''
                        try:
                            csv_data = session.post(redcap_url,data=data)
                        except Exception as e:
                            print(f'An error has occured: Project category: {project_category} API token: {token} Index: {index} REDCap Project name not found, may check your API code')
                            Error = 'REDCap Project name may not found, please check your API code'
                            backup_log(datetime.now(), '', project_category, token, index, Error)
                            exit_input = input("Enter any key to exit")
                            if exit_input:
                                sys.exit(1)
                            else:
                                time.sleep(1000)

                        if csv_data.status_code == 200:   
                            with open(file_path, mode='wb') as file:
                                file.write(csv_data.content)
                                count += 1
                            print(f'{file_name}         Saved!')
                        else:
                            print(f'CSV Data Dictionary: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                            backup_log('csv_data_dictionary', file_name)
        except Exception as e:
            print(f'An error has occured: {e}')
            backup_log('csv_data_dictionary', file_name)

        print(f'CSV Data Dictionary: {count} files saved successfully')
        return count

    def xml_metadata_only(self):
        count = 0
        print(f'\nXML Meta Data Started!\n')
        try:
            with requests.Session() as session:
                for token, file_path in self.file_paths.items():
                    #The base name of a path is the last component of the path
                    file_name = os.path.basename(file_path)
                    file_path = os.path.join(file_path, 'XML Metadata Only')
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)

                    file_path = os.path.join(file_path, file_name)[:215] + '.xml'
                    if not os.path.exists(file_path):
                        data_config = {'token' : token,
                                    'content' : 'project_xml',
                                    'format' : 'xml',
                                    'returnMetadataOnly' : 'true',
                                    'exportFiles' : 'false',
                                    'exportSurveyFields' : 'false',
                                    'exportDataAccessGroups' : 'false',
                                    'returnFormat' : 'json'
                                        }
                        xml_data = ''
                        try:
                            xml_data = session.post(redcap_url, data = data_config)
                        except Exception as e:
                            print(f'An error has occured: Project category: {project_category} API token: {token} Index: {index} REDCap Project name not found, may check your API code')
                            Error = 'REDCap Project name may not found, please check your API code'
                            backup_log(datetime.now(), '', project_category, token, index, Error)
                            exit_input = input("Enter any key to exit")
                            if exit_input:
                                sys.exit(1)
                            else:
                                time.sleep(1000)
                        # write xml to local storage
                        if xml_data.status_code == 200:
                            with open(file_path, mode = 'wb') as file:
                                file.write(xml_data.content)
                                count += 1
                            print(f'{file_name}         Saved!')
                        else:
                            print(f'XML Metadata Only: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                            backup_log('xml_metadata_only', file_name)
        except Exception as e:
            print(f'An error has occured: {e}')
            backup_log('xml_metadata_only', file_name)
                        
        print(f'XML Metadata Only: {count} files saved successfully')
        return count

    def xml_metadata_and_data(self):
        count = 0
        print(f'\nXML Meta Data with Data Started!\n')
        try:
            with requests.Session() as session:
                for token, file_path in self.filepaths.items():
                    #The base name of a path is the last component of the path
                    file_name = os.path.basename(file_path)
                    file_path = os.path.join(file_path, 'XML Metadata and Data')
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)

                    file_path = os.path.join(file_path, file_name)[:215] + '.xml'
                    if not os.path.exists(file_path):
                        data_config = {'token' : token,
                        'content' : 'project_xml',
                        'format' : 'xml',
                        'returnMetadataOnly' : 'false',
                        'exportFiles' : 'false',
                        'exportSurveyFields' : 'false',
                        'exportDataAccessGroups' : 'false',
                        'returnFormat' : 'json'
                            }
                        xml_data = ''
                        try:
                            xml_data = session.post(redcap_url, data = data_config)
                        except Exception as e:
                            print(f'An error has occured: Project category: {project_category} API token: {token} Index: {index} REDCap Project name not found, may check your API code')
                            Error = 'REDCap Project name may not found, please check your API code'
                            backup_log(datetime.now(), '', project_category, token, index, Error)
                            exit_input = input("Enter any key to exit")
                            if exit_input:
                                sys.exit(1)
                            else:
                                time.sleep(1000)
                        # write xml to local storage
                        if xml_data.status_code == 200:
                            with open(file_path, mode = 'wb') as file:
                                file.write(xml_data.content)
                                count += 1
                            print(f'{file_name}         Saved!')
                        else:
                            print(f'XML Metadata and Data: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                            backup_log('xml_metadata_and_data', file_name)
        except Exception as e:
            print(f'An error has occured: {e}')
            backup_log('xml_metadata_and_data', file_name)

        print(f'XML Metadata and Data: {count} files saved successfully')
        return count

        





# This function will register the log of the backup
def backup_log(date_time, project_name, category, api_token, api_index, error):

    current_date = date.today().strftime('%B-%d-%Y')

    root = 'D:\\Work\\MNTD\\Backup\\'+current_date

    log_file = root + '\\REDCap backup log.csv'

    if not os.path.exists(log_file): # if the file is new, we have to setup the header row
        with open(log_file, mode='x', newline='') as file:
            header = [["SN",	"date-time", "project_name", "category", "api_token", "api_index", "Error"]]
            writer = csv.writer(file)
            writer.writerows(header)



    date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, mode='r') as readfile:
        reader = csv.reader(readfile)
        reader = list(reader)
    last = reader[-1][0]
    SN = int(last) + 1 if last != 'SN' else 1  # automatic serial number
    log_data = [
        [SN, date_time, project_name, category, api_token, api_index, error]
    ]

    with open(log_file, mode='a', newline='') as file:
        writer =csv.writer(file)
        writer.writerows(log_data)
    






def projectList(api_dictionary):
    projects = dict()
    #! This code is from redcap Api: export project info
    with requests.Session() as session:
        for project_category in api_dictionary.keys():
            project_list = []
            index = 0
            for token in api_dictionary[project_category]: 
                data = {
                'token': token,
                'content': 'project',
                'format': 'json',
                'returnFormat': 'json'
                }
                try:
                    r =session.post(redcap_url,data = data).json()
                    print(r['project_title'])
                    project_list.append(r['project_title'])
                    projects[project_category]=project_list
                    index +=1
                except Exception as e:
                    print(f' An error has occured: Project category: {project_category} API token: {token} Index: {index} REDCap Project name not found, may check your API code')
                    Error = 'REDCap Project name may not found, please check your API code'
                    backup_log(datetime.now(), '', project_category, token, index, Error)
                    exit_input = input("Enter any key to exit")
                    if exit_input:
                        sys.exit(1)
                    else:
                        time.sleep(1000)
    return projects

def subFolderCreater(projects):
    file_paths = dict()
    for folder in projects.keys():
        sub_root_1 = folder
        if not os.path.exists(sub_root_1):
            os.makedirs(sub_root_1)
        for project, token in zip(projects[folder], api_dictionary[folder]): 
            print(project)
            if re.findall(r'[\/:?"<>|]', project):
                project = re.sub(r'[\\/:?"<>|]','_',project)
            # print(project)
            sub_root_2 = sub_root_1 + '\\' + project.strip()
                
            if not os.path.exists(sub_root_2):   #create directory in local computer if it doesn't exist
                os.makedirs(sub_root_2)
            file_paths[token] = sub_root_2    

    print('All Folder Created Successfully')
    return file_paths

def dataExporterFunctionCaller(file_paths):
    Exporter(file_paths)
    count_csv_raw = Exporter.csv_data_raw(file_paths)
    print(f'Summary [CSV Raw Data]: {count_csv_raw} Total files saved successfully')

    count_csv_label = Exporter.csv_data_label(file_paths)
    print(f'Summary [CSV LABELED Data]: {count_csv_label} Total files saved successfully')

    count_data_dictionary = Exporter.csv_data_dictionary(file_paths)
    print(f'Summary [Data Dictionary]: {count_data_dictionary} Total files saved successfully')

    count_xml_metadata_only =   Exporter.xml_metadata_only(file_paths)
    print(f'Summary [Meta Data Only]: {count_xml_metadata_only} Total files saved successfully')

    count_xml_metadata_and_data = Exporter.xml_metadata_and_data(file_paths)
    print(f'Summary [Meta Data and Data]: {count_xml_metadata_and_data} Total files saved successfully')


    print("_"*30)
    print("\n\nBackup Completed")
    exit_input = input("Enter any key to exit")
    if exit_input:
        sys.exit(1)
    else:
        print("Closing the program...")
        time.sleep(1000)


        
def projectInfo(api_dictionary, error_log=None):
    function_of_error = None
    

    if error_log :
        print(error_log)
        function_of_error = error_log[6]
        error_key = error_log[3]
        error_value = error_log[5] # previous log index + 1; to get the current log
        new_dict = {}
        # print(error_key)

        # Start adding items after the specified key-value position
        start_adding = False
        
        for key, values in api_dictionary.items():
            # Check if we've reached the start key
            if key == error_key:
                print('True')
                # Try to find the index of the specified start value in the list of values
                try:
                    start_index = int(error_value) -1
                    print(start_index)
                    # Add the sublist from start_value to the end of the list
                    new_dict[key] = values[start_index:]
                    # Set flag to add the rest of the keys
                    print(new_dict)
                    start_adding = True
                except ValueError:
                    raise ValueError(f"Value '{error_value}' not found in the list for key '{error_log[4]}'.")
            elif start_adding:
                # For all keys after start_key, add their entire list of values
                new_dict[key] = values

        print(new_dict)
    elif not error_log:
        projectlist = projectList(api_dictionary)
        file_paths = subFolderCreater(projectList)
        dataExporterFunctionCaller(file_paths)







# Summary count of
print(f'Project_Catagory {" "*18} Count \n{"_"*40}')
for key in api_dictionary.keys():
    print(f'{key} : {" "*(35-len(key))} {len(api_dictionary[key])}')

total = sum(len(value) for value in api_dictionary.values())
print(f'\n {"_"*40}\n')
print(f"Total : {total}")
print(f'\n{"_"*40}\n')


current_date = date.today().strftime('%B-%d-%Y')
root = base_folder+current_date
sub_root_1 = '' 
sub_root_2 = ''
sub_root_3 = ''
os.chdir(root)

if not os.path.exists(root):
    # This will be execute at the initial stage (if there no error log file exist)
    os.makedirs(root)
    projectInfo(api_dictionary)
elif os.path.exists(root):
    # If may the root folder already created, but the execution had halted due to errors
    log_file_path = os.path.join(root, 'REDCap backup log.csv' )
    last_log = []
    if os.path.exists(log_file_path):
        with open(log_file_path) as logFile:
            # retrieve the last line(recent error) from the csv file
            last_log = list(csv.reader(logFile))[-1]
    projectInfo(api_dictionary, last_log)










                









