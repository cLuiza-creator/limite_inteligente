import streamlit as st
import sympy as sp
from sympy.integrals.manualintegrate import integral_steps


def calcular_e_exibir_integral(variavel, expr):
    st.markdown("---")  # Separador para organizar a coluna
    st.markdown("### 🔍 Integral Indefinida")

    try:
        # 1. Preparar a expressão da integral (o símbolo da cobrinha)
        # Usamos sp.latex() porque você importou como 'sp'
        integral_montada = sp.latex(sp.Integral(expr, variavel))
        st.latex(rf"{integral_montada}")

        # 2. Calcular o resultado real
        resultado = sp.integrate(expr, variavel)
        resultado_latex = sp.latex(resultado)

        # 3. Exibir o resultado principal
        st.write("O resultado é:")
        st.latex(rf"{resultado_latex} + C")

        # 4. Passo a Passo (O Expander)
        with st.expander("Ver detalhes do cálculo"):
            st.write("Aplicando as regras de integração para funções elementares:")

            # Exibe a substituição ou regra direta
            # Aqui você pode adicionar mais lógica depois, mas o básico é mostrar:
            st.latex(rf"\int {sp.latex(expr)} \, dx = {resultado_latex} + C")

            st.info(
                "Nota: Para funções polinomiais, trigonométricas e raízes, utilizamos as tabelas fundamentais de integração.")

    except Exception as e:
        st.error(f"Não foi possível calcular a integral: {e}")