import numpy as np
import pydot
import graphviz
from keras.utils import plot_model
from keras.models import Sequential
from keras.layers.core import Activation, Dense





training_data = np.array([[0,0],[0,1],[1,0],[1,1]])
target_data   = np.array([  [0],  [1],  [1],  [0]])

model = Sequential()

model.add(Dense(10,input_dim=2, activation='sigmoid'))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(1, activation='relu'))


# X  0   0
# X  0  
model.compile(loss='mean_squared_error', optimizer='adam',metrics=['binary_accuracy'])

plot_model(model, show_shapes=True, to_file='model.png')
model.fit(training_data, target_data,nb_epoch=5000, verbose=2)


print(model.predict(training_data))
