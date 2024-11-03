This Python Project Called 'REDCap_Backup'.

The project developed to take regular project backup from the REDCap remote server, and save into local storage in organized file structure.

How it work
1. The python request an API request to the REDCap server.
2. Fetch the data in various format (csv raw, csv label, data dictionary, XML metadata, and  XML metadata with data)
3. Organize it with the format -- Date |
                                       | -> Project Category |
                                                             | -> Project Name  |
                                                                                | Project File Type |
                                                                                                    | data File
4. Finaly save those files into local storage.
                                          
