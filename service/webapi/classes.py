class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Probe(object):
    def __init__(self, keystrokesID, FA, FR, GA, GR, sentence):
        self.sentence = sentence
        self.fa = FA
        self.fr = FR
        self.ga = GA
        self.gr = GR
        self.keystrokesID = keystrokesID
        # self.userid = userid
        # self.name = name


class PredictionResponse(object):
    def __init__(self, prediction: bool, likelihood: float):
        self.prediction = prediction
        self.likelihood = likelihood
