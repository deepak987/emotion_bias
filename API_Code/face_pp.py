import io
import os
import requests
import json
import time
from secrets import get_secret

from utils import all_images_in_directory
import csv
import pandas as pd


class Face_pp_Interface:
    headers = {
    "api_key": get_secret('FACE++_KEY'),
    "api_secret": get_secret('FACE++_SECRET'),
    "return_attributes": "emotion",
    }

    def __init__(self, directory_path, outfile_path, overwrite_file=True):
        self.directory_path = directory_path
        self.outfile_path = outfile_path
        self.columns = ['sadness', 'neutral','disgust', 'anger', 'surprise', 'fear', 'happiness']

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
            row = [file_name.split('/')[-1]]
            print(i, file_name)
            i+=1

            files = {"image_file": open(file_name, 'rb')}
            url = "https://api-us.faceplusplus.com/facepp/v3/detect"
            r = requests.post( url, data=self.headers, files=files)
            json_string = json.loads(r.content)
            
            emotions = json_string['faces'][0]['attributes']['emotion']
            for c in self.columns:
                row.append(emotions[c])
        
            self.save_result_to_file(row)
            
            
if __name__ == "__main__":
    model = Face_pp_Interface('../Data/FACES_young_a/resized/', '../Outputs/Facepp/FACES_young_a.csv')
    model.find_face_emotions()

