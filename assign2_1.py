import random
import argparse
import string
import math
import time

class Location:
	def __init__(self, label, x, y):
		self.label = label
		self.x = int(x)
		self.y = int(y)
	def get_coords(self):
		return (self.x, self.y)

	def get_label(self):
		return self.label

	def print_loc(self):
		print("Label: " + self.label + ", x: " + str(self.x) + ", y: " + str(self.y) )

	def has_label(self, label):
		return self.label == label

# Main genetic algorithm
def genetic(locations, term_criteria, mutation_rate, init_pop):
	best_path = None
	# STEP 1: Initialize population
	population = get_initial_population(locations, init_pop)
	start_time = time.time()
	# Will loop until termination criteria is met
	while(True):
		fitness_vals = []
		# STEP 2: Calculate fitness value for each state
		for p in population:
			fitness_vals.append(calc_fitness(p, locations))
		pop = [ (y,x) for x, y in zip(population, fitness_vals)]
		# STEP 3: Select parents for crossover
		parent1, parent2 = select_parents(pop)
		# STEP 4: Generate child from crosssover of parents
		# STEP 5: Mutation of child will happen in crossover function at random
		child = crossover(pop[0], pop[1], mutation_rate)
		pop.sort()
		# Check if algorithm should be terminated
		# Termination criteria is runtime of algorithm surpasses given time
		# If terminated will return the most fit (i.e. shortest path) state
		if(time.time() - start_time >= term_criteria):
			best_path = pop[0]
			break
		# Prune population for next iteration
		fitness_vals = []
		population = prune_pop(pop)
	return best_path

# Calculate the fitness of a state
# Calculated by total distance of state path
def calc_fitness(state, locations):
	fitness = 0
	for i in range(len(state)-1):
		loc1 = get_location(state[i], locations)
		loc2 = get_location(state[i+1], locations)

		fitness += get_distance(loc1, loc2)
	return fitness

# Get random states for initial population
# Ensures that locations are not visited twice
def get_initial_population(locs, init_pop):
	pop = []
	while(len(pop) < init_pop):
		state = ''
		unadded_chars = string.ascii_uppercase[:len(locs)]
		while(len(state) < len(locs)):
			label = unadded_chars[random.randint(0, len(unadded_chars)-1)]
			if(label not in state):
				state += label
				unadded_chars.replace(label, "")
		if(state not in pop):
			pop.append(state)
	return pop

# Get location object with given label value
def get_location(label, locations):
	for l in locations:
		if l.has_label(label):
			return l

# Mutate child by swapping two locations at random
def mutate(state):
	i, j = 0, 0
	while(i == j):
		i = random.randint(0, len(state)-1)
		j = random.randint(0, len(state)-1)
	mutant = state
	mutant[i] = state[j]
	mutant[j] = state[i]
	return mutant

# Crossover two parent states to create child state.
# Child will randomly mutate
# TODO: Figure out method of crossover, must not have repeating characters
def crossover(state1, state2, mutation_rate):
	new_state = ''

	if(random.randint(0, 100) < mutation_rate):
		new_state = mutate(new_state)
	return new_state

# Select two states to act as parents
# TODO: Figure out method of parent selection
def select_parents(pop):
	pass

# Prune population
# TODO: Prune population for next iteration
def prune_pop(pop):
	pass

# Get distance between two locations
def get_distance(loc1, loc2):
	x1, y1 = loc1.get_coords()
	x2, y2 = loc2.get_coords()
	return (math.sqrt((x1-x2)**2 + (y1-y2)**2))

# Read in file
def read_data(fname):
	locations = []
	with open(fname, 'r') as f:
		for l in f.readlines():
			l = l.split(" ")
			locations.append(Location(l[0], l[1], l[2]))
	return locations

def main(args):
	fname = args.filename
	term_criteria = args.terminate
	if (args.mutation_rate):
		mutation_rate = args.mutation_rate
	else:
		mutation_rate = 10
	if (args.init_pop):
		init_pop = args.init_pop
	else:
		init_pop = 10
	locations = read_data(fname)
	best_path = genetic(locations, term_criteria, mutation_rate, init_pop)
	print("Best path is: " + best_path[1] + " with distance " + str(best_path[0]))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--terminate', required=True, type=float)
	parser.add_argument('-m', '--mutation_rate', type=int)
	parser.add_argument('-i', '--init_pop', type=int)
	parser.add_argument('filename')
	main(parser.parse_args())