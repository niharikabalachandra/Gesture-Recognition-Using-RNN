import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import load_model
from keras.utils import np_utils
from imblearn.over_sampling import SMOTE
import time

# Import dataset
dataset = pd.read_csv('/home/sharath/LeapDeveloperKit_2.3.1+31549_linux/LeapSDK/src/one_file.csv',header=None)

#Split to Data samples and labels
x = dataset.iloc[:, 1:11].values
y = dataset.iloc[:, 11].values

#Number of time series to work on is 60
t=60
n_samples=len(dataset)/t


#Reshape input samples to Nx60x11
x = np.reshape(x, (x.shape[0]/t, t, x.shape[1]))
#Set labels to these N samples
indices=[ind for ind in range(len(y)) if ind%t==0]
y=y[indices]

# One-hot encode the classes
from sklearn.preprocessing import LabelEncoder
label_encoder=LabelEncoder()
y_new=label_encoder.fit_transform(y)
y_one_hot=np_utils.to_categorical(y_new)
y=y_one_hot

#Split data to training and testing data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

#Construct the model
n_neurons=7
start_time=time.time()
model = Sequential()
model.add(LSTM(n_neurons, input_shape=(X_train.shape[1],X_train.shape[2])))
model.add(Dense(output_dim=2,init = 'uniform', activation='sigmoid'))
model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])

#Train the model 
model.fit(X_train, y_train, epochs=100, batch_size=5)

#Evaluation of the Training time
print "%s Minutes of Execution" %str((time.time()-start_time)/60)

#Save the model for prediction
model.save('model_test.h5')
print "Model Saved"

# Evaluate the model on CV Data
scores = model.evaluate(X_test, y_test, verbose=0)
print "%s: %.2f%%" % (model.metrics_names[1], scores[1]*100)
