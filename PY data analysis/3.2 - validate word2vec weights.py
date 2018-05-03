from keras.layers.core import Activation, Dense
from keras.models import Sequential
from keras.utils import plot_model
from math import floor,sqrt
import numpy as np
import random
import pickle
import keras
import time
import sys
import os



#https://www.packtpub.com/mapt/book/big_data_and_business_intelligence/9781787128422/5/ch05lvl1sec37/exploring-glove

originalDataFile = open("wordNeighborMatrix.pkl","rb")
wordStatsFile = open('./wordFreqData.pkl','rb')
numWords = 4096 #more than 95% of words
originalData = pickle.load(originalDataFile)


WR = pickle.load(wordStatsFile)["wordRefrences"]
wordStatsFile.close()
del wordStatsFile #doesnt delete from disk
sortedListOfWords = list(sorted(WR, key=WR.get, reverse=True)[0:numWords])

EarlyModel = Sequential()
model = Sequential()
model.add(Dense(300,input_dim=4096,activation="sigmoid"))
EarlyModel.add(Dense(300,input_dim=4096,activation="sigmoid"))
model.add(Dense(4096,activation="sigmoid"))
EarlyModel.add(Dense(4096,activation="sigmoid"))

# model.compile(
#   loss='logcosh',
#   optimizer='adam',
#   metrics=['categorical-crossentropy','mean-squared-logarithmic-error','logcosh','mean-squared-error'],
# )

inp = "word2vec v6.hdf5" #input("\n\n\nType in the name of the weights file:\n\n ./3.1 - nn_checkpoints/")
model.load_weights("./3.1 - nn_checkpoints/"+str(inp))
EarlyModel.load_weights("./3.1 - nn_checkpoints/"+str(inp))
EarlyModel.pop()
# model.pop()
print("weights loaded!")

def gradify(number):
  min=0
  max=1
  
  gradients = u".░▒▓█"
  # gradients = "012345"
  if number <= min: 
    return gradients[0]
  if number >= max:
    return gradients[-1]
  return gradients[floor((len(gradients))*number)]


template = """
Word: {word}
  Appears around: {neighbors_actual}
  Prediction: {neighbors_pred}
  "Fingerprint":"""

os.system("cls")
response = ""
prevResp = ""
prevVec = [
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,

0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,

0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0] # is this lazy? yes. does it work? yes. does python have a good alternative? no.

while True:
  neighborCT = 10

  wordIndex = random.randint(0,4096)
  if response in sortedListOfWords:
    wordIndex = sortedListOfWords.index(response)
  elif response != "":
    response = input("didn't work, try again?")
    continue

  word = sortedListOfWords[wordIndex]
  vectorOfNeighbors = list(originalData[wordIndex])
  neighborIndexSorted = np.argsort(vectorOfNeighbors) #get indicies

  appearSTR = ""
  

  for i in range(1,10):
    index = neighborIndexSorted[-i]
    appearSTR += '{word}:({freq})\n    '.format(
      word=(sortedListOfWords)[index],
      freq=floor(1000*vectorOfNeighbors[index]),
    )
  appearSTR = '\n    '.join(sorted(appearSTR.split()))

  predictionSTR = ""
  word2vec300 = list(EarlyModel.predict(
    np.matrix(list(np.identity(4096)[wordIndex]))
  )[0])
  prediction = list(model.predict(
    np.matrix(list(np.identity(4096)[wordIndex]))
  )[0])

  predictedNeighborIndexSorted = np.argsort(prediction) #get indicies

  for i in range(1,10):
    index = predictedNeighborIndexSorted[-i]
    predictionSTR += '{word}:({freq})\n    '.format(
      word=sortedListOfWords[index],
      freq=floor(1000*prediction[index]),
    )
  predictionSTR = '\n    '.join(sorted(predictionSTR.split()))
  

  fingerprintSTR = ""
  for i in range(300):
    if i is 30:
      pass
      # fingerprintSTR +="\n"
    if i % 30 is 0:
      fingerprintSTR += "\n"
    fingerprintSTR += gradify(word2vec300[i])
  
  sys.stdout.buffer.write(template.format(
    word=word,
    neighbors_actual=appearSTR,
    neighbors_pred=predictionSTR,
  ).encode('utf8'))
  
  distance = 0
  for i in range(300):
    distance += (prevVec[i]-word2vec300[i])**2
  distance = sqrt(distance)

  sys.stdout.buffer.write(fingerprintSTR.encode('utf8'))

  sys.stdout.buffer.write(("similarity to previous response: "+str(distance)).encode('utf8'))
  time.sleep(.5)

  prevVec = word2vec300
  prevResp = response
  

  response = input('\nType in a word, or hit enter for random:\n> ')

  