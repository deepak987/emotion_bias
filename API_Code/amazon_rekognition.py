import boto3
import csv
from utils import all_images_in_directory
import pandas as pd
class Amazon_Rekognition_Processor:
    
    


    def __init__(self, directory_path, outfile_path, overwrite_file=True):
        self.directory_path = directory_path
        self.outfile_path = outfile_path
        self.columns = ['CALM', 'FEAR', 'HAPPY', 'ANGRY', 'DISGUSTED', 'SURPRISED', 'CONFUSED', 'SAD']
        if overwrite_file:
            with open(outfile_path, "w+", newline='') as fp:
                wr = csv.writer(fp)
                wr.writerow(['Image']+self.columns)
        self.client=boto3.client('rekognition')

    def save_result_to_file(self, result):
        
        with open(self.outfile_path, "a", newline='') as fp:
            wr = csv.writer(fp)
            wr.writerow(result)
        
        
    def find_face_emotions(self):
        
        already_done = pd.read_csv(self.outfile_path)
        all_image_files = all_images_in_directory(self.directory_path)
        for filename in all_image_files:
            print (filename.split('/')[-1])
            if  already_done.Image.str.contains(filename.split('/')[-1]).any():
                print('already done')
                continue
            
            with open(filename, 'rb') as image:
                response = self.client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
                if len(response['FaceDetails'])==0:
                    result = [filename,'Not Found']
                else:
                    emotions = response['FaceDetails'][0]['Emotions']
                    confidences = {}
                    for e in emotions:
                        confidences[e['Type']] = e['Confidence']
                    print(confidences)
                    result = [filename.split('/')[-1]]

                    for col in self.columns:
                        result.append(confidences[col])
                self.save_result_to_file(result)


if __name__ == "__main__":
    model = Amazon_Rekognition_Processor('../Data/FACES_middle_a/', '../Outputs/Amazon_Rekognition/FACES_middle_a.csv')
    model.find_face_emotions()

