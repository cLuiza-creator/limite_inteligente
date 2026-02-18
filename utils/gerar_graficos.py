import streamlit as st

# Plotly: Biblioteca para criar gráficos interativos (onde pode dar zoom, passar o mouse, etc).
import plotly.graph_objects as go

# Sympy: Biblioteca de matemática simbólica. Ela resolve equações, limites e derivadas
# da mesma forma que um humano faria no papel (algebricamente), e não apenas aproximando números.
from sympy import (
    symbols, sympify, limit, S, solve, denom, numer,
    Poly, degree, solveset, Interval, latex
)

# ==========================================
# 4. CRIAÇÃO DOS GRÁFICOS
# ==========================================

def criar_figura_base(variavel1,x_vals, y_vals, tendencia, expr, modo_simples):
    """Cria o objeto do gráfico (Figure) e desenha a linha azul da função."""
    fig = go.Figure()

    # Adiciona a linha principal da função (azul)
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals, mode='lines', name='f(x)',
        line=dict(width=3, color='#3388ff')
    ))

    # Se não estiver no modo simples, desenha uma bolinha vermelha no ponto escolhido
    if not modo_simples and tendencia not in [S.Infinity, -S.Infinity]:
        try:
            y_tend = float(expr.subs(variavel1, tendencia))
            fig.add_trace(go.Scatter(
                x=[tendencia], y=[y_tend], mode='markers', name='Ponto analisado',
                marker=dict(size=10, color='red')
            ))
        except:
            pass  # Se o ponto não existir, apenas ignora

    return fig


def configurar_layout_grafico(fig, theme, x_min, x_max, y_lim):
    """Aplica o estilo final, títulos, cores de fundo e limites dos eixos no gráfico."""
    fig.update_layout(
        template=theme['plotly_tema'],
        height=520,  # Altura do gráfico em pixels
        margin=dict(l=40, r=40, t=40, b=40),
        title="Visualização da Função e Assíntotas",
        paper_bgcolor=theme['plot_bg_color'],  # Cor fora do gráfico
        plot_bgcolor=theme['plot_bg_color'],  # Cor dentro do gráfico
        font=dict(color=theme['css_text']),
        xaxis=dict(
            title="x", range=[x_min, x_max],
            zeroline=True, zerolinewidth=2, zerolinecolor=theme['zeroline_color'],
            showgrid=True, gridcolor=theme['grid_color']
        ),
        yaxis=dict(
            title="f(x)", range=[-y_lim, y_lim],
            zeroline=True, zerolinewidth=2, zerolinecolor=theme['zeroline_color'],
            showgrid=True, gridcolor=theme['grid_color']
        ),
        hovermode="x unified",  # Mostra tooltip unificado ao passar mouse
        legend=dict(
            orientation="v", yanchor="top", y=0.98, xanchor="left", x=1.02,
            bordercolor=theme['css_text'], borderwidth=1, font=dict(color=theme['css_text'])
        )
    )


def adicionar_visualizacao_limite(variavel1, fig, expr, tendencia, x_min, x_max, y_lim, modo_simples):
    """Desenha as linhas pontilhadas laranjas que mostram o limite visualmente."""
    if not modo_simples and tendencia not in [S.Infinity, -S.Infinity]:
        try:
            # Calcula o limite exato usando Sympy
            lim_val = limit(expr, variavel1, tendencia)

            # Só desenha se o limite for um número real (não infinito ou complexo)
            if lim_val.is_real:
                lim_float = float(lim_val)
                # Linha horizontal laranja
                fig.add_trace(go.Scatter(
                    x=[x_min, x_max], y=[lim_float, lim_float], mode="lines",
                    name=f"Valor do limite: {lim_val}", line=dict(color="orange", width=3)
                ))
                # Linha vertical pontilhada
                fig.add_trace(go.Scatter(
                    x=[float(tendencia), float(tendencia)], y=[-y_lim, y_lim], mode="lines",
                    name=f"x → {tendencia}", line=dict(color="orange", width=2, dash="dot")
                ))
                # Ponto diamante laranja no encontro das linhas
                fig.add_trace(go.Scatter(
                    x=[float(tendencia)], y=[lim_float], mode='markers',
                    name='Valor do Limite', marker=dict(size=12, color='orange', symbol='diamond')
                ))
        except:
            pass

