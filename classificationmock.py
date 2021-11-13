import random
from trafficlightClass import *


class MockClassification:
    def __init__(self, accuracy) -> None:
        self.accuracy = accuracy
        self.count = 0
        self.currentState = lightTypes.red

    def get_state(self):
        return self.currentState

    def get_output(self):
        self.count += 1
        # change light types every 20 times
        if(self.count % 5 == 0):
            self.currentState = random.choice(TrafficLight.nextLights(self.currentState))
        if random.random() < self.accuracy:
            return self.currentState
        else:
            return random.choice(list(lightTypes))