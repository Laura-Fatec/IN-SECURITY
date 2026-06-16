"""
=============================================================================
MÓDULO: stats.py — Estatísticas e Relatório Analítico do Estoque
=============================================================================
Responsabilidade:
    Calcular e exibir métricas analíticas do inventário em tempo real,
    processando diretamente o dicionário em RAM (sem acessar o CSV).

Métricas calculadas:
    - Total de tipos únicos de produto (número de IDs distintos)
    - Volume bruto total de unidades físicas em estoque (soma das quantidades)
    - Valorização financeira do estoque (soma de qtd × preço para cada produto)
    - Contagem de produtos importados vs nacionais

Ponto de extensão:
    Este módulo pode ser facilmente expandido com:
    - Produto mais caro / mais barato
    - Produto com maior / menor estoque
    - Média de preços
    - Produtos com estoque abaixo de um mínimo configurável (alerta de reposição)
=============================================================================
"""


def exibir_estatisticas(inventario: dict):
    """
    Calcula e exibe no terminal um relatório estatístico completo do inventário.

    Algoritmo de cálculo (percurso único O(n)):
        Percorre o dicionário UMA ÚNICA VEZ acumulando todos os valores necessários.
        Isso é mais eficiente do que fazer múltiplos percursos (um para cada métrica).

    Tratamento de borda (inventário vazio):
        Se o dicionário estiver vazio, exibe mensagem adequada e retorna sem calcular,
        evitando divisões por zero ou operações em listas vazias.

    Args:
        inventario (dict): Dicionário { id: [nome, qtd, preco, importado] }
                           Vazio {} retorna mensagem de inventário vazio
    """
    print("\n================ RELATÓRIO ESTATÍSTICO DO ESTOQUE ================")

    # Conta os tipos únicos de produto = número de chaves no dicionário
    total_ids = len(inventario)

    # Trata o caso especial de inventário vazio
    if total_ids == 0:
        print("  Inventário vazio. Adicione produtos para ver estatísticas.")
        print("===================================================================")
        return

    # Inicializa acumuladores para o percurso único
    total_itens_fisicos = 0     # Soma de todas as quantidades (unidades em estoque)
    valor_total_financeiro = 0.0  # Soma de (qtd × preço) para cada produto
    qtd_importados = 0          # Contador de produtos marcados como importados

    # Percorre o inventário UMA VEZ calculando todas as métricas simultaneamente
    for dados in inventario.values():
        qtd = dados[1]          # Quantidade em estoque (índice 1)
        preco = dados[2]        # Preço unitário (índice 2)
        is_importado = dados[3] # Bool: True=importado, False=nacional (índice 3)

        # Acumula volume físico total (ex: 15 notebooks + 10 cadeiras = 25 unidades)
        total_itens_fisicos += qtd

        # Acumula valor financeiro: quantidade × preço de cada produto
        # Ex: 15 notebooks a R$2.500 = R$37.500 (só desse produto)
        valor_total_financeiro += (qtd * preco)

        # Incrementa contador de importados (bool True age como inteiro 1 no Python,
        # mas usamos if explícito para maior clareza de intenção)
        if is_importado:
            qtd_importados += 1

    # Exibe as métricas calculadas com formatação alinhada
    print(f"\n  {'Tipos únicos de produtos:':<35} {total_ids}")
    print(f"  {'Volume total de unidades em estoque:':<35} {total_itens_fisicos}")

    # Formata o valor financeiro com 2 casas decimais e separador de milhar
    print(f"  {'Valor total do estoque:':<35} R$ {valor_total_financeiro:,.2f}")

    print(f"  {'Produtos importados:':<35} {qtd_importados}")

    # Nacionais = total de tipos - importados (subtração simples, sem percurso extra)
    print(f"  {'Produtos nacionais:':<35} {total_ids - qtd_importados}")

    # Calcula e exibe percentual de importados (com proteção contra divisão por zero)
    percentual_imp = (qtd_importados / total_ids * 100) if total_ids > 0 else 0
    print(f"  {'% de produtos importados:':<35} {percentual_imp:.1f}%")

    print("===================================================================")