def inicializar_grafico(expr, col_esq):
    """Mostra a função escrita bonitinha (LaTeX) e opções de visualização."""
    with col_esq:
        try:
            # Converte a função para formato LaTeX (matemática bonita)
            expr_latex = latex(expr).replace("I", "i")
            st.latex(f"f(x) = {expr_latex}")
        except:
            st.write("Não foi possível converter a função para LaTeX.")

        st.subheader("Gráfico da Função")
        # Checkbox para o usuário limpar o gráfico se quiser
        modo_simples = st.checkbox("Exibir apenas a função (sem detalhes)")

    return modo_simples

# ==========================================
# 5. ANÁLISE MATEMÁTICA (ASSÍNTOTAS)
# ==========================================


def analisar_assintotas_verticais(variavel1,expr, fig, y_lim):
    """Procura onde o denominador é zero (divisão por zero) para achar assíntotas verticais."""
    st.write("### Assíntotas Verticais")
    try:
        d = denom(expr)  # Pega o denominador da função
        verticais = solve(d, variavel1)  # Resolve denominador = 0
        if verticais:
            for v in verticais:
                st.write(f"x = {v}")
                # Adiciona linha vertical vermelha no gráfico
                fig.add_trace(go.Scatter(
                    x=[float(v), float(v)], y=[-y_lim, y_lim], mode="lines",
                    name=f"Assíntota vertical x={v}", line=dict(color="crimson", width=2, dash="dashdot")
                ))
        else:
            st.write("Nenhuma assíntota vertical detectada.")
    except:
        st.write("Erro ao calcular assíntotas verticais.")



def analisar_assintotas_horizontais(variavel1,expr, fig, x_min, x_max):
    """Calcula o limite no infinito para ver se a função se estabiliza horizontalmente."""
    st.write("### Assíntotas Horizontais")
    try:
        lim_inf = limit(expr, variavel1, S.Infinity)  # Limite em +infinito
        lim_minf = limit(expr, variavel1, -S.Infinity)  # Limite em -infinito

        found = False
        # Se limite em +infinito for um número real
        if lim_inf.is_real:
            st.write(f"y = {lim_inf}  (x → ∞)")
            # Linha verde horizontal
            fig.add_trace(go.Scatter(
                x=[x_min, x_max], y=[float(lim_inf), float(lim_inf)], mode="lines",
                name=f"Assíntota horizontal y={lim_inf}", line=dict(color="#00cc66", width=2, dash="dash")
            ))
            found = True

        # Se limite em -infinito for real e diferente do anterior
        if lim_minf.is_real and lim_minf != lim_inf:
            st.write(f"y = {lim_minf}  (x → -∞)")
            fig.add_trace(go.Scatter(
                x=[x_min, x_max], y=[float(lim_minf), float(lim_minf)], mode="lines",
                name=f"Assíntota horizontal y={lim_minf}", line=dict(color="#00cc66", width=2, dash="dash")
            ))
            found = True

        if not found:
            st.write("Nenhuma assíntota horizontal detectada.")
    except:
        st.write("Erro ao calcular assíntotas horizontais.")


def analisar_assintotas_obliquas(variavel1,expr, fig, x_vals):
    """
    Verifica se existe assíntota inclinada (oblíqua).
    Fórmula: y = ax + b, onde a = lim f(x)/x e b = lim (f(x) - ax)
    """
    st.write("### Assíntotas Oblíquas")
    try:
        a = limit(expr / variavel1, variavel1, S.Infinity)
        b = limit(expr - a * variavel1, variavel1, S.Infinity)

        # Se 'a' e 'b' forem reais e 'a' não for zero (senão seria horizontal)
        if a.is_real and b.is_real and a != 0:
            st.write(f"y = {a}x + {b}")
            # Calcula os pontos Y da reta oblíqua para desenhar
            y_obl = [float(a * v + b) for v in x_vals]
            fig.add_trace(go.Scatter(
                x=x_vals, y=y_obl, mode='lines',
                line=dict(dash='dash', color='magenta'), name=f"Assíntota: y={a}x+{b}"
            ))
        else:
            st.write("Nenhuma assíntota oblíqua detectada.")
    except:
        st.write("Nenhuma assíntota oblíqua detectada.")


