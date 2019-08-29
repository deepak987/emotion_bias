import requests
import json
from secrets import get_secret
from utils import all_images_in_directory
import os

class MS_Face_Api_interface:
    subscription_key = get_secret('MS_API_KEY')
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }

    params = {
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'emotion',
    }
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def save_result_to_file(self, result, filename):

    def find_emotions(self):
        i = 0
        all_image_files = all_images_in_directory(self.directory_path)
        for filename in all_image_files:
            print (filename)
            if i>3:
                break
            i+=1
            with open(filename, 'rb') as image:
                im_data = image.read()
                response = requests.post(self.face_api_url, data = im_data, params=self.params, headers=self.headers )
                result = (json.dumps(response.json()))
                result = json.loads(result)[0]['faceAttributes']['emotion']
                print(result)

if __name__ == "__main__":
    model = MS_Face_Api_interface('../Data/FACES/')
    model.find_emotions()
