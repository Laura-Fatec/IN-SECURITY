"""
=============================================================================
MÓDULO: auth.py — Autenticação e Controle de Acesso
=============================================================================
Responsabilidade:
    Gerenciar todo o ciclo de vida de autenticação:
    - Primeiro acesso (criação do admin)
    - Login com limite de tentativas (proteção contra força bruta)
    - Alteração de credenciais
    - Geração de logs de auditoria (security.log)

Segurança implementada:
    1. Senhas nunca armazenadas em texto puro → apenas hash SHA-256
    2. Nomes de usuário também hasheados → nomes nunca expostos no arquivo
    3. Limite de 3 tentativas → dificulta ataques de força bruta (brute force)
    4. getpass → senha digitada é invisível no terminal
    5. Log de auditoria → rastreia TODOS os eventos de acesso

Fluxo de armazenamento (login.txt):
    O arquivo contém UMA linha no formato:
        HASH_USUARIO|HASH_SENHA
    Ambos são hashes SHA-256 de 64 caracteres — nada em texto legível.
=============================================================================
"""

import os           # Para verificar existência de arquivos e consultar o sistema
import sys          # Para encerrar o programa em caso de falha crítica
from datetime import datetime   # Para registrar timestamps nos logs
import getpass      # Para ocultar a senha durante a digitação no terminal
from crypto import calcular_sha256  # Nossa função de hashing SHA-256


# =============================================================================
# CONFIGURAÇÃO GLOBAL
# =============================================================================

ARQUIVO_LOGIN = "login.txt"     # Arquivo que armazena os hashes do administrador
ARQUIVO_LOG = "security.log"    # Arquivo de auditoria de eventos de segurança
MAX_TENTATIVAS = 3              # Número máximo de tentativas de login permitidas


# =============================================================================
# SEÇÃO 1: AUDITORIA (Log de Segurança)
# =============================================================================

def registrar_log(usuario: str, acao: str):
    """
    Grava um evento de segurança no arquivo de auditoria (security.log).

    Por que ter logs de segurança?
        - Permite rastrear quem acessou o sistema e quando
        - Detectar tentativas de invasão (muitas falhas de login seguidas)
        - Comprovar ações em caso de incidente de segurança
        - Boas práticas de compliance e auditoria

    Formato de cada linha no log:
        [2024-01-15 14:32:07] USUÁRIO: admin | AÇÃO: LOGIN - Acesso concedido

    Args:
        usuario (str): Nome do usuário que gerou o evento (em texto puro para legibilidade no log)
        acao (str): Descrição do evento ocorrido
    """
    # Formata o timestamp atual no padrão ISO (data e hora legíveis)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Abre o arquivo em modo APPEND ("a") — nunca apaga o histórico anterior
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] USUÁRIO: {usuario} | AÇÃO: {acao}\n")


# =============================================================================
# SEÇÃO 2: INICIALIZAÇÃO DO SISTEMA
# =============================================================================

def inicializar_autenticacao():
    """
    Garante que o sistema tenha um administrador configurado antes do primeiro uso.

    Quando é executada?
        - Sempre no início do login
        - Só faz algo se login.txt não existir OU estiver vazio

    Fluxo:
        1. Verifica se login.txt existe e tem conteúdo
        2. Se não → solicita criação do primeiro administrador
        3. Hasheia usuário e senha com SHA-256
        4. Salva APENAS os hashes (nunca o texto original) no login.txt
        5. Registra o evento no log de auditoria
    """
    # Verifica se o arquivo de login não existe ou está vazio (tamanho 0 bytes)
    if not os.path.exists(ARQUIVO_LOGIN) or os.stat(ARQUIVO_LOGIN).st_size == 0:
        print("\n=== CONFIGURAÇÃO INICIAL DO SISTEMA ===")
        print("Nenhum usuário administrativo encontrado.")

        # Loop para garantir que o usuário não seja deixado em branco
        usuario = input("Defina o nome de usuário: ").strip()
        while not usuario:
            print("❌ O usuário não pode ser vazio.")
            usuario = input("Defina o nome de usuário: ").strip()

        # getpass.getpass() → exibe prompt mas NÃO mostra o que o usuário digita
        # Isso evita que a senha apareça no terminal (shoulder surfing)
        senha = getpass.getpass("Defina a senha (invisível): ").strip()
        while not senha:
            print("❌ A senha não pode ser vazia.")
            senha = getpass.getpass("Defina a senha (invisível): ").strip()

        # Calcula os hashes SHA-256 — o texto original NUNCA é salvo
        hash_user = calcular_sha256(usuario)
        hash_senha = calcular_sha256(senha)

        # Salva no arquivo apenas os hashes, separados por "|"
        with open(ARQUIVO_LOGIN, "w", encoding="utf-8") as f:
            f.write(f"{hash_user}|{hash_senha}")

        print("✔ Administrador configurado com sucesso!\n")

        # Registra o evento histórico de criação do sistema
        registrar_log(usuario, "SISTEMA INICIALIZADO - Primeiro administrador criado")


