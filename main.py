import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import (
    symbols, sympify, limit, S, solve, denom, numer,
    Poly, degree, solveset, Interval, latex
)

from sympy.parsing.sympy_parser import (
    parse_expr,
    implicit_multiplication_application,
    convert_xor,
    standard_transformations
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
    entrada = expr_input.strip().lower()
    entrada = entrada.replace("sen", "sin")
    entrada = entrada.replace("raiz", "sqrt")

    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor
    )

    expr = parse_expr(
        entrada,
        transformations=transformations,
        local_dict={'x': x}
    )

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
            a = limit(expr / x, x, S.Infinity)
            b = limit(expr - a * x, x, S.Infinity)

            if a.is_real and b.is_real and a != 0:
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
            st.write("Nenhuma assíntota oblíqua detectada.")

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
            if sol is S.EmptySet:
                return "Não há solução nos reais."

            partes = []

            # Se for união de intervalos
            if hasattr(sol, "args"):
                intervalos = sol.args
            else:
                intervalos = [sol]

            for intervalo in intervalos:
                a, b = intervalo.start, intervalo.end

                esq = "(" if intervalo.left_open else "["
                dir = ")" if intervalo.right_open else "]"

                a_txt = "-∞" if a is S.NegativeInfinity else str(a)
                b_txt = "∞" if b is S.Infinity else str(b)

                partes.append(f"{esq}{a_txt}, {b_txt}{dir}")

            if len(partes) == 1:
                return partes[0]
            else:
                return " ∪ ".join(partes)

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


except Exception as e:
    st.error(f"Erro ao interpretar a função. Verifique a sintaxe.{e}")
