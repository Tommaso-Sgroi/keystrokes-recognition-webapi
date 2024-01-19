from random import random
from joblib import load
from os import sep

from keras import Input, Model
from keras.src.layers import Dense, Masking, Lambda, Flatten
from keras import backend as K


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
    def create_feature_extractor(input_shape):
        input_layer = Input(shape=input_shape)
        x = Dense(128, activation='relu')(input_layer)
        x = Dense(64, activation='relu')(x)
        x = Dense(32, activation='relu')(x)
        # x = Dense(16, activation='relu')(x)
        # output_layer = Dense(8, activation='relu')(x)
        return Model(inputs=input_layer, outputs=x)

    def create_decision_module(input_layer):
        x = Dense(64, activation='relu')(input_layer)
        x = Dense(32, activation='relu')(x)
        # x = Dense(16, activation='relu')(x)
        output_layer = Dense(1, activation='sigmoid')(x)
        return output_layer

    input_a = Input(shape=input_shape)
    input_b = Input(shape=input_shape)

    # mask = Masking(mask_value=0, input_shape=input_shape)
    masked_a = Masking(mask_value=0, input_shape=input_shape)(input_a)
    masked_b = Masking(mask_value=0, input_shape=input_shape)(input_b)

    # Create a shared feature extractor
    feature_extractor = create_feature_extractor(input_shape)

    # Connect both inputs to the shared feature extractor
    feature_vector_a = feature_extractor(masked_a)
    feature_vector_b = feature_extractor(masked_b)

    # concat = Concatenate()([feature_vector_A, feature_vector_B])
    # dense = Dense(64, activation='relu')(concat)

    # distance = Lambda(euclidean_distance, output_shape=(8))([feature_vector_A, feature_vector_B])
    # concat = Concatenate()([feature_vector_A, feature_vector_B])
    l1_distance = Lambda(lambda tensors: K.abs(tensors[0] - tensors[1]))([feature_vector_a, feature_vector_b])

    decision_module = create_decision_module(l1_distance)
    decision_module = Flatten()(decision_module)
    decision_module = Dense(1, activation='sigmoid')(decision_module)
    sm = Model(inputs=[input_a, input_b], outputs=decision_module)

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
        self.model.load_weights(f'{config["model_path"]}')
        super().__init__(shape=shape, threshold=threshold)

    def predict(self, input_data, probe_data):
        return self.model.predict([input_data, probe_data]) > self.threshold


def load_model(config: dict):
    # TODO load real model
    if config is None:
        config = dict()
        return RandomModel(shape=(0, 0, 0, 0), **config)
