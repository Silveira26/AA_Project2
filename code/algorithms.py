import time
import random
from utils import is_vertex_cover


# GOOD ALGORITHMS
def randomized_vertex_cover_fpt(graph, k):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0
    vertex_cover = set()
    remaining_graph = graph.copy()

    for _ in range(k):
        num_solutions_tested += 1
        if len(remaining_graph.edges()) == 0:
            break

        edge = random.choice(list(remaining_graph.edges()))
        num_operations += 1

        vertex = random.choice(edge)
        vertex_cover.add(vertex)
        num_operations += 1

        edges_to_remove = [e for e in remaining_graph.edges(vertex)]
        remaining_graph.remove_edges_from(edges_to_remove)
        num_operations += len(edges_to_remove)

    execution_time = time.time() - start_time

    if len(remaining_graph.edges()) == 0:
        return vertex_cover, num_operations, execution_time, num_solutions_tested
    else:
        return None, num_operations, execution_time, num_solutions_tested

def randomized_vertex_cover_fpt_v2(graph, k):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0
    vertex_cover = set()
    remaining_graph = graph.copy()
    tested_vertex_sets = set()

    for _ in range(k):
        if len(remaining_graph.edges()) == 0:
            break

        while True:
            edge = random.choice(list(remaining_graph.edges()))
            num_operations += 1

            vertex = random.choice(edge)
            temp_vertex_cover = vertex_cover.copy()
            temp_vertex_cover.add(vertex)

            temp_vertex_hash = hash(frozenset(temp_vertex_cover))
            if temp_vertex_hash not in tested_vertex_sets:
                tested_vertex_sets.add(temp_vertex_hash)
                break

        vertex_cover = temp_vertex_cover
        num_operations += 1

        edges_to_remove = [e for e in remaining_graph.edges(vertex)]
        remaining_graph.remove_edges_from(edges_to_remove)
        num_operations += len(edges_to_remove)
        num_solutions_tested += 1

    execution_time = time.time() - start_time

    if len(remaining_graph.edges()) == 0:
        return vertex_cover, num_operations, execution_time, num_solutions_tested
    else:
        return None, num_operations, execution_time, num_solutions_tested

def randomized_vertex_cover_fpt_v2_1(graph, k):
    start_time = time.time()
    num_operations = 0
    num_solutions_tested = 0
    
    vertex_cover = set()
    remaining_graph = graph.copy()
    added_vertices = set()

    while len(vertex_cover) < k:
        num_solutions_tested += 1
        if len(remaining_graph.edges()) == 0:
            break

        edge = random.choice(list(remaining_graph.edges()))
        num_operations += 1

        vertex = random.choice(edge)
        if vertex in added_vertices:
            continue

        vertex_cover.add(vertex)
        added_vertices.add(vertex)
        num_operations += 1

        edges_to_remove = [e for e in remaining_graph.edges(vertex)]
        remaining_graph.remove_edges_from(edges_to_remove)
        num_operations += len(edges_to_remove)

    execution_time = time.time() - start_time

    if len(remaining_graph.edges()) == 0 and len(vertex_cover) == k:
        return vertex_cover, num_operations, execution_time, num_solutions_tested
    else:
        return None, num_operations, execution_time, num_solutions_tested


