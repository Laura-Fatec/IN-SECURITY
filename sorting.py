"""
=============================================================================
MÓDULO: sorting.py — Algoritmos de Ordenação
=============================================================================
Responsabilidade:
    Implementar e expor algoritmos de ordenação para o inventário de produtos.
    O módulo decide automaticamente qual algoritmo usar baseado no volume de dados.

Algoritmos implementados:
    1. Bubble Sort  → Simples, O(n²), usado para n ≤ 100 itens
    2. Merge Sort   → Eficiente, O(n log n), usado para n > 100 itens

Critério de ordenação:
    Todos os algoritmos ordenam pela coluna NOME (índice 1 da lista de produto),
    de forma case-insensitive (ignora maiúsculas/minúsculas).

Complexidade de tempo (comparação):
    ┌──────────────┬──────────────┬──────────────┬──────────────┐
    │ Algoritmo    │ Melhor Caso  │ Caso Médio   │ Pior Caso    │
    ├──────────────┼──────────────┼──────────────┼──────────────┤
    │ Bubble Sort  │ O(n)         │ O(n²)        │ O(n²)        │
    │ Merge Sort   │ O(n log n)   │ O(n log n)   │ O(n log n)   │
    └──────────────┴──────────────┴──────────────┴──────────────┘
    
    Para 100 itens: Bubble Sort → ~10.000 operações; OK.
    Para 10.000 itens: Bubble Sort → 100M operações; Merge Sort → ~130K. Enorme diferença!

Estrutura da lista de produtos:
    Cada item é uma lista: [id, nome, qtd, preco, importado]
    Índices:                  0     1     2     3       4
=============================================================================
"""


# =============================================================================
# SEÇÃO 1: CONVERSÃO (dicionário → lista)
# =============================================================================

def converter_para_lista(inventario: dict) -> list:
    """
    Transforma o dicionário do inventário em uma lista de listas para ordenação.

    Por que converter?
        Algoritmos de ordenação trabalham melhor com listas (acesso por índice).
        O dicionário é ideal para busca por ID (O(1)), mas não para ordenar.

    Conversão realizada:
        { id: [nome, qtd, preco, imp] }
        →
        [ [id, nome, qtd, preco, imp], [id, nome, qtd, preco, imp], ... ]

    Args:
        inventario (dict): Dicionário { id_int: [nome, qtd, preco, importado] }

    Returns:
        list: Lista de listas [ [id, nome, qtd, preco, importado], ... ]
    
    Exemplo:
        { 101: ["Forno", 5, 999.0, False] }
        → [ [101, "Forno", 5, 999.0, False] ]
    """
    lista_produtos = []
    for id_prod, dados in inventario.items():
        # Combina o ID com os demais dados em uma única lista plana
        lista_produtos.append([id_prod] + dados)
        # [id_prod] + dados = [id_prod, nome, qtd, preco, importado]
    return lista_produtos


# =============================================================================
# SEÇÃO 2: BUBBLE SORT (Para pequenos conjuntos — n ≤ 100)
# =============================================================================

def bubble_sort(lista: list):
    """
    Ordena a lista in-place pelo campo Nome (índice 1) usando Bubble Sort.

    Como funciona o Bubble Sort?
        Percorre a lista comparando PARES de elementos adjacentes.
        Se o elemento da esquerda for "maior" que o da direita, TROCA os dois.
        Repete esse processo n vezes — a cada passagem, o maior elemento "flutua"
        (como uma bolha) para o final da lista.

    Visualização com [C, A, B]:
        Passagem 1: Compara C,A → troca → [A, C, B]
                    Compara C,B → troca → [A, B, C]   ← C chegou ao final
        Passagem 2: Compara A,B → ok    → [A, B, C]   ← já ordenado
        Resultado: [A, B, C] ✔

    Por que "in-place"?
        A lista é modificada diretamente na memória — não cria uma cópia.
        Isso economiza memória, mas significa que a lista original é alterada.

    Complexidade:
        - Tempo: O(n²) no pior caso — quadrático, ruim para grandes volumes
        - Espaço: O(1) — usa memória constante (sem listas auxiliares)

    Args:
        lista (list): Lista de produtos [id, nome, qtd, preco, imp] — modificada in-place
    """
    n = len(lista)

    # Loop externo: n passagens pela lista (i=0 a n-1)
    for i in range(n):
        # Loop interno: compara pares adjacentes
        # A cada passagem, os últimos i elementos já estão na posição correta
        # então não precisamos verificá-los novamente (n - i - 1)
        for j in range(0, n - i - 1):
            # Compara pelo NOME (índice 1), ignorando maiúsculas/minúsculas
            if lista[j][1].lower() > lista[j + 1][1].lower():
                # Troca os dois elementos de posição (swap)
                # Python permite troca elegante sem variável auxiliar:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]


