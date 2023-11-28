import random
import time
from utils import is_vertex_cover

def randomized_search(graph, k, max_iterations):
    start_time = time.time()
    num_operations = 0
    num_solutions_tested = 0

    for _ in range(max_iterations):
        num_operations += 1
        num_solutions_tested += 1
        candidate_cover = set(random.sample(list(graph.nodes()), k))
        num_operations += len(candidate_cover)

        if is_vertex_cover(graph, candidate_cover):
            num_operations += graph.number_of_edges()
            end_time = time.time()
            execution_time = end_time - start_time
            return candidate_cover, num_operations, execution_time, num_solutions_tested

    end_time = time.time()
    execution_time = end_time - start_time
    return None, num_operations, execution_time, num_solutions_tested