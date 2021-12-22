from enum import Enum


lightTypes = Enum('lightTypes', 'red green turnGreen yieldGreen yellow none blank')
# this will extend the traffic detected class thing
class TrafficLight: 

    lightFlow = {
        lightTypes.red: [lightTypes.green, lightTypes.turnGreen, lightTypes.yieldGreen, lightTypes.red], 
        lightTypes.green: [lightTypes.green, lightTypes.yellow],
        lightTypes.none: [lightTypes.none], 
        lightTypes.yellow: [lightTypes.yellow, lightTypes.red],
        lightTypes.yieldGreen: [lightTypes.yieldGreen, lightTypes.yellow],
        lightTypes.turnGreen: [lightTypes.turnGreen, lightTypes.yellow]
        }
    def __init__(self, typeIn) -> None:
        # will contain all of the regular tracking stuff that a tracking network uses
        # super(self)
        self.breakCount = 0
        self.currentType = typeIn

    def nextLights(lightType):
        return TrafficLight.lightFlow[lightType]

    def classIn(self, classification):
        # special case of blank for yellow
        if self.currentType == lightTypes.yellow and classification == lightTypes.blank:
            self.breakCount = 0
        # normal flow
        elif classification in self.lightFlow[self.currentType]:
            self.breakCount = 0
            self.currentType = classification
        # breaking
        elif self.breakCount == 1:
            self.breakCount = 0
            if classification == lightTypes.blank:
                self.currentType = lightTypes.yellow
            else:
                self.currentType = classification
        # break increment
        else:
            self.breakCount+=1

        return self.currentType