# =============================================================================
# SEÇÃO 3: FLUXO DE LOGIN
# =============================================================================

def realizar_login() -> bool:
    """
    Executa o fluxo completo de autenticação com proteção contra força bruta.

    Segurança implementada:
        - Máximo de MAX_TENTATIVAS (3) tentativas consecutivas
        - Senha invisível via getpass (não aparece no terminal)
        - Cada tentativa é comparada via hash SHA-256 (nunca texto puro)
        - Todos os eventos (sucesso ou falha) são registrados no log

    Proteção contra força bruta:
        Um atacante que tente senhas aleatoriamente será bloqueado
        após 3 tentativas, e cada tentativa fica registrada no log
        com timestamp — facilitando a detecção do ataque.

    Returns:
        bool: True se login bem-sucedido, False se bloqueado por tentativas
    """
    # Garante que o admin existe antes de tentar autenticar
    inicializar_autenticacao()

    # Lê os hashes salvos do arquivo de login
    with open(ARQUIVO_LOGIN, "r", encoding="utf-8") as f:
        linha = f.read().strip()
        hash_user_salvo, hash_senha_salvo = linha.split("|")

    tentativas = MAX_TENTATIVAS
    usuario = ""  # Inicializa para uso no log de bloqueio

    while tentativas > 0:
        print(f"\n--- AUTENTICAÇÃO (Tentativas restantes: {tentativas}) ---")
        usuario = input("Usuário: ").strip()

        # Senha digitada fica invisível no terminal — crucial para segurança física
        senha = getpass.getpass("Senha (invisível): ").strip()

        # Compara os hashes — NUNCA compara texto puro com texto puro
        # calcular_sha256(digitado) deve ser igual ao hash armazenado
        if (calcular_sha256(usuario) == hash_user_salvo and
                calcular_sha256(senha) == hash_senha_salvo):

            print("✔ Acesso concedido!")
            registrar_log(usuario, "LOGIN - Acesso concedido")
            return True  # Sinal verde para o main.py continuar

        else:
            tentativas -= 1
            print(f"❌ Usuário ou senha incorretos. Tentativas restantes: {tentativas}")

            # Registra CADA falha para rastrear possíveis ataques
            registrar_log(
                usuario,
                f"FALHA DE LOGIN - Tentativa incorreta (Restam {tentativas} tentativas)"
            )

    # Chegou aqui: esgotou todas as tentativas sem sucesso
    print("❌ Acesso negado. Limite de tentativas excedido.")
    registrar_log(usuario, "BLOQUEIO - Limite de tentativas de login excedido")
    return False  # Sinal vermelho → main.py encerrará o programa


# =============================================================================
# SEÇÃO 4: ALTERAÇÃO DE CREDENCIAIS
# =============================================================================

def alterar_credenciais():
    """
    Permite que o administrador logado altere seu usuário e senha de acesso.

    Segurança:
        - Nova senha também é invisível durante digitação (getpass)
        - Novos dados são hasheados antes de salvar — mesma proteção do cadastro
        - O evento é registrado no log de auditoria

    Nota de segurança:
        Em sistemas de produção reais, seria exigida a senha ATUAL antes
        de permitir a alteração. Aqui, como o usuário já está autenticado
        no sistema, essa validação extra foi omitida por simplicidade.
    """
    print("\n--- ALTERAR CREDENCIAIS DE ACESSO ---")

    novo_usuario = input("Novo usuário: ").strip()

    # Nova senha também fica invisível
    novo_senha = getpass.getpass("Nova senha (invisível): ").strip()

    # Validação: nem usuário nem senha podem ser vazios
    if not novo_usuario or not novo_senha:
        print("❌ Operação cancelada: Usuário e senha não podem ser vazios.")
        return

    # Aplica hashing nos novos dados antes de salvar
    hash_user = calcular_sha256(novo_usuario)
    hash_senha = calcular_sha256(novo_senha)

    # Sobrescreve o arquivo — mode "w" apaga o conteúdo anterior completamente
    with open(ARQUIVO_LOGIN, "w", encoding="utf-8") as f:
        f.write(f"{hash_user}|{hash_senha}")

    print("✔ Credenciais alteradas com sucesso!")
    registrar_log(novo_usuario, "ALTERAÇÃO DE CREDENCIAIS - Dados de login modificados")
