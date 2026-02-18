# ==========================================
# 1. IMPORTAÇÃO DE BIBLIOTECAS
# ==========================================

# Streamlit: A biblioteca que cria a interface web (botões, caixas de texto, layout).
import streamlit as st

# Sympy: Biblioteca de matemática simbólica. Ela resolve equações, limites e derivadas
# da mesma forma que um humano faria no papel (algebricamente), e não apenas aproximando números.
from sympy import (
    symbols, S
)

from utils.calculos import calcular_e_exibir_limite, analisar_inequacoes, calcular_raizes
from utils.css_config import obter_configuracao_tema, aplicar_css, renderizar_layout_colunas
from utils.gerar_dados_graficos import calcular_dados_grafico
from utils.gerar_graficos import criar_figura_base, configurar_layout_grafico, adicionar_visualizacao_limite, \
    inicializar_grafico, analisar_assintotas_verticais, analisar_assintotas_horizontais, analisar_assintotas_obliquas
from utils.normalizadores import interpretar_expressao


# ==========================================
# 1. ENTRADA DE DADOS E CÁLCULO <3
# ==========================================

def obter_inputs(coluna):
    """Coleta a função matemática e o valor de tendência que o usuário quer analisar."""
    with coluna:
        st.write("Digite a função em termos de x")
        st.write("(Ex: (4 - x^2)/(2 + x))")

        # Caixa de texto para o usuário digitar a função
        expr_input = st.text_input("Função f(x):", "(4 - x^2)/(2 + x)")

        # Cria uma lista de números de -100 a 100 e adiciona Infinito negativo e positivo
        tendencias = list(range(-100, 101))
        tendencias = [-S.Infinity] + tendencias + [S.Infinity]

        # Slider (barra de arrastar) para escolher para onde o x tende
        tendencia = st.select_slider(
            "x tende a:",
            options=tendencias,
            value=0
        )
    return expr_input, tendencia

# ==========================================
# 2. FUNÇÃO PRINCIPAL (MAIN) <3
# ==========================================

def main():
    """
    Função principal que organiza a execução de todo o programa.
    O Python começa a ler as definições acima, mas a execução real começa aqui.
    """

    # Define 'x' como um símbolo matemático globalmente.
    # Isso avisa ao Python que 'x' não é uma variável com um valor fixo (como x=10),
    # mas sim uma incógnita algébrica.
    variavel1 = symbols('x')

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
        expr = interpretar_expressao(variavel1,expr_input)

        # Calcula pontos do gráfico
        x_vals, y_vals, x_min, x_max, y_lim = calcular_dados_grafico(variavel1,expr, tendencia)

        # Inicia estrutura do gráfico na coluna esquerda
        modo_simples = inicializar_grafico(expr, col_esq)
        fig = criar_figura_base(variavel1, x_vals, y_vals, tendencia, expr, modo_simples)

        # Preenche a Coluna Direita com análises matemáticas
        with col_dir:
            # Se não for modo simples, calcula e desenha as assíntotas no gráfico
            if not modo_simples:
                analisar_assintotas_verticais(variavel1, expr, fig, y_lim)
                analisar_assintotas_horizontais(variavel1, expr, fig, x_min, x_max)
                analisar_assintotas_obliquas(variavel1, expr, fig, x_vals)
            else:
                st.info("Modo simples ativado: detalhes gráficos desativados.")

            # Exibe cálculos numéricos
            calcular_e_exibir_limite(variavel1, expr, tendencia)
            analisar_inequacoes(expr)
            calcular_raizes(expr)

        # Volta para a Coluna Esquerda para exibir o gráfico finalizado
        with col_esq:
            configurar_layout_grafico(fig, theme, x_min, x_max, y_lim)
            adicionar_visualizacao_limite(variavel1, fig, expr, tendencia, x_min, x_max, y_lim, modo_simples)
            # Renderiza o gráfico interativo na tela
            st.plotly_chart(fig, use_container_width=True, theme=None)

    except Exception as e:
        # Se algo der errado (ex: usuário digitou "xx" errado), mostra o erro
        st.error(f"Erro ao interpretar a função. Verifique a sintaxe. {e}")


# Verifica se este arquivo está sendo executado diretamente (padrão do Python)
if __name__ == "__main__":
    main()