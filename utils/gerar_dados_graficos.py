

import numpy as np
# Sympy: Biblioteca de matemática simbólica. Ela resolve equações, limites e derivadas
# da mesma forma que um humano faria no papel (algebricamente), e não apenas aproximando números.
from sympy import (
    symbols, sympify, limit, S, solve, denom, numer,
    Poly, degree, solveset, Interval, latex
)


def calcular_dados_grafico(variavel1,expr, tendencia):
    """
    Gera os pontos X e Y numéricos para desenhar o gráfico.
    O Sympy faz a matemática exata, o Numpy gera os pontos para o desenho.
    """
    # Se o gráfico for analisar infinito, mostramos um range maior (-100 a 100)
    # Se for um número local, focamos mais perto (-10 a 10)
    if tendencia in [S.Infinity, -S.Infinity]:
        x_min, x_max = -100, 100
    else:
        x_min, x_max = -10, 10

    # Cria 2000 pontos entre o mínimo e o máximo para a linha ficar suave
    x_vals = np.linspace(x_min, x_max, 2000)
    y_vals = []

    # Calcula o valor de Y para cada ponto X
    for val in x_vals:
        try:
            # Substitui x pelo valor numérico na expressão
            y = float(expr.subs(variavel1, val))

            # Se o valor for muito grande (assíntota), define como NaN (Not a Number)
            # Isso faz o gráfico "quebrar" a linha em vez de desenhar um risco vertical feio
            if abs(y) > 1e3:
                y_vals.append(np.nan)
            else:
                y_vals.append(y)
        except:
            # Se der erro matemático (ex: raiz de negativo), salva como NaN
            y_vals.append(np.nan)

    # Lógica para definir o tamanho automático do eixo Y (zoom vertical)
    y_validos = [v for v in y_vals if not np.isnan(v)]
    if y_validos:
        y_range = max(abs(min(y_validos)), abs(max(y_validos)))
        # Limita o zoom para não ficar gigante, máximo de 20 ou 1.2x o valor
        y_lim = min(y_range * 1.2, 20)
    else:
        y_lim = 10

    return x_vals, y_vals, x_min, x_max, y_lim

