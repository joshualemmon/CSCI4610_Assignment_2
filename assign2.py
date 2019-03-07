import random
import argparse
import string
import math
import time

# Genetic Algorithm Solution 

# Location class used for first domain
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

# Class for second domain maybe?

# Main genetic algorithm
# Need to expand to handle second domain
def genetic(locations, term_criteria, mutation_rate, init_pop, crossover_method=1):
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
		max_path = max(fitness_vals)
		fitness_vals = [max_path-x for x in fitness_vals]
		pop = [ (y,x) for x, y in zip(population, fitness_vals)]
		# STEP 3: Select parents for crossover
		# Maybe want to pick 40% of population to be parents
		num_parents = init_pop * 0.4
		if num_parents % 2 == 1:
			num_parents -= 1
		parents = select_parents(pop, num_parents)
		# STEP 4: Generate child from crosssover of parents
		# maybe want 20% of population to be children in next itertion
		# STEP 5: Mutation of child will happen in crossover function at random	
		children = crossover(parents, mutation_rate, crossover_method)
		# Check if algorithm should be terminated
		# Termination criteria is runtime of algorithm surpasses given time
		# If terminated will return the most fit (i.e. shortest path) state
		if(time.time() - start_time >= term_criteria):
			pop.sort(reverse=True)
			best_path = list(pop[0])
			best_path[0] = max_path - best_path[0]
			break
		# Prune population for next iteration
		population = prune_pop(pop, children)
		print("Time elapsed: ", time.time()-start_time)
	return tuple(best_path)

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
	while len(pop) < init_pop:
		state = ''
		unadded_chars = string.ascii_uppercase[:len(locs)]
		while len(state) < len(locs):
			label = unadded_chars[random.randint(0, len(unadded_chars)-1)]
			if label not in state:
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
	return None

# Mutate child by swapping two locations at random
# First mutation shuffles each half of the state independently
# Second mutation swaps two random indices of the state
def mutate(state, mutation=0):
	mutant = None
	if mutation == 1:
		mid = len(state)/2
		mutant = list(state)
		mutant_1 = mutant[:mid]
		random.shuffle(mutant1)
		mutant_2 = mutant[mid:]
		random.shuffle(mutant_2)
		mutant = []
		mutant.extend(mutant_1)
		mutant.extend(mutant_2)
	else:
		i, j = 0, 0
		while i == j:
			i = random.randint(0, len(state)-1)
			j = random.randint(0, len(state)-1)
		mutant = list(state)
		mutant[i] = state[j]
		mutant[j] = state[i]
	return ''.join(mutant)

# Crossover two parent states to create child state.
# Child will randomly mutate
def crossover(parents, mutation_rate, method=1):
	children = []
	while len(parents) > 0:
		i, j = 0, 0
		while i == j:
			i, j = random.randint(0, len(parents)-1), random.randint(0, len(parents)-1)
		parent1 = parents[i]
		parent2 = parents[j]

		child= ''
		pos = random.randint(0, len(parent1) -1)
		child += parent1[:pos]
		child += parent2[pos:]
		child = fix_child(child)

		if(random.randint(0, 99) < mutation_rate):
			child = mutate(child)

		children.append(child)
		parents.remove(parent1)
		parents.remove(parent2)
	return children

# Remove duplicate values/add in missing values
def fix_child(child):
	doubles = []
	missing = []
	for c in string.ascii_uppercase[:len(child)]:
		if child.count(c) == 0:
			missing.append(c)
		if child.count(c) == 2:
			doubles.append(c)
	child = list(child)
	for i in range(len(child)):
		if child[i] in doubles:
			doubles.remove(child[i])
			child[i] = missing[0]
			missing = missing[1:]
	return ''.join(child)

# Select two states to act as parents
# TODO: Figure out method of parent selection
def select_parents(pop, num_parents):
	fitness_sum = 0
	parents = []
	rand_pop = pop.copy()
	random.shuffle(rand_pop)
	for p in pop:
		fitness_sum +=  p[0]
	threshold = random.randint(0, int(fitness_sum))
	while len(parents) < num_parents:
		s = 0
		for p in rand_pop:
			s+= p[0]
			if s > threshold:
				parents.append(p[1])
				fitness_sum -= p[0]
				rand_pop.remove(p)
				random.shuffle(rand_pop)
				break
		threshold = random.randint(0, int(fitness_sum))
	return parents

# Prune population, should just return states
# TODO: Prune population for next iteration
# Maybe just replace lowest fitness states with children?
def prune_pop(pop, children):
	new_pop = []
	pop.sort(reverse=True)
	for p in pop:
		new_pop.append(p[1])
	new_pop.extend(children)
	return new_pop

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
	f.close()
	return locations

def write_path_to_file(path, locs, fname="output.txt"):
	with open(fname, 'w+') as f:
		for i in range(len(path)):
			loc = get_location(path[i], locs)
			x, y = loc.get_coords()
			f.write(str(x) + "," + str(y) + "\n")
	f.close()


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
	write_path_to_file(best_path[1], locations)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--terminate', required=True, type=float)
	parser.add_argument('-m', '--mutation_rate', type=int)
	parser.add_argument('-i', '--init_pop', type=int)
	parser.add_argument('filename')
	main(parser.parse_args())