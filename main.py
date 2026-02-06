# ==========================================
# 1. IMPORTAÇÃO DE BIBLIOTECAS
# ==========================================

# Streamlit: A biblioteca que cria a interface web (botões, caixas de texto, layout).
import streamlit as st

# Numpy: Biblioteca poderosa para lidar com arrays numéricos e cálculos matemáticos rápidos.
import numpy as np

# Plotly: Biblioteca para criar gráficos interativos (onde você pode dar zoom, passar o mouse, etc).
import plotly.graph_objects as go

# Sympy: Biblioteca de matemática simbólica. Ela resolve equações, limites e derivadas
# da mesma forma que um humano faria no papel (algebricamente), e não apenas aproximando números.
from sympy import (
    symbols, sympify, limit, S, solve, denom, numer,
    Poly, degree, solveset, Interval, latex
)

# Ferramentas do Sympy para ler o texto que o usuário digita e transformar em matemática
from sympy.parsing.sympy_parser import (
    parse_expr,
    implicit_multiplication_application,  # Permite escrever '2x' em vez de '2*x'
    convert_xor,  # Permite usar '^' para potência (opcional, mas o python usa **)
    standard_transformations
)

# Define 'x' como um símbolo matemático globalmente.
# Isso avisa ao Python que 'x' não é uma variável com um valor fixo (como x=10),
# mas sim uma incógnita algébrica.
x = symbols('x')


# ==========================================
# 2. CONFIGURAÇÃO VISUAL (CSS E TEMAS)
# ==========================================

def obter_configuracao_tema(tema_escuro):
    """
    Retorna um dicionário (uma lista de configurações) com cores
    baseadas na escolha do usuário (Claro ou Escuro).
    """
    if tema_escuro:
        # Configurações para modo escuro
        return {
            "plotly_tema": "plotly_dark",  # Tema pronto do gráfico
            "css_bg": "#0e1117",  # Cor de fundo da página
            "css_sidebar": "#262730",  # Cor da barra lateral
            "css_text": "#FAFAFA",  # Cor do texto
            "grid_color": "#444444",  # Cor da grade do gráfico
            "zeroline_color": "#777777",  # Cor da linha zero (eixos)
            "plot_bg_color": "#0e1117",  # Fundo do gráfico
            "btn_bg": "#2b313e",  # Fundo do botão
            "btn_color": "#ffffff",  # Texto do botão
            "btn_border": "#4a4e57",  # Borda do botão
            "btn_hover": "#3a4150",  # Cor do botão ao passar o mouse
            "toggle_bg": "#2b313e",  # Fundo do interruptor (toggle)
            "toggle_text": "#ffffff",  # Texto do interruptor
            "border_color": "#555"  # Cor da linha divisória
        }
    else:
        # Configurações para modo claro
        return {
            "plotly_tema": "plotly_white",
            "css_bg": "#FFFFFF",
            "css_sidebar": "#f8f9fa",
            "css_text": "#31333F",
            "grid_color": "#d1d1d1",
            "zeroline_color": "#000000",
            "plot_bg_color": "#ffffff",
            "btn_bg": "#4b7bec",
            "btn_color": "#ffffff",
            "btn_border": "#4b7bec",
            "btn_hover": "#3867d6",
            "toggle_bg": "#1f2937",
            "toggle_text": "#ffffff",
            "border_color": "#ccc"
        }


def aplicar_css(theme):
    """
    Injeta código CSS (estilo de web) diretamente na página para
    personalizar cores que o Streamlit padrão não alcança facilmente.
    """
    # st.markdown com unsafe_allow_html=True permite escrever HTML/CSS puro.
    st.markdown(f"""
        <style>
        /* Define cor de fundo e texto principal */
        .stApp {{ background-color: {theme['css_bg']}; color: {theme['css_text']}; }}

        /* Define cor da barra lateral */
        section[data-testid="stSidebar"] {{ background-color: {theme['css_sidebar']}; }}

        /* Força a cor do texto em parágrafos e títulos */
        p, h1, h2, h3, li, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p {{
            color: {theme['css_text']} !important;
        }}

        /* Estiliza os botões */
        div.stButton > button {{
            background-color: {theme['btn_bg']}; color: {theme['btn_color']};
            border: 1px solid {theme['btn_border']}; border-radius: 8px;
            font-weight: 600; transition: all 0.3s ease;
        }}
        /* Efeito ao passar o mouse no botão */
        div.stButton > button:hover {{
            background-color: {theme['btn_hover']}; color: {theme['btn_color']};
            border-color: {theme['btn_hover']};
        }}
        /* Efeito ao clicar no botão */
        div.stButton > button:active {{ transform: scale(0.98); }}

        /* Estiliza o toggle (interruptor de tema) */
        div[data-testid="stToggle"] label {{
            background-color: {theme['toggle_bg']} !important; border-radius: 8px; padding: 4px 8px;
        }}
        div[data-testid="stToggle"] label p {{
            font-size: 20px !important; font-weight: bold; color: {theme['toggle_text']} !important;
        }}
        div[data-testid="stToggle"] {{ color: {theme['toggle_text']} !important; }}
        </style>
    """, unsafe_allow_html=True)


