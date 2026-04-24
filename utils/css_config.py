import background
import streamlit as st
import os
import base64


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
            "border_color": "#555",
            "hr_color": "#444444",   # Um cinza escuro elegante para o modo noturno#

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

            "btn_bg": "#3b82f6",  # Um azul mais claro e vibrante para não sumir no cabeçalho!
            "btn_color": "#ffffff",  # Texto branco
            "btn_border": "#3b82f6",
            "btn_hover": "#2563eb",  # Azul mais forte ao passar o mouse
            "hr_color": "#1a1a8b",


            "toggle_bg": "#1f2937",
            "toggle_text": "#ffffff",
            "border_color": "#ccc",
            "hr_color": "#1a1a8b",
        }


def aplicar_css(theme):
    """
    Injeta código CSS com Fontes Customizadas do Google Fonts.
    """
    st.markdown(f"""
        <style>
        /* 1. IMPORTAÇÃO DA FONTE (Google Fonts) */
        @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap');

        /* 2. APLICAÇÃO DA FONTE EM TUDO */
        html, body, [class*="css"]  {{
            font-family: 'Lora', serif !important;
        }}

        /* Define cor de fundo e texto principal */
        .stApp {{ 
            background-color: {theme['css_bg']}; 
            color: {theme['css_text']}; 
        }}

        /* Define cor da barra lateral */
        section[data-testid="stSidebar"] {{ 
            background-color: {theme['css_sidebar']}; 
        }}

        /* Força a cor do texto e a fonte em parágrafos e títulos */
        p, h1, h2, h3, li, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p {{
            color: {theme['css_text']} !important;
            font-family: 'Lora', serif !important;
        }}

        /* Nova regra para pintar a linha horizontal (st.markdown("---")) */
        hr {{
            border: none;
            border-top: 2px solid {theme['hr_color']} !important;
            margin-top: 10px;
            margin-bottom: 20px;
        }}

        /* ---------------------------------------------------
           ESTILIZAÇÃO DE TODOS OS BOTÕES (Navegação e Download)
           --------------------------------------------------- */
        div.stButton > button, 
        div[data-testid="stDownloadButton"] button {{
            background-color: {theme['btn_bg']} !important; 
            border: 1px solid {theme['btn_border']} !important; 
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }}

        /* A MÁGICA AQUI: Força a cor do texto DENTRO dos botões */
        div.stButton > button p,
        div.stButton > button span,
        div[data-testid="stDownloadButton"] button p,
        div[data-testid="stDownloadButton"] button span {{
            color: {theme['btn_color']} !important;
            font-family: 'Lora', serif !important;
            font-weight: 600 !important; 
        }}

        /* Efeito ao passar o mouse */
        div.stButton > button:hover, 
        div[data-testid="stDownloadButton"] button:hover {{
            background-color: {theme['btn_hover']} !important; 
            border-color: {theme['btn_hover']} !important;
        }}

        /* Efeito ao clicar no botão */
        div.stButton > button:active,
        div[data-testid="stDownloadButton"] button:active {{ 
            transform: scale(0.98) !important; 
        }}

        /* Estiliza o toggle (interruptor de tema) */
        div[data-testid="stToggle"] label {{
            background-color: {theme['toggle_bg']} !important; 
            border-radius: 8px; 
            padding: 4px 8px;
        }}
        div[data-testid="stToggle"] label p {{
            font-size: 20px !important; 
            font-weight: bold; 
            color: {theme['toggle_text']} !important;
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



#mudando o visual


def renderizar_header():
    # 1. Carrega o logo
    diretorio_utils = os.path.dirname(os.path.abspath(__file__))
    arquivos = os.listdir(diretorio_utils)
    nome_real_do_arquivo = next((f for f in arquivos if f.lower().startswith('logo_branco_novo')), None)

    caminho_logo = None
    if nome_real_do_arquivo:
        caminho_logo = os.path.join(diretorio_utils, nome_real_do_arquivo)
    else:
        st.error(f"Não achei o logo na pasta: {diretorio_utils}")
        return

    st.markdown("""
            <style>
            /* Procura EXATAMENTE a linha de colunas que contém o ID #ancora-cabecalho */
            div[data-testid="stHorizontalBlock"]:has(#ancora-cabecalho) {
                background-color: #1a1a8b; /* Azul marinho do logo */
                padding: 15px 30px;        /* Espaço interno */
                border-radius: 10px;       /* Bordas arredondadas */
                align-items: center;       /* Alinha os botões com o meio do logo */
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

    # 2. Criação do layout com colunas
    col_logo, espaco, col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([3, 0.5, 1, 1, 1, 1])
    with col_logo:
        # Colocamos a âncora invisível aqui para o CSS identificar este bloco!
        st.markdown('<div id="ancora-cabecalho"></div>', unsafe_allow_html=True)
        # Exibe a imagem
        st.image(caminho_logo, width=200)

    # 3. Criação dos botões verdadeiros e lógica de clique
    with col_btn1:
        if st.button("Gráficos", use_container_width=True):
            st.session_state['pagina_atual'] = "Gráficos"

    with col_btn2:
        if st.button("Derivada", use_container_width=True):
            st.session_state['pagina_atual'] = "Derivada"

    with col_btn3:
        if st.button("Integral", use_container_width=True):
            st.session_state['pagina_atual'] = "Integral"
    with col_btn4:
        if st.button("Listas", use_container_width=True):
            st.session_state['pagina_atual'] = "Listas"

    st.markdown("---")  # Linha divisória

