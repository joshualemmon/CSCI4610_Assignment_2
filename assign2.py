import random
import argparse
import string
import math
import time

# Genetic Algorithm Solution 

# Location class used for first domain
# Nodes encoded as A-T starting in bottom left corner and
# moving left-right while moving up a row
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

# Town class used for second domain
# Each town will have a label A-G
# Each town tracks the distance to another town with a dictionary
class Town:
	def __init__(self, town, label):
		self.town = town
		self.label = label
		self.distances = dict()

	def get_label(self):
		return self.label

	def has_label(self, label):
		return self.label == label

	def set_dist(self, label, dist):
		self.distances[label] = dist

	def get_dist(self, label):
		return self.distances[label]

# Main genetic algorithm
# Need to expand to handle second domain
def genetic(inputs, term_criteria, mutation_rate, init_pop, crossover_method, mutation_method, domain):
	best_path = None
	# STEP 1: Initialize population
	population = get_initial_population(inputs, init_pop)
	start_time = time.time()
	# Will loop until termination criteria is met
	while(True):
		distances = []
		# STEP 2: Calculate fitness value for each state
		for p in population:
			distances.append(calc_distance(p, inputs, domain))
		max_path = max(distances)
		# Scale fitness so smaller paths are more fit
		fitness_vals = [max_path-x for x in distances]
		# Zip fitness value with respective population
		pop = [ (y,x) for x, y in zip(population, fitness_vals)]
		# STEP 3: Select parents for crossover
		# Maybe want to pick 40% of population to be parents
		num_parents = init_pop * 0.4
		# Want even number of parents
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
		# print("Time elapsed: ", time.time()-start_time)
	return tuple(best_path)

# Calculate the fitness of a state
# Calculated by total distance of state path
def calc_distance(state, inputs, domain):
	distance = 0
	for i in range(len(state)):
		loc1 = get_location(state[i-1], inputs)
		loc2 = get_location(state[i], inputs)
		distance += get_distance(loc1, loc2, domain)
	return distance

# Get random states for initial population
# Ensures that locations are not visited twice
def get_initial_population(inputs, init_pop):
	pop = []
	while len(pop) < init_pop:
		state = ''
		unadded_chars = string.ascii_uppercase[:len(inputs)]
		while len(state) < len(inputs):
			label = unadded_chars[random.randint(0, len(unadded_chars)-1)]
			if label not in state:
				state += label
				unadded_chars.replace(label, "")
		if(state not in pop):
			pop.append(state)
	return pop

# Get location object with given label value
def get_location(label, inputs):
	for i in inputs:
		if i.has_label(label):
			return i
	return None

# Mutate child by swapping two locations at random
# First mutation shuffles each half of the state independently
# Second mutation swaps two random indices of the state
def mutate(state, mutation=1):
	mutant = None
	if mutation == 1:
		i, j = 0, 0
		while i == j:
			i = random.randint(0, len(state)-1)
			j = random.randint(0, len(state)-1)
		mutant = list(state)
		mutant[i] = state[j]
		mutant[j] = state[i]
	else:
		mid = len(state)/2
		mutant = list(state)
		mutant_1 = mutant[:mid]
		random.shuffle(mutant1)
		mutant_2 = mutant[mid:]
		random.shuffle(mutant_2)
		mutant = []
		mutant.extend(mutant_1)
		mutant.extend(mutant_2)
	return ''.join(mutant)

# Crossover two parent states to create child state.
# Child will randomly mutate at rate mutation_rate
# 1 child created per pair of parents
# Should add edge recombination crossover for method #2, as its the most accurate
def crossover(parents, mutation_rate, method=1):
	children = []
	while len(parents) > 0:
		i, j = 0, 0
		while i == j:
			i, j = random.randint(0, len(parents)-1), random.randint(0, len(parents)-1)
		parent1 = parents[i]
		parent2 = parents[j]
		child= ''
		if method == 1:
			pos = random.randint(0, len(parent1) -1)
			child += parent1[:pos]
			child += parent2[pos:]
			child = fix_child(child)

			if(random.randint(0, 99) < mutation_rate):
				child = mutate(child)

			child = fix_child(child)
			children.append(child)
			parents.remove(parent1)
			parents.remove(parent2)
		else:
			neighbours = dict()
			for c in string.ascii_uppercase[:len(parent1)]:
				n_set = set()
				i = parent1.index(c)
				n_set.add(parent1[i-1])
				if(i+1 >= len(parent1)):
					i = -1
				n_set.add(parent1[i+1])
				i = parent2.index(c)
				n_set.add(parent2[i-1])
				if(i+1 >= len(parent2)):
					i = -1
				n_set.add(parent2[i+1])
				neighbours[c] = n_set
			r = random.randint(0,1)
			if r == 0:
				child += parent1[0]
			else:
				child += parent2[0]
			neighbours = remove_element(neighbours, child[0])
			while len(child) < len(parent1):
				least = get_least_neighbours(neighbours)
				neighbours.pop(least, None)
				child+= least
				neighbours = remove_element(neighbours, least)
			child = fix_child(child)
			if(random.randint(0, 99) < mutation_rate):
				child = mutate(child)

			children.append(child)
			parents.remove(parent1)
			parents.remove(parent2)
	return children