def renderizar_layout_colunas(border_color):
    """
    Divide a tela em duas colunas principais com uma linha divisória no meio.
    Retorna os objetos das colunas (esquerda e direita) para usarmos depois.
    """
    # Cria 3 colunas: Esquerda (larga), Divisor (fina), Direita (larga)
    col_esq, divisor, col_dir = st.columns([1.2, 0.05, 1])

    # Desenha uma linha vertical na coluna do meio usando HTML
    with divisor:
        st.markdown(
            f"""
            <div style="
                border-left: 2px solid {border_color};
                height: 100vh; /* Ocupa 100% da altura da visão */
                margin-left: 50%;
            "></div>
            """,
            unsafe_allow_html=True
        )
    return col_esq, col_dir


# ==========================================
# 3. ENTRADA DE DADOS E CÁLCULO
# ==========================================

def obter_inputs(coluna):
    """Coleta a função matemática e o valor de tendência que o usuário quer analisar."""
    with coluna:
        st.write("Digite a função em termos de x (ex: (4 - x**2)/(2 + x))")

        # Caixa de texto para o usuário digitar a função
        expr_input = st.text_input("Função f(x):", "(4 - x**2)/(2 + x)")

        # Cria uma lista de números de -100 a 100 e adiciona Infinito negativo e positivo
        tendencias = list(range(-100, 101))
        tendencias = [-S.Infinity] + tendencias + [S.Infinity]

        # Slider (barra de arrastar) para escolher para onde o x tende
        tendencia = st.select_slider(
            "x tende a:",
            options=tendencias,
            value=-2
        )
    return expr_input, tendencia


def interpretar_expressao(expr_input):
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
        local_dict={'x': x}  # Diz que 'x' no texto refere-se ao símbolo 'x'
    )


def calcular_dados_grafico(expr, tendencia):
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
            y = float(expr.subs(x, val))

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


# ==========================================
# 4. CRIAÇÃO DOS GRÁFICOS
# ==========================================

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


def criar_figura_base(x_vals, y_vals, tendencia, expr, modo_simples):
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
            y_tend = float(expr.subs(x, tendencia))
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


def adicionar_visualizacao_limite(fig, expr, tendencia, x_min, x_max, y_lim, modo_simples):
    """Desenha as linhas pontilhadas laranjas que mostram o limite visualmente."""
    if not modo_simples and tendencia not in [S.Infinity, -S.Infinity]:
        try:
            # Calcula o limite exato usando Sympy
            lim_val = limit(expr, x, tendencia)

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


# ==========================================
# 5. ANÁLISE MATEMÁTICA (ASSÍNTOTAS)
# ==========================================

def analisar_assintotas_verticais(expr, fig, y_lim):
    """Procura onde o denominador é zero (divisão por zero) para achar assíntotas verticais."""
    st.write("### Assíntotas Verticais")
    try:
        d = denom(expr)  # Pega o denominador da função
        verticais = solve(d, x)  # Resolve denominador = 0
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


def analisar_assintotas_horizontais(expr, fig, x_min, x_max):
    """Calcula o limite no infinito para ver se a função se estabiliza horizontalmente."""
    st.write("### Assíntotas Horizontais")
    try:
        lim_inf = limit(expr, x, S.Infinity)  # Limite em +infinito
        lim_minf = limit(expr, x, -S.Infinity)  # Limite em -infinito

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


def analisar_assintotas_obliquas(expr, fig, x_vals):
    """
    Verifica se existe assíntota inclinada (oblíqua).
    Fórmula: y = ax + b, onde a = lim f(x)/x e b = lim (f(x) - ax)
    """
    st.write("### Assíntotas Oblíquas")
    try:
        a = limit(expr / x, x, S.Infinity)
        b = limit(expr - a * x, x, S.Infinity)

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


# ==========================================
# 6. CÁLCULO DE LIMITES E RAÍZES
# ==========================================

