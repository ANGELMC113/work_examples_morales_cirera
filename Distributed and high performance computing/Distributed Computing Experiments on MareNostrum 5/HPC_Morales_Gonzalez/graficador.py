# graficador.py
"""Calcula las métricas y genera los gráficos del estudio."""

import pandas as pd
import glob
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


# Definiciones generales

INPUT_DIR_0 = "./Importado_Mare_Nostrum/csv/csv0/" # Directorio de las ejecuciones con 1 nodo

INPUT_DIR_1 = "./Importado_Mare_Nostrum/csv/csv1/"  # Directorio de la primera repetición
INPUT_DIR_2 = "./Importado_Mare_Nostrum/csv/csv2/"  # Directorio de la segunda repetición


""" Métricas calculadas:

- Métricas de repeticiones (2 por script): 1 lista de 6 valores por repetición y script, con 1 valor por configuración

    - Calculadas a partir del máximo entre todos los nodos de una repetición:
        - Tiempo (de ejecución de una repetición de un script)
        - Speedup
        - Eficiencia

    - Calculadas a partir de la suma de todos los nodos:
        - Energía (consumida por cada configuración)
        - Coste (de cada configuración)

        
- Métricas de scripts: 1 lista de 6 valores por script, con 1 valor por configuración

    - Calculadas a partir de la media (entre las 2 repeticiones) del máximo (entre todos los nodos):
        - Tiempo (medio de ejecición de un script)
        - Speedup
        - Eficiencia

    - Calculadas a partir de la media entre todos los nodos y repeticiones (N * 2):
        - Potencia media
        - Potencia media relativa
        - CPI
        - Memory bandwith

        
- Métricas únicas:

    - Energía y coste medios entre las 2 configuraciones de cada script (9 y 9 valores)
    - Energía y coste medios de 1 repetición del experimento (1 y 1 valores)
    - Energía y coste total de las 2 repeticiones (1 y 1 valores)

"""

# Configuraciones

CONFIG_NAMES = [
    "448×1 (caso MPI)", 
    "224×2", 
    "56×8", 
    "32×14", 
    "8×56", 
    "4×112 (caso OpenMP)"
]

KERNEL_NAMES = ['bt-mz', 'lu-mz', 'sp-mz']

# Diccionarios auxiliares para títulos y unidades

metric_titles = {
    'tiempo': 'Tiempo de ejecución',
    'speedup': 'Speedup',
    'efficiency': 'Eficiencia',
    'energia': 'Energía consumida',
    'potencia': 'Potencia media relativa',
    'bandwidth': 'Ancho de banda de memoria promedio'
}

metric_units = {
    'tiempo': 'Tiempo (s)',
    'speedup': 'Speedup',
    'efficiency': 'Efficiency', 
    'energia': 'Energía (kWh)',
    'potencia': 'Potencia relativa',
    'bandwidth': 'GB/s'
}


# Gráficas

def create_kernel_plots(metrics_to_plot):
    """Crea un gráfico por kernel y métrica con 3 líneas (4/6/8 nodos)."""
    
    node_styles = {
        4: {'color': '#1f77b4', 'marker': 'o', 'linestyle': '-', 'label': '4 nodos'},
        6: {'color': '#ff7f0e', 'marker': 's', 'linestyle': '--', 'label': '6 nodos'},
        8: {'color': '#2ca02c', 'marker': '^', 'linestyle': ':', 'label': '8 nodos'}
    }
    
    for metric_name, data in metrics_to_plot.items():
        # Crear una figura por kernel
        for k in range(3):
            plt.figure(figsize=(10, 6))
            
            # Dibujar las 3 líneas (nodos 4, 6, 8)
            for n in range(3):
                num_nodes = 2*n + 4
                values = data[(k, n)]
                style = node_styles[num_nodes]
                
                plt.plot(CONFIG_NAMES, values,
                        marker=style['marker'],
                        linestyle=style['linestyle'],
                        color=style['color'],
                        linewidth=2,
                        markersize=8,
                        label=style['label'])
                
                # Etiquetas de valores
                for i, val in enumerate(values):
                    plt.text(i, val + (max(values)*0.02), f'{val:.2f}',
                            ha='center',
                            va='bottom',
                            fontsize=9,
                            color=style['color'])
            
            # Personalización del gráfico
            plt.title(f"{metric_titles[metric_name]} - {KERNEL_NAMES[k]}", fontsize=14)
            plt.xlabel('Configuración MPI/OpenMP', fontsize=12)
            plt.ylabel(metric_units[metric_name], fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, linestyle='--', alpha=0.3)
            plt.legend(fontsize=10)
            
            # Ajustar márgenes y guardar
            plt.tight_layout()
            plt.savefig(f"{metric_name}_{KERNEL_NAMES[k]}.png", dpi=300)
            plt.close()


