"""
=============================================================================
MÓDULO: inventory.py — Gerenciamento do Inventário de Produtos
=============================================================================
Responsabilidade:
    Toda operação CRUD (Create, Read, Update, Delete) sobre os produtos:
    - Carregar dados cifrados do CSV para memória RAM (dict)
    - Salvar dados da RAM de volta ao CSV (cifrados)
    - Adicionar, remover e atualizar produtos

Arquitetura de armazenamento (duas camadas):
    ┌─────────────────────────────────────────────────────────┐
    │  DISCO (inventario.csv) — Dados CIFRADOS com César      │
    │  101;Zlujh;25;1299.99;Ayfse                             │  ← cifrado
    │  102;Aypfh Byhnmly;10;599.90;Ayhf                      │  ← cifrado
    └────────────────────────┬────────────────────────────────┘
                             │ carregar_inventario() — decifra
                             ▼
    ┌─────────────────────────────────────────────────────────┐
    │  RAM (dicionário Python) — Dados em TEXTO PURO          │
    │  { 101: ["Forno", 25, 1299.99, False],                  │  ← legível
    │    102: ["Cafeteira Bruhner", 10, 599.90, False] }      │  ← legível
    └────────────────────────┬────────────────────────────────┘
                             │ salvar_inventario() — cifra
                             ▼
    ┌─────────────────────────────────────────────────────────┐
    │  DISCO (inventario.csv) — Dados CIFRADOS novamente      │
    └─────────────────────────────────────────────────────────┘

Estrutura de cada produto no dicionário:
    { id_produto (int): [nome (str), quantidade (int), preco (float), importado (bool)] }
    Exemplo: { 101: ["Notebook", 15, 2499.99, True] }

Formato de cada linha no CSV (após cifrar):
    ID;NOME_CIFRADO;QTD_CIFRADA;PRECO_CIFRADO;IMPORTADO_CIFRADO
    O ID não é cifrado pois é usado como chave de busca direta.
=============================================================================
"""

import os  # Para verificar existência de arquivos
from crypto import cesar_encrypt, cesar_decrypt  # Funções de cifragem/decifragem


# =============================================================================
# CONFIGURAÇÃO GLOBAL
# =============================================================================

ARQUIVO_INV = "inventario.csv"  # Caminho do arquivo de persistência de dados


# =============================================================================
# SEÇÃO 1: PERSISTÊNCIA (Leitura e Escrita no CSV)
# =============================================================================

