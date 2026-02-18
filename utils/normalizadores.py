# Ferramentas do Sympy para ler o texto que o usuário digita e transformar em matemática
from sympy.parsing.sympy_parser import (
    parse_expr,
    implicit_multiplication_application,  # Permite escrever '2x' em vez de '2*x'
    convert_xor,  # Permite usar '^' para potência (opcional, mas o python usa **)
    standard_transformations
)

import streamlit as st

# Sympy: Biblioteca de matemática simbólica. Ela resolve equações, limites e derivadas
# da mesma forma que um humano faria no papel (algebricamente), e não apenas aproximando números.
from sympy import (
    symbols, sympify, limit, S, solve, denom, numer,
    Poly, degree, solveset, Interval, latex,ConditionSet, ImageSet, Union, FiniteSet
)


def interpretar_expressao(variavel1,expr_input):
    """
    Transforma o texto digitado (string) em uma expressão matemática do Sympy.
    """
    # Limpa espaços e coloca em minúsculas
    entrada = expr_input.strip().lower()

    # Substitui nomes em português para inglês (o Python entende inglês)
    entrada = entrada.replace("sen", "sin")
    entrada = entrada.replace("raiz", "sqrt")

    # Define regras de transformação (ex: entender que 2x é 2*x)
    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor
    )

    # Tenta converter o texto em expressão matemática
    return parse_expr(
        entrada,
        transformations=transformations,
        local_dict={'x': variavel1}  # Diz que 'x' no texto refere-se ao símbolo 'x'
    )


def formatar_solucao_inequacao(sol):
    """
    Formata a solução de forma robusta, aceitando intervalos simples,
    uniões e conjuntos periódicos (trigonometria).
    """
    # 1. Sem solução
    if sol is S.EmptySet:
        return "∅ (Conjunto Vazio)"

    # 2. Todos os Reais
    if sol is S.Reals:
        return "ℝ (Todos os Reais)"

    # 3. Conjuntos Condicionais (Quando o Sympy não consegue resolver totalmente)
    if isinstance(sol, ConditionSet):
        st.warning("A solução é uma condição complexa que não pôde ser simplificada.")
        return f"$${latex(sol)}$$"

    # 4. Conjuntos Periódicos (Comum em Trigonometria: ImageSet)
    if isinstance(sol, ImageSet):
        # Retorna em formato LaTeX matemático pois é impossível listar "início e fim"
        return f"Solução Periódica: $${latex(sol)}$$"

    # 5. Tentativa de formatar intervalos padrão (Interval ou Union de Intervals)
    try:
        partes = []

        # Se for uma união, pega os argumentos. Se for um só, cria lista.
        if isinstance(sol, Union):
            sub_conjuntos = sol.args
        else:
            sub_conjuntos = [sol]

        for sub in sub_conjuntos:
            # Se for um ponto isolado (FiniteSet)
            if isinstance(sub, FiniteSet):
                pontos = ", ".join([str(p) for p in sub])
                partes.append(f"{{{pontos}}}")

            # Se for um intervalo contínuo
            elif isinstance(sub, Interval):
                a, b = sub.start, sub.end

                # Formata infinito
                a_txt = "-∞" if a == -S.Infinity else str(a)
                b_txt = "∞" if b == S.Infinity else str(b)

                esq = "(" if sub.left_open else "["
                dir = ")" if sub.right_open else "]"

                partes.append(f"{esq}{a_txt}, {b_txt}{dir}")

            else:
                # Se houver algo misturado que não conhecemos, força LaTeX
                return f"$${latex(sol)}$$"

        return " ∪ ".join(partes)

    except Exception as e:
        # Fallback de segurança: se tudo der errado, mostra a matemática crua em LaTeX
        return f"$${latex(sol)}$$"

