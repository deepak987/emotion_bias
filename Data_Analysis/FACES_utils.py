emotion_map = {
    'a' : 'anger',
    'd' : 'disgust',
    'f' : 'fear',
    'h' : 'happiness',
    'n' : 'neutral',
    's' : 'sadness'
}
def emotion_from_filename(filename):
    emotion_initial = filename.split('_')[-2]
    return emotion_map[emotion_initial]
    