import os
import numpy as np
import pickle
from keras.preprocessing.text import text_to_word_sequence

numWords = 4096 #more than 95% of words
counterThing = np.zeros(#this is really big and might crash
  shape=(numWords,numWords),
)
wordStatsFile = open('./wordFreqData.pkl','rb')
WR = pickle.load(wordStatsFile)["wordRefrences"]
wordStatsFile.close()
del wordStatsFile #doesnt delete from disk
sortedListOfWords = sorted(WR, key=WR.get, reverse=True)[0:numWords]
del WR
filelist = os.listdir("../paradigms")
i = 0
progPCTctr = 0
counter=0


def process_line(text):
  visibilityRadius=8
  assert type(text) is str
  sequence = text_to_word_sequence(text)
  for i in range(len(sequence)): #could these lines be optimized further? this feels bruteforcy.
    focusword = sequence[i]
    if focusword in sortedListOfWords:
      focusIndex = sortedListOfWords.index(focusword)
      for j in range(i-visibilityRadius,i+visibilityRadius):
        if j > 0 and j < len(sequence) and sequence[j] in sortedListOfWords:
          targetWord = sequence[j]
          targetIndex = sortedListOfWords.index(targetWord)
          counterThing[focusIndex][targetIndex] += 1

for fileSTR in filelist:
  try:
    with open("../paradigms/"+fileSTR, encoding="utf8") as fp:
      print("Scanning file: "+str(fileSTR))
      for line in iter(fp.readline, ''):
        process_line(line)
  except Exception as error:
    print("didnt scan file "+str(error))
  finally:
    counter += 1
    progPCT = 100*counter/len(filelist)
    # if progPCT > progPCTctr:
    progPCTctr = int(progPCT)+2 #occasionally
    print(str(progPCT)+' of files scanned')

for i in range(len(counterThing)):
  row = counterThing[i]
  highest_val = int(max(row))
  if highest_val is not 0:
    for j in range(len(row)):
      row[j] /= highest_val

MATFILE = open("wordNeighborMatrix.pkl","wb")
pickle.dump(counterThing,MATFILE)
MATFILE.close()
  