
import numpy as np
import tensorflow as tf

punct = True

path_str = ""
num_of_epochs = 2000
num_of_characters = 26
if(punct):
    path_str = "_punct"
    num_of_characters = 35
num_of_keyboards = 10000

data_file_path = "carpalx-0.12\keren\data" + path_str + ".txt"
features = np.zeros([num_of_keyboards, num_of_characters, num_of_characters], dtype=int)
labels = np.zeros([num_of_keyboards], dtype=float)

print("loading data...")
with open(data_file_path, 'r') as data_file:
    for f in range(num_of_keyboards):
        line = data_file.readline()
        values = line.split(' ')

        for i in range(num_of_characters):
            for j in range(num_of_characters):
                features[f][i][j] = int(values[num_of_characters*i+j])

        labels[f] = float(values[-1])


print("training...")
split_point = int(0.8*num_of_keyboards)
x_train = features[:split_point]
x_test = features[split_point:]
y_train = labels[:split_point]
y_test = labels[split_point:]

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(num_of_characters, num_of_characters)),
    tf.keras.layers.Dense(64, activation='relu'),
    #tf.keras.layers.Dropout(0.5),
    #tf.keras.layers.Dense(32, activation='relu'),
    #tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1)])

model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.001),
    loss='mean_absolute_error')

predictions = model.fit(
    x_train, y_train,
    epochs=num_of_epochs,
    validation_split=0.2)

model.save('saved_model/my_model' + path_str)

print("testing...")
model.evaluate(x_test, y_test, verbose=2)

#print("qwerty_label: ", qwerty_label)
#print("qwerty_prediction: ", model.predict(qwerty_onehot))