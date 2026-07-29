import random
import string
import sys
import matplotlib.pyplot as plt
import csv
import time
import evolution_simulation
from pathlib import Path
from enum import IntEnum

class SimulationMode(IntEnum):
    GENERATION_COUNTING = 0,
    ONE_VARIABLE_GRAPHING = 1,
    RESULTS_PLOTTING = 2

class VariableToGraph(IntEnum):
    GOAL_LENGTH = 0,
    POPULATION_SIZE = 1,
    MUTATION_RATE = 2

class HeaderVariables(IntEnum):
    SIMULATION_MODE = 0,
    VARIABLE_TO_GRAPH = 1,
    NUMBER_OF_ITERATIONS = 2,
    MUTATION_RATE = 3,
    POPULATION_SIZE = 4,
    GOAL = 5,
    STARTING_VARIABLE_VALUE = 6,
    STEP_SIZE = 7

simulation_mode = SimulationMode.GENERATION_COUNTING

def get_safe_string(prompt, error_message):
    while True:
        try:
            print(prompt,end="")
            string = str(sys.stdin.read())
            print()
            if not string:
                print(error_message)
                continue
            return string
        except ValueError:
            print(error_message)

def get_safe_int(prompt, error_message):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(error_message)

def get_safe_float(prompt, error_message, number_range=(0.0, 1.0)):
    while True:
        try:
            number = float(input(prompt))
            if number < number_range[0] or number > number_range[1]:
                print(error_message)
                continue
            return number
        except ValueError:
            print(error_message)

def random_string(length):
    characters = string.printable
    return ''.join(random.choices(characters, k=length))

output_file = Path("iteration_results.csv")

counter = 2
while output_file.exists():
    output_file = Path(f"iteration_results_{counter}.csv")
    counter += 1

def plot_from_results(iteration_results, number_of_bins):
    plt.hist(iteration_results, bins=number_of_bins)

    plt.xlabel('Generations')
    plt.ylabel('Iterations')
    plt.title('Evolutionary Algorithm Iteration Density')

    plot_output_file = Path("Evolution.png")

    counter = 2
    while plot_output_file.exists():
        plot_output_file = Path(f"Evolution_{counter}.png")
        counter += 1

    plt.savefig(str(plot_output_file))

    plt.show()

def plot_goal_length_graph(goal_length_at_each_step, average_generation_counts):
    plt.plot(goal_length_at_each_step, average_generation_counts)

    plt.xlabel('Goal Length')
    plt.ylabel('Average Generation Count')
    plt.title('Evolutionary Algorithm Goal Length Effect')

    plot_output_file = Path("Evolution_Goal_Length.png")

    counter = 2
    while plot_output_file.exists():
        plot_output_file = Path(f"Evolution_Goal_Length_{counter}.png")
        counter += 1

    plt.savefig(str(plot_output_file))

    plt.show()

def plot_population_size_graph(population_size_at_each_step, average_generation_counts):
    plt.plot(population_size_at_each_step, average_generation_counts)

    plt.xlabel('Population Size')
    plt.ylabel('Average Generation Count')
    plt.title('Evolutionary Algorithm Population Size Effect')

    plot_output_file = Path("Evolution_Population_Size.png")

    counter = 2
    while plot_output_file.exists():
        plot_output_file = Path(f"Evolution_Population_size_{counter}.png")
        counter += 1

    plt.savefig(str(plot_output_file))

    plt.show()

def plot_mutation_rate_graph(mutation_rate_at_each_step, average_generation_counts):
    plt.plot(mutation_rate_at_each_step, average_generation_counts)

    plt.xlabel('Mutation Rate')
    plt.ylabel('Average Generation Count')
    plt.title('Evolutionary Algorithm Mutation Rate Effect')

    plot_output_file = Path("Evolution_Mutation_Rate.png")

    counter = 2
    while plot_output_file.exists():
        plot_output_file = Path(f"Evolution_Mutation_Rate_{counter}.png")
        counter += 1

    plt.savefig(str(plot_output_file))

    plt.show()

def print_simulation_parameters(simulation_parameters, simulation_parameter_names):
    for i in range(0, len(simulation_parameters)):
        if simulation_parameter_names[i].lower().strip() == "goal":
            print(f"{simulation_parameter_names[i]}: \"{simulation_parameters[i]}\"")
        elif simulation_parameter_names[i].lower().strip() == "mutation rate"\
        or   simulation_parameter_names[i].lower().strip() == "starting mutation rate"\
        or   simulation_parameter_names[i].lower().strip() == "target mutation rate"\
        or   (simulation_parameter_names[i].lower().strip() == "step size" and not float(simulation_parameters[i]).is_integer()):
            print(f"{simulation_parameter_names[i]}: {float(simulation_parameters[i]) * 100.0:.2f}% ({simulation_parameters[i]})")
        else:
            print(f"{simulation_parameter_names[i]}: {simulation_parameters[i]}")

