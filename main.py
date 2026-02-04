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

top_col1, top_col2 = st.columns([9, 1])

with top_col1:
    st.title("Analisador Completo de Funções")

with top_col2:
    st.write("")   # espaçamento
    tema_escuro = st.toggle("🌙")

# Lógica de Cores e Temas
if tema_escuro:
    plotly_tema = "plotly_dark"
    css_bg = "#0e1117"
    css_sidebar = "#262730"
    css_text = "#FAFAFA"
    grid_color = "#444444" # Grade mais escura para não ofuscar
else:
    plotly_tema = "plotly_white"
    css_bg = "#FFFFFF"
    css_sidebar = "#f0f2f6"
    css_text = "#31333F"
    grid_color = "#e5e5e5"

# Aplicação do CSS Dinâmico
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {css_bg};
        color: {css_text};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {css_sidebar};
    }}
    /* Força a cor do texto padrão inputs e markdown */
    p, h1, h2, h3, li {{
        color: {css_text} !important;
    }}
    </style>
""", unsafe_allow_html=True)

x = symbols('x')

# ===== LAYOUT EM DUAS COLUNAS =====
col_esq, divisor, col_dir = st.columns([1.2, 0.05, 1])

with divisor:
    # A linha divisória precisa ter cor adaptável ou neutra
    border_color = "#555" if tema_escuro else "#999"
    st.markdown(
        f"""
        <div style="
            border-left: 2px solid {border_color};
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

        # Controle de detalhes via checkbox
        modo_simples = st.checkbox("Exibir apenas a função (sem detalhes)")

        # Intervalo padrão
        if tendencia in [S.Infinity, -S.Infinity]:
            x_min, x_max = -100, 100
        else:
            x_min, x_max = -10, 10

        # Geração dos pontos do gráfico
        x_vals = np.linspace(x_min, x_max, 2000)
        y_vals = []

        for val in x_vals:
            try:
                y = float(expr.subs(x, val))

                # Evita explosão de escala por assíntotas
                if abs(y) > 1e3:
                    y_vals.append(np.nan)
                else:
                    y_vals.append(y)

            except:
                y_vals.append(np.nan)

        fig = go.Figure()

        # Traço principal da função
        # Ajustamos a cor da linha principal para contrastar bem em ambos (azul padrão funciona)
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name='f(x)',
            line=dict(width=3, color='#3388ff') # Azul um pouco mais vibrante
        ))

        # Se estiver em modo detalhe, marca o ponto analisado
        if not modo_simples and tendencia not in [S.Infinity, -S.Infinity]:
            try:
                y_tend = float(expr.subs(x, tendencia))

                fig.add_trace(go.Scatter(
                    x=[tendencia],
                    y=[y_tend],
                    mode='markers',
                    name='Ponto analisado',
                    marker=dict(size=10, color='red')
                ))
            except:
                pass

        # Ajuste inteligente do eixo Y
        y_validos = [v for v in y_vals if not np.isnan(v)]

        if y_validos:
            y_range = max(abs(min(y_validos)), abs(max(y_validos)))
            y_lim = min(y_range * 1.2, 20)
        else:
            y_lim = 10

        # AQUI É ONDE O TEMA É APLICADO AO GRÁFICO
        fig.update_layout(
            template=plotly_tema, # Usa a variável definida no início
            height=520,
            margin=dict(l=40, r=40, t=40, b=40),
            title="Visualização da Função e Assíntotas",
            xaxis=dict(
                title="x",
                range=[x_min, x_max],
                zeroline=True,
                zerolinewidth=2,
                showgrid=True,
                gridcolor=grid_color # Usa a cor da grade variável
            ),
            yaxis=dict(
                title="f(x)",
                range=[-y_lim, y_lim],
                zeroline=True,
                zerolinewidth=2,
                showgrid=True,
                gridcolor=grid_color # Usa a cor da grade variável
            ),
            hovermode="x unified",
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=1.02,
                # bgcolor removido para usar o padrão do tema (transparente ou adaptado)
                bordercolor=css_text, # Borda segue a cor do texto
                borderwidth=1
            )
        )

    # ===== PARTE DIREITA: ANÁLISE =====
    with col_dir:

        if not modo_simples:
            # Verticais
            st.write("### Assíntotas Verticais")

            try:
                d = denom(expr)
                verticais = solve(d, x)

                if verticais:
                    for v in verticais:
                        st.write(f"x = {v}")
                        fig.add_trace(go.Scatter(
                            x=[float(v), float(v)],
                            y=[-y_lim, y_lim],
                            mode="lines",
                            name=f"Assíntota vertical x={v}",
                            line=dict(color="crimson", width=2, dash="dashdot")
                        ))
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
                    fig.add_trace(go.Scatter(
                        x=[x_min, x_max],
                        y=[float(lim_inf), float(lim_inf)],
                        mode="lines",
                        name=f"Assíntota horizontal y={lim_inf}",
                        line=dict(color="#00cc66", width=2, dash="dash") # Verde mais claro para dark mode
                    ))

                if lim_minf.is_real and lim_minf != lim_inf:
                    st.write(f"y = {lim_minf}  (x → -∞)")
                    fig.add_trace(go.Scatter(
                        x=[x_min, x_max],
                        y=[float(lim_inf), float(lim_inf)],
                        mode="lines",
                        name=f"Assíntota horizontal y={lim_inf}",
                        line=dict(color="#00cc66", width=2, dash="dash")
                    ))

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
                        line=dict(dash='dash', color='magenta'), # Magenta é visível em ambos
                        name=f"Assíntota: y={a}x+{b}"
                    ))
                else:
                    st.write("Nenhuma assíntota oblíqua detectada.")

            except:
                st.write("Nenhuma assíntota oblíqua detectada.")

        else:
            st.info("Modo simples ativado: detalhes gráficos desativados.")

    # Exibir gráfico apenas depois de adicionar tudo
    with col_esq:
        # ===== REPRESENTAÇÃO VISUAL DO LIMITE =====
        try:
            if not modo_simples and tendencia not in [S.Infinity, -S.Infinity]:
                if tendencia not in [S.Infinity, -S.Infinity]:
                    lim_val = limit(expr, x, tendencia)

                    if lim_val.is_real:
                        lim_float = float(lim_val)

                        # Linha horizontal mostrando o valor do limite
                        fig.add_trace(go.Scatter(
                            x=[x_min, x_max],
                            y=[lim_float, lim_float],
                            mode="lines",
                            name=f"Valor do limite: {lim_val}",
                            line=dict(color="orange", width=3)
                        ))

                        # Linha vertical no ponto de tendência
                        fig.add_trace(go.Scatter(
                            x=[float(tendencia), float(tendencia)],
                            y=[-y_lim, y_lim],
                            mode="lines",
                            name=f"x → {tendencia}",
                            line=dict(color="orange", width=2, dash="dot")
                        ))

                        # Ponto indicativo do limite
                        fig.add_trace(go.Scatter(
                            x=[float(tendencia)],
                            y=[lim_float],
                            mode='markers',
                            name='Valor do Limite',
                            marker=dict(size=12, color='orange', symbol='diamond')
                        ))

        except:
            pass

        st.plotly_chart(fig, use_container_width=True)

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