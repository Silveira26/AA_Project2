from itertools import combinations

def exhaustive_search(graph, k):
    num_comparisons = 0
    num_operations = 0
    num_solutions_tested = 0

    num_vertices = graph.number_of_nodes()
    vertex_set = set(range(num_vertices))
    
    for subset in combinations(vertex_set, k):
        num_solutions_tested += 1
        num_operations += 1

        is_vertex_cover = True
        for edge in graph.edges():
            num_comparisons += 2
            num_operations += 1
            if edge[0] not in subset and edge[1] not in subset:
                is_vertex_cover = False
                break
        
        if is_vertex_cover:
            return subset, num_comparisons, num_operations, num_solutions_tested
    
    return set(), num_comparisons, num_operations, num_solutions_tested

def greedy_heuristic(graph, k):
    num_comparisons = 0
    num_operations = 0
    num_solutions_tested = 0

    vertex_cover = set()
    remaining_graph = graph.copy()

    while len(vertex_cover) < k and len(remaining_graph.edges()) > 0:
        num_comparisons += 1

        # Find the vertex with the highest degree
        u = max(remaining_graph, key=remaining_graph.degree)
        num_deleted_edges = remaining_graph.degree(u)

        vertex_cover.add(u)

        remaining_graph.remove_node(u)
        num_operations += num_deleted_edges

    # Check if a valid vertex cover was found
    if len(vertex_cover) == k and len(remaining_graph.edges()) == 0:
        num_solutions_tested += 1
        return vertex_cover, num_comparisons, num_operations, num_solutions_tested
    else:
        return set(), num_comparisons, num_operations, num_solutions_tested