def calcular_e_exibir_limite(expr, tendencia):
    """Exibe o resultado numérico/simbólico do limite."""
    st.subheader("Análise do Limite")
    try:
        # Define o texto visual para o ponto (Infinito usa símbolo ∞)
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

        # Tenta substituir direto para ver se dá erro (indeterminação 0/0)
        substituicao = expr.subs(x, tendencia)

        if substituicao in [S.NaN, S.ComplexInfinity]:
            st.error("Indeterminação detectada!")
        else:
            st.success(f"Resultado do limite: {resultado}")
    except:
        st.error("Não foi possível calcular o limite dessa expressão.")


def formatar_solucao_inequacao(sol):
    """Formata a resposta matemática de conjuntos (ex: [0, 5]) para texto legível."""
    if sol is S.EmptySet:
        return "Não há solução nos reais."

    partes = []
    # Verifica se a solução é composta de vários pedaços (união)
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


def analisar_inequacoes(expr):
    """Botões para resolver f(x) > 0 e f(x) < 0."""
    st.subheader("Análise de Inequações")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Resolver f(x) > 0"):
            try:
                # solveset resolve desigualdades
                sol = solveset(expr > 0, x, domain=S.Reals)
                st.write(formatar_solucao_inequacao(sol))
            except:
                st.error("Não foi possível resolver essa inequação.")

    with col2:
        if st.button("Resolver f(x) < 0"):
            try:
                sol = solveset(expr < 0, x, domain=S.Reals)
                st.write(formatar_solucao_inequacao(sol))
            except:
                st.error("Não foi possível resolver essa inequação.")


def calcular_raizes(expr):
    """Encontra onde a função cruza o eixo X (f(x) = 0)."""
    st.write("### Raízes da Função")
    try:
        zeros = solve(expr, x)  # Resolve a equação f(x) = 0
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


# ==========================================
# 7. FUNÇÃO PRINCIPAL (MAIN)
# ==========================================

def main():
    """
    Função principal que organiza a execução de todo o programa.
    O Python começa a ler as definições acima, mas a execução real começa aqui.
    """

    # 1. Configura a página (título da aba do navegador e layout wide/largo)
    st.set_page_config(page_title="Analisador Completo de Funções", layout="wide")

    # 2. Cabeçalho e Botão de Tema
    top_col1, top_col2 = st.columns([9, 1])
    with top_col1:
        st.title("Analisador Completo de Funções")
    with top_col2:
        st.write("")
        st.write("")
        # Cria um switch visual (retorna True ou False)
        tema_escuro = st.toggle("🌙", value=True)

    # 3. Aplica o tema escolhido
    theme = obter_configuracao_tema(tema_escuro)
    aplicar_css(theme)

    # 4. Renderiza as colunas principais
    col_esq, col_dir = renderizar_layout_colunas(theme['border_color'])

    # 5. Obtém a entrada do usuário
    expr_input, tendencia = obter_inputs(col_esq)

    # Bloco principal de processamento (dentro de try/except para capturar erros de digitação)
    try:
        # Transforma texto em matemática
        expr = interpretar_expressao(expr_input)

        # Calcula pontos do gráfico
        x_vals, y_vals, x_min, x_max, y_lim = calcular_dados_grafico(expr, tendencia)

        # Inicia estrutura do gráfico na coluna esquerda
        modo_simples = inicializar_grafico(expr, col_esq)
        fig = criar_figura_base(x_vals, y_vals, tendencia, expr, modo_simples)

        # Preenche a Coluna Direita com análises matemáticas
        with col_dir:
            # Se não for modo simples, calcula e desenha as assíntotas no gráfico
            if not modo_simples:
                analisar_assintotas_verticais(expr, fig, y_lim)
                analisar_assintotas_horizontais(expr, fig, x_min, x_max)
                analisar_assintotas_obliquas(expr, fig, x_vals)
            else:
                st.info("Modo simples ativado: detalhes gráficos desativados.")

            # Exibe cálculos numéricos
            calcular_e_exibir_limite(expr, tendencia)
            analisar_inequacoes(expr)
            calcular_raizes(expr)

        # Volta para a Coluna Esquerda para exibir o gráfico finalizado
        with col_esq:
            configurar_layout_grafico(fig, theme, x_min, x_max, y_lim)
            adicionar_visualizacao_limite(fig, expr, tendencia, x_min, x_max, y_lim, modo_simples)
            # Renderiza o gráfico interativo na tela
            st.plotly_chart(fig, use_container_width=True, theme=None)

    except Exception as e:
        # Se algo der errado (ex: usuário digitou "xx" errado), mostra o erro
        st.error(f"Erro ao interpretar a função. Verifique a sintaxe. {e}")


# Verifica se este arquivo está sendo executado diretamente (padrão do Python)
if __name__ == "__main__":
    main()