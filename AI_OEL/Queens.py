import tkinter as tk
import random
import time

# Fitness function: number of non-attacking pairs of queens
def fitness(solution):
    n = len(solution)
    non_attacking = 0
    for i in range(n):
        for j in range(i + 1, n):
            if solution[i] != solution[j] and abs(solution[i] - solution[j]) != abs(i - j):
                non_attacking += 1
    return non_attacking

# Generate initial population
def generate_population(pop_size, n):
    return [[random.randint(0, n - 1) for _ in range(n)] for _ in range(pop_size)]

# Select parents using roulette wheel selection
def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    probabilities = [f / total_fitness for f in fitnesses]
    return random.choices(population, weights=probabilities, k=2)

# Crossover: Single-point crossover
def crossover(parent1, parent2):
    point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutation: Randomly change a queen's row in one column
def mutate(solution, mutation_rate):
    if random.random() < mutation_rate:
        col = random.randint(0, len(solution) - 1)
        solution[col] = random.randint(0, len(solution) - 1)
    return solution

# GUI-based Genetic Algorithm
class EightQueensGA:
    def __init__(self, root, pop_size, n, max_generations, mutation_rate):
        self.root = root
        self.n = n
        self.pop_size = pop_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.cell_size = 50
        self.canvas = tk.Canvas(root, width=n * self.cell_size, height=n * self.cell_size)
        self.canvas.pack()
        self.generation_label = tk.Label(root, text="Generation: 0", font=("Arial", 14))
        self.generation_label.pack()
        self.start_button = tk.Button(root, text="Start", command=self.run_ga, font=("Arial", 14))
        self.start_button.pack()

    def draw_board(self, solution):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                    fill=color
                )
        for col, row in enumerate(solution):
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(
                x - 15, y - 15, x + 15, y + 15,
                fill="red"
            )

    def run_ga(self):
        population = generate_population(self.pop_size, self.n)
        for generation in range(self.max_generations):
            fitnesses = [fitness(individual) for individual in population]
            best_fitness = max(fitnesses)
            best_solution = population[fitnesses.index(best_fitness)]
            self.generation_label.config(text=f"Generation: {generation + 1}, Best Fitness: {best_fitness}")
            self.draw_board(best_solution)
            self.root.update()
            time.sleep(0.1)

            if best_fitness == self.n * (self.n - 1) // 2:
                print(f"Solution found in generation {generation}: {best_solution}")
                return

            new_population = []
            for _ in range(self.pop_size // 2):
                parent1, parent2 = select_parents(population, fitnesses)
                child1, child2 = crossover(parent1, parent2)
                child1 = mutate(child1, self.mutation_rate)
                child2 = mutate(child2, self.mutation_rate)
                new_population.extend([child1, child2])
            population = new_population

        print("No perfect solution found.")
        return

# Create GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("8-Queens Problem - Genetic Algorithm")
    app = EightQueensGA(root, pop_size=100, n=8, max_generations=600, mutation_rate=0.1)
    root.mainloop()