def write_simulation_headers(simulation_mode, variable_to_graph, number_of_iterations, mutation_rate, population_size, goal, starting_variable_value, step_size):
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([int(simulation_mode), int(variable_to_graph), number_of_iterations, mutation_rate, population_size, goal, starting_variable_value, step_size])
    except FileNotFoundError:
        print("Error: The specified file does not exist.")
        sys.exit(1)
    except PermissionError:
        print("Error: You do not have permission to access this file.")
        sys.exit(2)
    except csv.Error as e:
        print(f"An error occurred while parsing the CSV: {e}")
        sys.exit(3)


mode = SimulationMode.GENERATION_COUNTING

if len(sys.argv) == 2:
    if sys.argv[1] == "-p" or sys.argv[1] == "--plot":
        mode = SimulationMode.RESULTS_PLOTTING
    elif sys.argv[1] == "-v" or sys.argv[1] == "--variable":
        mode = SimulationMode.ONE_VARIABLE_GRAPHING

if mode == SimulationMode.GENERATION_COUNTING:
    iteration_results = []

    goal = get_safe_string("Enter Goal String (any data entered will be treated as a string; press Ctrl+D on linux/mac, Ctrl+Z on Windows, to terminate the Goal String):\n", "Invalid or empty Goal String.\nPlease try again.")
    population_size = get_safe_int("Enter Population Size: ", "Invalid Population Size.\nPlease try again.")
    mutation_rate = get_safe_float("Enter Mutation Rate (as a decimal): ", "Invalid Mutation Rate.\nPlease try again.")

    print()

    number_of_iterations = get_safe_int("Enter Number of Iterations: ", "Invalid Number of Iterations.\nPlease try again.")

    number_of_bins = get_safe_int("Enter Number of Bins in the final histograph: ", "Invalid Number of Bins.\nPlease try again.")

    print()

    write_simulation_headers(SimulationMode.GENERATION_COUNTING, VariableToGraph.GOAL_LENGTH, number_of_iterations, mutation_rate, population_size, goal, 0, 0)

    start_time = time.perf_counter()

    iteration_results = evolution_simulation.run(goal, population_size, mutation_rate, number_of_iterations, str(output_file))

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print( f"Finished in {execution_time:.2f} seconds")

    print()

    print_simulation_parameters(\
            [goal, population_size,\
            mutation_rate, number_of_iterations],\
            ["Goal", "Population Size", "Mutation Rate", "Number of Iterations"])

    plot_from_results(iteration_results, number_of_bins)

