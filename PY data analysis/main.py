import numpy as np
import tensorflow as tf
from keras.layers import Dense, Dropout, Activation
from keras.models import Sequential

model = Sequential()

model.add(Dense(10, input_dim=2, activation="sigmoid"))
model.add(Dense(10, activation="sigmoid"))
model.add(Dense(1, activation="sigmoid"))
model.add(Activation('sigmoid'))
model.compile(
  loss='binary_crossentropy', 
  optimizer='sgd',
  metrics=['accuracy'],
)

x=np.array([[0,0],[0,1],[1,0],[1,1]])
y=np.array([[0],[1],[1],[0]])#.transpose()

model.fit(x, y, epochs=30, batch_size=4)

print(model.predict(np.array([[0,1]])))