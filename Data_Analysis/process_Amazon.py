import pandas as pd
from FACES_utils import emotion_from_filename


class Amazon_Processor:
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
        amazon_emotions = ['CALM', 'FEAR', 'HAPPY', 'ANGRY', 'DISGUSTED', 'SURPRISED', 'CONFUSED', 'SAD']
        self.results_df['prediction'] = (self.results_df[amazon_emotions].idxmax(axis=1))