elif mode == SimulationMode.ONE_VARIABLE_GRAPHING:
    variable_choice = ""
    variable_to_graph = VariableToGraph.GOAL_LENGTH
    while True:
        try:
            variable_choice = str(input("Variables used In the simulation:\n\t1) Goal String Length.\n\t2) Population Size.\n\t3) Mutation Rate.\nChoose variable to graph: "))
            variable_choice = variable_choice.strip()
            variable_choice = variable_choice.lower()

            if variable_choice == "1" or variable_choice == "goal" or variable_choice == "goal length" or variable_choice == "goal length." or variable_choice == "goal string length" or variable_choice == "goal string length.":
                variable_to_graph = VariableToGraph.GOAL_LENGTH
                break
            elif variable_choice == "2" or variable_choice == "population" or variable_choice == "population size" or variable_choice == "population size.":
                variable_to_graph = VariableToGraph.POPULATION_SIZE
                break
            elif variable_choice == "3" or variable_choice == "mutation" or variable_choice == "mutation rate" or variable_choice == "mutation rate.":
                variable_to_graph = VariableToGraph.MUTATION_RATE
                break
            else:
                raise ValueError()
        except ValueError:
            print(f"Variable choice: {variable_choice} is invalid.\nPlease choose again.\n")

    if variable_to_graph == VariableToGraph.GOAL_LENGTH:
        starting_goal_length = get_safe_int("Enter Starting Goal Length: ", "Invalid Goal Length.\nPlease try again.")

        target_goal_length = starting_goal_length
        while target_goal_length == starting_goal_length:
            target_goal_length = get_safe_int("Enter Target Goal Length: ", "Invalid Goal Length.\nPlease try again.")
            if target_goal_length == starting_goal_length:
                print("Target Goal Length cannot be the same as Starting Goal Length.\nPlease try again.")

        goal_length_distance = (int)(abs(starting_goal_length - target_goal_length))
        step_direction = 1 if starting_goal_length < target_goal_length else -1

        step_size = 0
        while  (step_size > 0 and step_direction == -1)\
            or (step_size < 0 and step_direction == 1)\
            or abs(step_size) > goal_length_distance\
            or step_size == 0:
            step_size = get_safe_int("Enter Step Size: ", "Invalid Step Size.\nPlease try again.")

            if step_size > 0 and step_direction == -1:
                print("Error: Wrong direction!\nStep Size is positive while Starting Goal Length is bigger than Target Goal Length\nPlease try again.")
                continue
            if step_size < 0 and step_direction == 1:
                print("Error: Wrong direction!\nStep Size is negative while Starting Goal Length is smaller than Target Goal Length\nPlease try again.")
                continue
            if abs(step_size) > goal_length_distance:
                print(f"Step Size ({step_size}) is bigger than total distance between Starting Goal Length ({starting_goal_length}) and Target Goal Length ({target_goal_length}).\nPlease try again.")
                continue
            if step_size == 0:
                print("Step Size can't be zero.\nPlease try again.")
                continue


        number_of_iterations = get_safe_int("Enter Number of Iterations per Step: ", "Invalid Number of Iterations.\nPlease try again.")

        print()

        population_size = get_safe_int("Enter Population Size: ", "Invalid Population Size.\nPlease try again.")
        mutation_rate = get_safe_float("Enter Mutation Rate (as a decimal): ", "Invalid Mutation Rate.\nPlease try again.")

        print()
        
        start_time = time.perf_counter()

        number_of_steps = int(goal_length_distance / abs(step_size)) + 1

        should_do_additional_step = (goal_length_distance % abs(step_size) > 0)

        average_generation_counts = []
        goal_length_at_each_step = []

        write_simulation_headers(mode, variable_to_graph, number_of_iterations, mutation_rate, population_size, "", starting_goal_length, step_size)

        for step_index in range(0, number_of_steps):
            goal = random_string(starting_goal_length + (step_index * step_size))
            goal_length_at_each_step.append(starting_goal_length + (step_index * step_size))
            print(f"Step: {step_index + 1} / {number_of_steps + (1 if should_do_additional_step else 0)}")
            print()
            iteration_results = evolution_simulation.run(goal, population_size, mutation_rate, number_of_iterations, str(output_file))
            average_generation_counts.append(sum(iteration_results) / len(iteration_results))
            print()

        if should_do_additional_step:
            goal = random_string(target_goal_length)
            goal_length_at_each_step.append(target_goal_length)
            print(f"Step: {number_of_steps + (1 if should_do_additional_step else 0)} / {number_of_steps + (1 if should_do_additional_step else 0)}")
            print()
            iteration_results = evolution_simulation.run(goal, population_size, mutation_rate, number_of_iterations, str(output_file))
            average_generation_counts.append(sum(iteration_results) / len(iteration_results))
            print()

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        print( f"Finished in {execution_time:.2f} seconds")

        print()

        print_simulation_parameters(\
                    [starting_goal_length, target_goal_length,\
                    step_size, population_size,\
                    mutation_rate, number_of_iterations,\
                    number_of_steps],\
                    ["Starting Goal Length", "Target Goal Length",\
                    "Step Size", "Population Size",\
                    "Mutation Rate", "Number of Iterations per Step",\
                    "Number of Steps"])

        plot_goal_length_graph(goal_length_at_each_step, average_generation_counts)

    elif variable_to_graph == VariableToGraph.POPULATION_SIZE:
        starting_population_size = get_safe_int("Enter Starting Population Size: ", "Invalid Population Size.\nPlease try again.")

        target_population_size = starting_population_size
        while target_population_size == starting_population_size:
            target_population_size = get_safe_int("Enter Target Population Size: ", "Invalid Population Size.\nPlease try again.")
            if target_population_size == starting_population_size:
                print("Target Population Size cannot be the same as Starting Population Size.\nPlease try again.")

        population_size_distance = (int)(abs(starting_population_size - target_population_size))
        step_direction = 1 if starting_population_size < target_population_size else -1

        step_size = 0
        while  (step_size > 0 and step_direction == -1)\
            or (step_size < 0 and step_direction == 1)\
            or abs(step_size) > population_size_distance\
            or step_size == 0:
            step_size = get_safe_int("Enter Step Size: ", "Invalid Step Size.\nPlease try again.")

            if step_size > 0 and step_direction == -1:
                print("Error: Wrong direction!\nStep Size is positive while Starting Population Size is bigger than Target Population Size\nPlease try again.")
                continue
            if step_size < 0 and step_direction == 1:
                print("Error: Wrong direction!\nStep Size is negative while Starting Population Size is smaller than Target Population Size\nPlease try again.")
                continue
            if abs(step_size) > population_size_distance:
                print(f"Step Size ({step_size}) is bigger than total distance between Starting Population Size ({starting_population_size}) and Target Population Size ({target_population_size}).\nPlease try again.")
                continue
            if step_size == 0:
                print("Step Size can't be zero.\nPlease try again.")
                continue


        number_of_iterations = get_safe_int("Enter Number of Iterations per Step: ", "Invalid Number of Iterations.\nPlease try again.")

        print()

        goal = get_safe_string("Enter Goal String (any data entered will be treated as a string; press Ctrl+D on linux/mac, Ctrl+Z on Windows, to terminate the Goal String):\n", "Invalid or empty Goal String.\nPlease try again.")
        mutation_rate = get_safe_float("Enter Mutation Rate (as a decimal): ", "Invalid Mutation rate.\nPlease try again.")

        print()

        start_time = time.perf_counter()

        number_of_steps = int(population_size_distance / abs(step_size)) + 1

        should_do_additional_step = (population_size_distance % abs(step_size) > 0)

        average_generation_counts = []
        population_size_at_each_step = []

        write_simulation_headers(mode, variable_to_graph, number_of_iterations, mutation_rate, 0, goal, starting_population_size, step_size)

        for step_index in range(0, number_of_steps):
            population_size = starting_population_size + (step_index * step_size)
            population_size_at_each_step.append(population_size)
            print(f"Step: {step_index + 1} / {number_of_steps + (1 if should_do_additional_step else 0)}")
            print()
            iteration_results = evolution_simulation.run(goal, population_size, mutation_rate, number_of_iterations, str(output_file))
            average_generation_counts.append(sum(iteration_results) / len(iteration_results))
            print()

        if should_do_additional_step:
            population_size = target_population_size
            population_size_at_each_step.append(population_size)
            print(f"Step: {number_of_steps + (1 if should_do_additional_step else 0)} / {number_of_steps + (1 if should_do_additional_step else 0)}")
            print()
            iteration_results = evolution_simulation.run(goal, population_size, mutation_rate, number_of_iterations, str(output_file))
            average_generation_counts.append(sum(iteration_results) / len(iteration_results))
            print()

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print( f"Finished in {execution_time:.2f} seconds")

        print()

        print_simulation_parameters(\
                    [goal, starting_population_size,\
                    target_population_size, step_size,\
                    mutation_rate, number_of_iterations,\
                    number_of_steps],\
                    ["Goal", "Starting Population Size",\
                    "Target Population Size", "Step Size",\
                    "Mutation Rate","Number of Iterations per Step",\
                    "Number of Steps"])

        plot_population_size_graph(population_size_at_each_step, average_generation_counts)

    elif variable_to_graph == VariableToGraph.MUTATION_RATE:
        starting_mutation_rate = get_safe_float("Enter Starting Mutation Rate: ", "Invalid Mutation Rate.\nPlease try again.")

        target_mutation_rate = starting_mutation_rate
        while target_mutation_rate == starting_mutation_rate:
            target_mutation_rate = get_safe_float("Enter Target Mutation Rate: ", "Invalid Mutation Rate.\nPlease try again.")
            if target_mutation_rate == starting_mutation_rate:
                print("Target Mutation Rate cannot be the same as Starting Mutation Rate.\nPlease try again.")

        mutation_rate_distance = (float)(abs(starting_mutation_rate - target_mutation_rate))
        step_direction = 1 if starting_mutation_rate < target_mutation_rate else -1

        step_size = 0
        while  (step_size > 0 and step_direction == -1)\
            or (step_size < 0 and step_direction == 1)\
            or abs(step_size) > mutation_rate_distance\
            or step_size == 0:
            step_size = get_safe_float("Enter Step Size: ", "Invalid Step Size.\nPlease try again.")

            if step_size > 0 and step_direction == -1:
                print("Error: Wrong direction!\nStep Size is positive while Starting Mutation Rate is bigger than Target Mutation Rate\nPlease try again.")
                continue
            if step_size < 0 and step_direction == 1:
                print("Error: Wrong direction!\nStep Size is negative while Starting Mutation Rate is smaller than Target Mutation Rate\nPlease try again.")
                continue
            if abs(step_size) > mutation_rate_distance:
                print(f"Step Size ({step_size}) is bigger than total distance between Starting Mutation Rate ({starting_mutation_rate}) and Target Mutation Rate ({target_mutation_rate}).\nPlease try again.")
                continue
            if step_size == 0:
                print("Step Size can't be zero.\nPlease try again.")
                continue


        number_of_iterations = get_safe_int("Enter Number of Iterations per Step: ", "Invalid Number of Iterations.\nPlease try again.")

        print()

        goal = get_safe_string("Enter Goal String (any data entered will be treated as a string; press Ctrl+D on linux/mac, Ctrl+Z on Windows, to terminate the Goal String):\n", "Invalid or empty Goal String.\nPlease try again.")
        population_size = get_safe_int("Enter Population Size: ", "Invalid Population Size.\nPlease try again.")

        print()

        start_time = time.perf_counter()

        number_of_steps = int(mutation_rate_distance / abs(step_size)) + 1

        should_do_additional_step = (abs(mutation_rate_distance / abs(step_size)) - (int)(abs(mutation_rate_distance / abs(step_size))) != 0)

        average_generation_counts = []
        mutation_rate_at_each_step = []

        write_simulation_headers(mode, variable_to_graph, number_of_iterations, 0, population_size, goal, starting_mutation_rate, step_size)

        for step_index in range(0, number_of_steps):
            mutation_rate = starting_mutation_rate + (step_index * step_size)
            mutation_rate_at_each_step.append(mutation_rate)
            print(f"Step: {step_index + 1} / {number_of_steps + (1 if should_do_additional_step else 0)}")
            print()
            iteration_results = evolution_simulation.run(goal, population_size, mutation_rate, number_of_iterations, str(output_file))
            average_generation_counts.append(sum(iteration_results) / len(iteration_results))
            print()

        if should_do_additional_step:
            mutation_rate = target_mutation_rate
            mutation_rate_at_each_step.append(mutation_rate)
            print(f"Step: {number_of_steps + (1 if should_do_additional_step else 0)} / {number_of_steps + (1 if should_do_additional_step else 0)}")
            print()
            iteration_results = evolution_simulation.run(goal, population_size, mutation_rate, number_of_iterations, str(output_file))
            average_generation_counts.append(sum(iteration_results) / len(iteration_results))
            print()
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print( f"Finished in {execution_time:.2f} seconds")
        
        print()

        print_simulation_parameters(\
                    [goal, population_size,\
                    starting_mutation_rate, target_mutation_rate,\
                    step_size, number_of_iterations,\
                    number_of_steps],\
                    ["Goal", "Population Size",\
                    "Starting Mutation Rate", "Target Mutation Rate",\
                    "Step Size", "Number of Iterations per Step",\
                    "Number of Steps"])

        plot_mutation_rate_graph(mutation_rate_at_each_step, average_generation_counts)

       
