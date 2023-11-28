import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot data for a given performance metric
def plot_metric(metric_folder, metric_name):
    extracted_files = []
    for root, dirs, files in os.walk("..\\data\\CSV\\results"):
        for file in files:
            extracted_files.append(os.path.join(root, file))

    # Paths for exhaustive and greedy algorithm files for the given metric
    exhaustive_files = [f for f in extracted_files if f"exhaustive\\{metric_folder}\\" in f]
    greedy_files = [f for f in extracted_files if f"greedy\\{metric_folder}\\" in f]

    # Creating plots for each K value
    for k_value in ['12.5', '25.0', '50.0', '75.0']:
        exhaustive_data = pd.read_csv([f for f in exhaustive_files if f"K_{k_value}.csv" in f][0])
        greedy_data = pd.read_csv([f for f in greedy_files if f"K_{k_value}.csv" in f][0])

        plt.figure(figsize=(12, 6))
        plt.plot(exhaustive_data['num_vertices'], exhaustive_data[k_value], label='Exhaustive', color='blue')
        plt.plot(greedy_data['num_vertices'], greedy_data[k_value], label='Greedy', color='red')

        plt.title(f'{metric_name} for Exhaustive vs. Greedy Algorithms (K={k_value})')
        plt.xlabel('Number of Vertices')
        plt.ylabel(f'{metric_name} (K={k_value})')
        plt.legend()
        plt.grid(True)

        # Save the figure to a file with the title as the name
        file_name = f"..\\generated_charts\\VS\\{metric_name} for Exhaustive vs. Greedy Algorithms (K={k_value}).png"
        plt.savefig(file_name)

        # Show the plot
        #plt.show()

def plot_exhaustive(metric_folder, metric_name):
    extracted_files = []
    for root, dirs, files in os.walk("..\\data\\CSV\\results"):
        for file in files:
            extracted_files.append(os.path.join(root, file))

    # Paths for exhaustive and greedy algorithm files for the given metric
    exhaustive_files = [f for f in extracted_files if f"exhaustive\\{metric_folder}\\" in f]

    # Creating plots for each K value
    for k_value in ['12.5', '25.0', '50.0', '75.0']:
        exhaustive_data = pd.read_csv([f for f in exhaustive_files if f"K_{k_value}.csv" in f][0])

        plt.figure(figsize=(12, 6))
        for edge_value, edge_color in [('12.5','blue'), ('25.0','red'), ('50.0','green'), ('75.0','orange')]:
            plt.plot(exhaustive_data['num_vertices'], exhaustive_data[edge_value], label=f'Edge={edge_value}%', color=edge_color)

        plt.title(f'Exhaustive {metric_name} (K={k_value})')
        plt.xlabel('Number of Vertices')
        plt.ylabel(f'{metric_name} (K={k_value})')
        plt.legend()
        plt.grid(True)

        # Save the figure to a file with the title as the name
        file_name = f"..\\generated_charts\\Exhaustive\\{metric_name} (K={k_value}).png"
        plt.savefig(file_name)

        # Show the plot
        #plt.show()

def plot_greedy(metric_folder, metric_name):
    extracted_files = []
    for root, dirs, files in os.walk("..\\data\\CSV\\results"):
        for file in files:
            extracted_files.append(os.path.join(root, file))

    # Paths for exhaustive and greedy algorithm files for the given metric
    greedy_files = [f for f in extracted_files if f"greedy\\{metric_folder}\\" in f]

    # Creating plots for each K value
    for k_value in ['12.5', '25.0', '50.0', '75.0']:
        greedy_data = pd.read_csv([f for f in greedy_files if f"K_{k_value}.csv" in f][0])

        plt.figure(figsize=(12, 6))
        for edge_value, edge_color in [('12.5','blue'), ('25.0','red'), ('50.0','green'), ('75.0','orange')]:
            plt.plot(greedy_data['num_vertices'], greedy_data[edge_value], label=f'Edge={edge_value}%', color=edge_color)

        plt.title(f'Greedy {metric_name} (K={k_value})')
        plt.xlabel('Number of Vertices')
        plt.ylabel(f'{metric_name} (K={k_value})')
        plt.legend()
        plt.grid(True)

        # Save the figure to a file with the title as the name
        file_name = f"..\\generated_charts\\Greedy\\{metric_name} (K={k_value}).png"
        plt.savefig(file_name)

        # Show the plot
        #plt.show()

def plot_all(metric_folder, metric_name):
    plot_metric(metric_folder, metric_name)
    plot_exhaustive(metric_folder, metric_name)
    plot_greedy(metric_folder, metric_name)

def charts_main():
    if(not os.path.exists('..\\generated_charts')):
        os.mkdir('..\\generated_charts')
    
    if(not os.path.exists('..\\generated_charts\\VS')):
        os.mkdir('..\\generated_charts\\VS')

    if(not os.path.exists('..\\generated_charts\\Exhaustive')):
        os.mkdir('..\\generated_charts\\Exhaustive')
    
    if(not os.path.exists('..\\generated_charts\\Greedy')):
        os.mkdir('..\\generated_charts\\Greedy')

    # Plotting for the 'num_comparisons' metric
    plot_all('num_comparisons', 'Number of Comparisons')

    # Plotting for the 'num_operations' metric
    plot_all('num_operations', 'Number of Operations')

    # Plotting for the 'num_solutions_tested' metric
    plot_all('num_solutions_tested', 'Solutions Tested')

    # Plotting for the 'time' metric
    plot_all('time', 'Time Taken (ms)')

if __name__ == "__main__":
    charts_main()