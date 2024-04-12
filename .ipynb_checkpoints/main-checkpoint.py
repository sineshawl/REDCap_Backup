import json
import requests

my_tokens = {}
url = 'https://redcapsvr2.ahri.gov.et/api/'


# Open the Json file for reading which contain API tokens 
with open('api_keys.json', mode = 'r') as file:
    # Load the JSON data from file
    my_tokens = json.load(file)
print(len(my_tokens.items()))

# Summary count of
print(f'Project_Catagory {" "*18} Count \n{"_"*40}')
for key in my_tokens.keys():
    print(f'{key} : {" "*(35-len(key))} {len(my_tokens[key])}')

def project_name(my_tokens):
    my_dic = dict()
    #! This code is from redcap Api: export project info
    with requests.Session() as session:
        for project in my_tokens.keys():
            project_list = []
            for token in my_tokens[project]: 
                data = {
                'token': token,
                'content': 'project',
                'format': 'json',
                'returnFormat': 'json'
                }
                r =dict(session.post(url,data = data).json())
                r['project_title']
                # project_list.append(r['project_title'])
                # my_dic[project]=project_list
    return my_dic

projects  = project_name(my_tokens)
# print(projects.keys())