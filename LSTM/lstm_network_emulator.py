import tensorflow as tf
import os
import numpy as pd
import pandas as pd

# read from the local file 
file_location = './data.csv'

first_dataset = pd.read_csv(file_location)

first_dataset.head()

first_dataset_indexed = first_dataset.set_index(['Time'])

throughput = first_dataset_indexed["Throughput"]
throughput.plot()

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
first_dataset_scaled = scaler.fit_transform(first_dataset_indexed)

from sklearn.model_selection import train_test_split

train, test = train_test_split(first_dataset_scaled, test_size=0.10, shuffle=False)

from keras.preprocessing.sequence import TimeseriesGenerator

n_input = 3
n_features = 1

generatorTrain = TimeseriesGenerator(train, train, length=n_input, batch_size=2)
generatorTest = TimeseriesGenerator(test, test, length=n_input, batch_size=1)

batch_0 = generatorTrain[0]
x, y = batch_0

print("Samples: %d" % len(generatorTrain))

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

model = Sequential()
model.add(LSTM(300, activation='sigmoid', input_shape=(n_input, n_features)))
model.add(Dense(1))
model.summary()

model.compile(optimizer='adam', loss='mse')
model.fit(generatorTrain, epochs=10, batch_size=15, shuffle=False)

import numpy as np

predictions = []

first_batch = train[-n_input:]
current_batch = first_batch.reshape((1, n_input, n_features))

for i in range(len(test)):
    current_pred = model.predict(current_batch)[0]
    predictions.append(current_pred)
    current_batch_rmv_frist = current_batch[:, 1:, :]
    current_batch = np.append(current_batch_rmv_frist, [[current_pred]], axis=1)

import matplotlib.pyplot as plt

predictions_actual_size = scaler.inverse_transform(predictions)
test_data_actual_scale = scaler.inverse_transform(test)


throughput = first_dataset_indexed["Throughput"]

# Save the initial graph as an image
fig, ax = plt.subplots()
ax.plot(throughput)
ax.set_title('Initial Throughput')
plt.savefig('./out/initial_throughput_plot.png')

# ...

# Save the plots as images
fig, ax = plt.subplots()
ax.plot(predictions_actual_size, label='Predictions')
ax.plot(test_data_actual_scale, label='Actual')
ax.legend()
plt.savefig('./out/results_plot.png')


from sklearn.metrics import accuracy_score, mean_squared_error

mean_squared_error(test, predictions)

import pickle

with open('VanillaEpoch300.pkl', 'wb') as f:
    pickle.dump(model, f)
