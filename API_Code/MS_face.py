import requests
import json
from secrets import get_secret
from utils import all_images_in_directory
import os
import time
import csv
import pandas as pd

class MS_Face_Interface:
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

    def __init__(self, directory_path, outfile_path, overwrite_file=True):
        self.directory_path = directory_path
        self.outfile_path = outfile_path
        if overwrite_file:
            columns = ['image','anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
            with open(outfile_path, "w+", newline='') as fp:
                wr = csv.writer(fp)
                wr.writerow(columns)

    def save_result_to_file(self, result, imagename):
        keys = list(result.keys())
        keys.sort()
        row = [imagename]
        for k in keys:
            row.append(result[k])
        with open(self.outfile_path, "a", newline='') as fp:
            wr = csv.writer(fp)
            wr.writerow(row)
        
    def find_face_emotions(self):
        i = 0
        start = time.time()
        previous = start - 3
        already_done = pd.read_csv(self.outfile_path)
        print(already_done)
        all_image_files = all_images_in_directory(self.directory_path)
        for filename in all_image_files:
            print (filename.split('/')[-1])
            if  already_done.image.str.contains(filename.split('/')[-1]).any():
                print('already done')
                continue
            
            i+=1
            print(i)
            with open(filename, 'rb') as image:
                im_data = image.read()
                while time.time() - previous < 3:
                    time.sleep(0.1)
                previous = time.time()
                response = requests.post(self.face_api_url, data = im_data, params=self.params, headers=self.headers )
                print ('request',time.time() - start)
                result = (json.dumps(response.json()))
                result = json.loads(result)[0]['faceAttributes']['emotion']
                self.save_result_to_file(result, filename.split('/')[-1])

if __name__ == "__main__":
    model = MS_Face_Interface('../Data/FACES_young_a/', '../Outputs/MS_Face/FACES_young_a.csv')
    model.find_face_emotions()
