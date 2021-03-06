from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret_google.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_email(service, messageId):
    message = service.users().messages().get(userId='me', id=messageId).execute()
    #save_email(message)
    #print("get_email returning: " + str(message));
    return message;

#
def save_email(email):
    file = open("emails/" + email['id'] + ".json", 'w', -1)
    file.write(str(email))
    file.close()
    #print(str(email['payload']['headers']));
    subject = ''
    for header in email['payload']['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
    print(subject)

def subjectForEmail(email):
    for header in email['payload']['headers']:
        if header['name'] == 'Subject':
            return str(header['value'])
    return "no subject found"


def getListOfNewEmailSubjects():
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    response = service.users().messages().list(userId="me",q="label:inbox is:unread category:primary").execute()

    messages = []
    metadatas = []

    if len(messages) >10:
        print("More than 10 messages. Aborting...")
        return
    
    if 'messages' in response:
        messages.extend(response['messages'])

    subjects = []

    for message in messages:
        #print("getting email " + str(message)) 
        subject = subjectForEmail(get_email(service, message['id']))
        subjects.append(subject)
        print("Subject: " + subject)

    return subjects;

#
def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])
    """

    """credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    response = service.users().messages().list(userId='me', q='METADATA').execute()

    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    for message in messages:
        get_email(service, message['id'])
        break"""

    print("Emails received: " + str(getListOfNewEmailSubjects()))

if __name__ == '__main__':
    main()
