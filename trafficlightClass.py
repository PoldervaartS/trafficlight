from enum import Enum

lightTypes = Enum(
    'lightTypes',
    'red green turnProtected turnYield yellow none blank')
lightShape = Enum('lightShape', 'round arrow none')


# this will extend the traffic detected class thing
class TrafficLight:

    lightFlow = {
        lightTypes.red: [
            lightTypes.green, lightTypes.turnProtected, lightTypes.turnYield,
            lightTypes.red
        ],
        lightTypes.green: [lightTypes.green, lightTypes.yellow],
        lightTypes.blank: [lightTypes.blank],
        lightTypes.yellow: [lightTypes.red],
        lightTypes.turnYield: [lightTypes.red],
        lightTypes.turnProtected:
        [lightTypes.turnProtected, lightTypes.yellow]
    }

    def __init__(self, typeIn) -> None:
        # will contain all of the regular tracking stuff that a tracking network uses
        # super(self)
        self.breakCount = 0
        self.currentType = typeIn[0]
        # keeps track of the last 20 inputs for doing subsections like flashing yellow turn or protected turn.
        # 20 was chosen as aiming for 10fps gives us 2 seconds of input to cycle over and realize.
        self.latestValues = [(lightTypes.none, lightShape.none)] * 20
        self.latestValues[0] = typeIn
        self.classificationCount = 1

    def nextLights(lightType):
        return TrafficLight.lightFlow[lightType]

    def classIn(self, classification):
        # classification of type (color, shape)
        self.latestValues[self.classificationCount %
                          len(self.latestValues)] = classification
        self.classificationCount += 1
        # Yellow is special because dealing with the time interval more
        if (classification[0] == lightTypes.blank
                or classification[0] == lightTypes.yellow) and (
                    self.currentType == lightTypes.yellow
                    or self.currentType == lightTypes.turnYield):
            # Flashing Yellow
            if self.currentType == lightTypes.yellow:
                self.breakCount = 0
                sumBlanks = sum([
                    1 if lighttype[0] == lightTypes.blank else 0
                    for lighttype in self.latestValues
                ])
                # HYPERPARAMETER timed 1 second on 1 second off.
                if sumBlanks / len(self.latestValues) >= .25:
                    self.currentType = lightTypes.turnYield

            else:
                self.breakCount += 1

        # classification of protected turn versus regular green
        elif classification[0] == lightTypes.green and (
                self.currentType == lightTypes.green
                or self.currentType == lightTypes.turnProtected):
            self.breakCount = 0
            sumArrows = sum([
                1 if lighttype[1] == lightShape.arrow else 0
                for lighttype in self.latestValues
            ])
            # HYPERPARAMETER
            if sumArrows / len(self.latestValues) > .3:
                self.currentType = lightTypes.turnProtected
            else:
                self.currentType = lightTypes.green

        # normal flow
        elif classification[0] in self.lightFlow[self.currentType]:
            self.breakCount = 0
            self.currentType = classification
        # breaking
        elif self.breakCount >= 1 and classification[0] != lightTypes.blank:
            self.breakCount = 0
            self.currentType = classification[0]
        # break increment
        else:
            self.breakCount += 1

        return self.currentType