# =============================================================================
# SEÇÃO 3: MERGE SORT (Para grandes volumes — n > 100)
# =============================================================================

def merge_sort(lista: list):
    """
    Ordena a lista usando Merge Sort — algoritmo de divisão e conquista.

    Como funciona o Merge Sort?
        1. DIVIDE: Se a lista tem mais de 1 elemento, divide ao meio
        2. CONQUISTA: Chama merge_sort recursivamente em cada metade
        3. COMBINA: Junta (merge) as duas metades já ordenadas em ordem

    Visualização com [D, B, C, A]:
        Divide: [D, B] | [C, A]
        Divide: [D] | [B]  e  [C] | [A]
        Merge:  [B, D]     e  [A, C]
        Merge final: [A, B, C, D] ✔

    Recursividade:
        A função chama a si mesma com listas menores até atingir o caso base
        (lista com 1 elemento — que já está "ordenada" por definição).

    Complexidade:
        - Tempo: O(n log n) em todos os casos — muito eficiente
        - Espaço: O(n) — cria listas auxiliares (esquerda e direita)

    Args:
        lista (list): Lista de produtos — modificada in-place
    """
    if len(lista) > 1:
        # Calcula o ponto médio para dividir a lista
        mid = len(lista) // 2

        # Cria duas sublistas (cópias independentes)
        esquerda = lista[:mid]   # Primeira metade
        direita = lista[mid:]    # Segunda metade

        # RECURSÃO: ordena cada metade independentemente
        # A recursão continua até listas de tamanho 1 (caso base)
        merge_sort(esquerda)
        merge_sort(direita)

        # MERGE (combinação): intercala os dois subconjuntos ordenados
        i = 0  # Ponteiro para a esquerda
        j = 0  # Ponteiro para a direita
        k = 0  # Ponteiro para a lista original (onde vamos inserir)

        # Enquanto houver elementos em AMBAS as metades, compara e insere o menor
        while i < len(esquerda) and j < len(direita):
            # Compara pelo NOME (índice 1), case-insensitive
            if esquerda[i][1].lower() < direita[j][1].lower():
                lista[k] = esquerda[i]  # Elemento da esquerda é menor → insere
                i += 1
            else:
                lista[k] = direita[j]   # Elemento da direita é menor → insere
                j += 1
            k += 1

        # Copia os elementos restantes da esquerda (se houver)
        while i < len(esquerda):
            lista[k] = esquerda[i]
            i += 1
            k += 1

        # Copia os elementos restantes da direita (se houver)
        while j < len(direita):
            lista[k] = direita[j]
            j += 1
            k += 1


# =============================================================================
# SEÇÃO 4: SELEÇÃO AUTOMÁTICA DE ALGORITMO
# =============================================================================

def obter_inventario_ordenado(inventario: dict) -> list:
    """
    Ponto de entrada principal — decide qual algoritmo usar e retorna lista ordenada.

    Critério de seleção automática:
        ≤ 100 produtos → Bubble Sort (simples, suficiente para volumes pequenos)
        > 100 produtos → Merge Sort (eficiente, escala para grandes volumes)

    Esta decisão automática é transparente para o chamador — quem usa a função
    não precisa saber qual algoritmo foi executado internamente.

    Args:
        inventario (dict): Dicionário completo do inventário

    Returns:
        list: Nova lista ordenada por nome [ [id, nome, qtd, preco, imp], ... ]
              (o dicionário original NÃO é modificado)
    """
    lista = converter_para_lista(inventario)
    total = len(lista)

    if total <= 100:
        # Bubble Sort: adequado para poucos produtos, código mais simples
        print(f"  [Ordenação] {total} produtos → usando Bubble Sort")
        bubble_sort(lista)
    else:
        # Merge Sort: necessário para performance com muitos produtos
        print(f"  [Ordenação] {total} produtos → usando Merge Sort (mais eficiente)")
        merge_sort(lista)

    return lista