# ??? Algorithms
def randomized_vertex_cover_fpt_D(graph, k, max_attempts= 10000):
    start_time = time.time()
    num_operations = 0
    num_solutions_tested = 0

    vertex_cover = set()
    
    tested_combinations = set()  # To track combinations of vertices already tested

    for _ in range(max_attempts):
        num_solutions_tested += 1
        vertex_cover = set()
        remaining_graph = graph.copy()
        added_vertices = set()
        while len(vertex_cover) < k:
            
            if len(remaining_graph.edges()) == 0:
                break

            edge = random.choice(list(remaining_graph.edges()))
            num_operations += 1

            vertex = random.choice(edge)
            if vertex in added_vertices:
                continue

            vertex_cover.add(vertex)
            added_vertices.add(vertex)
            num_operations += 1

            edges_to_remove = [e for e in remaining_graph.edges(vertex)]
            remaining_graph.remove_edges_from(edges_to_remove)
            num_operations += len(edges_to_remove)

        combination = frozenset(vertex_cover)
        if combination in tested_combinations:
            continue
        tested_combinations.add(combination)

        if is_vertex_cover(graph, vertex_cover):
            break

    execution_time = time.time() - start_time

    if len(remaining_graph.edges()) == 0 and len(vertex_cover) == k:
        return vertex_cover, num_operations, execution_time, num_solutions_tested
    else:
        return None, num_operations, execution_time, num_solutions_tested

# BAD ALGORITHMS
def randomized_vertex_cover_fpt_keeper(graph, k, max_attempts=1000):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0
    best_vertex_cover = None
    best_cover_metric = float('inf')  # Define a metric to evaluate the best cover
    tested_combinations = set()  # To track tested combinations of vertices

    for _ in range(max_attempts):
        num_solutions_tested += 1
        vertex_cover = set()
        remaining_graph = graph.copy()

        while len(vertex_cover) < k:
            if len(remaining_graph.edges()) == 0:
                break

            edge = random.choice(list(remaining_graph.edges()))
            vertex = random.choice(edge)

            if vertex in vertex_cover:
                continue  # Skip if the vertex is already in the cover

            vertex_cover.add(vertex)
            num_operations += 1

            edges_to_remove = [e for e in remaining_graph.edges(vertex)]
            remaining_graph.remove_edges_from(edges_to_remove)
            num_operations += len(edges_to_remove)

        # Check if the combination has been tested before
        combination = frozenset(vertex_cover)
        if combination in tested_combinations:
            continue
        tested_combinations.add(combination)

        # Update the best vertex cover if a better one is found
        current_metric = sum(vertex_cover)  # Example: sum of vertex indices
        if current_metric < best_cover_metric and len(vertex_cover) == k:
            best_cover_metric = current_metric
            best_vertex_cover = vertex_cover

        if len(remaining_graph.edges()) == 0:
            break  # Stop if all edges are covered

    execution_time = time.time() - start_time
    return best_vertex_cover, num_operations, execution_time, num_solutions_tested

def randomized_vertex_cover_fpt_attempts(graph, k, max_attempts):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0

    vertex_cover = set()
    remaining_graph = graph.copy()
    tested_combinations = set()  # To track combinations of vertices already tested

    for _ in range(max_attempts):
        num_solutions_tested += 1

        # Generate a random combination of k vertices
        vertices = list(remaining_graph.nodes())
        num_operations += 1  # Counting the operation to list nodes

        random_combination = tuple(sorted(random.sample(vertices, k)))
        num_operations += k  # Counting the operations in sampling

        # Check if this combination has been tested before
        if random_combination in tested_combinations:
            continue  # Skip this combination as it's already been tested
        tested_combinations.add(random_combination)
        num_operations += 1  # Counting the operation of adding to the set

        # Check if the combination forms a vertex cover
        is_vertex_cover = all(any(v in random_combination for v in edge) for edge in remaining_graph.edges())
        num_operations += len(remaining_graph.edges()) * k  # Counting the operations in checking edges

        if is_vertex_cover:
            execution_time = time.time() - start_time
            return set(random_combination), num_operations, execution_time, num_solutions_tested

    execution_time = time.time() - start_time
    return None, num_operations, execution_time, num_solutions_tested  # No valid cover found

