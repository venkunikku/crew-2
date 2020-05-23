from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing  import StandardScaler, MinMaxScaler
from scipy import stats
import tensorflow as tf
from pylab import rcParams
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
import h5py
from keras.models import Sequential, load_model
from keras.layers import Input, Dense, BatchNormalization, Dropout, Conv1D, MaxPooling1D
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import regularizers
import numpy as np




## 10 classes
class_name = ([0 , 'air_conditioner'], [1, 'car_horn'], [2, 'children_playing'], [3, 'dog_bark'], 
                          [4, 'drilling'], [5, 'engine_idling'], [6, 'gun_shot'], [7, 'jackhammer'], 
                          [8, 'siren'], [9, 'street_music'])



## one_hot_encoede function for 10 labels 
def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode




# load features and labels

features_array = joblib.load('features_array.sav')
audio_class = joblib.load('audio_class.sav')


features = np.array(features_array)
labels = one_hot_encode(audio_class)


# Train, test, validation set split

train_x_temp, test_x, train_y_temp, test_y = train_test_split(features, labels, test_size=0.2, random_state=98)
train_x, valid_x, train_y, valid_y = train_test_split(train_x_temp, train_y_temp, test_size=0.2, random_state=432)

sc = StandardScaler()
sc.fit(train_x)


'''
Another suggestion is using minmax scaler
scaler = MinMaxScaler(feature_range=(-1,1))
scaler.fit(train_x)

'''

train_x = sc.transform(train_x)
valid_x = sc.transform(valid_x)
test_x = sc.transform(test_x)

## build Keras NN model
model=Sequential()

model.add(Dense(units=400,activation='relu', input_dim =149))
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(Dense(units=500,activation='relu'))
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(Dense(units=400,activation='relu'))
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(Dense(units=10,activation='softmax'))

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])


nb_epoch = 150
batch_size = [256]

for batches in batch_size:
    checkpointer = ModelCheckpoint(filepath="NN.h5",
                               verbose=0,
                               save_best_only=True)

    earlystopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0) # 'patience' number of not improving epochs

    history = model.fit(train_x, train_y,
                        epochs=nb_epoch,
                        batch_size=batches,
                        shuffle=True,
                        validation_data=(valid_x, valid_y),
                        verbose=1,
                        callbacks=[checkpointer,  earlystopping]).history