def main():
    """Ejecuta la lectura de los csv y crea los gráficos."""

    csv_matrix: list[list[list[list[pd.DataFrame | None]]]] = [[[[]
                for _ in range(2)]          # 2 repeticiones
            for _ in range(3)]          # 3 kernels
        for _ in range(3)]          # 4, 6 u 8 nodos (N = 2*i+4)
    """ Matriz de archivos .csv.
    Organizados según número de nodos n, kernel k, repetición r y nodo i.
    Mide 3 x 3 x 2 x N (N puede ser 4, 6 u 8).
    Por ejemplo, csv_matrix[0][2][1][3] contiene los datos
        del nodo 3 de la segunda repetición del kernel sp-mz con 4 nodos.
        (El número de nodo no se corresponde con el real, es irrelevante.)
    """


    # Lectura y organización de los csv

    # Ejecuciones en 1 nodo y cálculo de los tiempos concurrentes

    times_1: dict[str, list[float]] = {"bt-mz" : [], "lu-mz" : [], "sp-mz" : []}
    """times[kernel] es la lista de los 3 tiempos concurrentes (de las 3 repeticiones) de ese kernel."""

    files0 = [
        
        glob.glob(f"{INPUT_DIR_0}ej1/*time.csv"),
        glob.glob(f"{INPUT_DIR_0}ej2/*time.csv"),
        glob.glob(f"{INPUT_DIR_0}ej3/*time.csv"),
    ]

    for files in files0:
        for file in files:
            df = pd.read_csv(file, sep=';')
            kernel = (df['JOBNAME'].to_string(index= False))
            time = float(df['TIME_SEC'].iloc[0])
            times_1[kernel].append(time)

    T_1 = [((1/3) * sum(times_1[kernel])) for kernel in times_1.keys()]
    """T_1[k] es el tiempo concurrente del kernel k."""

    print("Tiempos en 1 nodo:", T_1)


    # Ejecuciones en 4, 6 y 8 nodos

    files = [
        glob.glob(f"{INPUT_DIR_1}*time.csv"),
        glob.glob(f"{INPUT_DIR_2}*time.csv")
    ]

    for r in range(2):          # Para cada repetición
        for file in files[r]:       # Leemos todos los csv
            df = pd.read_csv(file, sep=';')
            kernel = file[34:36]
            num_nodes = int(file[38])

            match num_nodes:
                case 4:
                    n = 0
                case 6:
                    n = 1
                case 8:
                    n = 2
                case _:
                    raise ImportError

            match kernel:
                case "bt":
                    k = 0
                case "lu":
                    k = 1
                case "sp":
                    k = 2
                case _:
                    raise ImportError

            csv_matrix[n][k][r].append(df)


    # Cálculo de métricas derivadas

    metrics_to_plot = {
        'tiempo': {},
        'speedup': {},
        'efficiency': {},
        'energia': {},
        'potencia': {},
        'bandwidth': {}
    }

    enery_table: list[list[float]] = [[0 for _ in range(3)] for _ in range(3)]
    """energy_table[k][n] is the average (betweeen both repetitions) energy consumed by kernel k with n nodes."""

    for k in range(3):      # Para cada kernel  
        
        for n in range(3):      # Para cada número de nodos        
            num_nodes = 2*n+4

            max_times: list[list[int]] = [None, None]
            """max_times[r][c] is the maximum time for configuration c at repetition r, in s."""

            sum_energies: list[list[float]] = [None, None]
            """sum_energies[r][c] is the sum of the energies consumed by configuration c at repetition r, in KWh."""

            powers: list[list[list[float]]] = [None, None]
            """powers[r][i][c] is the average power of node i for configuration c at repetition r, in W."""
        
            for r in range(2):          # Para cada repetición

                times: list[list[float]] = [list(csv_matrix[n][k][r][i]['TIME_SEC']) for i in range(num_nodes)]
                """times[i][c] is the time taken by node i for configuration c, in s."""

                times_by_config: list[list[float]] = [[times[i][c] for i in range(num_nodes)] for c in range(6)]
                """times_by_config[c] is the list of times of all nodes for configuration c."""

                max_times[r] = [max(times_by_config[c]) for c in range(6)]


                powers[r] = [list(csv_matrix[n][k][r][i]['DC_NODE_POWER_W']) for i in range(num_nodes)]

                energies: list[list[float]] = [[times[i][c] * powers[r][i][c] / (60*60*1000) for c in range(6)] for i in range(num_nodes)]
                """energies[i][c] is the energy consumed by node i for configuration c, in KWh."""

                sum_energies[r] = [sum(energies[i][c] for i in range(num_nodes)) for c in range(6)]


            mean_max_times: list[float] = [0.5 * (max_times[0][c] + max_times[1][c]) for c in range(6)]
            """mean_max_times[c] is the mean maximum time for configuration c."""

            mean_speedup: list[float] = [T_1[k] / mean_max_times[c] for c in range(6)]
            """mean_speedup[c] is the mean speedup for configuration c."""

            mean_efficiency: list[float] = [mean_speedup[c] / (num_nodes) for c in range(6)]
            """mean_efficiency[c] is the mean efficiency for configuration c."""

            mean_sum_energies: list[float] = [0.5 * (sum_energies[0][c] + sum_energies[1][c]) for c in range(6)]
            """mean_sum_energies[c] is the mean sum of energies for configuration c."""

            enery_table[k][n] = sum(mean_sum_energies)

            mean_rel_power: list[float] = [(1/700) * (1/(2*num_nodes)) * sum(powers[r][i][c] for r in range(2) for i in range(num_nodes)) for c in range(6)]
            """mean_rel_power[c] is the mean power of configuration c between all nodes and repetitions, normalized wrt 700 W."""

            mean_cpi: list[float] = [1/(2*num_nodes) * sum([list(csv_matrix[n][k][r][i]["CPI"])[c] for i in range(num_nodes) for r in range(2)]) for c in range(6)]
            """mean_cpi[c] is the mean cpi of configuration c between all nodes and repetitions."""

            mean_mem_bw: list[float] = [1/(2*num_nodes) * sum([list(csv_matrix[n][k][r][i]["MEM_GBS"])[c] for i in range(num_nodes) for r in range(2)]) for c in range(6)]
            """mean_mem_bw[c] is the mean memory bandwith of configuration c between all nodes and repetitions."""


            metrics_to_plot['tiempo'][(k, n)] = mean_max_times
            metrics_to_plot['speedup'][(k, n)] = mean_speedup
            metrics_to_plot['efficiency'][(k, n)] = mean_efficiency
            metrics_to_plot['energia'][(k, n)] = mean_sum_energies
            metrics_to_plot['potencia'][(k, n)] = mean_rel_power
            # El CPI siempre es 1.
            metrics_to_plot['bandwidth'][(k, n)] = mean_mem_bw


    enery_sums = [sum(enery_table[k][n] for n in range(3)) for k in range(3)]
    """energy_sums[k] is the sum of the energies consumed by kernel k."""

    energy_repe = sum(enery_sums)
    energy_total = energy_repe * 2

    cost_table = [[enery_table[k][n] * 0.2 for n in range(3)] for k in range(3)]
    cost_sums = [enery_sums[k] * 0.2 for k in range(3)]

    cost_repe = energy_repe * 0.2
    cost_total = energy_total * 0.2

    print("Energy table:", enery_table)
    print("Energy sums:", enery_sums)
    print("Totals:", energy_repe, energy_total)

    print("Cost table:", cost_table)
    print("Cost sums:", cost_sums)
    print("Totals:", cost_repe, cost_total)

    # Creación final de los gráficos
    create_kernel_plots(metrics_to_plot)



if __name__ == "__main__":
    main()