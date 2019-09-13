import base64
import json
import time
import io
import os
import ssl
import http.client as httplib  # Python 3
import requests
from secrets import get_secret
from utils import all_images_in_directory
import os
import csv
import pandas as pd

class Sighthound_Interface:
    subscription_key = get_secret('MS_API_KEY')
    headers = {"Content-type": "application/json",
           "X-Access-Token": get_secret('SIGHTHOUND_API_KEY')}

    def __init__(self, directory_path, outfile_path, overwrite_file=True):
        self.directory_path = directory_path
        self.outfile_path = outfile_path
        self.columns = ['neutral', 'sadness', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

        if overwrite_file:
            with open(outfile_path, "w+", newline='') as fp:
                wr = csv.writer(fp)
                wr.writerow(['Image']+self.columns)

    def save_result_to_file(self, result):
        with open(self.outfile_path, "a", newline='') as fp:
            wr = csv.writer(fp)
            wr.writerow(result)
        
    def find_face_emotions(self):
        
        all_image_files = all_images_in_directory(self.directory_path)
        i=0
        for file_name in all_image_files:
            print(i, file_name)
            i+=1
            conn = httplib.HTTPSConnection("dev.sighthoundapi.com", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

            image_data = base64.b64encode(open(file_name, "rb").read()).decode()
            params = json.dumps({"image": image_data})
            conn.request("POST", "/v1/detections?type=face,person&faceOption=emotion", params, self.headers)
            response = conn.getresponse()
            result = response.read()
            #print("Detection Results = " + str(result))
            result = json.loads(result)
            row = [file_name.split('/')[-1]]

            time.sleep(2)
            if "objects" in result: 
                for o in result['objects']:
                    if o.get('attributes'):

                        emotions = o['attributes']['emotionsAll']
                        for c in self.columns:
                            row.append(emotions[c])
            self.save_result_to_file(row)
            
if __name__ == "__main__":
    model = Sighthound_Interface('../Data/FACES_middle_a/', '../Outputs/Sighthound/FACES_middle_a.csv')
    model.find_face_emotions()





   