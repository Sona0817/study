import warnings
warnings.filterwarnings('ignore')
import argparse
import numpy as np
import pandas as pd
import librosa
import joblib

def call_data():
    data, sr = librosa.load(args.wav_file, sr=16000)
    mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=args.n_mfcc)

    mean_mfcc = []
    mfccs = []
    for m in mfcc:
        mean_mfcc.append(np.mean(m))
    mfccs.append(mean_mfcc)
    
    meta_data = {'age':[args.age],
                 'gender':[args.gender],
                 'respiratory':[args.respiratory],
                 'fever_or_muscle':[args.fever_or_muscle_pain]
                 }
    df_meta = pd.DataFrame(meta_data)
    df_mfcc = pd.DataFrame(mfccs, columns=['mfcc'+str(i+1) for i in range(args.n_mfcc)])
    df = df_meta.join(df_mfcc)
    df.to_csv('./data_preprocessing.csv', index=False)

    return df

def test_model(data):
    model = joblib.load(args.model)
    pred = model.predict(data)
    print(pred)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wav_file, age, gender, respiratory, fever_or_muscle_pain, model')
    parser.add_argument('--wav_file', type=str, help='single wav file path')
    parser.add_argument('--id', type=int, default=1, help='patient id')
    parser.add_argument('--age', type=int, help='patient age')
    parser.add_argument('--gender', type=int, default=0, help='male=0, female=1')
    parser.add_argument('--respiratory', type=int, default=0, help='patient has respiratory? no=0, yes=1')
    parser.add_argument('--fever_or_muscle_pain', type=int, default=0, help='patient has fever or muscle pain? no=0, yes=1')
    parser.add_argument('--model', type=str, default='./SMOTE_RF.pkl', help='model file path')
    parser.add_argument('--n_mfcc', type=int, default=30, help='mfcc feature select')
    args = parser.parse_args()

    mfccs = []
    data = call_data()
    test_model(data)