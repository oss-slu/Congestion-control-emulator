import tensorflow as tf
import argparse
import tensorflow as tf
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import TimeseriesGenerator 
from keras.models import Sequential 
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math
import matplotlib.pyplot as plt


file_location = './data_ingress.csv'

first_dataset = pd.read_csv(file_location)

first_dataset.head()

first_dataset_indexed = first_dataset.set_index(['Time'])

throughput = first_dataset_indexed["Throughput"]

# set up command-line argument parser
parser = argparse.ArgumentParser(description='Train an LSTM model with custom parameters.')
parser.add_argument('--epochs', type=int, default=10, help='Number of epochs for training.')
parser.add_argument('--predictions', type=int, default=10, help='# of predictions past runtime in seconds')
parser.add_argument('--n_input', type=int, default=10, help='change this value based on how much data you have for more accurate predictions')
args = parser.parse_args()

epochs = args.epochs
seconds_past = args.predictions
ninput = args.n_input

scaler = MinMaxScaler()
first_dataset_scaled = scaler.fit_transform(first_dataset_indexed)

train,test = train_test_split(first_dataset_scaled, test_size = 0.10, shuffle = False)

n_input = ninput
n_features = 1

generatorTrain = TimeseriesGenerator(train, train, length=n_input, batch_size=2)
generatorTest = TimeseriesGenerator(test, test, length=n_input, batch_size=1)

batch_0 = generatorTrain[0]
x ,y = batch_0

#These print statements help visualize the data processing and generatorTrain the LSTM uses

#print(x,y)
#number of samples
#print("Samples: %d" % len(generatorTrain))
#print each sample
#for i in range(len(generatorTrain)):
  #x, y = generatorTrain[i]
  #print('%s => %s' % (x , y))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(300, activation = 'tanh',input_shape=(n_input, n_features)))
model.add(Dense(1))
#model.add(Dropout(.02))
model.summary()

from keras.optimizers import Adam

#editing learning rate
learning_rate = 0.001
optimizer = Adam(learning_rate=learning_rate)

model.compile(optimizer=optimizer, loss='mse')
model.fit(generatorTrain, epochs=epochs, batch_size=80, shuffle=False)

import numpy as np
predictions = []

first_batch = train[-n_input:]
current_batch = first_batch.reshape((1, n_input, n_features))
#print(current_batch)

#while loop to adjust how much the model is trained (change training<(this part))
training = 0
while(training<3):
    for i in range(len(test)):
        #get the prediction value for first
        current_pred = model.predict(current_batch)[0]

        #append the prediction into array
        predictions.append(current_pred)

        #remove the first value
        current_batch_rmv_frist = current_batch[:,1:,:]
        #update the batch
        current_batch = np.append(current_batch_rmv_frist,[[current_pred]],axis=1)
    training+=1

#print([i[0] for i in predictions])

predictions_actual_size = scaler.inverse_transform(predictions)
test_data_actual_scale = scaler.inverse_transform(test)

plt.plot(predictions_actual_size)
plt.plot(test_data_actual_scale)

# New variable for amount of predictions in seconds past the data cutoff

predictions = []

first_batch = train[-n_input:]
current_batch = first_batch.reshape((1, n_input, n_features))

# Predict len(test) + seconds_past data points
for i in range(len(test) + seconds_past):
    current_pred = model.predict(current_batch)[0]
    predictions.append(current_pred)
    current_batch_rmv_frist = current_batch[:, 1:, :]
    current_batch = np.append(current_batch_rmv_frist, [[current_pred]], axis=1)

# Rescale the predictions to the original data scale
predictions_actual_size = scaler.inverse_transform(predictions)

# Create x-axis values for the predictions
x_test = np.arange(len(train), len(train) + len(test) + seconds_past, 1)

# Save the plots as images
fig, ax = plt.subplots()
ax.plot(predictions_actual_size, label='Predictions')
ax.plot(test_data_actual_scale, label='Actual')
ax.legend()
plt.savefig('./out/results_plot.png')

# Truncate predictions_actual_size to match the length of test_data_actual_scale
truncated_predictions_actual_size = predictions_actual_size[:len(test_data_actual_scale)]

mse = mean_squared_error(test_data_actual_scale, truncated_predictions_actual_size)
rmse = math.sqrt(mse)
mae = mean_absolute_error(test_data_actual_scale, truncated_predictions_actual_size)

print("Mean squared error (MSE): ", mse)
print("Root mean squared error (RMSE): ", rmse)
print("Mean absolute error (MAE): ", mae)
