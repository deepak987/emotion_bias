import pandas as pd
from FACES_utils import emotion_from_filename


class Sighthound_Processor:
    """
    Convert the raw API result to a usable form
    """
    def __init__(self, datafile, dataset_name = 'FACES'):
        self.results_df = pd.read_csv(datafile)
        self.dataset = dataset_name
 
    def extract_true_labels(self):
        if self.dataset == 'FACES':
            self.results_df['true_label'] = self.results_df.Image.apply(emotion_from_filename)

    def find_predicted_labels(self):
        sighthound_emotions = ['neutral', 'sadness', 'disgust', 'anger', 'surprise', 'fear', 'happiness']
        self.results_df['prediction'] = (self.results_df[sighthound_emotions].idxmax(axis=1))