elif mode == SimulationMode.RESULTS_PLOTTING:
    try:
        results_header = []
        results_data = []
        with open(input("Enter CSV file path: ").strip().strip("'\""), "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            results_data = list(reader)
            results_header = results_data[0]
        if int(results_header[int(HeaderVariables.SIMULATION_MODE)]) == SimulationMode.GENERATION_COUNTING:
            iteration_results = results_data[2]
            
            print_simulation_parameters(\
                [results_header[int(HeaderVariables.GOAL)], results_header[int(HeaderVariables.POPULATION_SIZE)],\
                results_header[int(HeaderVariables.MUTATION_RATE)], results_header[int(HeaderVariables.NUMBER_OF_ITERATIONS)]],\
                ["Goal", "Population Size", "Mutation Rate", "Number of Iterations"])
            
            temp = []
            for iteration_result in iteration_results:
                temp.append(int(iteration_result))
            iteration_results = temp
            plot_from_results(iteration_results, get_safe_int("Enter Number of Bins in the final histograph: ", "Invalid Number of Bins.\nPlease try again."))
        elif int(results_header[int(HeaderVariables.SIMULATION_MODE)]) == SimulationMode.ONE_VARIABLE_GRAPHING:
            iteration_results_list = results_data[2:]

            for i in range(0, len(iteration_results_list)):
                iteration_results = iteration_results_list[i]
                temp = []
                for iteration_result in iteration_results:
                    temp.append(int(iteration_result))
                iteration_results_list[i] = temp

            if int(results_header[int(HeaderVariables.VARIABLE_TO_GRAPH)]) == VariableToGraph.GOAL_LENGTH:
                average_generation_counts = []
                goal_length_at_each_step = []

                starting_goal_length = int(results_header[int(HeaderVariables.STARTING_VARIABLE_VALUE)])
                step_size = int(results_header[int(HeaderVariables.STEP_SIZE)])

                goal_length = 0
                for step_index in range(0, len(iteration_results_list)):
                    iteration_results = iteration_results_list[step_index]

                    goal_length = starting_goal_length + (step_index * step_size)
                    goal_length_at_each_step.append(goal_length)

                    average_generation_counts.append(sum(iteration_results) / len(iteration_results))

                print_simulation_parameters(\
                    [starting_goal_length, goal_length, step_size, results_header[int(HeaderVariables.POPULATION_SIZE)],\
                    results_header[int(HeaderVariables.MUTATION_RATE)], results_header[int(HeaderVariables.NUMBER_OF_ITERATIONS)],\
                    len(iteration_results_list)],\
                    ["Starting Goal Length", "Target Goal Length", "Step Size",\
                    "Population Size", "Mutation Rate", "Number of Iterations per Step", "Number of Steps"])

                plot_goal_length_graph(goal_length_at_each_step, average_generation_counts)

            elif int(results_header[int(HeaderVariables.VARIABLE_TO_GRAPH)]) == VariableToGraph.POPULATION_SIZE:
                average_generation_counts = []
                population_size_at_each_step = []

                starting_population_size = int(results_header[int(HeaderVariables.STARTING_VARIABLE_VALUE)])
                step_size = int(results_header[int(HeaderVariables.STEP_SIZE)])

                population_size = 0
                for step_index in range(0, len(iteration_results_list)):
                    iteration_results = iteration_results_list[step_index]

                    population_size = starting_population_size + (step_index * step_size)
                    population_size_at_each_step.append(population_size)

                    average_generation_counts.append(sum(iteration_results) / len(iteration_results))

                print_simulation_parameters(\
                    [results_header[int(HeaderVariables.GOAL)], starting_population_size, population_size, step_size,\
                    results_header[int(HeaderVariables.MUTATION_RATE)], results_header[int(HeaderVariables.NUMBER_OF_ITERATIONS)],\
                    len(iteration_results_list)],\
                    ["Goal", "Starting Population Size", "Target Population Size", "Step Size",\
                    "Mutation Rate", "Number of Iterations per Step", "Number of Steps"])

                plot_population_size_graph(population_size_at_each_step, average_generation_counts)

            elif int(results_header[int(HeaderVariables.VARIABLE_TO_GRAPH)]) == VariableToGraph.MUTATION_RATE:
                average_generation_counts = []
                mutation_rate_at_each_step = []

                starting_mutation_rate = float(results_header[int(HeaderVariables.STARTING_VARIABLE_VALUE)])
                step_size = float(results_header[int(HeaderVariables.STEP_SIZE)])

                mutation_rate = 0
                for step_index in range(0, len(iteration_results_list)):
                    iteration_results = iteration_results_list[step_index]

                    mutation_rate = starting_mutation_rate + (step_index * step_size)
                    mutation_rate_at_each_step.append(mutation_rate)

                    average_generation_counts.append(sum(iteration_results) / len(iteration_results))

                print_simulation_parameters(\
                    [results_header[int(HeaderVariables.GOAL)], results_header[int(HeaderVariables.POPULATION_SIZE)],\
                    starting_mutation_rate, mutation_rate, step_size,\
                    results_header[int(HeaderVariables.NUMBER_OF_ITERATIONS)],\
                    len(iteration_results_list)],\
                    ["Goal", "Population Size", "Starting Mutation Rate", "Target Mutation Rate", "Step Size",\
                    "Number of Iterations per Step", "Number of Steps"])

                plot_mutation_rate_graph(mutation_rate_at_each_step, average_generation_counts)

    except FileNotFoundError:
        print("Error: The specified file does not exist.")
        sys.exit(1)
    except PermissionError:
        print("Error: You do not have permission to access this file.")
        sys.exit(2)
    except csv.Error as e:
        print(f"An error occurred while parsing the CSV: {e}")
        sys.exit(3)
