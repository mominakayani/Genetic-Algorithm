

initial_population = [
    [2, 4, 3, 1],
    [1, 2, 3, 4],
    [2, 1, 3, 2],
    [4, 3, 1, 1]
]
def count_conflicts(state):
    """Count pairs of queens attacking each other."""
    conflicts = 0
    n = len(state)

    for i in range(n):
        for j in range(i + 1, n):
            same_row = state[i] == state[j]
            same_diagonal = abs(state[i] - state[j]) == abs(i - j)

            if same_row or same_diagonal:
                conflicts += 1

    return conflicts


def roulette_selection(population, random_values):
    """
    Lower conflict count is better.
    Convert conflict count to positive selection weight.
    """
    weights = [1 / (1 + count_conflicts(s)) for s in population]
    total_weight = sum(weights)

    probabilities = [w / total_weight for w in weights]
    cumulative = []
    running_total = 0

    for p in probabilities:
        running_total += p
        cumulative.append(running_total)

    selected = []

    for r in random_values:
        for i, boundary in enumerate(cumulative):
            if r <= boundary:
                selected.append(population[i][:])
                break

    return selected, probabilities


def one_point_crossover(parent1, parent2):
    """Crossover after the second queen position."""
    child1 = parent1[:2] + parent2[2:]
    child2 = parent2[:2] + parent1[2:]
    return child1, child2


def evaluate(population, generation_name):
    print(f"\n{generation_name}")
    print("-" * 48)

    for i, state in enumerate(population, start=1):
        conflicts = count_conflicts(state)
        print(
            f"State {i}: {state}, "
            f"Conflicts = {conflicts}"
        )



evaluate(initial_population, "Generation 0 (Initial Population)")

population = initial_population


roulette_values = [
    [0.20, 0.60, 0.70, 0.95],  # Selection for Generation 1
    [0.10, 0.40, 0.70, 0.90]   # Selection for Generation 2
]


for generation in range(2):
    selected, probabilities = roulette_selection(
        population, roulette_values[generation]
    )

    print(f"\nGeneration {generation + 1} selection probabilities:")
    for i, p in enumerate(probabilities, start=1):
        print(f"State {i}: {p:.4f} ({p * 100:.2f}%)")

   
    new_population = []

    for i in range(0, 4, 2):
        child1, child2 = one_point_crossover(
            selected[i], selected[i + 1]
        )
        new_population.extend([child1, child2])

    
    population = new_population

    evaluate(population, f"Generation {generation + 1}")

    best_conflicts = min(count_conflicts(s) for s in population)
    print(f"Best conflicts = {best_conflicts}")

    if best_conflicts == 0:
        print("Solution found!")
