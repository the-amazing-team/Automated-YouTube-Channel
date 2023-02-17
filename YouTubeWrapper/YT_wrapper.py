#using YouTube API  
 import os 
 import google.auth 
 import google.auth.transport.requests 
 import google.oauth2.credentials 
 import googleapiclient.errors 
 import googleapiclient.discovery 
 import googleapiclient.http 
  
 # Set the path to the video file 
 VIDEO_FILE = "path/to/your/video.mp4" 
  
 # Set the title, description, tags and privacy status for the video 
 VIDEO_TITLE = "My Awesome Video" 
 VIDEO_DESCRIPTION = "This is a video I created using Python!" 
 VIDEO_TAGS = ["Python", "Programming", "Tutorial"] 
 VIDEO_PRIVACY = "unlisted"  # Set to "private", "public" or "unlisted" 
  
 # Setting the API scopes and credentials 
 SCOPES = ["https://www.googleapis.com/auth/youtube.upload"] 
 CLIENT_SECRETS_FILE = "client_secrets.json" 
 API_NAME = "youtube" 
 API_VERSION = "v3" 
  
 # Authenticate with the YouTube API  
 credentials = None 
 if os.path.exists("token.json"): 
     credentials = google.oauth2.credentials.Credentials.from_authorized_user_file("token.json", SCOPES) 
 if not credentials or not credentials.valid: 
     if credentials and credentials.expired and credentials.refresh_token: 
         credentials.refresh(google.auth.transport.requests.Request()) 
     else: 
         flow = google.auth.OAuth2WebServerFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES) 
         credentials = flow.run_local_server(port=0) 
     with open("token.json", "w") as token: 
         token.write(credentials.to_json()) 
  
 # Creating a YouTube client 
 youtube = googleapiclient.discovery.build(API_NAME, API_VERSION, credentials=credentials) 
  
 # Creating a request to upload the video 
 request_body = { 
     "snippet": { 
         "title": VIDEO_TITLE, 
         "description": VIDEO_DESCRIPTION, 
         "tags": VIDEO_TAGS 
     }, 
     "status": { 
         "privacyStatus": VIDEO_PRIVACY 
     } 
 } 
 media_file = googleapiclient.http.MediaFileUpload(VIDEO_FILE) 
 upload_request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file) 
  
 # Upload and result 
 response = upload_request.execute()
