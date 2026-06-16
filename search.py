"""
=============================================================================
MÓDULO: search.py — Algoritmos de Busca
=============================================================================
Responsabilidade:
    Implementar dois algoritmos clássicos de busca para localizar produtos
    no inventário por nome.

Algoritmos implementados:
    1. Busca Linear → Percorre todos os elementos; aceita busca parcial
    2. Busca Binária → Divisão e conquista; exige nome EXATO e lista ordenada

Quando usar cada um?
    ┌─────────────────┬───────────────────────────────────────────────────┐
    │ Busca Linear    │ Quando o usuário lembra parte do nome             │
    │                 │ Ex: "cafe" encontra "Cafeteira", "Café"           │
    │                 │ Desvantagem: mais lenta — O(n)                    │
    ├─────────────────┼───────────────────────────────────────────────────┤
    │ Busca Binária   │ Quando o usuário sabe o nome EXATO do produto     │
    │                 │ Ex: deve digitar "Cafeteira Philips" exatamente   │
    │                 │ Vantagem: muito mais rápida — O(log n)            │
    └─────────────────┴───────────────────────────────────────────────────┘

Comparação de performance:
    Para 1.000 produtos:
    - Busca Linear:  até 1.000 comparações no pior caso
    - Busca Binária: no máximo 10 comparações (log₂(1000) ≈ 10)
=============================================================================
"""

from sorting import obter_inventario_ordenado  # Necessário para a busca binária


# =============================================================================
# SEÇÃO 1: BUSCA LINEAR (Percorre todo o dicionário)
# =============================================================================

def busca_linear_por_nome(inventario: dict, nome_busca: str) -> list:
    """
    Percorre todos os produtos procurando o termo de busca no nome (parcial ou completo).

    Como funciona?
        Itera sobre CADA produto do dicionário e verifica se o termo
        de busca está CONTIDO no nome do produto (usando operador 'in').
        A comparação ignora maiúsculas/minúsculas (ambos convertidos para lower()).

    Vantagem sobre busca binária:
        - Aceita busca PARCIAL: "cafe" encontra "Cafeteira", "Café Expresso"
        - Não exige lista ordenada — opera diretamente no dicionário
        - Retorna MÚLTIPLOS resultados (tudo que corresponder)

    Desvantagem:
        - Complexidade O(n): quanto mais produtos, mais lenta fica
        - Para 10.000 produtos, verifica todos os 10.000

    Exemplo:
        busca_linear_por_nome(inv, "cafe")
        → encontra todos os produtos cujo nome CONTÉM "cafe" (case-insensitive)

    Args:
        inventario (dict): Dicionário { id: [nome, qtd, preco, importado] }
        nome_busca (str): Termo de busca (pode ser parcial, ex: "cafe", "note")

    Returns:
        list: Lista de todos os produtos encontrados no formato [id, nome, qtd, preco, importado]
              Lista vazia [] se nada for encontrado
    """
    resultados = []
    nome_busca_lower = nome_busca.lower()  # Converte busca para minúsculo UMA VEZ (eficiência)

    # Percorre TODOS os produtos — daí o nome "linear" (linha por linha)
    for id_prod, dados in inventario.items():
        # 'in' verifica se nome_busca_lower está CONTIDO em dados[0].lower()
        # Ex: "cafe" in "cafeteira philips" → True
        # Ex: "cafe" in "notebook dell" → False
        if nome_busca_lower in dados[0].lower():
            # Constrói a lista plana [id, nome, qtd, preco, importado] para exibição
            resultados.append([id_prod] + dados)

    return resultados


# =============================================================================
# SEÇÃO 2: BUSCA BINÁRIA (Divisão e conquista — requer nome exato e lista ordenada)
# =============================================================================

def busca_binaria_por_nome(inventario: dict, nome_busca: str):
    """
    Aplica busca binária clássica para localizar um produto pelo nome EXATO.

    Pré-requisito FUNDAMENTAL:
        A lista DEVE estar ordenada pelo campo nome.
        A busca binária SÓ funciona em listas ordenadas — sem isso, o resultado
        seria incorreto. Por isso, chamamos obter_inventario_ordenado() primeiro.

    Como funciona a Busca Binária?
        1. Define os ponteiros: low=0 (início) e high=n-1 (fim da lista)
        2. Calcula o elemento do MEIO: mid = (low + high) // 2
        3. Compara o nome do meio com o nome buscado:
           - Se IGUAL → achou! Retorna o produto.
           - Se nome_meio < nome_busca → o produto está na METADE DIREITA → low = mid + 1
           - Se nome_meio > nome_busca → o produto está na METADE ESQUERDA → high = mid - 1
        4. Repete até encontrar ou até low > high (não encontrado → retorna None)

    Visualização com lista ordenada [Ar Condicionado, Cafeteira, Forno, Notebook]:
        Busca: "Forno"
        Passo 1: low=0, high=3, mid=1 → "Cafeteira" < "Forno" → low = 2
        Passo 2: low=2, high=3, mid=2 → "Forno" == "Forno" → ENCONTRADO! ✔

    Complexidade:
        - Tempo: O(log n) — divide o espaço de busca pela metade a cada passo
        - Espaço: O(n) — precisamos da lista ordenada em memória

    Args:
        inventario (dict): Dicionário completo do inventário
        nome_busca (str): Nome EXATO do produto (busca parcial NÃO funciona aqui)

    Returns:
        list: O produto encontrado [id, nome, qtd, preco, importado], ou None se não achar
    """
    # Obtém a lista já ordenada por nome (usando Bubble Sort ou Merge Sort automaticamente)
    lista_ordenada = obter_inventario_ordenado(inventario)
    nome_busca_lower = nome_busca.lower()  # Converte uma vez para comparação case-insensitive

    # Inicializa os ponteiros de busca
    low = 0                          # Índice do início da região de busca
    high = len(lista_ordenada) - 1  # Índice do fim da região de busca

    # Continua enquanto ainda houver região para buscar
    while low <= high:
        # Calcula o índice do elemento do meio
        # Usar // (divisão inteira) garante índice inteiro válido
        mid = (low + high) // 2
        nome_atual = lista_ordenada[mid][1].lower()  # Nome do produto no meio

        if nome_atual == nome_busca_lower:
            # ✔ ENCONTRADO: retorna o produto completo
            return lista_ordenada[mid]

        elif nome_atual < nome_busca_lower:
            # O nome do meio vem ANTES do buscado na ordem alfabética
            # → O produto que buscamos está na METADE DIREITA
            # → Descartamos tudo à esquerda, incluindo o meio
            low = mid + 1

        else:
            # O nome do meio vem DEPOIS do buscado na ordem alfabética
            # → O produto que buscamos está na METADE ESQUERDA
            # → Descartamos tudo à direita, incluindo o meio
            high = mid - 1

    # Loop terminou sem encontrar (low > high significa região vazia)
    return None
