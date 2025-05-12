import numpy as np

class GeneticAlgorithm:
    def __init__(self, population_size=50, generations=100, mutation_rate=0.1, crossover_rate=0.5):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    def initialize_population(self, gene_count):
        return np.random.uniform(-1, 1, (self.population_size, gene_count))

    def generate_signal(self, individual, X):
        input_dim = X.shape[1]
        hidden_dim = 4
        output_dim = 1

        # Decode weights and biases from the genome
        idx = 0
        W1 = individual[idx:idx + input_dim * hidden_dim].reshape(input_dim, hidden_dim)
        idx += input_dim * hidden_dim
        b1 = individual[idx:idx + hidden_dim]
        idx += hidden_dim
        W2 = individual[idx:idx + hidden_dim * output_dim].reshape(hidden_dim, output_dim)
        idx += hidden_dim * output_dim
        b2 = individual[idx:idx + output_dim]

        # Feedforward computation
        hidden = np.maximum(0, np.dot(X, W1) + b1)  # Hidden layer activation
        logits = np.dot(hidden, W2) + b2      # Output layer (before activation)

        # Scaled sigmoid: outputs in [-1, 1] for smoother decisions
        sigmoid = 1 / (1 + np.exp(-logits))   # [0, 1]
        output = 2 * sigmoid - 1              # Scale to [-1, 1]

        return output.flatten()

    def simulate_portfolio(self, individual, X, daily_returns, trading_penalty=0.001):
        signals = self.generate_signal(individual, X)
        signals = signals[:-1]  # Drop last signal (no next-day return to pair with it)
        shifted_returns = daily_returns[1:]  # Drop first return (corresponds to next day)

        strategy_returns = signals * shifted_returns
        portfolio_value = np.cumprod(1 + strategy_returns)

        # Calculate trading activity as absolute day-to-day signal changes
        signal_diff = np.abs(np.diff(signals))
        penalty = trading_penalty * np.sum(signal_diff)

        if np.isnan(portfolio_value[-1]) or np.isinf(portfolio_value[-1]):
            return -np.inf

        return portfolio_value[-1] - penalty

    def compute_fitness(self, population, X, daily_returns):
        return np.array([
            self.simulate_portfolio(individual, X, daily_returns)
            for individual in population
        ])

    def select_parents(self, population, fitness):
        fitness = np.array(fitness)
        fitness = fitness - np.min(fitness) + 1e-6  # Avoid negatives
        probabilities = fitness / np.sum(fitness)
        idx = np.random.choice(len(population), size=2, p=probabilities)
        return population[idx[0]], population[idx[1]]

    def crossover(self, parent1, parent2):
        if np.random.rand() < self.crossover_rate:
            point = np.random.randint(1, len(parent1))
            child1 = np.concatenate([parent1[:point], parent2[point:]])
            child2 = np.concatenate([parent2[:point], parent1[point:]])
            return child1, child2
        return parent1.copy(), parent2.copy()

    def mutate(self, individual):
        if np.random.rand() < self.mutation_rate:
            idx = np.random.randint(len(individual))
            individual[idx] += np.random.normal(0, 0.1)
        return individual

    def evolve_population(self, population, fitness):
        new_population = []
        while len(new_population) < self.population_size:
            p1, p2 = self.select_parents(population, fitness)
            c1, c2 = self.crossover(p1, p2)
            new_population.append(self.mutate(c1))
            if len(new_population) < self.population_size:
                new_population.append(self.mutate(c2))
        return np.array(new_population)

    def run(self, X, daily_returns):
        input_dim = X.shape[1]
        hidden_dim = 4
        output_dim = 1

        # Total genes = input*hidden + hidden + hidden*output + output
        gene_count = input_dim * hidden_dim + hidden_dim + hidden_dim * output_dim + output_dim

        population = self.initialize_population(gene_count)
        best_solution = None
        best_fitness = -np.inf

        for generation in range(self.generations):
            fitness = self.compute_fitness(population, X, daily_returns)
            best_idx = np.argmax(fitness)
            if fitness[best_idx] > best_fitness:
                best_fitness = fitness[best_idx]
                best_solution = population[best_idx]

            # Uncomment if you want to monitor progress
            # print(f"Generation {generation}: Best Fitness = {best_fitness:.5f}")

            population = self.evolve_population(population, fitness)

        return best_solution