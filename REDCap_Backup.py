import json
import requests
import os
import csv
import re
from datetime import date


redcap_url = 'https://redcapsvr2.ahri.gov.et/api/'

api_dictionary = {  "ACHIDES_RDT_Comparison": ["1CAAC4F69A2C1A58EB1C35DA3C410204", "7D396AC18878D01B819234B403333560", "8D8C81DF12F2B218811E67ABA1A2CEA6", "B1D70261D5D24A8C19F82D04F660E17E", "76872991E3E7517C6F89102BD201A7F2", "20BAB8B252A60B63456996B20F92E8FF", "0F3A2120D2DB18B20084685AC5D55264", "4875B03D097D60475C79DCFC53CE8EBA", "A995DC296138BA31A0A1E058582BD129", "F892DB5EBC135430F6839EBAA02A1017", "FC0D8A331DAE66AA72EA537FF4F43CAA", "841968247197D8BB2BC8F8DC85D8704A", "DDE58B59251E8CF1F455B3E1A6F0B94F", "AF7EAAE18D5FCD5B694474A162AEB877", "DF1F549DE15AD9CC698424E1A907DD38", "2478848931256C42F42FDBD62A25F611", "9585A6B52D25DC72EDF054FDB8C7D674", "FAD07B340AA79080C1DB80FB16E0D12B", "96ECC7F58102DB0CD86BA1A349561099"], 
                    "ACHIDES_Deletion_Surveillance_1": ["C74D4290825D6EB70BEB189DAB4AE4AF", "AEE0B607FC8432E5567EBBBE76EF743E", "8082921E542A3849B2DEB6B658581E1E", "94C2CA0EDD0266E8256283046A954059", "18D9A45B0806D3DE02D1AB824591E4E3", "6D7B91178E1AA3B486414EAFF27A4380", "AF7B71CE6D30213F4AAF147838F051CB"], 
                    "ACHIDES_Deletion_Surveillance_2": ["0E333729F880651B6A5F37F1499B633B", "C1BC3B7CA61406D80AAF2AF34F31F4EF", "667DA198E29D550B79C383E0B569628F", "B0F7CBF17E4939D6B60B741395EF8EB5", "96B4DEBC38C9164C212C4D5DDE485AD0", "515965BD85A6E0584050812B53B811B6", "B19C555091FC8EA4444F38373DEEC19A", "814B2F3EB5408BF8DC11CBB2BFB5F54D", "80A2EB279B25B5A9593DD7ECA167A4F3", "8C0F424C4B8640202A52C4A38535671E", "DAEB3FF46327AC0FC105E6659C91DBEC"], 
                    "ACHIDES_Deletion_Surveillance_3": ["4EDE1D27D1F8736C966F7AD3A667EAD5", "3E639036348C36727E54A61B4C14BB36", "D3B896BB97FDFC77772A5120EDD37512", "AABBC93821994E8605A60AEE90AD04FA", "7B12B20F3D2E534D205A26F3AFEDDA83", "FB194D31172148D8F8E8A771C4E2F825", "4E368E4169424EB71440E3746F65F2BD", "4DCF525610534A69426E1B48D147A22F", "40B7548AB81056D1733C84C2241825E5", "88D49A5C2EBCA6B3353E590C28886FAE", "079D41B7BC5A97FB0A7F6D0F71F958A7", "EA798AF890A8E7FC8011CE33788B0ED5", "ECE3C92394E210F3A07DE138AF788826", "82FC6A9FDD20C32047A62AD43B87CF7A", "6A53243BF602FF51EE459370B4530F99", "149FE5FA104EFCD1918D5E271BD43E05", "8FE1CA871729D5C079C646B0D643B708"], 
                    "ACHIDES_Deletion_Surveillance_4": ["7D1AB79C4F7F2C7B98092BDD1009A0DD", "2AB1D2B358F099430A3CC6FE96C69353", "D53F6421B6EC35AC62CD6A1D230971EA", "44FC9EAB3A27011AA4F2B55B9B2E6726", "4B74DBAED8CBE13992CA19B4420AD686", "D3CD763712EFC1F115E20C4A8F248A66", "43DC779610E694B488611ACD3D48E983", "F8F8A80BF9DD47B0BC4B3119F235B0E6", "2646233072A23FE5104959B2EC4DD72C", "7E8B808753C73AA534F5A92D48427DA1", "E0AE47B4B8D66572CD373E09643C6036", "3D5BBD29FD6EE7AB4BA1B6F0C3205EFC"],
                    "VISPA": ["A0A3A4421C4FB1E9111A93CC2558C28C", "0CB9AEA10AE5C28B0CB313D89DBDAC2F", "382FF1927148A7A6C19F0CA188BCD135"], 
                    "PvSTATEM": ["BD35D27FE7787A5E392785AB99D2E565", "8FE7D9D9B4623DE2D9C6C1DDD39F9726", "4B56D2ADAD8F8743966E1814F76A3B4D", "E85B022C4D4C4E284CAD6DE26ACFAE30", "872CA2D5401A431B5AAC3D4D9AD07FA3", "37D040E89688A56B1E1DB67506DB560D", "E94F38856D037F1EC117E09337A71620" ], 
                    "TES2023": ["6025293C85ABC257E3534859A9D42AEE", "A182AA78F1135A9D78CD78ED736C4052", "81F2A228C3F258C2071BFA4D48DBA463", "CA54BF4522A0C9D5FF12E002CFEADE80", "CB820DDD8078FE7CF179EAEEE1964C1D", "0AB30BEA22F3CE1E9FEF4DCFC3008F51"], 
                    "TES2021": ["F966C6C0E477A4B6964A3B7006362430", "E0A541B8E0A6291F014CC4038DB7707D", "F48FFD9176CAC511A32DB9D682DA0772", "8454B65DC2F333D0F7942A45C909091F", "26A7EB7D984A2F7AA7E1E901A21D194C"], 
                    "HAMMS": ["64BFA82BE7D39473D502D4E76ACE7594", "F31D073929E6C0F0664BBD3BAAC7A6EE"],
                    "tMDA_RCD": ["20FBDB12A056DC0805F6044F05258A5B", "449B3EC5F9638D8748E0B0A9F5D424B5", "7A4C874E09CAF102D93415F95AD4ADD1", "30E0D8A4DA56295A759C440AD8929357", "008DE1C92DD677C73FA5D1FC90CE8440", "5E9060E83438B4B4AD0F73A4041EE822"], 
                    "EMAGEN": ["5609E8929C22B2C8E3904B7BDAF9417F", "A87DC6B58DB5385E080D469DD4EDE065", "AAE3FC76E0D82780F23CAB1D67743CC1", "F31C8DD3DA25C09B01C35B411B6AA155", "19C7E15B5C8F2A3C9DA7464ECCA82160", "325B19247FDA1AE7FD0C0322524B7EF6", "9C423E9CD4C52DE7F3B218EBDAC63442", "99373C4470B8373494D352B1CBA3F888"], 
                    "Bioinformatics": ["C2EB94BA2986C987A5045F8F3C60F0DF", "2205F516FF36D564FB2E2B09D7B70A6F"], 
                    "INDIE1": ["220369D65142CD1D4C65604338F67340", "C8624EA4FB1C1C684201CDE5ED206D33", "A963E6C01A8393165C6AC441D7B86B65", "BD4E4AD9840314326B0307BAEAF13EC0", "2407822A3395D95C814085EBA387299A", "ABAF811429AADD7A034BE4BFB215218C", "13D45ECBD60615DCF4C4E53CD16EBCFE", "2A0FA0B05E04C6920DB6EF2F264F4A34", "97D7F7BF04FAB56E37D8BE9731527F61", "7F13A4E3226A64D3FBF361191152E141"], 
                    "INDIE2": ["ED37701E09D6853BCD465173E9CF2372", "6638FF741CDC9EB7EF74FD4C0AA41BA2", "750C923061397E7F50DDC315590699D8", "DAE2EC0FA0E3FF1B04150F1B84875BD8", "0DDCC49FD54FAE264407F4FAC1176FF1", "2111BA9019498B99FF0E59E415B74F65", "B3F32771E4E1DDE0117F75D81A2FBD90", "1F87C5B41B1C53E0937EF01C26BB6C3E", "446BB07B0DE63D6EEF6391AD6EF3F2F1"],
                    "Urban_Malaria_1": ["39F0B04EF9D86ABC29E1D8737F5E2C89"], 
                    "Urban_Malaria_2": ["1CC32FC1E7AD537819B6D9F60D360113", "994E3AF84A27799FCD8BD06194806F72", "0794CB868C0AAB8A50ACFEB1A37332BF", "44B3260188D98A1B306872EF6B08D1CE", "4E1D04A540EBBFDAE351AFFFFF26CD83"], 
                    "Urban_Malaria_3": ["7996283497DE13353D97CD5B103B0360", "65971F1AE4FC37A89AC8416CF457E048", "887789CFE3799033C20ACDB87F0B197D", "2C7E1BADE8C45CBFF0A3627C225E428C", "98164A4A9DFB32552480EDAEC71C5783"],
                    "REDCap_8_11_5": ["6159263D1A704D5E95F46D9B7D3BA478"]
                    }
