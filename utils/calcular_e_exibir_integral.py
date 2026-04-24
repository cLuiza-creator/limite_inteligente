import streamlit as st
import sympy as sp


def calcular_e_exibir_integral(variavel, expr):
    # Removi o título extra e o separador para não brigar com o título da main.py

    try:
        # 1. Calcula o resultado real direto
        resultado = sp.integrate(expr, variavel)
        resultado_latex = sp.latex(resultado)

        # 2. Exibe o resultado principal
        st.write("O resultado da integral indefinida é:")
        st.latex(rf"{resultado_latex} + C")

        # 3. Passo a Passo (O Expander)
        with st.expander("Ver detalhes do cálculo"):
            st.write("Aplicando as regras de integração para funções elementares:")

            # Aqui sim mostramos a integral completa bonitona!
            st.latex(rf"\int {sp.latex(expr)} \, dx = {resultado_latex} + C")

            st.info(
                "Nota: Para funções polinomiais, trigonométricas e raízes, utilizamos as tabelas fundamentais de integração.")

    except Exception as e:
        st.error(f"Não foi possível calcular a integral: {e}")