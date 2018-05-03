from keras.layers.core import Activation, Dense
from keras.models import Sequential
# from keras.utils import plot_model
import numpy as np
import pickle
import keras
import time
import os

#https://www.packtpub.com/mapt/book/big_data_and_business_intelligence/9781787128422/5/ch05lvl1sec37/exploring-glove

targetDataFile = open("wordNeighborMatrix.pkl","rb")
targetData = np.matrix(pickle.load(targetDataFile))
mask = np.multiply(np.identity(4096)-1,-1) #0 1 1; 1 0 1; 1 1 0 ...
targetData = np.multiply(targetData,mask) #if two words are next to each other, doesnt matter
trainingData = np.identity(4096) #not a placeholder.

model = Sequential()

model.add(Dense(300,input_dim=4096,activation="sigmoid"))
model.add(Dense(4096,activation="sigmoid"))

model.compile(
  loss='mean_squared_error',
  optimizer='adam',
  metrics=['accuracy','mean_squared_error','mean_squared_logarithmic_error','categorical_crossentropy','logcosh'],
)

# plot_model(model, show_shapes=True, to_file='model.png')

inp = input("\n\n\nWould you like to try and load a weights file?\nType the filename, or leave blank for no:\n\n$/3.1 - nn_checkpoints/")
initEPO = 0
if inp != "":
  print("\n")
  print("loading weights...\n(SYSTEM MAY FREEZE FOR ~30 SECONDS if using gpu)")
  model.load_weights("./3.1 - nn_checkpoints/"+str(inp))
  print("weights loaded!")
else:
  print("\nok, lets start fresh!")
time.sleep(2)
print("LET THE TRAINING BEGIN!\n\n\n")

model.fit(
  trainingData, targetData,
  initial_epoch= initEPO,
  epochs=300000,
  verbose=2,
  batch_size=128,#128 examples per epoch
  callbacks = [
    keras.callbacks.ModelCheckpoint(
      "./3.1 - nn_checkpoints/v6-sigmoid-weights.hdf5",
      verbose=0,
      save_best_only=False,
      save_weights_only=False,
      mode='auto',
      period=500, #save weights every 500 epochs
    ),
    keras.callbacks.TensorBoard(
      log_dir='./3.2 - Graph/v6 sigmoid',
      write_graph=True,
      # write_grads=True,b
      # histogram_freq=500,
      # embeddings_metadata="./3.2 - Metadata",
      # embeddings_freq=500,
      # embeddings_layer_names=2,
      # write_images=True,
    ),
  ],
) 