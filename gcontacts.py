from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv

# Modify this to your .csv file name
filename = "contacts.csv"


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/contacts']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)


    # Call the People API
    print('List 10 connection names')
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=10,
        personFields='names,emailAddresses,phoneNumbers').execute()
    connections = results.get('connections', [])

    for person in connections:
        names = person.get('names', [])
        if names:
            name = names[0].get('displayName')
            nums = person.get('phoneNumbers', [])            
            print(name)
            if nums:
                num = nums[0].get('value')
                print(num)
            print('\n')
        
    #add contacts from a csv file:
    fields = [] 
    rows = [] 
    with open(filename, 'r') as csvfile: 
        csvreader = csv.reader(csvfile) 
        fields = next(csvreader) 

        for row in csvreader: 
            rows.append(row) 

        print("Total no. of rows: %d"%(csvreader.line_num)) 
    
    print('Field names are:' + ', '.join(field for field in fields)) 
    print('\nFirst 5 rows are:\n') 
    for row in rows[:5]: 
        for col in row: 
            print("%10s"%col), 
        print('\n') 

    print("Entering the data: ")
    for row in rows:
        x = 0
        thisName = None
        thisNumber = None
        for col in row:
            # Name:
            if x == 0: 
                thisName = col
            # No:
            if x == 1:
                thisNumber = col
            x = x + 1
        if thisName is None or thisNumber is None:
            print("Error: One or More fields is empty")
            continue
        response = service.people().createContact(
            body={
                    "names": [
                        {
                            "givenName": thisName
                        }
                    ],
                    "phoneNumbers": [
                        {
                            'value': thisNumber
                        }
                    ]
                }
        ).execute()
        print('created: ')
        print(response)

        
        



    
    
    
    # # Call the People API to delete all users: 
    # print('List 10 connection names')
    # results = service.people().connections().list(
    #     resourceName='people/me',
    #     pageSize=10,
    #     personFields='names,emailAddresses,phoneNumbers').execute()
    # connections = results.get('connections', [])

    # for person in connections:
    #     print('Deleting')
    #     names = person.get('names', [])
    #     if names:
    #         name = names[0].get('displayName')
    #         nums = person.get('phoneNumbers', [])            
    #         print(name)
    #         if nums:
    #             num = nums[0].get('value')
    #             print(num)
    #     # Deleting the user
    #     toDel = person.get('resourceName')
    #     service.people().deleteContact(
    #         resourceName = toDel
    #     ).execute()   
            




if __name__ == '__main__':
    main()