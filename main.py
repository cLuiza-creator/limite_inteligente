# ==========================================
# 1. IMPORTAÇÃO DE BIBLIOTECAS
# ==========================================
import streamlit as st
from sympy import symbols, S

# SEUS IMPORTS ANTIGOS
from utils.calculos import calcular_e_exibir_limite, analisar_inequacoes, calcular_raizes
from utils.css_config import obter_configuracao_tema, aplicar_css, renderizar_layout_colunas
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
    variavel1 = symbols('x')

    st.set_page_config(page_title="Analisador Completo de Funções", layout="wide")

    top_col1, top_col2 = st.columns([9, 1])
    with top_col1:
        st.title("Analisador Completo de Funções")
    with top_col2:
        st.write("")
        st.write("")
        tema_escuro = st.toggle("🌙", value=True)

    theme = obter_configuracao_tema(tema_escuro)
    aplicar_css(theme)
    col_esq, col_dir = renderizar_layout_colunas(theme['border_color'])

    expr_input, tendencia = obter_inputs(col_esq)

    try:
        expr = interpretar_expressao(variavel1, expr_input)
        x_vals, y_vals, x_min, x_max, y_lim = calcular_dados_grafico(variavel1, expr, tendencia)

        modo_simples = inicializar_grafico(expr, col_esq)
        fig = criar_figura_base(variavel1, x_vals, y_vals, tendencia, expr, modo_simples)

        # ==========================================
        # COLUNA DIREITA (CÁLCULOS E DERIVADA)
        # ==========================================
        with col_dir:
            if not modo_simples:
                analisar_assintotas_verticais(variavel1, expr, fig, y_lim)
                analisar_assintotas_horizontais(variavel1, expr, fig, x_min, x_max)
                analisar_assintotas_obliquas(variavel1, expr, fig, x_vals)
            else:
                st.info("Modo simples ativado: detalhes gráficos desativados.")

            # >>> AQUI ESTÁ A NOVA CHAMADA DA DERIVADA <<<
            calcular_e_exibir_derivada(variavel1, expr)

            # Seus cálculos antigos continuam aqui
            st.markdown("---") # Separador visual
            calcular_e_exibir_limite(variavel1, expr, tendencia)
            analisar_inequacoes(variavel1, expr)
            calcular_raizes(variavel1, expr)

        # COLUNA ESQUERDA (GRÁFICO)
        with col_esq:
            configurar_layout_grafico(fig, theme, x_min, x_max, y_lim)
            adicionar_visualizacao_limite(variavel1, fig, expr, tendencia, x_min, x_max, y_lim, modo_simples)
            st.plotly_chart(fig, use_container_width=True, theme=None)

    except Exception as e:
        st.error(f"Erro ao interpretar a função. Verifique a sintaxe. {e}")

if __name__ == "__main__":
    main()