import streamlit as st
import sympy as sp


def calcular_e_exibir_derivada(variavel1, expressao):
    """
    Função principal que gerencia a exibição na interface Streamlit.
    """
    st.subheader("🔍 Derivada Passo a Passo")
    st.markdown("---")

    try:
        # Simplifica a expressão antes de começar para evitar passos desnecessários (ex: x + x vira 2x)
        expressao_simplificada = sp.simplify(expressao)

        resultado, passos = obter_passos_derivada(expressao_simplificada, variavel1)

        # Exibe os passos identificados
        for passo in passos:
            st.latex(passo)

        # Resultado final
        st.success("Resultado Final:")
        st.latex(
            rf"\frac{{d}}{{dx}} \left( {sp.latex(expressao_simplificada)} \right) = {sp.latex(sp.simplify(resultado))}")

    except Exception as e:
        st.error(f"Erro ao processar: {e}")
        st.latex(sp.latex(sp.diff(expressao, variavel1)))


def obter_passos_derivada(expr, x):
    """
    Núcleo lógico: Identifica a estrutura da função e aplica APENAS a regra correspondente.
    Retorna: (expressão_derivada, lista_de_latex)
    """
    passos = []

    # ---------------------------------------------------------
    # 1. CASOS TRIVIAIS (Números e x isolado)
    # ---------------------------------------------------------
    if expr.is_constant(x):
        return sp.Integer(0), []  # Não mostra passo para derivada de constante (reduz poluição visual)

    if expr == x:
        return sp.Integer(1), []  # Não mostra passo para derivada de x (reduz poluição visual)

    # ---------------------------------------------------------
    # 2. REGRA DA SOMA (Detecta + ou -)
    # ---------------------------------------------------------
    if expr.is_Add:
        passos.append(r"\text{Regra da Soma: Deriva-se cada termo separadamente.}")

        termos = expr.args
        resultado = 0
        termos_derivados_latex = []

        for termo in termos:
            deriv, sub_passos = obter_passos_derivada(termo, x)
            resultado += deriv

            # Só adiciona sub-passos se o termo for complexo (não for x ou constante)
            if not termo.is_constant(x) and termo != x:
                passos.extend(sub_passos)

            termos_derivados_latex.append(sp.latex(deriv))

        passos.append(rf"\text{{Juntando os termos: }} {' + '.join(termos_derivados_latex)}")
        return resultado, passos

    # ---------------------------------------------------------
    # 3. REGRA DA CONSTANTE E PRODUTO
    # ---------------------------------------------------------
    if expr.is_Mul:
        # Verifica se é "Número * Função" (Ex: 3x^2) -> NÃO É REGRA DO PRODUTO, é linearidade
        coeficientes = [arg for arg in expr.args if arg.is_constant(x)]
        funcoes = [arg for arg in expr.args if not arg.is_constant(x)]

        if coeficientes:
            # Junta todos os números em um só (ex: 2 * 3 * x -> 6 * x)
            constante = sp.Mul(*coeficientes)
            resto = sp.Mul(*funcoes)

            # Se sobrou apenas uma função (ex: 5 * x^2), deriva o resto e multiplica
            deriv_resto, sub_passos = obter_passos_derivada(resto, x)
            passos.extend(sub_passos)  # Mostra como derivou o x^2

            return constante * deriv_resto, passos

        # Se chegou aqui, é Função * Função (Ex: x * sen(x)) -> REGRA DO PRODUTO REAL
        else:
            u = expr.args[0]
            v = sp.Mul(*expr.args[1:])  # Trata todo o resto como 'v'

            passos.append(r"\textbf{Regra do Produto:} (u \cdot v)' = u'v + uv'")
            passos.append(rf"u = {sp.latex(u)}, \quad v = {sp.latex(v)}")

            du, passos_u = obter_passos_derivada(u, x)
            dv, passos_v = obter_passos_derivada(v, x)

            if passos_u: passos.extend(passos_u)
            if passos_v: passos.extend(passos_v)

            resultado = du * v + u * dv
            passos.append(
                rf"\text{{Aplicação: }} ({sp.latex(du)}) \cdot ({sp.latex(v)}) + ({sp.latex(u)}) \cdot ({sp.latex(dv)})")
            return resultado, passos

    # ---------------------------------------------------------
    # 4. REGRA DA POTÊNCIA E CADEIA (Ex: x^2, (x+1)^2, sqrt(x))
    # ---------------------------------------------------------
    if expr.is_Pow:
        base, expoente = expr.args

        # Caso especial: Raiz Quadrada (Exponente 1/2)
        if expoente == sp.Rational(1, 2):
            passos.append(r"\textbf{Regra da Raiz Quadrada:} \frac{d}{dx}\sqrt{u} = \frac{1}{2\sqrt{u}} \cdot u'")
            if base == x:
                return 1 / (2 * sp.sqrt(x)), passos
            else:
                dbase, sub = obter_passos_derivada(base, x)
                passos.extend(sub)
                return (1 / (2 * sp.sqrt(base))) * dbase, passos

        # Regra do Tombo Padrão
        if expoente.is_constant(x):
            novo_expoente = expoente - 1

            # Caso simples: x^n
            if base == x:
                passos.append(
                    rf"\text{{Regra do Tombo: }} \frac{{d}}{{dx}}({sp.latex(expr)}) = {sp.latex(expoente)}x^{{{sp.latex(novo_expoente)}}}")
                return expoente * x ** novo_expoente, passos

            # Caso Cadeia: (u)^n
            else:
                passos.append(r"\textbf{Regra da Cadeia (Potência):} n(u)^{n-1} \cdot u'")
                passos.append(rf"u = {sp.latex(base)}")

                dbase, sub = obter_passos_derivada(base, x)
                passos.extend(sub)

                res = expoente * (base ** novo_expoente) * dbase
                passos.append(
                    rf"\text{{Resultado: }} {sp.latex(expoente)}({sp.latex(base)})^{{{sp.latex(novo_expoente)}}} \cdot ({sp.latex(dbase)})")
                return res, passos

    # ---------------------------------------------------------
    # 5. TRIGONOMÉTRICAS (Seno, Cosseno, Tangente)
    # ---------------------------------------------------------
    if isinstance(expr, (sp.sin, sp.cos, sp.tan)):
        arg = expr.args[0]
        func_nome = type(expr).__name__

        regras = {
            'sin': (sp.cos(arg), r"\cos(u)"),
            'cos': (-sp.sin(arg), r"-\sin(u)"),
            'tan': (sp.sec(arg) ** 2, r"\sec^2(u)")
        }

        derivada_externa, nome_latex = regras[func_nome]

        # Se for sin(x) simples
        if arg == x:
            passos.append(rf"\text{{Derivada Trigonométrica: }} ({sp.latex(expr)})' = {sp.latex(derivada_externa)}")
            return derivada_externa, passos

        # Se for sin(u) -> Cadeia
        else:
            passos.append(rf"\textbf{{Regra da Cadeia (Trig):}} \frac{{d}}{{dx}}{func_nome}(u) = {nome_latex} \cdot u'")
            passos.append(rf"u = {sp.latex(arg)}")

            darg, sub = obter_passos_derivada(arg, x)
            passos.extend(sub)

            res = derivada_externa * darg
            passos.append(rf"\text{{Montagem: }} {sp.latex(derivada_externa)} \cdot ({sp.latex(darg)})")
            return res, passos

    # ---------------------------------------------------------
    # 6. GENÉRICO (Se nada acima funcionou)
    # ---------------------------------------------------------
    # Este bloco só roda se for uma função que não mapeamos (ex: log, exp, sec)
    res = sp.diff(expr, x)
    passos.append(rf"\text{{Derivada direta aplicada: }} {sp.latex(res)}")
    return res, passos