def randomized_vertex_cover_fpt_best(graph, k, max_attempts):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0

    remaining_graph = graph.copy()
    tested_combinations = set()  # To track combinations of vertices already tested

    for _ in range(max_attempts):
        num_solutions_tested += 1

        # Generate a random combination of k vertices
        vertices = list(remaining_graph.nodes())
        num_operations += 1  # Counting the operation to list nodes

        random_combination = tuple(sorted(random.sample(vertices, k)))
        num_operations += k  # Counting the operations in sampling

        # Check if this combination has been tested before
        if random_combination in tested_combinations:
            continue  # Skip this combination as it's already been tested
        tested_combinations.add(random_combination)
        num_operations += 1  # Counting the operation of adding to the set

        # Check if the combination forms a vertex cover
        is_vertex_cover = all(any(v in random_combination for v in edge) for edge in remaining_graph.edges())
        num_operations += len(remaining_graph.edges()) * k  # Counting the operations in checking edges

        if is_vertex_cover:
            execution_time = time.time() - start_time
            return set(random_combination), num_operations, execution_time, num_solutions_tested

    execution_time = time.time() - start_time
    return None, num_operations, execution_time, num_solutions_tested  # No valid cover found

def randomized_vertex_cover_best_solution(graph, k):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0
    best_vertex_cover = None
    best_metric = float('inf')  # Define an appropriate metric

    remaining_graph = graph.copy()

    while True:
        num_solutions_tested += 1
        vertex_cover = set()

        for _ in range(k):
            if len(remaining_graph.edges()) == 0:
                break

            edge = random.choice(list(remaining_graph.edges()))
            num_operations += 1

            vertex = random.choice(edge)
            vertex_cover.add(vertex)
            num_operations += 1

            edges_to_remove = [e for e in remaining_graph.edges(vertex)]
            remaining_graph.remove_edges_from(edges_to_remove)
            num_operations += len(edges_to_remove)

        current_metric = sum(vertex_cover)  # Example metric
        if current_metric < best_metric and len(vertex_cover) == k:
            best_metric = current_metric
            best_vertex_cover = vertex_cover

        if len(remaining_graph.edges()) == 0 or num_solutions_tested >= 1000:  # Set a limit to attempts
            break

    execution_time = time.time() - start_time
    return best_vertex_cover, num_operations, execution_time, num_solutions_tested

def randomized_vertex_cover_no_repeats(graph, k, max_attempts=1000):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0
    tested_combinations = set()
    remaining_graph = graph.copy()

    for _ in range(max_attempts):
        num_solutions_tested += 1
        vertex_cover = set()

        while len(vertex_cover) < k:
            if len(remaining_graph.edges()) == 0:
                break
            edge = random.choice(list(remaining_graph.edges()))
            vertex = random.choice(edge)
            vertex_cover.add(vertex)

        combination = frozenset(vertex_cover)
        if combination in tested_combinations:
            continue
        tested_combinations.add(combination)

        if len(remaining_graph.edges()) == 0:
            execution_time = time.time() - start_time
            return vertex_cover, num_operations, execution_time, num_solutions_tested

    execution_time = time.time() - start_time
    return None, num_operations, execution_time, num_solutions_tested

def randomized_vertex_cover_combined(graph, k, max_attempts=1000):
    start_time = time.time()

    num_operations = 0
    num_solutions_tested = 0
    best_vertex_cover = None
    best_metric = float('inf')
    tested_combinations = set()
    remaining_graph = graph.copy()

    for _ in range(max_attempts):
        num_solutions_tested += 1
        vertex_cover = set()

        while len(vertex_cover) < k:
            if len(remaining_graph.edges()) == 0:
                break
            edge = random.choice(list(remaining_graph.edges()))
            vertex = random.choice(edge)
            vertex_cover.add(vertex)

        combination = frozenset(vertex_cover)
        if combination in tested_combinations:
            continue
        tested_combinations.add(combination)

        current_metric = sum(vertex_cover)  # Example metric
        if current_metric < best_metric:
            best_metric = current_metric
            best_vertex_cover = vertex_cover

        if len(remaining_graph.edges()) == 0:
            execution_time = time.time() - start_time
            return best_vertex_cover, num_operations, execution_time, num_solutions_tested

    execution_time = time.time() - start_time
    return best_vertex_cover, num_operations, execution_time, num_solutions_tested