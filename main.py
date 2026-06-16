"""
=============================================================================
MÓDULO: main.py — Ponto de Entrada e Orquestrador do Sistema
=============================================================================
Nome do sistema: IN-SECURITY — Secure Inventory System v1.0

Responsabilidade:
    Orquestrar o fluxo completo da aplicação:
    1. Ativar suporte a cores no terminal
    2. Executar autenticação obrigatória
    3. Carregar o inventário cifrado para RAM
    4. Exibir o menu interativo em loop
    5. Despachar ações para os módulos especializados
    6. Salvar os dados de volta ao CSV cifrado ao encerrar

Arquitetura de módulos:
    main.py          ← VOCÊ ESTÁ AQUI (orquestrador)
    ├── auth.py      ← Autenticação, login, log de segurança
    ├── inventory.py ← CRUD de produtos + persistência no CSV
    ├── sorting.py   ← Bubble Sort e Merge Sort
    ├── search.py    ← Busca linear e busca binária
    ├── stats.py     ← Relatório estatístico do estoque
    └── crypto.py    ← SHA-256 (senhas) + Cifra de César (dados)

Estratégia de persistência (Lazy Save):
    Modificações são feitas apenas na memória RAM durante toda a sessão.
    O arquivo CSV só é regravado ao encerrar (opção 0) ou quando há mudanças.
    A flag `modificado` controla se há dados pendentes para salvar.
=============================================================================
"""

import os       # Para limpar a tela e detectar o sistema operacional
import sys      # Para encerrar o programa com sys.exit()
import time     # Para pausas estratégicas na interface (time.sleep)
import ctypes   # Para ativar cores ANSI no terminal do Windows

# Importações dos módulos do projeto (todos no mesmo diretório)
import auth
import inventory
import sorting
import search
import stats
import secret   # Easter egg — evento secreto ativado pelo comando "99"


# =============================================================================
# CONFIGURAÇÃO DA INTERFACE (CORES ANSI)
# =============================================================================

# Detecção automática: testa se o terminal suporta ANSI.
# Se aparecerem caracteres estranhos tipo "?[96m", o sistema desativa sozinho.
def _detectar_suporte_cores() -> bool:
    if os.name == 'nt':  # Windows
        try:
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(-11)  # STDOUT
            m = ctypes.c_ulong()
            kernel32.GetConsoleMode(h, ctypes.byref(m))
            resultado = kernel32.SetConsoleMode(h, m.value | 0x0004)
            return resultado != 0  # 0 = falhou, qualquer outro = sucesso
        except Exception:
            return False
    return True  # Linux/Mac suportam ANSI nativamente

USAR_CORES = _detectar_suporte_cores()

if USAR_CORES:
    # Códigos de escape ANSI para colorir o terminal
    # Formato: \033[CODIGOm  onde CODIGO define a cor/estilo
    VERDE   = '\033[92m'   # Verde brilhante — sucesso, confirmações
    VERMELHO= '\033[91m'   # Vermelho brilhante — erros, opção sair
    AZUL    = '\033[94m'   # Azul brilhante — separadores, produtos nacionais
    CIANO   = '\033[96m'   # Ciano — títulos, destaque de seções
    AMARELO = '\033[93m'   # Amarelo — opções do menu, avisos
    NEGRITO = '\033[1m'    # Negrito — ênfase textual
    RESET   = '\033[0m'    # Reseta TODAS as formatações anteriores (obrigatório no final)
else:
    # Modo seguro: todas as variáveis viram strings vazias
    # O código do menu funciona identicamente, mas sem nenhuma cor aplicada
    VERDE = VERMELHO = AZUL = CIANO = AMARELO = NEGRITO = RESET = ""


# =============================================================================
# SEÇÃO 1: INFRAESTRUTURA DO TERMINAL
# =============================================================================