# This function will export raw CSV
def csv_data_raw(file_paths):
    count = 0
    with requests.Session() as session:
        for token, file_path in file_paths.items():
            #The base name of a path is the last component of the path
            file_name = os.path.basename(file_path)
            file_path = os.path.join(file_path, 'CSV Data Raw')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_path = os.path.join(file_path, file_name)[:215] + '.csv'

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
            csv_data = session.post(redcap_url,data=data)

            if csv_data.status_code == 200:   
                with open(file_path, mode='wb') as file:
                    file.write(csv_data.content)
                    count += 1
            else:
                print(f'CSV Data Raw : {count} files Saved! \n But Something Wrong with Loading {file_name}')
                
    print(f'CSV Data Raw: {count} files saved successfully')
    return count


# This function will export Labeled CSV
def csv_data_label(file_paths):
    count = 0
    with requests.Session() as session:
        for token, file_path in file_paths.items():
            #The base name of a path is the last component of the path
            file_name = os.path.basename(file_path)
            file_path = os.path.join(file_path, 'CSV Data Label')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_path = os.path.join(file_path, file_name)[:215] + '.csv'

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
            csv_data = session.post(redcap_url,data=data)

            if csv_data.status_code == 200:   
                with open(file_path, mode='wb') as file:
                    file.write(csv_data.content)
                    count += 1
            else:
                print(f'CSV Data Label: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                
    print(f'CSV Data Label: {count} files saved successfully')
    return count

def csv_data_dictionary(file_paths):
    count = 0
    with requests.Session() as session:
        for token, file_path in file_paths.items():
            #The base name of a path is the last component of the path
            file_name = os.path.basename(file_path)
            file_path = os.path.join(file_path, 'CSV Data Dictionary')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_path = os.path.join(file_path, file_name)[:215] + '.csv'

            data = {
                'token': token,
                'content': 'metadata',
                'format': 'csv',
                'returnFormat': 'csv'
            }
            csv_data = session.post(redcap_url,data=data)

            if csv_data.status_code == 200:   
                with open(file_path, mode='wb') as file:
                    file.write(csv_data.content)
                    count += 1
            else:
                print(f'CSV Data Dictionary: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                
    print(f'CSV Data Dictionary: {count} files saved successfully')
    return count

def xml_metadata_only(file_path):
    count = 0
    with requests.Session() as session:
        for token, file_path in file_paths.items():
            #The base name of a path is the last component of the path
            file_name = os.path.basename(file_path)
            file_path = os.path.join(file_path, 'XML Metadata Only')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_path = os.path.join(file_path, file_name)[:215] + '.xml'

            data_config = {'token' : token,
                          'content' : 'project_xml',
                          'format' : 'xml',
                          'returnMetadataOnly' : 'true',
                          'exportFiles' : 'false',
                          'exportSurveyFields' : 'false',
                          'exportDataAccessGroups' : 'false',
                          'returnFormat' : 'json'
                            }
            xml_data = session.post(redcap_url, data = data_config)

            # write xml to local storage
            if xml_data.status_code == 200:
                with open(file_path, mode = 'wb') as file:
                    file.write(xml_data.content)
                    count += 1
            else:
                print(f'XML Metadata Only: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                
    print(f'XML Metadata Only: {count} files saved successfully')
    return count

def xml_metadata_and_data(file_path):
    count = 0
    with requests.Session() as session:
        for token, file_path in file_paths.items():
            #The base name of a path is the last component of the path
            file_name = os.path.basename(file_path)
            file_path = os.path.join(file_path, 'XML Metadata and Data')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_path = os.path.join(file_path, file_name)[:215] + '.xml'

            data_config = {'token' : token,
              'content' : 'project_xml',
              'format' : 'xml',
              'returnMetadataOnly' : 'false',
              'exportFiles' : 'false',
              'exportSurveyFields' : 'false',
              'exportDataAccessGroups' : 'false',
              'returnFormat' : 'json'
                }
            xml_data = session.post(redcap_url, data = data_config)

            # write xml to local storage
            if xml_data.status_code == 200:
                with open(file_path, mode = 'wb') as file:
                    file.write(xml_data.content)
                    count += 1
            else:
                print(f'XML Metadata and Data: {count} files Saved! \n But Something Wrong with Loading {file_name}')
                
    print(f'XML Metadata and Data: {count} files saved successfully')
    return count
        

# Summary count of
print(f'Project_Catagory {" "*18} Count \n{"_"*40}')
for key in api_dictionary.keys():
    print(f'{key} : {" "*(35-len(key))} {len(api_dictionary[key])}')



projects = dict()
#! This code is from redcap Api: export project info
with requests.Session() as session:
    for project_category in api_dictionary.keys():
        project_list = []
        for token in api_dictionary[project_category]: 
            data = {
            'token': token,
            'content': 'project',
            'format': 'json',
            'returnFormat': 'json'
            }
            r =session.post(redcap_url,data = data).json()
            print(r['project_title'])
            project_list.append(r['project_title'])
            projects[project_category]=project_list




current_date = date.today().strftime('%B-%d-%Y')
root = 'E:\\MNTD\Backup\\'+current_date
sub_root_1 = ''
sub_root_2 = ''
sub_root_3 = ''
file_paths = dict()

if not os.path.exists(root):
    os.makedirs(root)
os.chdir(root)

for folder in projects.keys():
    sub_root_1 = folder
    if not os.path.exists(sub_root_1):
        os.makedirs(sub_root_1)
    for project, token in zip(projects[folder], api_dictionary[folder]): 
        if re.findall(r'[\/:?"<>|]', project):
              project = re.sub(r'[\\/:?"<>|]','_',project)
        # print(project)
        sub_root_2 = sub_root_1 + '\\' + project.strip()
               
        if not os.path.exists(sub_root_2):   #create directory in local computer if it doesn't exist
            os.makedirs(sub_root_2)
        file_paths[token] = sub_root_2    


print('All Folder Created Successfully')

count_csv_raw = csv_data_raw(file_paths)
print(f'Summary [CSV Raw Data]: {count_csv_raw} Total files saved successfully')

count_csv_label = csv_data_label(file_paths)
print(f'Summary [CSV LABELED Data]: {count_csv_label} Total files saved successfully')

count_data_dictionary = csv_data_dictionary(file_paths)
print(f'Summary [Data Dictionary]: {count_data_dictionary} Total files saved successfully')

count_xml_metadata_only = xml_metadata_only(file_paths)
print(f'Summary [Meta Data Only]: {count_xml_metadata_only} Total files saved successfully')

count_xml_metadata_and_data = xml_metadata_and_data(file_paths)
print(f'Summary [Meta Data and Data]: {count_xml_metadata_and_data} Total files saved successfully')
