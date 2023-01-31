# one problem is that eval is not slow
# another problem is that random numbers are not thread safe

# simple ga for one max
from random import seed
from random import randint
from random import randrange
from random import random
from joblib import Parallel
from joblib import delayed



# calculate the number of ones in a binary string
def fitness(candidate):
	# one max
	return sum(candidate)

# generate a random binary string of a given length
def random_bitstring(length):
	return [randint(0, 1) for _ in range(length)]

# evaluate a population of bit strings
def evaluate(pop):
	return [(s, fitness(s)) for s in pop]
	# executor = Parallel(n_jobs=8, backend='multiprocessing')
	# tasks = (delayed(fitness)(s) for s in pop)
	# scores = executor(tasks)
	# return list(zip(pop, scores))

# locate the population member with best fitness
def get_best(epoch, pop, best):
	# sort the population ascending order, in place
	pop.sort(key=lambda tup: tup[1])
	# get the population member with the best fitness
	pop_best = pop[-1]
	# check if population best is better than the current best
	if pop_best[1] > best[1]:
		print(f'>e:{epoch}, fitness={pop_best[1]}')
		return pop_best
	# keep the current best
	return best

# tournament selection
def tournament(pop, n_rounds):
	# select a starting point
	best = pop[randrange(len(pop))]
	# enumerate selection rounds
	for _ in range(n_rounds):
		# select an opponent
		candidate = pop[randrange(len(pop))]
		# check if opponent is better that best so far
		if candidate[1] > best[1]:
			best = candidate
	return best

# select the next generation
def select(pop, n_rounds):
	return [tournament(pop, n_rounds) for _ in range(len(pop))]
	# executor = Parallel(n_jobs=8, backend='multiprocessing')
	# tasks = (delayed(tournament)(pop, n_rounds) for _ in range(len(pop)))
	# selected = executor(tasks)
	# print(len(selected))
	# return list(selected)

# crossover for two binary strings
def crossover(s1, s2):
	# select a split point
	ix = randrange(len(s1))
	# perform one-point cross over
	return s1[:ix] + s2[ix:], s2[:ix] + s1[ix:]

# apply mutation to a bitstring
def mutate(candidate, m_rate):
	# mutate in place
	for i in range(len(candidate)):
		# check for a mutation
		if random() < m_rate:
			# flip a bit
			candidate[i] = 1 - candidate[i]

def create_children(s1, s2):
	# perform cross over and get two children
	c1, c2 = crossover(s1[0], s2[0])
	# mutate children
	mutate(c1, m_rate)
	mutate(c2, m_rate)
	return c1, c2

# create the next generation
def reproduce(parents, m_rate):
	nextegen = list()
	# enumerate population in pairs
	for i in range(0, len(parents), 2):
		# select parents to cross over
		s1, s2 = parents[i], parents[i+1]
		# create crossed and mutated
		c1, c2 = create_children(s1, s2)
		# store children in the next generation
		nextegen.append(c1)
		nextegen.append(c2)
	return nextegen

# run the n_pop algorithm
def evolve(n_strings, length, n_epochs, n_rounds, m_rate):
	# keep track of the best solution found
	best = (None, 0)
	# create the initial population
	pop = [random_bitstring(length) for _ in range(n_pop)]
	# enumerate epochs
	for epoch in range(n_epochs):
		# evaluate the population
		pop = evaluate(pop)
		# check for new best
		best = get_best(epoch, pop, best)
		# select parents of the next generation
		parents = select(pop, n_rounds)
		# create children to comprise the next generation
		pop = reproduce(parents, m_rate)
	return best

# length of bit strings
length = 1000
# population size
n_pop = 1000
# maximum epochs
n_epochs = 500
# number of tournaments for selection
n_rounds = 3
# mutation rate
m_rate = 0.005
# seed the random number generator
seed(1)
# run the process
solution = evolve(n_pop, length, n_epochs, n_rounds, m_rate)


# [Finished in 43.1s]
