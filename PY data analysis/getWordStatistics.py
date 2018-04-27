import numpy as np
from keras.preprocessing.text import text_to_word_sequence
import os
import pickle
#https://machinelearningmastery.com/prepare-text-data-deep-learning-keras/


#TODO: find adjacent words and make tuples.

allFoundWords = set()
wordRefrences = dict()
articlesWithWord = dict()

def process_line(text):
  assert type(text) is str
  result = text_to_word_sequence(text)
  wordsInArticle = set();
  for word in result:
    if word not in wordsInArticle: #first occourence
      wordsInArticle.add(word)#add it to tracker for THIS article
      if word not in allFoundWords:#if the word is new for all of the wikis, start counting it
        allFoundWords.add(word) #global tracker
        wordRefrences[word]=0   #global counter, LONG EXPLANATION PLACEHOLDER
        articlesWithWord[word]=0#global counter, per article
        wordsInArticle.add(word)#LOCAL tracker, ensures no duplicates
      articlesWithWord[word] += 1
    wordRefrences[word] += 1
      

filelist = os.listdir("../paradigms")
i = 0
try:
  for file in filelist:
    i += 1
    with open("../paradigms/"+file, encoding="utf8") as fp:
      print("Percent Progress: "+str(100*counter/len(filelist)))
      for line in iter(fp.readline, ''):
        process_line(line)

  pickleFile = open('./wordData.pkl','wb')
  pickle.dump({
    "allFoundWords":allFoundWords,
    "wordRefrences": wordRefrences,
    "articlesWithWord": articlesWithWord
  },pickleFile)
  pickleFile.close()
  
except Exception as e:
  print(e)
  print(file)
  print(line)
  raise(e)

# for key in sorted(wordRefrenes, key=wordRefrenes.get,reverse=True)[0:1000]:
# 	print(key + ' --- ' + str(wordRefrenes[key]))