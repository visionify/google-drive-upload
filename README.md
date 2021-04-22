# google-drive-upload
Upload files/folders to google drive easily with Python.

## Overview
Sometimes you just want to upload a bunch of files to Google Drive. Maybe it's your backup images, or some of your old work documents. And it's cumbersome to do so manually.

This project shows you how you can achieve this without too much headache.   

Please share any suggestions and improvements through the Issues section on github.

## Prerequisites
* You would need to enable Google Drive v3 APIs on your Google Account. Follow the instructions available [here](https://developers.google.com/workspace/guides/create-project ) to create a GCP Project.
* After project is created, click on API & Services box and Create Credentials and OAuth Client ID. This would be used as credentials for this project. [This](https://developers.google.com/workspace/guides/create-credentials) page provides more details on how to create credentials. 
* Download the OAuth Client Credentials to your local machine. We will be using this in the next step. 

## Setup 
* On Google Drive, create a folder where documents will be uploaded. Update permissions for this folder ("Anyone with the link" to "Editor") 
* Note down the Folder ID. The folder ID is what's displayed at the end of GDrive URL. Example:
```
# The last part of the URL (1nuOnhLH...oS9JFZcnqr) is the GDrive folder ID. 
drive.google.com/drive/u/1/folder/1nuOnhLH...oS9JFZcnqr
```

* Clone this repository
```
git clone https://github.com/visionify/google-drive-upload.git
cd google-drive-upload
```

* Create a `.env` file with the local folder & the Google Drive folder.  
```
# This is the folder you would like to Zip and upload to Google Drive
folder=/Users/harsh/pictures

# This is the folder-id on Google Drive where you want to upload the images.
gdrive_folder=1nuOnhLH...oS9JFZcnqr
```

* Install need python dependencies.
```
pip3 -r requirements.txt
```

* Copy over the credentials.json file into this directory.

* Run the program. For the first run, this program would open up a browser where you can login and allow access to Google Drive. Subsequent runs will use the pre-stored credentials.
```
python3 gdrive-upload.py
```

## Feedback
Please share any feedback and suggestions through the Issues tab on Github.
 