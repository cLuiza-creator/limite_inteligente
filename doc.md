# Documentação Matemática: Fundamentos de Cálculo Computacional

Este documento detalha a metodologia matemática aplicada no software. O objetivo do sistema é realizar o estudo analítico completo de funções reais de variável real, automatizando o cálculo de limites, a determinação de assíntotas e a análise de raízes e sinais.

## 1. Definição e Interpretação Algébrica

O núcleo do sistema opera sobre uma função $f(x)$ definida pelo usuário. O tratamento matemático inicial converte a entrada textual em uma árvore de expressão simbólica.

* **Formalização:** Seja $S$ a string de entrada. O sistema a converte para uma expressão $E(x)$ onde $x$ é tratado como uma variável simbólica (não numérica), permitindo manipulações algébricas exatas sem perda de precisão (erros de arredondamento).
* **Domínio Computacional:** O sistema assume, por padrão, que o domínio $D_f \subseteq \mathbb{R}$, exceto onde explicitamente identificado (divisões por zero ou raízes pares de números negativos).

---

## 2. Teoria dos Limites

O cálculo de limites é a base para a análise de continuidade e comportamento assintótico. O software utiliza algoritmos de expansão em série (como a série de Gruntz) para determinar o comportamento da função.

### 2.1. Definição Formal Aplicada
Para um ponto de tendência $p$ (finito ou infinito), o software calcula $L$ tal que:

$$
L = \lim_{x \to p} f(x)
$$

O sistema é capaz de identificar três resultados possíveis:
1.  **Convergência:** $L \in \mathbb{R}$ (o limite existe e é finito).
2.  **Divergência:** $L = \infty$ ou $L = -\infty$.
3.  **Indeterminação/Inexistência:** Casos onde os limites laterais diferem ($\lim_{x \to p^-} \neq \lim_{x \to p^+}$) ou oscilam indefinidamente.

---

## 3. Estudo Assintótico

A detecção de assíntotas é realizada através da aplicação direta dos teoremas de limites no infinito e análise de singularidades.

### 3.1. Assíntotas Verticais
As assíntotas verticais ocorrem em pontos de descontinuidade infinita. Para uma função racional $f(x) = \frac{N(x)}{D(x)}$, o algoritmo busca o conjunto de pontos $V$ tal que:

$$
V = \{ x_0 \in \mathbb{R} \mid D(x_0) = 0 \text{ e } N(x_0) \neq 0 \}
$$

Geometricamente, se $x = a$ é uma assíntota vertical, então:
$$
\lim_{x \to a^+} f(x) = \pm \infty \quad \text{ou} \quad \lim_{x \to a^-} f(x) = \pm \infty
$$

### 3.2. Assíntotas Horizontais
Descrevem o comportamento da função quando $x$ cresce indefinidamente em módulo. O sistema avalia dois limites independentes:

$$
y = L_1 \quad \text{se} \quad \lim_{x \to +\infty} f(x) = L_1
$$
$$
y = L_2 \quad \text{se} \quad \lim_{x \to -\infty} f(x) = L_2
$$

Se $L_1$ ou $L_2$ forem finitos, a reta $y = L$ é plotada no gráfico.

### 3.3. Assíntotas Oblíquas
Quando a função tende ao infinito mas não horizontalmente, verifica-se a existência de um comportamento linear assintótico da forma $y = ax + b$. O cálculo segue o seguinte algoritmo matemático:

1.  **Cálculo do Coeficiente Angular ($a$):**
    $$
    a = \lim_{x \to \infty} \frac{f(x)}{x}
    $$
    *Condição:* $a \in \mathbb{R}$ e $a \neq 0$.

2.  **Cálculo do Coeficiente Linear ($b$):**
    $$
    b = \lim_{x \to \infty} (f(x) - a \cdot x)
    $$
    *Condição:* $b \in \mathbb{R}$.

Se ambas as condições forem satisfeitas, a reta $y = ax + b$ é renderizada.

---

## 4. Análise de Raízes e Sinais

### 4.1. Zeros da Função
O sistema resolve a equação fundamental $f(x) = 0$ para encontrar as interseções com o eixo das abscissas.
* **Raízes Reais ($S_{\mathbb{R}}$):** Pontos onde o gráfico corta o eixo $x$.
* **Raízes Complexas ($S_{\mathbb{C}}$):** Soluções envolvendo a unidade imaginária $i$, indicando que não há interseção geométrica no plano real para aqueles componentes.

### 4.2. Inequações (Intervalos de Sinal)
O software determina os subconjuntos do domínio onde a função é positiva ou negativa.
* **Intervalo de Positividade:** $P = \{x \mid f(x) > 0\}$
* **Intervalo de Negatividade:** $N = \{x \mid f(x) < 0\}$

