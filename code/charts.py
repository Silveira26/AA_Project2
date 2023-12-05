import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_randomized(metric_folder, metric_name, iteration):
    extracted_files = []
    for root, dirs, files in os.walk("..\\data\\CSV\\results"):
        for file in files:
            extracted_files.append(os.path.join(root, file))

    randomized_files = [f for f in extracted_files if f"ftp_attempts\\It{iteration}\\{metric_folder}\\" in f]

    # Creating plots for each K value
    for k_value in ['12.5', '25.0', '50.0', '75.0']:
        randomized_data = pd.read_csv([f for f in randomized_files if f"K_{k_value}.csv" in f][0])

        plt.figure(figsize=(12, 6))
        for edge_value, edge_color in [('12.5','blue'), ('25.0','red'), ('50.0','green'), ('75.0','orange')]:
            plt.plot(randomized_data['num_vertices'], randomized_data[edge_value], label=f'Edge={edge_value}%', color=edge_color)

        plt.title(f'Iteration {iteration} Randomized {metric_name} (K={k_value})')
        plt.xlabel('Number of Vertices')
        plt.ylabel(f'{metric_name} (K={k_value})')
        plt.legend()
        plt.grid(True)

        # Save the figure to a file with the title as the name
        file_name = f"..\\generated_charts\\ftp_attempts\\It{iteration}\\{metric_name} (K={k_value}).png"
        plt.savefig(file_name)

        # Show the plot
        #plt.show()


def charts_main(iteration):
    if(not os.path.exists('..\\generated_charts')):
        os.mkdir('..\\generated_charts')

    if(not os.path.exists('..\\generated_charts\\ftp_attempts')):
        os.mkdir('..\\generated_charts\\ftp_attempts')
    
    if(not os.path.exists('..\\generated_charts\\ftp_attempts\\It'+str(iteration))):
        os.mkdir('..\\generated_charts\\ftp_attempts\\It'+str(iteration))

    # Plotting for the 'num_operations' metric
    plot_randomized('num_operations', 'Number of Operations', iteration)

    # Plotting for the 'num_solutions_tested' metric
    plot_randomized('num_solutions_tested', 'Solutions Tested', iteration)

    # Plotting for the 'time' metric
    plot_randomized('time', 'Time Taken (ms)', iteration)

if __name__ == "__main__":
    charts_main()