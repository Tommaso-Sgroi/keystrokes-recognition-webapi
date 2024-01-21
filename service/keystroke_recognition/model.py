from random import random
from joblib import load
from os import sep
import numpy as np
from keras import Input, Model
from keras.src.initializers.initializers import RandomNormal
from keras.src.layers import Dense, Masking, Lambda, Flatten
from keras import backend as K
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
for device in physical_devices:
    tf.config.experimental.set_memory_growth(device, True)


class ModelInterface(object):
    def __init__(self, shape, threshold=0.5):
        self.shape = shape
        self.threshold = threshold


class RandomModel(ModelInterface):

    def predict(self, input_data, probe_data):
        # reshape the input data
        pred = random()
        return pred, (pred > self.threshold) and len(input_data) > 0 and len(probe_data) > 0


def create_siamese_model(input_shape):

    initializer = RandomNormal(mean=0.0, stddev=0.01)

    def create_feature_extractor(input_shape):
        input_layer = Input(shape=input_shape)
        x = Dense(128, activation='relu', kernel_initializer=initializer)(input_layer)
        x = Dense(64, activation='relu', kernel_initializer=initializer)(x)
        x = Dense(32, activation='relu', kernel_initializer=initializer)(x)
        # x = Dense(16, activation='relu')(x)
        # output_layer = Dense(8, activation='relu')(x)
        return Model(inputs=input_layer, outputs=x)

    def create_decision_module(input_layer):
        x = Dense(64, activation='relu', kernel_initializer=initializer)(input_layer)
        x = Dense(32, activation='relu', kernel_initializer=initializer)(x)
        # x = Dense(16, activation='relu')(x)
        output_layer = Dense(1, activation='sigmoid', kernel_initializer=initializer)(x)
        return output_layer

    input_a = Input(shape=input_shape)
    input_b = Input(shape=input_shape)

    feature_extractor = create_feature_extractor(input_shape)

    # Connect both inputs to the shared feature extractor
    feature_vector_a = feature_extractor(input_a)
    feature_vector_b = feature_extractor(input_b)

    l1_distance = Lambda(lambda tensors: K.abs(tensors[0] - tensors[1]))([feature_vector_a, feature_vector_b])

    decision_module = create_decision_module(l1_distance)
    decision_module = Flatten()(decision_module)
    decision_module = Dense(1, activation='sigmoid')(decision_module)
    sm = Model(inputs=[input_a, input_b], outputs=decision_module)

    # dense = Dense(64, activation='relu')(l1_norm)
    # flattened = Flatten()(dense)
    # output = Dense(1, activation='sigmoid', name='classification_layer')(merged)

    # sig = Dense(1, activation='sigmoid')(distance)

    # model = Model(inputs=[input_a, input_b], outputs=output)

    return sm

class KeystrokeRecognitionModel(ModelInterface):

    def __init__(self, config_path: str, threshold=0.5):
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)['model']
        self.scaler = load(config["scaler_path"])
        shape = config['shape']
        threshold = config['threshold']
        self.model = create_siamese_model(shape)
        tf.keras.models.load_model(config["model_path"], safe_mode=False, custom_objects={'K': K})

        # print(self.model.input_shape, config["model_path"])
        # self.model.load_weights(f'{config["model_path"]}').expect_partial()
        super().__init__(shape=shape, threshold=threshold)

    def predict(self, input_data, probe_data):
        # apply scaling
        input_data = np.array([input_data, probe_data])

        n_samples, nx, ny = input_data.shape
        my_data = input_data.reshape((1, n_samples * nx * ny))

        my_data = self.scaler.transform(my_data)
        # probe_data = self.scaler.transform(probe_data)

        my_data = my_data.reshape(n_samples, nx, ny)
        # probe_data = probe_data.reshape(self.shape)
        input_data = my_data[0, :, :]
        probe_data = my_data[1, :, :]
        input_data = input_data.reshape((1, *input_data.shape))
        probe_data = probe_data.reshape((1, *probe_data.shape))
        try:
            pred = self.model.predict([input_data, probe_data])
        except Exception as e:
            print(e)
            return

        return pred > self.threshold, pred
        # return self.model.predict([[input_data], [probe_data]]) > self.threshold

    def normalize_dataset(self, X_input, X_probe):
        x_trainnn = np.array(X_input)
        x_testtt = np.array(X_probe)

        nsamples_test, nx, ny, nz = x_testtt.shape
        nsamples_train, nx, ny, nz = x_trainnn.shape

        x_trainnn = x_trainnn.reshape((nsamples_train, nx * ny * nz))
        x_testtt = x_testtt.reshape((nsamples_test, nx * ny * nz))

        # apply normalizations
        x_trainnn = self.scaler.transform(x_trainnn)
        x_trainnn = x_trainnn.reshape((nsamples_train, nx, ny, nz))

        x_testtt = self.scaler.transform(x_testtt)
        x_testtt = x_testtt.reshape((nsamples_test, nx, ny, nz))

        # separate siamese keystrokes
        _a, _b = x_trainnn[:, 0, :, :], x_trainnn[:, 1, :, :]

        _a_probe, _b_probe = x_testtt[:, 0, :, :], x_testtt[:, 1, :, :]

        return _a, _b, _a_probe, _b_probe

    def summary(self):
        return self.model.summary()


def load_model(config: dict):
    # TODO load real model
    if config is None:
        config = dict()
        return RandomModel(shape=(0, 0, 0, 0), **config)