O resultado é expresso em notação de união de intervalos, por exemplo: $(-\infty, -2) \cup (3, +\infty)$.

---

## 5. Método de Visualização Numérica (Discretização)

Para a representação gráfica, é necessário transpor o domínio contínuo para um conjunto discreto de dados.

### 5.1. Vetorização do Domínio
O intervalo de visualização $[x_{min}, x_{max}]$ é dividido em $n = 2000$ subintervalos. O passo de amostragem $\Delta x$ é dado por:

$$
\Delta x = \frac{x_{max} - x_{min}}{n - 1}
$$

Gerando o vetor $X = [x_0, x_1, ..., x_{n-1}]$.

### 5.2. Tratamento de Singularidades Numéricas
Ao calcular o vetor imagem $Y = f(X)$, o sistema aplica um filtro para correta visualização de descontinuidades.

Seja $y_i = f(x_i)$. Se $|y_i|$ excede um limiar arbitrário (indicando proximidade de uma assíntota vertical) ou se $y_i \notin \mathbb{R}$, o valor é substituído por `NaN` (Not a Number). Isso impede que o motor gráfico (Plotly) interpole uma linha reta através da assíntota, garantindo a fidelidade visual ao conceito matemático de descontinuidade.

---

## 6. Cálculo Diferencial e Análise Algorítmica

O sistema implementa um motor de diferenciação simbólica que transcende o simples cálculo do resultado final. A metodologia adotada mimetiza o raciocínio analítico humano, realizando a **decomposição estrutural** da função para identificar e aplicar regras de derivação específicas passo a passo.

### 6.1. Decomposição da Árvore de Expressão
Diferente de abordagens numéricas (diferenças finitas), o software analisa a função $f(x)$ como uma árvore sintática de operações. O algoritmo realiza uma travessia recursiva (*tree traversal*) para identificar a operação dominante (nó raiz) e decidir qual teorema de cálculo aplicar.

A análise prioriza a estrutura "bruta" inserida pelo usuário, evitando simplificações algébricas prematuras que ocultariam a aplicação de regras fundamentais (como a Regra do Quociente).

### 6.2. Regras de Derivação Implementadas

O motor de inferência categoriza a expressão $f(x)$ em um dos seguintes arquétipos e aplica o algoritmo correspondente:

#### A. Linearidade (Soma e Subtração)
Se $f(x) = \sum_{i=1}^{n} c_i \cdot g_i(x)$, o sistema aplica a propriedade de linearidade do operador diferencial:
$$
\frac{d}{dx} \left[ \sum c_i g_i(x) \right] = \sum c_i \frac{d}{dx}[g_i(x)]
$$
Onde a derivada da soma é tratada como a soma das derivadas.

#### B. Regra do Produto (Leibniz)
Identificada quando a operação principal é uma multiplicação entre duas funções não constantes $u(x)$ e $v(x)$. O algoritmo aplica:
$$
\frac{d}{dx} [u(x) \cdot v(x)] = u'(x) \cdot v(x) + u(x) \cdot v'(x)
$$
O sistema isola os termos $u$ e $v$ e resolve suas derivadas recursivamente.

#### C. Regra do Quociente
Para funções racionais ou divisões explícitas da forma $f(x) = \frac{N(x)}{D(x)}$, o sistema detecta a estrutura fracionária antes de qualquer simplificação. A derivada é computada expandindo a fórmula:
$$
\frac{d}{dx} \left[ \frac{N(x)}{D(x)} \right] = \frac{N'(x) \cdot D(x) - N(x) \cdot D'(x)}{[D(x)]^2}
$$
Esta abordagem garante que o usuário visualize a estrutura da divisão, mesmo que a fração seja simplificável algebricamente a posteriori.

#### D. Regra da Cadeia (Composição de Funções)
Fundamental para funções compostas $f(g(x))$, como potências $(u^n)$, raízes $\sqrt{u}$ ou funções trigonométricas $\sin(u)$. O algoritmo identifica a função externa $f$ e a interna $u = g(x)$, aplicando:
$$
\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)
$$
Onde $f'$ é a derivada da função externa avaliada na interna, multiplicada pela derivada da interna (recursão).

### 6.3. Otimização Visual e Resultado Final
O processo de exibição é dividido em duas etapas:
1.  **Etapa Intermediária (Didática):** Exibe a aplicação crua da regra (ex: mostra a montagem da Regra do Quociente sem realizar as multiplicações e subtrações no numerador).
2.  **Etapa Final (Simplificada):** Após a montagem estrutural, o sistema invoca algoritmos de simplificação algébrica para apresentar o resultado na forma mais compacta possível:
    $$
    \frac{d}{dx} f(x) = \text{simplify}(\text{Resultado Bruto})
    $$