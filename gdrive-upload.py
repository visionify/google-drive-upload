from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import zipfile
from tqdm import tqdm
import glob
import socket
import random

from dotenv import load_dotenv

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']

class GDriveUploader(object):
    def __init__(self):
        self.service = None

    def check_prereqs(self):
        if not os.path.exists('.env'):
            print('Please create a .env file and populate local_folder and gdrive_folder values.')
            return False

        if not os.path.exists('credentials.json'):
            print('Please create project on GCP Console and download the credentials.json for OAuth2')
            return False

        load_dotenv()
        self.local_folder = os.getenv('local_folder')
        self.gdrive_folder = os.getenv('gdrive_folder')

        if self.local_folder is None or self.gdrive_folder is None:
            print('Please create a .env file and populate local_folder and gdrive_folder values.')
            return False

        if not os.path.exists(self.local_folder):
            print('Folder {} not found. Please include the correct folder name under local_folder'.format(self.local_folder))
            return False

        return True

    def authenticate(self):
        """
        Authenticate with Google Drive using Drive v3 API.
        """

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

        self.service = build('drive', 'v3', credentials=creds)

    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

    def upload(self):

        print('Uploading file: {} to GDrive folder {}'.format(self.local_folder, self.gdrive_folder))
        print('Compressing local folder into ZIP file.')

        zipfile_name = os.path.basename(self.local_folder) + '.zip'
        zipf = zipfile.ZipFile(zipfile_name, 'w', zipfile.ZIP_DEFLATED)
        self.zipdir(self.local_folder, zipf)
        zipf.close()

        uploaded_file_name = os.path.basename(self.local_folder)
        file_metadata = {
            'name': uploaded_file_name,
            'parents': [self.gdrive_folder]
        }

        media = MediaFileUpload(
            zipfile_name,
            mimetype='application/octet-stream'
        )

        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        os.remove(zipfile_name)

        print('Upload complete for file {}, Gdrive ID: {}'.format(uploaded_file_name, file.get('id')))


def main():
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
    # Create the Google Drive Uploader Object
    gdrive = GDriveUploader()

    # Check for pre-requisites.
    if gdrive.check_prereqs() is False:
        print('Error during upload. Exiting.')
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
        return -1

    # Authenticate with Google Drive
    gdrive.authenticate()

    # Upload folders
    gdrive.upload()

    # Done.
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')


if __name__ == '__main__':
    main()
