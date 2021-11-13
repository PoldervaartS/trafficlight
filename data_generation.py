import msvcrt
import time
import threading
import sys
import getopt
from typing_extensions import runtime
from classificationmock import MockClassification
from trafficlightClass import TrafficLight
from trafficlightClass import lightTypes


light = TrafficLight(lightTypes.none)
typeIn = lightTypes.none
quitting = False


def main(argv):
    runType = 0
    outputfile = ""
    accuracy = -1
    try:
        opts, args = getopt.getopt(argv,"t:o:a:",["type=", "ofile=", "accuracy"])
    except getopt.GetoptError:
        print("main.py -t <runType 0 or 1> -o <outputFile> -a <accuracy>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -t <runType 0 or 1> -o <outputFile> -a <accuracy>')
            sys.exit()
        elif opt in ("-t", "--type"):
            runType = int(arg)
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-a", "--accuracy"):
            accuracy = float(arg)

    if runType == 1:
        keyInputModel()
    elif runType == 0:
        if accuracy == -1 or outputfile == "":
            print("Model Data Generation requires specificed mock input accuracy, output file destination")
            sys.exit(2)
        modelVerification(accuracy, outputfile)
    else:
        print("Invalid Run Type: 0 or 1")


def keyInputModel():
    threading.Thread(target=slaveThreadFunction).start()
    # start a seperate thread that every second wakes up and pulls the value from the current type forever
    # keypress option that turns off the other thread and changes it to just update on keypress
    # if main thread simply be listening for kb input to change the light type
    while True:
        inputVal = msvcrt.getch()
        print(inputVal)
        if(inputVal == b'\x1b'):
            print("Quitting")
            global quitting
            quitting = True
            quit()

        global typeIn
        if(inputVal == b'r'):
            typeIn = lightTypes.red
        elif(inputVal == b'g'):
            typeIn = lightTypes.green
        elif(inputVal == b'n'):
            typeIn = lightTypes.none
        elif(inputVal == b'y'):
            typeIn = lightTypes.yellow
        elif(inputVal == b'G'):
            typeIn = lightTypes.yieldGreen
        elif(inputVal == b'b'):
            typeIn = lightTypes.blank


def modelVerification(accuracy:int, outFile:str):
    # will need to open the file
    # first line will be model accuracy
    output = MockClassification(accuracy)
    f = open(outFile, 'w')
    f.write('TrueState,MockClassification,StateStatus\n')
    while True:
        # every line after that will be the model output and the FSM output
        mockClassification = output.get_output()
        trueState = output.get_state()
        light.classIn(mockClassification)
        # print to line the
        f.write(f'{trueState},{mockClassification},{light.currentType}\n')


def slaveThreadFunction():
    while True:
        global typeIn
        global light
        light.classIn(typeIn)
        print(f'Light Type: {light.currentType}\tbreaks: {light.breakCount}')
        time.sleep(1)
        global quitting
        if quitting:
            break



if __name__ == "__main__":
    main(sys.argv[1:])