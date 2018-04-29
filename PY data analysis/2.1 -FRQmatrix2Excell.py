import pandas as pd
import numpy
import pickle

file = open("wordNeighborMatrix.pkl","rb")

## convert your array into a dataframe
df = pd.DataFrame (pickle.load(file))

## save to xlsx file

filepath = 'wordFreq.csv'

df.to_csv(filepath, index=False)