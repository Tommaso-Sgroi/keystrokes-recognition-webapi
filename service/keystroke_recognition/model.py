from random import random


class ModelInterface(object):
    def __init__(self, shape, threshold=0.5):
        self.shape = shape
        self.threshold = threshold


class RandomModel(ModelInterface):

    def predict(self, input_data, probe_data):
        # reshape the input data
        pred = random()
        return pred, (pred > self.threshold) and len(input_data) > 0 and len(probe_data) > 0


def load_model(model_path='./model'):
    # TODO load real model
    model = RandomModel(shape=(0, 0, 0, 0))
    # return a placeholder random model
    return model
