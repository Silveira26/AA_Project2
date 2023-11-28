"""
Problem: Vertex Cover

For a given undirected graph G(V, E), with n vertices and m edges, does G have a vertex cover
with k vertices? A vertex cover of G is a set C of vertices, such that each edge of G is incident to, at
least, one vertex in C.
"""

import os
import time
import pickle
from algorithms import exhaustive_search, greedy_heuristic
from utils import is_vertex_cover, writeTo_csv, writeTo_xlsx, generate_all,generate_random_graph
from charts import charts_main

def program(percentage_k=0.125):
    vertice_count = range(4, 33)
    data_greedy = []
    data_exhaustive = []

    chart_data = {
        'exhaustive' : {
            'num_vertices' : [],
            'edge_percentage' : [],
            'num_comparisons' : [],
            'num_operations' : [],
            'num_solutions_tested' : [],
            'time' : []
        },
        'greedy' : {
            'num_vertices' : [],
            'edge_percentage' : [],
            'num_comparisons' : [],
            'num_operations' : [],
            'num_solutions_tested' : [],
            'time' : []
        }
    }

    # Cycle through the number of vertices
    for num_vertices in vertice_count:
        #print(f'--Vertices: {num_vertices}')
        # Generate the max number of edges
        max_num_edges = int(num_vertices * (num_vertices - 1) / 2)

        # Generate the number of edges to be used
        num_edges_dict = {
            0.125 : int(0.125 * max_num_edges),
            0.25 : int(0.25 * max_num_edges),
            0.5 : int(0.5 * max_num_edges),
            0.75 : int(0.75 * max_num_edges)
        }
        
        # Cycle through the number of edges
        for edges_weight in num_edges_dict.keys():
            # Generate the graph with the specified number of vertices and edges
            #generated_graph = generate_random_graph(num_vertices, num_edges_dict[edges_weight])

            # Get graph from pickle file
            generated_graph = pickle.load(open(f'../dump/Normal/K_{percentage_k*100}/V({num_vertices})/G({num_vertices},{edges_weight*100}%).pickle', 'rb'))

            # Calculate the number of vertices to be used
            k = int(percentage_k * num_vertices)

            # Solve using exhaustive search algorithm
            start = time.time()
            vertex_cover_exhaustive, exhaustive_num_comparisons, exhaustive_num_operations, exhaustive_num_solutions  = exhaustive_search(generated_graph, k)
            end = time.time()
            exhaustive_time=end-start
            
            # Solve using greedy heuristic algorithm
            start = time.time()
            vertex_cover_greedy, greedy_num_comparisons, greedy_num_operations, greedy_num_solutions  = greedy_heuristic(generated_graph, k)
            end = time.time()
            greedy_time=end-start


            # Generate the normal graph
            #generate_all(generated_graph,generated_graph.nodes(), f'Normal/K_{percentage_k*100}/V({num_vertices})/G({num_vertices},{edges_weight*100}%)')

            # Generate the exhaustive graph
            #generate_all(generated_graph,vertex_cover_exhaustive, f'Exhaustive/K_{percentage_k*100}/V({num_vertices})/G({num_vertices},{edges_weight*100}%)')

            # Generate the greedy graph
            #generate_all(generated_graph,vertex_cover_greedy, f'Greedy/K_{percentage_k*100}/V({num_vertices})/G({num_vertices},{edges_weight*100}%)')

            is_vertex_cover_exhaustive = is_vertex_cover(generated_graph, vertex_cover_exhaustive)
            is_vertex_cover_greedy = is_vertex_cover(generated_graph, vertex_cover_greedy)

            # Append the exhaustive data to the list
            data_exhaustive.append([num_vertices, # Number of vertices
                                    edges_weight*100, # Percentage of edges
                                    num_edges_dict[edges_weight], # Number of edges
                                    percentage_k*100, # Percentage of k
                                    k, # Number of k
                                    vertex_cover_exhaustive, # Vertex cover
                                    is_vertex_cover_exhaustive, # Is vertex cover
                                    exhaustive_num_comparisons, # Number of comparisons
                                    exhaustive_num_operations, # Number of operations
                                    exhaustive_num_solutions, # Number of solutions
                                    exhaustive_time]) # Time
            
            # Append the greedy data to the list
            data_greedy.append([num_vertices, # Number of vertices
                                edges_weight*100, # Percentage of edges
                                num_edges_dict[edges_weight], # Number of edges
                                percentage_k*100, # Percentage of k
                                k, # Number of k
                                vertex_cover_greedy, # Vertex cover
                                is_vertex_cover_greedy, # Is vertex cover
                                greedy_num_comparisons, # Number of comparisons
                                greedy_num_operations, # Number of operations
                                greedy_num_solutions, # Number of solutions
                                greedy_time]) # Time
            
            # Append the exhaustive data to the chart data
            chart_data['exhaustive']['num_vertices'].append(num_vertices)
            chart_data['exhaustive']['edge_percentage'].append(edges_weight*100)
            chart_data['exhaustive']['num_comparisons'].append(exhaustive_num_comparisons)
            chart_data['exhaustive']['num_operations'].append(exhaustive_num_operations)
            chart_data['exhaustive']['num_solutions_tested'].append(exhaustive_num_solutions)
            chart_data['exhaustive']['time'].append(exhaustive_time)

            # Append the greedy data to the chart data
            chart_data['greedy']['num_vertices'].append(num_vertices)
            chart_data['greedy']['edge_percentage'].append(edges_weight*100)
            chart_data['greedy']['num_comparisons'].append(greedy_num_comparisons)
            chart_data['greedy']['num_operations'].append(greedy_num_operations)
            chart_data['greedy']['num_solutions_tested'].append(greedy_num_solutions)
            chart_data['greedy']['time'].append(greedy_time)
            
    return data_exhaustive, data_greedy, chart_data

if __name__ == '__main__':
    
    if not os.path.exists('img'):
        os.makedirs('img')
    if not os.path.exists('dump'):
        os.makedirs('dump')

    for k_percentage in [0.125, 0.25, 0.5, 0.75]:
        #print(f'K: {k_percentage*100}%')
        data_exhaustive, data_greedy, chart_data = program(k_percentage)

        writeTo_xlsx(k_percentage,data_exhaustive, data_greedy, chart_data)
        writeTo_csv(k_percentage,data_exhaustive, data_greedy, chart_data)
    
    #print('Generating charts...')
    charts_main()
    #print('Done!')


