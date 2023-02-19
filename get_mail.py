from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from bs4 import BeautifulSoup



def get_topN_mails(n=10):
    creds = Credentials.from_authorized_user_file('token.json', ['https://mail.google.com/'])
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().list(userId='me', maxResults=10).execute()


    message_list=[]
    if 'messages' in result:
        messages = result['messages']
        
        for message in messages:    
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            if msg['payload']['mimeType'] == 'text/html':
                    
                    data = msg['payload']['body']['data']
                    decoded_data = base64.urlsafe_b64decode(data).decode()
                    soup = BeautifulSoup(decoded_data, "html.parser")
                    #print(soup.get_text())
                    message_list.append(soup.get_text())
            else:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == "text/plain":
                                    
                        data = part['body']['data']
                        #base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
                        decoded_data = base64.urlsafe_b64decode(data.encode('ASCII')).decode()
                        message_list.append(decoded_data)
                        #print(decoded_data)
    return message_list
      
            
                
            