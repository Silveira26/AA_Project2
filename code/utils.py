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


def writeTo_xlsx(k_percentage, data_randomized, chart_data,iteration):
    # Pre-Check
    directory = Path('../data/XLSX/It'+ str(iteration) + '/')
    directory.mkdir(parents=True, exist_ok=True)
    if not os.path.isfile('../data/XLSX/It'+ str(iteration) +'/ftp_attempts.xlsx'):
        workbook_randomized = openpyxl.Workbook()
        workbook_randomized.save('../data/XLSX/It'+ str(iteration) +'/ftp_attempts.xlsx')

    # Write DataFrame to the Excel files
    with pd.ExcelWriter('../data/XLSX/It'+ str(iteration) +'/ftp_attempts.xlsx', mode='a', engine='openpyxl') as writer_randomized:
        df_randomized = pd.DataFrame(data_randomized, columns=['num_vertices', 'edge_percentage', 'num_edges', 'k_percentage', 'k', 'vertex_cover', 'is_vertex_cover', 'num_operations', 'num_solutions_tested', 'time'])
        df_randomized.to_excel(writer_randomized, sheet_name=f'K_{k_percentage*100}', index=False)

        writeXlsx_results(k_percentage,writer_randomized,chart_data['randomized'],'num_operations')
        writeXlsx_results(k_percentage,writer_randomized,chart_data['randomized'],'num_solutions_tested')
        writeXlsx_results(k_percentage,writer_randomized,chart_data['randomized'],'time')
        

def writeXlsx_results(k_percentage,writer,chart_data,method):
    df = pd.DataFrame(chart_data)
    df_pivot = pd.pivot(df, index='num_vertices', columns='edge_percentage', values=method)
    df_pivot.reset_index(inplace=True)
    df_pivot.to_excel(writer, sheet_name=f'K_{k_percentage*100}_{method}', index=False)
        

def writeTo_csv(k_percentage,data_randomized,chart_data, iteration):
    #Pre- Check
    directory = Path('../data/CSV/complete/ftp_attempts/It'+ str(iteration) + '/')
    directory.mkdir(parents=True, exist_ok=True)

    # Create DataFrame
    df_randomized = pd.DataFrame(data_randomized, columns=['num_vertices', 'edge_percentage', 'num_edges', 'k_percentage', 'k', 'vertex_cover', 'is_vertex_cover', 'num_operations', 'num_solutions_tested', 'time'])
    
    # Write DataFrame to CSV file
    df_randomized.to_csv(f'../data/CSV/complete/ftp_attempts/It{iteration}/K_{k_percentage*100}.csv', index=False)
    
    writeTo_csv_results(k_percentage,chart_data,'num_operations',iteration)
    writeTo_csv_results(k_percentage,chart_data,'num_solutions_tested',iteration)
    writeTo_csv_results(k_percentage,chart_data,'time',iteration)

def writeTo_csv_results(k_percentage,chart_data, method, iteration):
    #Pre- Check
    directory = Path('../data/CSV/results/ftp_attempts/It'+ str(iteration) + '/'+method+'/')
    directory.mkdir(parents=True, exist_ok=True)

    # Create DataFrame
    df_randomized = pd.DataFrame(chart_data['randomized'])

    df_pivot_randomized = pd.pivot(df_randomized, index='num_vertices', columns='edge_percentage', values=method)
    df_pivot_randomized.reset_index(inplace=True)

    # Write DataFrame to CSV file
    df_pivot_randomized.to_csv(f'../data/CSV/results/ftp_attempts/It{iteration}/{method}/K_{k_percentage*100}.csv', index=False)


def is_vertex_cover(graph, cover):
    if cover is None:   #Pre check
        return False
    
    for edge in graph.edges():
        if edge[0] not in cover and edge[1] not in cover:
            return False
    return True