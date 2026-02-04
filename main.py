import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import (
    symbols, sympify, limit, S, solve, denom, numer,
    Poly, degree, solveset, Interval, latex
)

st.set_page_config(page_title="Analisador Completo de Funções", layout="wide")

st.title("Analisador Completo de Funções")

x = symbols('x')

# ===== LAYOUT EM DUAS COLUNAS =====
col_esq, divisor,col_dir = st.columns([1.2, 0.05, 1])

with divisor:
    st.markdown(
        """
        <div style="
            border-left: 2px solid #999;
            height: 100vh;
            margin-left: 50%;
        "></div>
        """,
        unsafe_allow_html=True
    )

with col_esq:

    st.write("Digite a função em termos de x (ex: (4 - x**2)/(2 + x))")

    expr_input = st.text_input("Função f(x):", "(4 - x**2)/(2 + x)")

    tendencias = list(range(-100, 101))
    tendencias = [-S.Infinity] + tendencias + [S.Infinity]

    tendencia = st.select_slider(
        "x tende a:",
        options=tendencias,
        value=-2
    )

try:
    expr = sympify(expr_input)

    with col_esq:

        try:
            expr_latex = latex(expr).replace("I", "i")
            st.latex(f"f(x) = {expr_latex}")
        except:
            st.write("Não foi possível converter a função para LaTeX.")

        st.subheader("Gráfico da Função")

        x_vals = np.linspace(-100, 100, 3000)
        y_vals = []

        for val in x_vals:
            try:
                y_vals.append(float(expr.subs(x, val)))
            except:
                y_vals.append(np.nan)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name='f(x)'
        ))

    # ===== PARTE DIREITA: ANÁLISE =====
    with col_dir:

        st.subheader("Assíntotas Detectadas")

        # Verticais
        st.write("### Assíntotas Verticais")
        try:
            d = denom(expr)
            verticais = solve(d, x)

            if verticais:
                for v in verticais:
                    st.write(f"x = {v}")
                    fig.add_vline(
                        x=float(v),
                        line=dict(color="red", dash="dash"),
                        annotation_text=f"x={v}"
                    )
            else:
                st.write("Nenhuma assíntota vertical detectada.")
        except:
            st.write("Erro ao calcular assíntotas verticais.")

        # Horizontais
        st.write("### Assíntotas Horizontais")
        try:
            lim_inf = limit(expr, x, S.Infinity)
            lim_minf = limit(expr, x, -S.Infinity)

            if lim_inf.is_real:
                st.write(f"y = {lim_inf}  (x → ∞)")
                fig.add_hline(
                    y=float(lim_inf),
                    line=dict(color="green", dash="dot"),
                    annotation_text=f"y={lim_inf}"
                )

            if lim_minf.is_real and lim_minf != lim_inf:
                st.write(f"y = {lim_minf}  (x → -∞)")
                fig.add_hline(
                    y=float(lim_minf),
                    line=dict(color="green", dash="dot"),
                    annotation_text=f"y={lim_minf}"
                )

            if not lim_inf.is_real and not lim_minf.is_real:
                st.write("Nenhuma assíntota horizontal detectada.")

        except:
            st.write("Erro ao calcular assíntotas horizontais.")

        # Oblíquas
        st.write("### Assíntotas Oblíquas")
        try:
            num = numer(expr)
            den = denom(expr)

            grau_num = degree(Poly(num, x))
            grau_den = degree(Poly(den, x))

            if grau_num == grau_den + 1:
                a = limit(expr / x, x, S.Infinity)
                b = limit(expr - a*x, x, S.Infinity)

                st.write(f"y = {a}x + {b}")

                y_obl = [float(a * v + b) for v in x_vals]

                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_obl,
                    mode='lines',
                    line=dict(dash='dash', color='purple'),
                    name=f"Assíntota: y={a}x+{b}"
                ))
            else:
                st.write("Nenhuma assíntota oblíqua detectada.")
        except:
            st.write("Erro ao calcular assíntotas oblíquas.")

    # Exibir gráfico apenas depois de adicionar tudo
    with col_esq:
        st.plotly_chart(fig)

    # ===== LIMITES =====
    with col_dir:

        st.subheader("Análise do Limite")

        try:
            if tendencia == S.Infinity:
                resultado = limit(expr, x, S.Infinity)
                ponto = "∞"
            elif tendencia == -S.Infinity:
                resultado = limit(expr, x, -S.Infinity)
                ponto = "-∞"
            else:
                resultado = limit(expr, x, tendencia)
                ponto = str(tendencia)

            st.write(f"Limite quando x → {ponto}")

            substituicao = expr.subs(x, tendencia)

            if substituicao in [S.NaN, S.ComplexInfinity]:
                st.error("Indeterminação detectada!")
            else:
                st.success(f"Resultado do limite: {resultado}")

        except:
            st.error("Não foi possível calcular o limite dessa expressão.")

        # ===== INEQUAÇÕES =====
        st.subheader("Análise de Inequações")

        def formatar_solucao(sol):
            texto = str(sol)
            texto = texto.replace("Interval.open", "")
            texto = texto.replace("Union", "União de intervalos:")
            texto = texto.replace("oo", "∞")
            return texto

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Resolver f(x) > 0"):
                try:
                    sol = solveset(expr > 0, x, domain=S.Reals)
                    st.write(formatar_solucao(sol))
                except:
                    st.error("Não foi possível resolver essa inequação.")

        with col2:
            if st.button("Resolver f(x) < 0"):
                try:
                    sol = solveset(expr < 0, x, domain=S.Reals)
                    st.write(formatar_solucao(sol))
                except:
                    st.error("Não foi possível resolver essa inequação.")

        st.write("### Raízes da Função")

        try:
            zeros = solve(expr, x)

            reais = []
            complexas = []

            for z in zeros:
                if z.is_real:
                    reais.append(z)
                else:
                    complexas.append(z)

            if reais:
                st.write("**Raízes reais:**")
                for r in reais:
                    st.latex(f"x = {latex(r)}")
            else:
                st.warning("A função não possui raízes reais.")

            if complexas:
                st.write("**Raízes complexas:**")
                for c in complexas:
                    expr_latex = latex(c).replace("I", "i")
                    st.latex(f"x = {expr_latex}")

        except:
            st.write("Não foi possível determinar as raízes.")

except Exception as e:
    st.error("Erro ao interpretar a função. Verifique a sintaxe.")
