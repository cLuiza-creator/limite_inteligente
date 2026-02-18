import streamlit as st


# Sympy: Biblioteca de matemática simbólica. Ela resolve equações, limites e derivadas
# da mesma forma que um humano faria no papel (algebricamente), e não apenas aproximando números.
from sympy import (
    symbols, sympify, limit, S, solve, denom, numer,
    Poly, degree, solveset, Interval, latex
)

from utils.normalizadores import formatar_solucao_inequacao


# ==========================================
# 6. CÁLCULO DE LIMITES E RAÍZES
# ==========================================

def calcular_e_exibir_limite(variavel1, expr, tendencia):
    """Exibe o resultado numérico/simbólico do limite."""
    st.subheader("Análise do Limite")
    try:
        # Define o texto visual para o ponto (Infinito usa símbolo ∞)
        if tendencia == S.Infinity:
            resultado = limit(expr, variavel1, S.Infinity)
            ponto = "∞"
        elif tendencia == -S.Infinity:
            resultado = limit(expr, variavel1, -S.Infinity)
            ponto = "-∞"
        else:
            resultado = limit(expr, variavel1, tendencia)
            ponto = str(tendencia)

        st.write(f"Limite quando x → {ponto}")

        # Tenta substituir direto para ver se dá erro (indeterminação 0/0)
        substituicao = expr.subs(variavel1, tendencia)

        if substituicao in [S.NaN, S.ComplexInfinity]:
            st.error("Indeterminação detectada!")
        else:
            st.success(f"Resultado do limite: {resultado}")
    except:
        st.error("Não foi possível calcular o limite dessa expressão.")


def analisar_inequacoes(variavel1, expr):
    """Botões para resolver f(x) > 0 e f(x) < 0."""
    st.subheader("Análise de Inequações")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Resolver f(x) > 0"):
            try:
                # solveset resolve desigualdades
                sol = solveset(expr > 0, variavel1, domain=S.Reals)
                st.write(formatar_solucao_inequacao(sol))
            except:
                st.error("Não foi possível resolver essa inequação.")

    with col2:
        if st.button("Resolver f(x) < 0"):
            try:
                sol = solveset(expr < 0, variavel1, domain=S.Reals)
                st.write(formatar_solucao_inequacao(sol))
            except:
                st.error("Não foi possível resolver essa inequação.")


def calcular_raizes(variavel1,expr):
    """Encontra onde a função cruza o eixo X (f(x) = 0)."""
    st.write("### Raízes da Função")
    try:
        zeros = solve(expr, variavel1)  # Resolve a equação f(x) = 0
        reais = []
        complexas = []

        # Separa raízes reais de complexas
        for z in zeros:
            if z.is_real:
                reais.append(z)
            else:
                complexas.append(z)

        if reais:
            st.success("A função possui raízes reais:")
            for r in reais:
                st.latex(f"x = {latex(r)}")

        if complexas:
            if not reais:
                st.info("A função não possui raízes reais, apenas complexas.")
            st.write("**Raízes complexas:**")
            for c in complexas:
                expr_latex = latex(c).replace("I", "i")
                st.latex(f"x = {expr_latex}")

        if not reais and not complexas:
            st.warning("Não foram encontradas raízes para essa função.")
    except:
        st.error("Não foi possível determinar as raízes da função.")



