#include <iostream>
#include <fstream>
#include <random>
#include <string>
#include <thread>
#include <atomic>
#include <chrono>
#include <algorithm>
#include <execution>
#include <functional>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
using namespace std;

const string printable_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c";
thread_local random_device rand_device;
thread_local mt19937 generator(rand_device());
thread_local uniform_int_distribution<int> character_distribution(0, printable_characters.size() - 1);

vector<int> iteration_results;
mutex iteration_results_mutex;
unique_lock<mutex> iteration_results_lock(iteration_results_mutex, std::defer_lock);

atomic<int> target_number_of_iterations;
atomic<int> current_number_of_iteration = 0;
atomic<bool> is_done_iterating = false;

atomic<bool> has_started_saving_values = false;
atomic<long> write_start_position;

ofstream output_file;

char random_character(){
    return printable_characters[character_distribution(generator)];
}

string random_string(int length) {
    string result;
    result.resize(length);

    generate_n(result.begin(), length, random_character);
    
    return result;
}

void mutate_one_point(char* point, discrete_distribution<>* mutation_distribution)
{
    (*point) = (*mutation_distribution)(generator) ? random_character() : (*point);
}

void mutate_member(string* member, discrete_distribution<>* mutation_distribution){
    for(size_t i = 0; i < member->size(); i++)
	mutate_one_point(member->data() + i, mutation_distribution);
}

void mutate_population(string* population, int population_size, discrete_distribution<>* mutation_distribution){
    for(int i = 0; i < population_size; i++)
        mutate_member(population + i, mutation_distribution);
}

int evaluate_fitness(string member, string goal){
    int fitness = 0;
    for(size_t i = 0; i < member.size(); i++)
        if(member.at(i) == goal.at(i))
	    fitness++;
    return fitness;
}

void sort_by_fitness(string* population, int population_size, string goal){
    sort(population, population + population_size, [&](string first_member, string second_member){
        return evaluate_fitness(first_member, goal) > evaluate_fitness(second_member, goal);
    });
}

string* generate_random_population(int population_size, int member_size){
    string* population = new string[population_size];

    for(int i = 0; i < population_size; i++)
        population[i] = random_string(member_size);

    return population;
}

void advance_to_next_generation(string* population, string* temp_population, int population_size, discrete_distribution<>* mutation_distribution){
    if(population_size % 2 == 0){
        copy(population, population + (int)(population_size / 2), temp_population);
        copy(population, population + (int)(population_size / 2), temp_population + (int)(population_size / 2));
        copy(temp_population, temp_population + population_size, population);
    }
    else{
        copy(population, population + (int)(population_size / 2) + 1, temp_population);
        copy(population, population + (int)(population_size / 2), temp_population + (int)(population_size / 2) + 1);
        copy(temp_population, temp_population + population_size, population);
    }
    mutate_population(population, population_size, mutation_distribution);
}

void iterate(string goal, int population_size, double mutation_rate){
    discrete_distribution<> mutation_distribution({1.0 - mutation_rate, mutation_rate});

    int generation_index = 0;
    string* population = generate_random_population(population_size, goal.size());
    string* temp_population = new string[population_size];
    string best_member = "";
    while(!is_done_iterating.load()){
        do{
	    sort_by_fitness(population, population_size, goal);
	    best_member = population[0];
	    if(best_member == goal)
                break;
	    advance_to_next_generation(population, temp_population, population_size, (&mutation_distribution));
	    generation_index++;
	}while(best_member != goal && !is_done_iterating.load());
	if(!is_done_iterating.load()){
	    if(!iteration_results_lock.owns_lock())
	        iteration_results_lock.lock();
	    iteration_results.push_back(generation_index);
	    if(iteration_results_lock.owns_lock())
	        iteration_results_lock.unlock();
	    generation_index = 0;
	    best_member = "";
	    delete[] population;
	    population = generate_random_population(population_size, goal.size());
	    if(!is_done_iterating.load()) current_number_of_iteration.store(current_number_of_iteration.load() + 1);
	    if(!is_done_iterating.load()) printf("Iterations Done: %i / %i\n", current_number_of_iteration.load(), target_number_of_iterations.load());
            if(current_number_of_iteration.load() >= target_number_of_iterations.load())
                is_done_iterating.store(true);
	}
    }
    delete[] population;
    delete[] temp_population;
}

void save_to_file(string output_file_path){
    if(!iteration_results_lock.owns_lock())
        iteration_results_lock.lock();
    vector<int> iteration_results_copy(iteration_results);
    if(iteration_results_lock.owns_lock())
        iteration_results_lock.unlock();

    filesystem::path file_path(output_file_path);
    bool is_output_file_empty = true;
    if(filesystem::exists(file_path))
        is_output_file_empty = filesystem::is_empty(file_path);

    if(!output_file.is_open()){
        if(filesystem::exists(file_path))
            output_file.open(output_file_path, ios::out | ios::in | ios::ate);
        else
            output_file.open(output_file_path, ios::out | ios::ate);
    }

    if(!has_started_saving_values.load())
        write_start_position.store(output_file.tellp());
    else
        output_file.seekp(write_start_position.load());

    if (!output_file.is_open()){
        printf("Failed to open the save file \"%s\"!\n", output_file_path.c_str());
    }
    else{
        if(!is_output_file_empty)
	    output_file << "\n";

	for(size_t i = 0; i < iteration_results_copy.size(); i++){
	    if(i == (iteration_results_copy.size() - 1))
		output_file << to_string(iteration_results_copy.at(i));
	    else
		output_file << to_string(iteration_results_copy.at(i)) + ",";
	}
	has_started_saving_values.store(true);
    }
}

void auto_save(string output_file_path){
    while(!is_done_iterating.load()){
	save_to_file(output_file_path);
        this_thread::sleep_for(chrono::milliseconds(100));
    }
}

pybind11::array_t<int> run(string goal, int population_size, double mutation_rate, int number_of_iterations, string output_file_path){
    if(iteration_results_lock.owns_lock())
        iteration_results_lock.unlock();
    
    iteration_results.clear();
    iteration_results.shrink_to_fit();

    current_number_of_iteration.store(0);
    target_number_of_iterations.store(number_of_iterations);

    is_done_iterating.store(false);
    
    has_started_saving_values.store(false);

    thread auto_save_thread(auto_save, output_file_path);

    printf("Total Threads Used: %i\n\n", thread::hardware_concurrency() + 1);

    thread iteration_threads[thread::hardware_concurrency()];
    for(size_t i = 0; i < thread::hardware_concurrency(); i++)
        iteration_threads[i] = thread(iterate, goal, population_size, mutation_rate);
    for(size_t i = 0; i < thread::hardware_concurrency(); i++)
        iteration_threads[i].join();
    auto_save_thread.join();

    save_to_file(output_file_path);

    output_file.close();

    pybind11::array_t<int> result = pybind11::array_t<int>(iteration_results.size());

    pybind11::buffer_info buf = result.request();
    int *ptr = static_cast<int *>(buf.ptr);

    for (size_t i = 0; i < iteration_results.size(); i++) {
        ptr[i] = iteration_results.at(i);
    }

    return result;
}

PYBIND11_MODULE(evolution_simulation, m){
    m.doc() = "A Monte Carlo Simulation of Evolution.";
    m.def("run", &run, "The function that runs the simulation.",
          pybind11::arg("goal"), pybind11::arg("population_size"), pybind11::arg("mutation_rate"),
	  pybind11::arg("number_of_iterations"), pybind11::arg("output_file_path"));
}
