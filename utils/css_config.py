import streamlit as st


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

