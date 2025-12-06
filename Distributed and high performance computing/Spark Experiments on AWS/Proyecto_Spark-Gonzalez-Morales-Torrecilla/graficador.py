# graficador.py
'''Programa para crear los gráficos con los tiempos de las ejecuciones.
Requiere hard-codear los tiempos.'''

import matplotlib.pyplot as plt


# Elapsed (wall clock) times per version (h:mm:ss or m:ss):
# Indexes correspond to x1, x2, x4, x8 and x15 sizes.

C_PYTHON1: list[str] = ['0:12.91', '0:26.15', '0:50.58', '1:37.84', '3:14.65']       # CAMBIAR SEGÚN RESULTADO
C_RDD1: list[str] = ['0:22.06', '0:30.36', '0:43.92', '1:05.51', '1:53.29']          # CAMBIAR SEGÚN RESULTADO
C_DF1: list[str] = ['0:36.11', '0:40.51', '0:45.65', '0:59.42', '1:25.65']           # CAMBIAR SEGÚN RESULTADO

C_PYTHON2: list[str] = ['0:12.84', '0:26.52', '0:50.34', '1:40.64', '3:24.32']       # CAMBIAR SEGÚN RESULTADO
C_RDD2: list[str] = ['0:24.78', '0:31.64', '0:44.81', '1:08.95', '1:58.07']          # CAMBIAR SEGÚN RESULTADO
C_DF2: list[str] = ['0:37.40', '0:40.11', '0:46.86', '1:02.80', '1:24.53']           # CAMBIAR SEGÚN RESULTADO


def clock_to_float(clocks: list[str]) -> list[float]:
    '''Convert a clock in m:ss:ds format to seconds in float format.'''
    return [60 * float(clock[0]) + float(clock[2:]) for clock in clocks]


t_python1: list[float] = clock_to_float(C_PYTHON1)
t_rdd1: list[float] = clock_to_float(C_RDD1)
t_df1: list[float] = clock_to_float(C_DF1)

t_python2: list[float] = clock_to_float(C_PYTHON2)
t_rdd2: list[float] = clock_to_float(C_RDD2)
t_df2: list[float] = clock_to_float(C_DF2)

t_python_AVG: list[float] = [0 for i in range(5)]
t_rdd_AVG: list[float] = [0 for i in range(5)]
t_df_AVG: list[float] = [0 for i in range(5)]

for i in range(5):
    t_python_AVG[i] = (t_python1[i] + t_python2[i]) / 2
    t_rdd_AVG[i] = (t_rdd1[i] + t_rdd2[i]) / 2
    t_df_AVG[i] = (t_df1[i] + t_df2[i]) / 2

print("Tiempos medios:")
print("Python:", t_python_AVG)
print("RDD:", t_rdd_AVG)
print("DF:", t_df_AVG)

fig, ax = plt.subplots()
ax.plot([1, 2, 4, 8, 16], t_python_AVG, 'o', linewidth=1, linestyle='-', label='Python')
ax.plot([1, 2, 4, 8, 16], t_rdd_AVG, 'o', linewidth=1, linestyle='-', label='RDD')
ax.plot([1, 2, 4, 8, 16], t_df_AVG, 'o', linewidth=1, linestyle='-', label='DF')
ax.set_title("Tiempos medios por versión y entrada (s)")
ax.legend()
plt.grid()
plt.show() # Se puede guardar la imagen mediante la interfaz.