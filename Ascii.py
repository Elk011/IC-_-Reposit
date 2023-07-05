import numpy as np
import ast
import re
import csv

with open('/content/Antenna 70 GHz.txt', 'r') as file:
    linhas = file.readlines()

stop = float(input('Qual a Frequência máxima simulada ? :'))

plots = []
c_plot = []
parametros = {}
c_parametros = {}

for line in linhas:
    line = line.strip()

    if line.startswith('#Parameters'):
        if c_plot:
            plots.append(c_plot)
            parametros[len(plots)-1] = c_parametros
            c_plot = []
            c_parametros = {}
        try:
            param_string = re.search(r'{(.*?)}', line).group(1)
            param_list = param_string.split('; ')
            c_parametros = dict(param.split('=') for param in param_list)
        except (AttributeError, ValueError):
            continue

    elif line and not line.startswith('#'):
        frequency, value = map(float, line.split("\t"))
        if frequency <= stop:
            c_plot.append((frequency, value))

if c_parametros: # Verifica o último Plot
    plots.append(c_plot)
    parametros[len(plots)-1] = c_parameters

for i, plot in enumerate(plots):
    frequencies, values = zip(*plot)
    params = parametros[i]
    params_str = ', '.join([f"{key}={value}" for key, value in params.items()])
    plt.plot(frequencies, values)
            #  ,label=f"Plot {i+1} ({params_str})")

plt.xlabel("Frequencia GHz")
plt.ylabel("Perda de Retorno dB")
plt.legend()
plt.show()
print("Número de gráficos:", len(plots))

for i, params in parametros.items():
    print(f"Parâmetros do gráfico {i+1}:")
    for key, value in params.items():
        print(f"{key} = {value}")

filename = "graph_data.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Plot']+list(parametros[0].keys()) + ['Pico', 'BW'])  # Write the header row
    for i, plot in enumerate(plots):
        x, y = zip(*plot)
        BW_novo = 0
        menor_x = 0
        maior_x = 0
        largura = []
        ganho = []


        for j in range(len(y)):
            if y[j] < -10:
                largura.append(x[j])
                ganho.append(y[j])
            elif y[j] >= -10 and len(largura) > 0:
                # marker.append(j);
                intervalo_GHz = largura
                perda_retorno = ganho
                novamenor_F = np.min(intervalo_GHz)
                novamaior_F = np.max(intervalo_GHz)
                BW = novamaior_F - novamenor_F

                if BW > BW_novo:
                  BW_novo = BW
                  intervalo = intervalo_GHz
                  Pico = np.min(perda_retorno)
                  Frequencia = intervalo[np.argmin(perda_retorno)]
                  menor_F = novamenor_F
                  maior_F = novamaior_F

                largura = []
                ganho = []

        if menor_F is None or maior_F is None:
            print(f"Não há valores de frequência menores que -10 para o Plot {i+1}.")
        else:
            print(f"Plot {i+1}:")
            print("O intervalo de valores da Largura de Banda:", intervalo)
            print("O menor valor da frequência dentro desse intervalo é:", menor_F)
            print("O maior valor da frequência dentro desse intervalo é:", maior_F)
            print("A Largura de banda será:", BW_novo)
            print("O pico de ressonância é:", Pico)
            print("A F correspondente a esse ponto é:", Frequencia)

        print()  # Linha em branco
        params = parametros[i]
        writer.writerow([i+1] + list(params.values()) + [Pico, BW_novo]) # Plot + parâmetros + y()

print("Dataset Novo:", filename)


