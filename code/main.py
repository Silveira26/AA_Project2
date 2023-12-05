"""
Problem: Vertex Cover

For a given undirected graph G(V, E), with n vertices and m edges, does G have a vertex cover
with k vertices? A vertex cover of G is a set C of vertices, such that each edge of G is incident to, at
least, one vertex in C.
"""

import os
import pickle
from algorithms import *
from utils import *
from charts import charts_main

def program(percentage_k=0.125):
    vertice_count = range(4, 33) # 4, 33 / 129 / 257
    data_randomized = []

    chart_data = {
        'randomized' : {
            'num_vertices' : [],
            'edge_percentage' : [],
            'num_operations' : [],
            'num_solutions_tested' : [],
            'time' : []
        },
    }

    # Cycle through the number of vertices
    for num_vertices in vertice_count:
        print(f'--Vertices: {num_vertices}')
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

            # Solve using Randomized algorithm
            randomized_cover, num_operations_randomized, execution_time_randomized, num_solutions_tested_randomized = randomized_fpt_attempts(generated_graph, k) #100000

            # Generate the normal graph
            #generate_all(generated_graph,generated_graph.nodes(), f'Normal/K_{percentage_k*100}/V({num_vertices})/G({num_vertices},{edges_weight*100}%)')

            # Generate the Randomized graph
            #generate_all(generated_graph, randomized_cover, f'randomized/K_{percentage_k*100}/V({num_vertices})/G({num_vertices},{edges_weight*100}%)')


            is_vertex_cover_randomized = is_vertex_cover(generated_graph, randomized_cover)

            # Append the randomized data to the list
            data_randomized.append([
                num_vertices,
                edges_weight * 100,
                num_edges_dict[edges_weight],
                percentage_k * 100,
                k,
                randomized_cover,
                is_vertex_cover_randomized,
                num_operations_randomized,
                num_solutions_tested_randomized,
                execution_time_randomized
            ])
        
            
            # Append the randomized data to the chart data
            chart_data['randomized']['num_vertices'].append(num_vertices)
            chart_data['randomized']['edge_percentage'].append(edges_weight * 100)
            chart_data['randomized']['num_operations'].append(num_operations_randomized)
            chart_data['randomized']['num_solutions_tested'].append(num_solutions_tested_randomized)
            chart_data['randomized']['time'].append(execution_time_randomized)
            
    return data_randomized, chart_data

if __name__ == '__main__':
    
    if not os.path.exists('img'):
        os.makedirs('img')
    if not os.path.exists('dump'):
        os.makedirs('dump')

    for it in range(1,11,1):
        print(f'Iteration: {it}')
        start_time = time.time()
        for k_percentage in [0.125, 0.25, 0.5, 0.75]:
            print(f'K: {k_percentage*100}%')
            data_randomized, chart_data = program(k_percentage)

            writeTo_xlsx(k_percentage,data_randomized, chart_data,it)
            writeTo_csv(k_percentage,data_randomized, chart_data, it)

        print('Generating charts...')
        charts_main(it)
        print('Done Iteration' + str(it) + ' in ' + str(time.time() - start_time) + ' seconds')
        print('----------------------------------------')


