from google.cloud import vision
from google.cloud.vision import types
import io
import os
from utils import all_images_in_directory
import csv
import pandas as pd
class Google_Vision_Processor:
    def __init__(self, directory_path, outfile_path, overwrite_file=True):
        self.directory_path = directory_path
        self.outfile_path = outfile_path
        if overwrite_file:
            columns = ['image','sorrow', 'anger', 'joy', 'surprise']
            with open(outfile_path, "w+", newline='') as fp:
                wr = csv.writer(fp)
                wr.writerow(columns)

    def save_result_to_file(self, row):
        
        with open(self.outfile_path, "a", newline='') as fp:
            wr = csv.writer(fp)
            wr.writerow(row)
        
    def find_face_emotions(self):
        client = vision.ImageAnnotatorClient()
        all_image_files = all_images_in_directory(self.directory_path)
        already_done = list(pd.read_csv(self.outfile_path).image)

        for image_file_name in all_image_files:
            
            print(image_file_name)
            if image_file_name.split('/')[-1] in already_done:
                continue
            with io.open(image_file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # Performs label detection on the image file
            response = client.face_detection(image=image)
            faces = response.face_annotations

            # Names of likelihood from google.cloud.vision.enums
            likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                            'LIKELY', 'VERY_LIKELY')
            result = [image_file_name.split('/')[-1]]            
            for face in faces:
                result.append(likelihood_name[face.sorrow_likelihood])
                result.append(likelihood_name[face.anger_likelihood])
                result.append(likelihood_name[face.joy_likelihood])
                result.append(likelihood_name[face.surprise_likelihood])
                self.save_result_to_file(result)

        

gvp = Google_Vision_Processor('../Data/FACES_old_a/', '../Outputs/Google_Vision/FACES_old_a.csv', False)
gvp.find_face_emotions()