# Find the neighbour set with the fewest elements
def get_least_neighbours(neighbours):
	least_neighbours = []
	least = 999
	for key in neighbours.keys():
		if len(neighbours[key]) < least:
			least_neighbours = []
			least = len(neighbours[key])
			least_neighbours.append(key)
		elif len(neighbours[key]) == least:
			least_neighbours.append(key)
	if(len(least_neighbours) == 1):
		return least_neighbours[0]
	else:
		i = random.randint(0, len(least_neighbours)-1)
		return least_neighbours[i]

# Removes the given element from each set in neighbours, if the element
# exists in the set.
def remove_element(neighbours, element):
	for key in neighbours.keys():
		s = neighbours[key]
		s.discard(element)
		neighbours[key] = s	
	return neighbours

# Remove duplicate values/add in missing values from crossover
def fix_child(child):
	multiples = []
	missing = []
	fixed = False
	while(not fixed):
		fixed = True
		for c in string.ascii_uppercase[:len(child)]:
			if child.count(c) == 0:
				fixed = False
				missing.append(c)
			if child.count(c) > 1:
				fixed = False
				multiples.append(c)
		child = list(child)
		for i in range(len(child)):
			if child[i] in multiples:
				multiples.remove(child[i])
				child[i] = missing[random.randint(0, len(missing)-1)]
				missing = missing[1:]
	return ''.join(child)

# Select states to act as parents
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

# Prune population
def prune_pop(pop, children):
	new_pop = []
	pop.sort(reverse=True)
	for p in pop:
		new_pop.append(p[1])
	new_pop.extend(children)
	return new_pop

# Get distance between two locations
def get_distance(loc1, loc2, domain):
	if domain == 1:
		x1, y1 = loc1.get_coords()
		x2, y2 = loc2.get_coords()
		return (math.sqrt((x1-x2)**2 + (y1-y2)**2))
	else:
		return loc1.get_dist(loc2.get_label())

# Read in file
def read_data(fname, domain):
	if domain == 1:
		locations = []
		with open(fname, 'r') as f:
			for l in f.readlines():
				l = l.split(" ")
				locations.append(Location(l[0], l[1], l[2]))
		f.close()
		return locations
	else:
		towns = []
		with open(fname, 'r') as f:
			for i, l in enumerate(f.readlines()):
				vals = l.split(" ")
				t = Town(vals[0], string.ascii_uppercase[i])
				vals = vals[1:]
				for j, v in enumerate(vals):
					t.set_dist(string.ascii_uppercase[j], int(v))
				towns.append(t)
		f.close()
		return towns

# Write output file for use in graph generation
def write_path_to_file(path, locs, domain, dist):
	fname = "output.txt"
	with open(fname, 'w+') as f:
		f.write(str(domain) + "\n")
		f.write(str(dist) + "\n")
		if domain == 1:
			for i in range(len(path)):
				loc = get_location(path[i], locs)
				x, y = loc.get_coords()
				f.write(str(x) + "," + str(y) + "\n")
		else:
			f.write(path + "\n")
	f.close()

def main(args):
	fname = args.filename
	term_criteria = args.terminate
	domain = args.domain
	mutation_rate = args.mutation_rate
	init_pop = args.init_pop
	crossover_method = args.crossover_method
	mutation_method = args.mutation_method

	print("Finding best path for domain " + str(domain) + " with parameters:")
	print("Teminates after " + str(term_criteria) + " seconds")
	print("With an initial population of " + str(init_pop))
	print("Mutates at a rate of " + str(mutation_rate) + "%")
	print("Using mutation method " + str(mutation_method))
	print("Using crossover method " + str(crossover_method))

	inputs = read_data(fname, domain)
	best_path = genetic(inputs, term_criteria, mutation_rate, init_pop, crossover_method, mutation_method, domain)
	print("Best path is: " + best_path[1] + " with distance " + str(best_path[0]))
	write_path_to_file(best_path[1], inputs, domain, best_path[0])

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--terminate', default=0, type=int)
	parser.add_argument('-m', '--mutation_rate', default=10, type=int)
	parser.add_argument('-c', '--crossover_method', default=1, type=int)
	parser.add_argument('-mm', '--mutation_method', default=1, type=int)
	parser.add_argument('-i', '--init_pop', default=10, type=int)
	parser.add_argument('-d', '--domain', default=1, type=int)
	parser.add_argument('filename')
	main(parser.parse_args())