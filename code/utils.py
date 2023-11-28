import pickle
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import os
import pandas as pd
import openpyxl


def generate_random_graph(num_vertices, num_edges):
    return nx.gnm_random_graph(num_vertices, num_edges,seed=97981)


def generate_graph_image(graph, nodelist, filename, color='#06D6A0'):
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos=pos, with_labels=True)
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=nodelist, node_color=color)
    plt.savefig(filename)
    plt.close()


def generate_graph_pickle(graph, filename):
    pickle.dump(graph, open(filename, 'wb'))

def generate_all(graph, nodelist, filename, color='#06D6A0'):
    directory = Path('../img/' + '/'.join(filename.split('/')[:-1]) )
    directory.mkdir(parents=True, exist_ok=True)
    generate_graph_image(graph, nodelist, f'../img/{filename}.png', color)

    directory = Path('../dump/' + '/'.join(filename.split('/')[:-1]) )
    directory.mkdir(parents=True, exist_ok=True) 
    generate_graph_pickle(graph, f'../dump/{filename}.pickle')


def writeTo_xlsx(k_percentage, data_exhaustive, data_greedy, chart_data):
    # Pre-Check
    directory = Path('../data/XLSX')
    directory.mkdir(parents=True, exist_ok=True)
    if not os.path.isfile('../data/XLSX/exhaustive.xlsx'):
        workbook_exhaustive = openpyxl.Workbook()
        workbook_exhaustive.save('../data/XLSX/exhaustive.xlsx')

    # Create the greedy.xlsx file if it doesn't exist
    if not os.path.isfile('../data/XLSX/greedy.xlsx'):
        workbook_greedy = openpyxl.Workbook()
        workbook_greedy.save('../data/XLSX/greedy.xlsx')

    # Write DataFrame to the Excel files
    with pd.ExcelWriter('../data/XLSX/exhaustive.xlsx', mode='a', engine='openpyxl') as writer_exhaustive:
        df_exhaustive = pd.DataFrame(data_exhaustive, columns=['num_vertices', 'edge_percentage', 'num_edges', 'k_percentage', 'k', 'vertex_cover', 'is_vertex_cover', 'num_comparisons', 'num_operations', 'num_solutions_tested', 'time'])
        df_exhaustive.to_excel(writer_exhaustive, sheet_name=f'K_{k_percentage*100}', index=False)

        writeXlsx_results(k_percentage,writer_exhaustive,chart_data['exhaustive'],'num_comparisons')
        writeXlsx_results(k_percentage,writer_exhaustive,chart_data['exhaustive'],'num_operations')
        writeXlsx_results(k_percentage,writer_exhaustive,chart_data['exhaustive'],'num_solutions_tested')
        writeXlsx_results(k_percentage,writer_exhaustive,chart_data['exhaustive'],'time')
        

    with pd.ExcelWriter('../data/XLSX/greedy.xlsx', mode='a', engine='openpyxl') as writer_greedy:
        df_greedy = pd.DataFrame(data_greedy, columns=['num_vertices','edge_percentage', 'num_edges', 'k_percentage', 'k', 'vertex_cover', 'is_vertex_cover', 'num_comparisons', 'num_operations', 'num_solutions_tested', 'time'])
        df_greedy.to_excel(writer_greedy, sheet_name=f'K_{k_percentage*100}', index=False)

        writeXlsx_results(k_percentage,writer_greedy,chart_data['greedy'],'num_comparisons')
        writeXlsx_results(k_percentage,writer_greedy,chart_data['greedy'],'num_operations')
        writeXlsx_results(k_percentage,writer_greedy,chart_data['greedy'],'num_solutions_tested')
        writeXlsx_results(k_percentage,writer_greedy,chart_data['greedy'],'time')

def writeXlsx_results(k_percentage,writer,chart_data,method):
    df = pd.DataFrame(chart_data)
    df_pivot = pd.pivot(df, index='num_vertices', columns='edge_percentage', values=method)
    df_pivot.reset_index(inplace=True)
    df_pivot.to_excel(writer, sheet_name=f'K_{k_percentage*100}_{method}', index=False)
        

def writeTo_csv(k_percentage,data_exhaustive, data_greedy,chart_data):
    #Pre- Check
    directory = Path('../data/CSV/complete/exhaustive')
    directory.mkdir(parents=True, exist_ok=True)

    directory = Path('../data/CSV/complete/greedy')
    directory.mkdir(parents=True, exist_ok=True)

    # Create DataFrame
    df_exhaustive = pd.DataFrame(data_exhaustive, columns=['num_vertices', 'edge_percentage', 'num_edges', 'k_percentage', 'k', 'vertex_cover', 'is_vertex_cover', 'num_comparisons', 'num_operations', 'num_solutions_tested', 'time'])
    df_greedy = pd.DataFrame(data_greedy, columns=['num_vertices','edge_percentage', 'num_edges', 'k_percentage', 'k', 'vertex_cover', 'is_vertex_cover', 'num_comparisons', 'num_operations', 'num_solutions_tested', 'time'])

    # Write DataFrame to CSV file
    df_exhaustive.to_csv(f'../data/CSV/complete/exhaustive/K_{k_percentage*100}.csv', index=False)
    df_greedy.to_csv(f'../data/CSV/complete/greedy/K_{k_percentage*100}.csv', index=False)

    writeTo_csv_results(k_percentage,chart_data,'num_comparisons')
    writeTo_csv_results(k_percentage,chart_data,'num_operations')
    writeTo_csv_results(k_percentage,chart_data,'num_solutions_tested')
    writeTo_csv_results(k_percentage,chart_data,'time')

def writeTo_csv_results(k_percentage,chart_data, method):
    #Pre- Check
    directory = Path('../data/CSV/results/exhaustive/'+method+'/')
    directory.mkdir(parents=True, exist_ok=True)

    directory = Path('../data/CSV/results/greedy/'+method+'/')
    directory.mkdir(parents=True, exist_ok=True)

    # Create DataFrame
    df_exhaustive = pd.DataFrame(chart_data['exhaustive'])
    df_greedy = pd.DataFrame(chart_data['greedy'])

    df_pivot_exhaustive = pd.pivot(df_exhaustive, index='num_vertices', columns='edge_percentage', values=method)
    df_pivot_exhaustive.reset_index(inplace=True)

    df_pivot_greedy = pd.pivot(df_greedy, index='num_vertices', columns='edge_percentage', values=method)
    df_pivot_greedy.reset_index(inplace=True)

    # Write DataFrame to CSV file
    df_pivot_exhaustive.to_csv(f'../data/CSV/results/exhaustive/{method}/K_{k_percentage*100}.csv', index=False)
    df_pivot_greedy.to_csv(f'../data/CSV/results/greedy/{method}/K_{k_percentage*100}.csv', index=False)


def is_vertex_cover(graph, cover):
    if cover is None:   #Pre check
        return False
    
    for edge in graph.edges():
        if edge[0] not in cover and edge[1] not in cover:
            return False
    return True