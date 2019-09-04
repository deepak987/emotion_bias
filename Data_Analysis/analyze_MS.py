import pandas as pd 
from FACES_utils import emotion_from_filename
class MS_Face_Analyzer:
    """
    Convert the raw API result to a usable form
    """
    def __init__(self, datafile, dataset_name = 'FACES'):
        self.results_df = pd.read_csv(datafile)
        self.dataset = dataset_name
    
    def extract_true_labels(self):
        if self.dataset == 'FACES':
            self.results_df['true_label'] = self.results_df.image.apply(emotion_from_filename)

    def find_predicted_labels(self):
        MS_EMOTIONS = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
        self.results_df['prediction'] = (self.results_df[MS_EMOTIONS].idxmax(axis=1))

# analyzer = MS_Face_Analyzer('../Outputs/MS_Face/FACES_middle_a.csv')
# analyzer.find_predicted_labels()
# analyzer.extract_true_labels()
# print(analyzer.results_df)
