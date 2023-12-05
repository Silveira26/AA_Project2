import time
import random
from utils import is_vertex_cover

# Algorithms
def randomized_fpt(graph, k):
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

        graph_edges = list(remaining_graph.edges())
        edge = random.choice(graph_edges)
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

def randomized_fpt_attempts(graph, k, max_attempts= 10000):
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