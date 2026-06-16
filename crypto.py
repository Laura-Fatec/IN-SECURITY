"""
=============================================================================
MÓDULO: crypto.py — Criptografia e Hashing
=============================================================================
Responsabilidade:
    Centralizar TODAS as operações criptográficas do sistema, separando
    completamente a lógica de segurança do restante da aplicação.

Técnicas utilizadas:
    1. SHA-256  → Hashing unidirecional para senhas (não é possível reverter)
    2. Cifra de César → Criptografia simétrica leve para dados do inventário

Por que SHA-256 para senhas?
    - É uma função de hash: transforma qualquer texto em um código fixo de 64 chars
    - É IRREVERSÍVEL: não existe função de "descriptografar" — só dá pra comparar
    - Mesmo uma vírgula diferente gera um hash completamente diferente
    - Padrão da indústria para armazenamento seguro de credenciais
=============================================================================
"""

import hashlib  # Biblioteca nativa do Python para funções de hash criptográfico


# =============================================================================
# SEÇÃO 1: HASHING (Para Senhas — Unidirecional)
# =============================================================================

def calcular_sha256(texto: str) -> str:
    """
    Converte qualquer texto em um hash SHA-256 de 64 caracteres hexadecimais.

    Como funciona:
        1. Codifica o texto em bytes (UTF-8 para suportar acentos)
        2. Passa pelo algoritmo SHA-256 da biblioteca hashlib
        3. Retorna o resultado em formato hexadecimal legível (ex: "a3f1b2...")

    Por que usar isso para senhas?
        - A senha NUNCA fica salva em texto puro no arquivo login.txt
        - No login, a senha digitada é hasheada e COMPARADA com o hash salvo
        - Se um atacante roubar o arquivo login.txt, só verá hashes inúteis

    Args:
        texto (str): Qualquer string — nome de usuário, senha, etc.

    Returns:
        str: Hash SHA-256 em hexadecimal (sempre 64 caracteres)

    Exemplo:
        calcular_sha256("admin") → "8c6976e5b5410415bde908bd4dee15..."
        calcular_sha256("admin") → "8c6976e5b5410415bde908bd4dee15..."  ← SEMPRE igual
        calcular_sha256("Admin") → "f0e4c2f76c58916ec258f246851bea..."  ← DIFERENTE!
    """
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()


# =============================================================================
# SEÇÃO 2: CIFRA DE CÉSAR (Para Inventário — Bidirecional)
# =============================================================================

def cesar_encrypt(texto, chave: int = 7) -> str:
    """
    Cifra um texto usando a Cifra de César com deslocamento configurável.

    O que é a Cifra de César?
        Cada letra do alfabeto é substituída pela letra N posições à frente.
        Com chave=7: 'a' → 'h', 'b' → 'i', 'z' → 'g' (volta ao início — módulo 26)

    Regras de comportamento:
        - Letras minúsculas (a-z): são cifradas dentro do bloco minúsculo
        - Letras maiúsculas (A-Z): são cifradas dentro do bloco maiúsculo
        - Números, pontos, vírgulas, espaços: passam SEM ALTERAÇÃO
          → Isso preserva a estrutura numérica (preços, quantidades) no CSV

    Por que usar para o inventário e não para senhas?
        - O inventário PRECISA ser lido de volta (descriptografado)
        - Senhas não precisam — só precisamos comparar hashes
        - A Cifra de César é leve e suficiente para proteger dados em repouso no CSV

    Args:
        texto: Qualquer valor (str, int, float, bool) — será convertido para str
        chave (int): Número de posições de deslocamento (padrão: 7)

    Returns:
        str: Texto cifrado

    Exemplo com chave=7:
        "Maçã 10" → "Thçh 10"  (letras deslocam, acento e número mantidos)
    """
    texto_str = str(texto)  # Garante que int/float/bool sejam tratados como string
    resultado = []

    for char in texto_str:
        if 'a' <= char <= 'z':
            # Fórmula: subtrai o valor ASCII de 'a' para normalizar (0-25),
            # aplica o deslocamento com módulo 26 (para "dar a volta" no alfabeto),
            # e soma de volta o valor ASCII de 'a' para obter a letra cifrada.
            resultado.append(chr((ord(char) - ord('a') + chave) % 26 + ord('a')))

        elif 'A' <= char <= 'Z':
            # Mesma lógica, mas normalizado em relação a 'A' para maiúsculas
            resultado.append(chr((ord(char) - ord('A') + chave) % 26 + ord('A')))

        else:
            # Caracteres não-alfabéticos (números, pontos, vírgulas) passam intactos
            resultado.append(char)

    return "".join(resultado)


def cesar_decrypt(texto_cifrado: str, chave: int = 7) -> str:
    """
    Reverte a Cifra de César, recuperando o texto original.

    Princípio matemático:
        Cifrar com chave K é o mesmo que decifrar com chave (26 - K).
        Portanto, a descriptografia reutiliza o mesmo algoritmo de cifragem,
        apenas invertendo a direção do deslocamento.

    Exemplo:
        cesar_encrypt("hello", 7) → "olssv"
        cesar_decrypt("olssv", 7) → "hello"  ← texto original restaurado

    Args:
        texto_cifrado (str): Texto que foi cifrado com cesar_encrypt
        chave (int): A MESMA chave usada na cifragem (padrão: 7)

    Returns:
        str: Texto original, descriptografado
    """
    # Decifrar com chave K = Cifrar com (26 - K)
    # Exemplo: chave=7 → decifra com chave=19 (7+19=26, volta ao início)
    return cesar_encrypt(texto_cifrado, 26 - chave)