def carregar_inventario() -> dict:
    """
    Lê o arquivo CSV cifrado e reconstrói o dicionário de produtos em RAM.

    Processo de carregamento:
        1. Abre o arquivo inventario.csv (cria vazio se não existir)
        2. Para cada linha: divide pelos ";" e decifra cada campo individualmente
        3. Converte os tipos: ID→int, QTD→int, PREÇO→float, IMPORTADO→bool
        4. Monta o dicionário { id: [nome, qtd, preco, importado] }

    Por que converter tipos após decifrar?
        A Cifra de César opera sobre strings. Então "25" (qtd) é cifrado e salvo
        como texto. Ao carregar, deciframos para "25" (str) e depois int("25")=25.

    Returns:
        dict: Dicionário com todos os produtos { id_int: [nome, qtd, preco, importado] }
              Retorna dicionário vazio {} se o arquivo não existir ou estiver vazio
    """
    inventario = {}

    # Se o arquivo não existe, cria vazio e retorna dicionário vazio
    if not os.path.exists(ARQUIVO_INV):
        with open(ARQUIVO_INV, "w", encoding="utf-8") as f:
            pass  # Cria arquivo vazio (sem escrever nada)
        return inventario

    # Lê o arquivo linha a linha
    with open(ARQUIVO_INV, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()  # Remove espaços e \n das extremidades

            if not linha:  # Pula linhas em branco
                continue

            # Divide a linha nos 5 campos separados por ";"
            partes = linha.split(";")

            if len(partes) == 5:  # Valida que a linha tem exatamente 5 campos
                # Campo 0 — ID: não cifrado, converte diretamente para int
                id_prod = int(partes[0])

                # Campos 1-4 — Decifra cada campo com César antes de usar
                nome = cesar_decrypt(partes[1])                     # str
                qtd = int(cesar_decrypt(partes[2]))                 # str → int
                preco = float(cesar_decrypt(partes[3]))             # str → float

                # Importado estava salvo como "True" ou "False" (string cifrada)
                importado_str = cesar_decrypt(partes[4])            # str: "True"/"False"
                importado = True if importado_str == "True" else False  # str → bool

                # Adiciona ao dicionário em RAM
                inventario[id_prod] = [nome, qtd, preco, importado]

    return inventario


def salvar_inventario(inventario: dict):
    """
    Cifra todos os campos do dicionário e grava no CSV em lote (todas de uma vez).

    Estratégia de gravação em lote:
        Modificações (add/remove/update) são feitas APENAS na RAM durante a sessão.
        Só quando o usuário escolhe "Salvar e Sair" (opção 0) ou explicitamente
        salva, todos os dados são escritos de volta ao CSV cifrado.
        → Isso minimiza operações de I/O e protege contra gravações parciais.

    Processo de cifragem por campo:
        - nome, qtd, preco, importado → cada um passa por cesar_encrypt()
        - ID não é cifrado (mantido como inteiro puro)
        - Separador de campos: ";" (ponto-e-vírgula)

    Args:
        inventario (dict): Dicionário completo { id: [nome, qtd, preco, importado] }
    """
    # Mode "w" sobrescreve todo o arquivo — apaga versão anterior
    with open(ARQUIVO_INV, "w", encoding="utf-8") as f:
        for id_prod, dados in inventario.items():
            # Cifra cada campo individualmente com a Cifra de César
            nome_cif  = cesar_encrypt(dados[0])   # nome: str → str cifrada
            qtd_cif   = cesar_encrypt(dados[1])   # qtd: int → str cifrada ("25" → "25" cifrado)
            preco_cif = cesar_encrypt(dados[2])   # preco: float → str cifrada
            imp_cif   = cesar_encrypt(dados[3])   # bool → str "True"/"False" → cifrada

            # Grava linha no formato: ID;NOME_CIFRADO;QTD_CIFRADA;PRECO_CIFRADO;IMP_CIFRADA
            f.write(f"{id_prod};{nome_cif};{qtd_cif};{preco_cif};{imp_cif}\n")


# =============================================================================
# SEÇÃO 2: OPERAÇÕES CRUD (Create, Read, Update, Delete)
# =============================================================================

def adicionar_produto(inventario: dict) -> bool:
    """
    Coleta dados do novo produto via input e insere no dicionário em RAM.

    Validações realizadas:
        - ID deve ser inteiro e ÚNICO (não pode repetir)
        - Nome não pode ser vazio
        - Quantidade deve ser inteiro (não aceita 1.5 unidades, por exemplo)
        - Preço deve ser numérico (aceita decimais)
        - Importado: entrada S/N, convertida para bool True/False

    Args:
        inventario (dict): Dicionário atual passado por referência (modificado in-place)

    Returns:
        bool: True se produto adicionado com sucesso, False se houve erro
    """
    print("\n--- ADICIONAR PRODUTO ---")
    try:
        # ID deve ser inteiro — ValueError se usuário digitar texto
        id_prod = int(input("ID do produto (número inteiro único): "))

        # Verifica unicidade — não permite sobrescrever produto existente
        if id_prod in inventario:
            print("❌ Erro: ID já existente no sistema. Use outro ID.")
            return False

        nome = input("Nome do produto: ").strip()
        if not nome:
            print("❌ Erro: O nome não pode ser vazio.")
            return False

        # int() garante que quantidade seja número inteiro (não aceita 5.5)
        qtd = int(input("Quantidade em estoque: "))
        if qtd < 0:
            print("❌ Erro: Quantidade não pode ser negativa.")
            return False

        # float() aceita tanto "10" quanto "10.5" para preço
        preco = float(input("Preço unitário (ex: 29.90): "))
        if preco < 0:
            print("❌ Erro: Preço não pode ser negativo.")
            return False

        # Entrada S/N → converte para bool (True=importado, False=nacional)
        imp_resp = input("É importado? (S/N): ").strip().upper()
        importado = True if imp_resp == "S" else False

        # Insere no dicionário em RAM (ainda NÃO salva no disco)
        inventario[id_prod] = [nome, qtd, preco, importado]
        print("✔ Produto adicionado com sucesso em RAM!")
        print("  (As alterações serão gravadas no CSV ao encerrar ou salvar)")
        return True

    except ValueError:
        # Captura erro se usuário digitar texto onde era esperado número
        print("❌ Erro: ID e Quantidade devem ser inteiros; Preço deve ser numérico.")
        return False


def remover_produto(inventario: dict) -> bool:
    """
    Remove um produto do dicionário em RAM pelo seu ID.

    A remoção é feita com 'del' — operação O(1) em dicionários Python.
    Como o dicionário usa hash internamente, não é necessário percorrer todos os itens.

    Args:
        inventario (dict): Dicionário atual (modificado in-place)

    Returns:
        bool: True se removido com sucesso, False se ID não encontrado ou erro
    """
    print("\n--- REMOVER PRODUTO ---")
    try:
        id_prod = int(input("Digite o ID do produto para remover: "))

        if id_prod in inventario:
            # Exibe confirmação antes de remover (nome do produto)
            nome_produto = inventario[id_prod][0]
            confirmar = input(f"Confirmar remoção de '{nome_produto}'? (S/N): ").strip().upper()

            if confirmar == "S":
                del inventario[id_prod]  # Remove a chave e seus dados do dicionário
                print(f"✔ Produto '{nome_produto}' removido com sucesso de RAM!")
                return True
            else:
                print("Operação cancelada pelo usuário.")
                return False

        print("❌ Produto não encontrado com esse ID.")
        return False

    except ValueError:
        print("❌ ID inválido. Digite apenas números inteiros.")
        return False


def atualizar_produto(inventario: dict) -> bool:
    """
    Atualiza campos específicos de um produto existente no dicionário.

    Comportamento de campos em branco:
        Se o usuário deixar um campo vazio, o valor anterior é MANTIDO.
        Isso permite atualizar apenas o preço sem precisar redigitar nome e quantidade.

    Args:
        inventario (dict): Dicionário atual (modificado in-place)

    Returns:
        bool: True se atualizado com sucesso, False se ID não encontrado ou erro
    """
    print("\n--- ATUALIZAR PRODUTO ---")
    try:
        id_prod = int(input("Digite o ID do produto para atualizar: "))

        if id_prod not in inventario:
            print("❌ Produto não encontrado.")
            return False

        # Exibe os dados atuais para o usuário saber o que está modificando
        dados = inventario[id_prod]
        print(f"\nDados atuais:")
        print(f"  Nome:      {dados[0]}")
        print(f"  Qtd:       {dados[1]}")
        print(f"  Preço:     R$ {dados[2]:.2f}")
        print(f"  Importado: {'Sim' if dados[3] else 'Não'}")
        print("\n(Pressione Enter sem digitar para manter o valor atual)")

        # Coleta novos valores — campos vazios mantêm o valor original
        nome = input("Novo Nome: ").strip()
        qtd_str = input("Nova Quantidade: ").strip()
        preco_str = input("Novo Preço: ").strip()
        imp_resp = input("Alterar status de Importado? (S=Sim / N=Não / Enter=manter): ").strip().upper()

        # Aplica somente os campos que foram preenchidos
        if nome:
            inventario[id_prod][0] = nome

        if qtd_str:
            inventario[id_prod][1] = int(qtd_str)  # Converte para int

        if preco_str:
            inventario[id_prod][2] = float(preco_str)  # Converte para float

        if imp_resp in ["S", "N"]:
            inventario[id_prod][3] = (imp_resp == "S")  # "S" → True, "N" → False

        print("✔ Produto atualizado com sucesso em RAM!")
        return True

    except ValueError:
        print("❌ Erro: Quantidade deve ser inteiro e Preço deve ser numérico.")
        return False