def limpar_tela():
    """
    Limpa o conteúdo visível do terminal de forma cross-platform.

    Por que isso importa?
        Sem limpar a tela, o menu acumula no terminal a cada iteração.
        Limpar melhora drasticamente a experiência visual.

    Comandos utilizados:
        - 'cls'   → Windows (Command Prompt e PowerShell)
        - 'clear' → Linux e macOS (bash, zsh, etc.)

    os.name retorna:
        'nt'    → Windows
        'posix' → Linux / macOS
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def ativar_cores_windows():
    """
    Habilita o processamento de códigos de escape ANSI no terminal do Windows.

    Problema:
        Por padrão, o Windows PowerShell e o CMD antigo não processam
        os códigos ANSI (\033[92m etc.) — eles aparecem como texto literal.

    Solução:
        Usa a API do Windows (via ctypes) para ativar o modo
        ENABLE_VIRTUAL_TERMINAL_PROCESSING (código 0x0004) no handle stdout.
        Isso faz o Windows processar os códigos ANSI corretamente.

    Segurança:
        O try/except garante que se essa chamada falhar (terminal sem suporte
        ou ambiente sem permissão), o programa continua sem travar.
    """
    if os.name == 'nt':  # Só executa no Windows
        try:
            kernel32 = ctypes.windll.kernel32
            stdout_handle = kernel32.GetStdHandle(-11)  # -11 = STDOUT
            modo = ctypes.c_ulong()
            kernel32.GetConsoleMode(stdout_handle, ctypes.byref(modo))
            # Ativa o bit ENABLE_VIRTUAL_TERMINAL_PROCESSING com OR bit a bit
            kernel32.SetConsoleMode(stdout_handle, modo.value | 0x0004)
        except Exception:
            pass  # Silenciosamente ignora se não funcionar (terminal sem suporte)


# =============================================================================
# SEÇÃO 2: INTERFACE DO MENU
# =============================================================================

def exibir_menu_principal():
    """
    Exibe o menu principal estilizado com ASCII art e opções coloridas.

    Estrutura visual:
        - Cabeçalho em ASCII art com título do sistema
        - Linha separadora
        - Opções numeradas com cores para destacar os números
        - Linha separadora de fechamento

    As variáveis de cor (VERDE, CIANO, etc.) são globais e se ajustam
    automaticamente ao USAR_CORES definido no topo do arquivo.
    """
    print(f"{CIANO}{NEGRITO}")
    print(r"  ___ _  _     ___ ___ ___ _   _ ___ ___ _____     __")
    print(r" |_ _| \| |___/ __| __/ __| | | | _ \_ _|_   _\ \ / /")
    print(r"  | || .` |___\__ \ _| (__| |_| |   /| |  | |  \ V / ")
    print(r" |___|_|\_|   |___/___\\___|\___/|_|_\___| |_|   |_|  ")
    print(f"            [ SECURE INVENTORY SYSTEM v1.0 ]{RESET}")
    print(f"{AZUL}======================================================={RESET}")

    # Cada opção: número em amarelo + descrição em branco padrão
    print(f"{AMARELO} 1.{RESET} Adicionar Novo Produto")
    print(f"{AMARELO} 2.{RESET} Remover Produto por ID")
    print(f"{AMARELO} 3.{RESET} Atualizar Dados de Produto")
    print(f"{AMARELO} 4.{RESET} Listar Todos os Produtos (Ordenados)")
    print(f"{AMARELO} 5.{RESET} Buscar Produto por ID")
    print(f"{AMARELO} 6.{RESET} Buscar por Nome (Linear — aceita nome parcial)")
    print(f"{AMARELO} 7.{RESET} Buscar por Nome (Binária — requer nome exato)")
    print(f"{AMARELO} 8.{RESET} Exibir Relatório Estatístico")
    print(f"{AMARELO} 9.{RESET} Mudar Usuário/Senha de Acesso")
    print(f"{VERMELHO} 0.{RESET} Salvar e Encerrar Sistema")

    print(f"{AZUL}======================================================={RESET}")


def imprimir_tabela_produtos(lista_produtos: list):
    """
    Exibe uma lista de produtos em formato de tabela alinhada no terminal.

    Formatação:
        - Cada coluna tem largura fixa definida pelo especificador :<N>
        - Produtos importados exibidos em amarelo; nacionais em azul
        - A cor RESET garante que o estilo não "vaze" para o próximo print

    Formato das colunas:
        ID (7) | NOME (28) | QTD (6) | PREÇO (12) | ORIGEM (10)

    Args:
        lista_produtos (list): Lista de listas no formato [id, nome, qtd, preco, importado]
                               Compatível com a saída de converter_para_lista e busca
    """
    if not lista_produtos:
        print(f"\n{VERMELHO}  Nenhum produto cadastrado ou encontrado.{RESET}")
        return

    # Cabeçalho da tabela com formatação negrito
    print(f"\n{NEGRITO}{'ID':<7} | {'NOME DO PRODUTO':<28} | {'QTD':<6} | {'PREÇO (R$)':<12} | {'ORIGEM':<10}{RESET}")
    print("-" * 72)  # Linha divisória de 72 caracteres

    for prod in lista_produtos:
        # prod[4] = importado (bool) — define a cor e o texto da origem
        if prod[4]:
            origem = f"{AMARELO}Importado{RESET}"
        else:
            origem = f"{AZUL}Nacional {RESET}"

        # Imprime a linha formatada com larguras fixas para alinhamento de colunas
        # prod[3]:<12.2f → preço com 2 casas decimais em campo de 12 chars
        print(f"{prod[0]:<7} | {prod[1]:<28} | {prod[2]:<6} | {prod[3]:<12.2f} | {origem}")


# =============================================================================
# SEÇÃO 3: FLUXO PRINCIPAL
# =============================================================================

def main():
    """
    Função principal — ponto de entrada e orquestrador do fluxo completo.

    Sequência de execução:
        1. Ativa suporte a cores ANSI no Windows
        2. Limpa a tela para apresentação limpa
        3. Executa autenticação — aborta se falhar (sys.exit)
        4. Carrega o inventário cifrado do CSV para o dicionário em RAM
        5. Entra no loop do menu interativo
        6. Ao sair (opção 0): salva se houver modificações pendentes
    """
    # Passo 1: Configura o terminal para aceitar cores (Windows precisa disso)
    ativar_cores_windows()
    limpar_tela()

    # Passo 2: Autenticação obrigatória — nenhuma funcionalidade sem login
    print(f"{CIANO}=== IN-SECURITY — Secure Inventory System ==={RESET}")
    if not auth.realizar_login():
        # realizar_login retorna False após 3 tentativas fracassadas
        print(f"{VERMELHO}Sistema encerrado por segurança.{RESET}")
        sys.exit()  # Encerra completamente o programa

    # Passo 3: Carrega os dados do CSV (decifra automaticamente durante o carregamento)
    inventario = inventory.carregar_inventario()
    print(f"\n{VERDE}✔ Inventário carregado: {len(inventario)} produto(s) em memória.{RESET}")
    time.sleep(1.2)  # Breve pausa para o usuário ver a confirmação

    # Flag de controle: indica se houve qualquer modificação durante a sessão
    # Evita reescrever o CSV desnecessariamente se nada foi alterado
    modificado = False

    # Passo 4: Loop principal do menu
    while True:
        limpar_tela()
        exibir_menu_principal()
        opcao = input(f"\n{NEGRITO}Selecione uma operação (0-9):{RESET} ").strip()

        # ── Opção 1: Adicionar produto ──────────────────────────────────────
        if opcao == "1":
            if inventory.adicionar_produto(inventario):
                modificado = True  # Marca que há dados não salvos
            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 2: Remover produto ─────────────────────────────────────────
        elif opcao == "2":
            if inventory.remover_produto(inventario):
                modificado = True
            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 3: Atualizar produto ────────────────────────────────────────
        elif opcao == "3":
            if inventory.atualizar_produto(inventario):
                modificado = True
            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 4: Listar todos os produtos ordenados ────────────────────────
        elif opcao == "4":
            # obter_inventario_ordenado decide automaticamente Bubble Sort vs Merge Sort
            lista_ordenada = sorting.obter_inventario_ordenado(inventario)
            print(f"\n{VERDE}>>> PRODUTOS ORDENADOS ALFABETICAMENTE POR NOME <<<{RESET}")
            imprimir_tabela_produtos(lista_ordenada)
            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 5: Busca direta por ID ─────────────────────────────────────
        elif opcao == "5":
            print(f"\n{CIANO}--- BUSCA POR ID ---{RESET}")
            try:
                id_prod = int(input("Informe o ID do produto: "))
                if id_prod in inventario:
                    # Dicionário Python: acesso por chave é O(1) — instantâneo
                    dados = inventario[id_prod]
                    imprimir_tabela_produtos([[id_prod] + dados])
                else:
                    print(f"{VERMELHO}❌ ID {id_prod} não cadastrado no sistema.{RESET}")
            except ValueError:
                print(f"{VERMELHO}❌ ID inválido. Digite apenas números.{RESET}")
            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 6: Busca linear por nome (parcial) ─────────────────────────
        elif opcao == "6":
            print(f"\n{CIANO}--- BUSCA LINEAR POR NOME (aceita nome parcial) ---{RESET}")
            nome = input("Digite o nome ou trecho do produto: ")
            resultados = search.busca_linear_por_nome(inventario, nome)

            if resultados:
                print(f"{VERDE}✔ {len(resultados)} produto(s) encontrado(s):{RESET}")
                imprimir_tabela_produtos(resultados)
            else:
                print(f"{VERMELHO}❌ Nenhum produto com '{nome}' no nome.{RESET}")

            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 7: Busca binária por nome (exato) ──────────────────────────
        elif opcao == "7":
            print(f"\n{CIANO}--- BUSCA BINÁRIA POR NOME (nome EXATO necessário) ---{RESET}")
            print(f"{AMARELO}⚠ Atenção: A busca binária exige o nome completo e exato do produto.{RESET}")
            nome = input("Digite o nome EXATO do produto: ")
            resultado = search.busca_binaria_por_nome(inventario, nome)

            if resultado:
                print(f"{VERDE}✔ Produto encontrado:{RESET}")
                imprimir_tabela_produtos([resultado])
            else:
                print(f"{VERMELHO}❌ Nenhum produto com nome exato '{nome}'.{RESET}")
                print(f"   Dica: Use a busca linear (opção 6) para busca por nome parcial.")

            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 8: Relatório estatístico ────────────────────────────────────
        elif opcao == "8":
            stats.exibir_estatisticas(inventario)
            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 9: Alterar credenciais ──────────────────────────────────────
        elif opcao == "9":
            auth.alterar_credenciais()
            input(f"\nPressione {NEGRITO}Enter{RESET} para continuar...")

        # ── Opção 0: Salvar e encerrar ─────────────────────────────────────────
        elif opcao == "0":
            if modificado:
                # Há dados pendentes → cifra e grava no CSV antes de sair
                print(f"\n{AMARELO}Gravando alterações cifradas no inventario.csv...{RESET}")
                inventory.salvar_inventario(inventario)
                print(f"{VERDE}✔ Dados cifrados e persistidos com segurança.{RESET}")
            else:
                # Nenhuma modificação → não reescreve o CSV (mais eficiente)
                print(f"\n{VERDE}Nenhuma alteração pendente. CSV preservado.{RESET}")

            print(f"{CIANO}Sistema encerrado com segurança. Até logo!{RESET}")
            break  # Sai do while True → termina o programa naturalmente

        # ── Comando secreto "99" — Easter egg ──────────────────────────────────
        elif opcao == "99":
            # Ativa o evento narrativo completo (produto secreto + policia + hacking + wipe)
            wipe_executado = secret.ativar_evento_secreto(inventario)
            # Após o evento, encerra de qualquer forma:
            # - Wipe bem-sucedido: nao ha mais dados para salvar
            # - Falha (capturado): narrativa encerrada, nao faz sentido continuar
            if wipe_executado:
                print(f"{VERMELHO}Sistema encerrado. Nenhum dado restante.{RESET}")
            else:
                print(f"{AMARELO}Encerrando sistema apos o evento.{RESET}")
            break  # Sai do loop sem tentar salvar arquivos ja apagados

        # ── Opcao invalida ─────────────────────────────────────────────────────
        else:
            print(f"{VERMELHO}Opcao '{opcao}' invalida. Escolha entre 0 e 9.{RESET}")
            time.sleep(1.5)  # Pausa para o usuario ler a mensagem antes de limpar


# =============================================================================
# PONTO DE ENTRADA DO PYTHON
# =============================================================================

if __name__ == "__main__":
    # Este bloco só executa quando main.py é rodado diretamente:
    #   python main.py  → executa
    # Não executa se main.py for importado como módulo por outro arquivo.
    # Isso é uma boa prática Python — protege o código de efeitos colaterais
    # indesejados ao importar o módulo em testes ou outros scripts.
    main()
