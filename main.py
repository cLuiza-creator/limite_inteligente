# ==========================================
# 1. IMPORTAÇÃO DE BIBLIOTECAS
# ==========================================
import streamlit as st
from sympy import symbols, S

from utils.calcular_e_exibir_integral import calcular_e_exibir_integral
# SEUS IMPORTS ANTIGOS
from utils.calculos import calcular_e_exibir_limite, analisar_inequacoes, calcular_raizes
from utils.css_config import obter_configuracao_tema, aplicar_css, renderizar_layout_colunas, renderizar_header
from utils.gerar_dados_graficos import calcular_dados_grafico
from utils.gerar_graficos import criar_figura_base, configurar_layout_grafico, adicionar_visualizacao_limite, \
    inicializar_grafico, analisar_assintotas_verticais, analisar_assintotas_horizontais, analisar_assintotas_obliquas
from utils.normalizadores import interpretar_expressao

# >>> NOVO IMPORT AQUI <<<
from utils.derivadas import calcular_e_exibir_derivada

# ==========================================
# FUNÇÕES DE ENTRADA (MANTIVE IGUAL)
# ==========================================
def obter_inputs(coluna):
    with coluna:
        st.write("Digite a função em termos de x")
        st.write("(Ex: (4 - x^2)/(2 + x))")
        expr_input = st.text_input("Função f(x):", "(4 - x^2)/(2 + x)")
        tendencias = list(range(-100, 101))
        tendencias = [-S.Infinity] + tendencias + [S.Infinity]
        tendencia = st.select_slider("x tende a:", options=tendencias, value=0)
    return expr_input, tendencia

# ==========================================
# MAIN
# ==========================================
def main():
    # 1. Configurações Iniciais
    variavel1 = symbols('x')
    st.set_page_config(page_title="Analisador Completo de Funções", layout="wide")

    # 2. Define a página inicial caso seja o primeiro acesso
    if 'pagina_atual' not in st.session_state:
        st.session_state['pagina_atual'] = "Gráficos"

    # 3. Chama o cabeçalho azul no topo (sempre visível)
    renderizar_header()

    # 4. Configurações Visuais e Tema (sempre visíveis)
    tema_escuro = st.toggle("🌙", value=True)
    theme = obter_configuracao_tema(tema_escuro)
    aplicar_css(theme)

    # ==========================================
    # 5. CONTROLE DE NAVEGAÇÃO (A MÁGICA)
    # ==========================================

    if st.session_state['pagina_atual'] == "Gráficos":
        col_esq, col_dir = renderizar_layout_colunas(theme['border_color'])
        expr_input, tendencia = obter_inputs(col_esq)

        try:
            expr = interpretar_expressao(variavel1, expr_input)
            x_vals, y_vals, x_min, x_max, y_lim = calcular_dados_grafico(variavel1, expr, tendencia)

            modo_simples = inicializar_grafico(expr, col_esq)
            fig = criar_figura_base(variavel1, x_vals, y_vals, tendencia, expr, modo_simples)

            # ==========================================
            # PREENCHENDO A COLUNA DA DIREITA (CÁLCULOS)
            # ==========================================
            with col_dir:
                # Passando os argumentos EXATAMENTE como o seu arquivo exige:
                analisar_assintotas_verticais(variavel1, expr, fig, y_lim)
                analisar_assintotas_horizontais(variavel1, expr, fig, x_min, x_max)
                analisar_assintotas_obliquas(variavel1, expr, fig, x_vals)

                calcular_e_exibir_limite(variavel1, expr, tendencia)
                adicionar_visualizacao_limite(variavel1, fig, expr, tendencia, x_min, x_max, y_lim, modo_simples)

                analisar_inequacoes(variavel1, expr)
                calcular_raizes(variavel1, expr)

            # ==========================================
            # EXIBINDO O GRÁFICO FINAL NA COLUNA ESQUERDA
            # ==========================================
            with col_esq:
                # Aplica o layout (agora com os limites dos eixos corretos)
                configurar_layout_grafico(fig, theme, x_min, x_max, y_lim)

                # Desenha o gráfico na tela
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Não foi possível processar a função: {e}")



#botão das deri

    elif st.session_state['pagina_atual'] == "Derivada":

        st.title("📈 Calculadora de Derivadas")

        st.write("Digite uma função abaixo para ver o resultado e o passo a passo da derivação.")

        # 1. Dividimos a tela: Coluna maior pro texto, menor pro LaTeX

        col_input, col_latex = st.columns([2, 1])

        with col_input:

            expr_input_derivada = st.text_input("Função f(x):", value="x**2 * sin(x)")

        # Variável para segurar a função depois de lida

        expr_deriv = None

        if expr_input_derivada:

            try:

                # Tenta ler o que o usuário digitou

                expr_deriv = interpretar_expressao(variavel1, expr_input_derivada)

                # Se leu com sucesso, exibe o LaTeX na coluna da direita!

                with col_latex:

                    st.markdown("<br>", unsafe_allow_html=True)  # Dá um espacinho para alinhar com a caixa de texto

                    # Importando o latex do sympy rapidinho caso não esteja no topo do arquivo

                    from sympy import latex

                    st.latex(rf"f(x) = {latex(expr_deriv)}")


            except Exception:

                # Se o usuário estiver digitando e a função ainda estiver "quebrada" (ex: "x + ")

                with col_latex:

                    st.markdown("<br><br>", unsafe_allow_html=True)

                    st.caption("⏳ Aguardando função válida...")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Se a função é válida, roda os cálculos!

        if expr_deriv is not None:

            try:
                calcular_e_exibir_derivada(variavel1, expr_deriv)

            except Exception as e:

                st.error("Não foi possível calcular a derivada dessa função.")



    elif st.session_state['pagina_atual'] == "Integral":

        st.title("🧮 Calculadora de Integrais")

        st.write("Digite uma função abaixo para ver o resultado e o passo a passo da integração indefinida.")

        # 1. Dividimos a tela: Coluna maior pro texto, menor pro LaTeX

        col_input, col_latex = st.columns([2, 1])

        with col_input:

            # Coloquei aquela função clássica que você testou antes como exemplo

            expr_input_integral = st.text_input("Função f(x):", value="(4 - x**2)/(x + 2)")

        # Variável para segurar a função depois de lida

        expr_int = None

        if expr_input_integral:

            try:

                # Tenta ler o que o usuário digitou usando a sua função normalizadora

                expr_int = interpretar_expressao(variavel1, expr_input_integral)

                # Se leu com sucesso, exibe o LaTeX na coluna da direita!

                with col_latex:

                    st.markdown("<br>", unsafe_allow_html=True)  # Espacinho para alinhar

                    from sympy import latex

                    st.latex(rf"f(x) = {latex(expr_int)}")


            except Exception:

                # Se o usuário estiver no meio da digitação e o código quebrar

                with col_latex:

                    st.markdown("<br><br>", unsafe_allow_html=True)

                    st.caption("⏳ Aguardando função válida...")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Se a função é válida, roda os cálculos chamando a sua função!

        if expr_int is not None:

            try:

                calcular_e_exibir_integral(variavel1, expr_int)

            except Exception as e:

                st.error("Não foi possível calcular a integral dessa função.")



if __name__ == "__main__":
        main()