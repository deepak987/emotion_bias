import pandas as pd
numeric_values = {
    'VERY_UNLIKELY':1,
    'UNLIKELY':2,
    'POSSIBLE':3,
    'LIKELY':4,
    'VERY_LIKELY':5
}

def to_numeric(vision_result_path):
    df = pd.read_csv(vision_result_path)
    df['sorrow'] = df.sorrow.apply(lambda x: numeric_values.get(x,-1))
    df['anger'] = df.anger.apply(lambda x: numeric_values.get(x,-1))
    df['joy'] = df.joy.apply(lambda x: numeric_values.get(x,-1))
    df['surprise'] = df.surprise.apply(lambda x: numeric_values.get(x,-1))
    print(df)

to_numeric('../Outputs/Google_Vision/FACES_old_a.csv')