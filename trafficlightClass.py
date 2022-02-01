from enum import Enum


lightTypes = Enum('lightTypes', 'red green turnProtected turnYield yellow none blank cautionRed')
# this will extend the traffic detected class thing
class TrafficLight: 

    lightFlow = {
        lightTypes.red: [lightTypes.green, lightTypes.turnProtected, lightTypes.turnYield, lightTypes.red],
        lightTypes.cautionRed: [lightTypes.cautionRed], 
        lightTypes.green: [lightTypes.green, lightTypes.yellow],
        lightTypes.none: [lightTypes.none], 
        lightTypes.yellow: [lightTypes.yellow, lightTypes.red],
        lightTypes.turnYield: [lightTypes.turnYield, lightTypes.yellow],
        lightTypes.turnProtected: [lightTypes.turnProtected, lightTypes.yellow]
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
        if classification == lightTypes.blank:
            if self.currentType == lightTypes.red:
                self.currentType = lightTypes.cautionRed
                self.breakCount = 0
            elif self.currentType == lightTypes.turnYield or self.currentType == lightTypes.cautionRed:
                self.breakCount = 0
            else:
                self.breakCount += 1
        # normal flow
        elif classification in self.lightFlow[self.currentType]:
            self.breakCount = 0
            self.currentType = classification
        # breaking
        elif self.breakCount >= 1 and classification != lightTypes.blank:
            self.breakCount = 0
            self.currentType = classification
        # break increment
        else:
            self.breakCount+=1

        return self.currentType
