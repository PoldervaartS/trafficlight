# Traffic Light Finite State Machine
This is a finite state machine created centered around the actions of Traffic Lights. In continued research of autonomous vehicles, there is an explicit need to properly categorize the traffic lights in order to allow the vehicle to make the appropriate decisions. 

To ward off the inherent noise of directly feeding network classifications to planning modules, the intermediate step of a state machine is used to guard against innacurate classifications that break the traditional traffic flow. 


## Data Generation
run `data_generation.py` with the args `-o <outputFile to write to> -a <accuracy of mock model>`

This script will write the generated data to the data file specified in the following format.

 - TrueState - Ground truth state of the traffic light
 - MockClassification - Noisy output of the mock classification based on true state and accuracy
- StateStatus - Status of the light stored in the finite state machine
`TrueState,MockClassification,StateStatus`

## Results
pictures of results goes here once I do the data analysis. Make it look *pretty*
With a planned rate of 10hz, these graphs show the performance of the finite state machine given various accuracies resulting in randomly assigning a different traffic light class. 