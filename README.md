# Natural Selection Monte Carlo Simulation

A Monte Carlo simulation of the evolutionary mechanism of mutation and natural selection in C++ and Python.

# A Break Down of the Algorithm for each Iteration:

1. This simulation generates a population of text objects each having the same length as the desired goal but initially is filled with random characters.
2. With each generation the population is sampled for fitness, as each correct character in the correct position (a character that exists in the goal text existing in the member's text in the exact same position) counts as one point of fitness.
3. If any member's text matches the goal text break the loop and output how many generations the simulation has iterated through.
4. Otherwise, After sampling the fitness of all population members the population is then sorted based on its members' fitness, the most fit first.
5. Then the fitness sorted population will lose the less fit half of its population.
6. Then the fit half of the population will be copied into the population to simulate reproduction.
7. After reproduction, the new generation will then be mutated, as the simulation will go through all members, character by character, and change that single character to a random character or keep it the same based on the specified mutation rate.
8. Repeat with the new generation as the population.

# Running the Simulation

Running the main.py Python script from the command line with no options will result in a single step simulation with a specified iteration count that outputs a bar graph with a specific number of bins that shows the distribution of how many generations it takes to reach a specific goal with a specific mutation rate and a specific fixed population size.

However running the simulation with the -v flag will allow the user to perform a multi-step simulation, each step with a specific iteration count, where each step changes the value of one of the following simulation variables:
1) Goal Size.
2) Population Size.
3) Mutation Rate.

After choosing the desired variable to test, the user is then asked to specify the initial value of that variable, the target value for that variable, and the size of each step that the simulation takes; and then the user will be asked specify the fixed value of the rest of the simulation variables.

The result of a multi-step simulation is a graph where each point is the average generation count needed for each iteration across all iterations of that step.

Running the simulation will cause the creation of 2 files where the simulation is run; one is a PNG image of the resulting graph, and the other is a CSV file that includes all the information of the simulation, including all variables, and the number of generations needed to reach the goal at each iteration.

Additionally, the user may run the simulation with the -g flag and then provide a path to the CSV file output by a previous simulation in order to re-graph it.

# Installation

For a successful build of this repository the following dependencies must be installed:
1) python version 3.12 or higher.
2) gcc version 13.3.0 or higher.
3) pybind11 version 3.0.4 or higher.

After installing the necessary dependencies, one may clone this repository and go the 'evolution simulation' folder and execute build.sh, then copy the resulting '.so' library file into the same folder where the simulation script 'main.py' is present.

Note: the above building method only works in Linux, this repository has not been tested for Windows support, though the code itself is not operating system dependent.
