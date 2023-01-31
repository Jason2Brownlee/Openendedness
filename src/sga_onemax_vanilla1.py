# simple ga for one max
from random import seed
from random import randint
from random import randrange
from random import random

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

# locate the population member with best fitness
def get_best(pop):
	# sort the population ascending order, in place
	pop.sort(key=lambda tup: tup[1])
	# return the last item with largest fitness
	return pop[-1]

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

# create the next generation
def reproduce(parents, m_rate):
	nextegen = list()
	# enumerate population in pairs
	for i in range(0, len(parents), 2):
		# select members to cross over
		s1, s2 = parents[i], parents[i+1]
		# perform cross over and get two children
		c1, c2 = crossover(s1[0], s2[0])
		# mutate children
		mutate(c1, m_rate)
		mutate(c2, m_rate)
		# store children in the next generation
		nextegen.append(c1)
		nextegen.append(c2)
	return nextegen

# run the n_pop algorithm
def evolve(n_strings, length, n_epochs, n_rounds, m_rate):
	# keep track of the best solution found
	best = None
	# create the initial population
	pop = [random_bitstring(length) for _ in range(n_pop)]
	# enumerate epochs
	for epoch in range(n_epochs):
		# evaluate the population
		pop = evaluate(pop)
		# check for new best
		candidate = get_best(pop)
		if best is None or candidate[1] > best[1]:
			# we have a new best
			best = candidate
			# report best performance
			print('>e:%d, fitness=%d ' % (epoch, best[1]))
		# select parents of the next generation
		parents = select(pop, n_rounds)
		# create children to comprise the next generation
		pop = reproduce(parents, m_rate)
	return best

# length of bitstrings
length = 1000
# population size
n_pop = 1000
# maximum epochs
n_epochs = 500
# number of tournaments for selection
n_rounds = 3
# mutation rate
m_rate = 0.01
# seed the random number generator
seed(1)
# run the process
evolve(n_pop, length, n_epochs, n_rounds, m_rate)


# 43.3s
