"""
=============================================================================
MÓDULO: secret.py — Evento Secreto "Produto 99"
=============================================================================
Easter egg oculto ativado quando o usuário digita "99" no menu principal.

Fluxo narrativo:
    ACO 1 — Produto encontrado: ACTION FIGURE Megan Fox Hiper-Realista™
    ATO 2 — Alerta: a polícia estava monitorando. Conexão interceptada.
    ATO 3 — Minigame de hacking: decifre 3 códigos para iniciar o wipe
    ATO 4 — Autodestruição dramática com contagem regressiva
    ATO 5 — Sistema apaga login.txt, inventario.csv e security.log

Técnicas narrativas de terminal usadas:
    - Digitação letra a letra (efeito typewriter) para criar tensão
    - time.sleep() estratégico para ritmo cinematográfico
    - ASCII art para impacto visual
    - Cifra de César como mecânica do minigame (reusa crypto.py!)
    - Barra de progresso fake para simular o wipe
=============================================================================
"""

import os
import sys
import time
import random
from crypto import cesar_decrypt   # Reusa o módulo de crypto do próprio projeto!


# =============================================================================
# CORES ANSI — detecta automaticamente se o terminal suporta
# =============================================================================
import os as _os, ctypes as _ctypes

def _suporta_ansi() -> bool:
    if _os.name == 'nt':
        try:
            k = _ctypes.windll.kernel32
            h = k.GetStdHandle(-11)
            m = _ctypes.c_ulong()
            k.GetConsoleMode(h, _ctypes.byref(m))
            return k.SetConsoleMode(h, m.value | 0x0004) != 0
        except Exception:
            return False
    return True

if _suporta_ansi():
    VERDE    = '\033[92m'
    VERMELHO = '\033[91m'
    AZUL     = '\033[94m'
    CIANO    = '\033[96m'
    AMARELO  = '\033[93m'
    MAGENTA  = '\033[95m'
    NEGRITO  = '\033[1m'
    RESET    = '\033[0m'
    BLINK    = '\033[5m'
else:
    VERDE = VERMELHO = AZUL = CIANO = AMARELO = MAGENTA = NEGRITO = RESET = BLINK = ""



# =============================================================================
# UTILITÁRIOS DE NARRATIVA
# =============================================================================

def _digitar(texto: str, delay: float = 0.035, cor: str = ""):
    """
    Imprime o texto letra por letra, simulando digitação em tempo real.

    Usado para criar suspense e dar ritmo cinematográfico às cenas.
    O delay padrão de 35ms por caractere simula uma digitação rápida.

    Args:
        texto (str): Texto a ser "digitado"
        delay (float): Pausa em segundos entre cada caractere
        cor (str): Código ANSI de cor (opcional)
    """
    print(cor, end="", flush=True)
    for char in texto:
        print(char, end="", flush=True)
        time.sleep(delay)
    print(RESET)


def _pause(segundos: float):
    """Pausa com pontinhos de suspense."""
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(segundos / 3)
    print()


def _barra_progresso(label: str, total: int = 30, cor: str = VERDE):
    """
    Exibe uma barra de progresso animada no terminal.

    Args:
        label (str): Texto exibido antes da barra
        total (int): Número de blocos da barra (largura)
        cor (str): Cor ANSI dos blocos preenchidos
    """
    print(f"\n{label}")
    print("[", end="", flush=True)
    for i in range(total):
        time.sleep(random.uniform(0.03, 0.12))  # Velocidade irregular = mais realista
        print(f"{cor}█{RESET}", end="", flush=True)
    print(f"] {VERDE}CONCLUÍDO{RESET}\n")


# =============================================================================
# ATO 1: PRODUTO SECRETO ENCONTRADO
# =============================================================================

def _ato1_produto_secreto():
    """
    Exibe o produto secreto ID 99 com toda a pompa que merece.
    Uma action figure da Megan Fox. Hiper-realista. Obviamente ilegal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    _digitar("\n[SISTEMA] Consultando banco de dados restrito...", 0.03, CIANO)
    time.sleep(0.8)
    _digitar("[SISTEMA] Produto ID #99 localizado.", 0.03, CIANO)
    time.sleep(0.5)

    print(f"\n{AMARELO}{'═' * 60}{RESET}")
    print(f"""
{MAGENTA}{NEGRITO}
        ██████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗████████╗ ██████╗
        ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
        ██████╔╝██████╔╝██║   ██║██║  ██║██║   ██║   ██║   ██║   ██║
        ██╔═══╝ ██╔══██╗██║   ██║██║  ██║██║   ██║   ██║   ██║   ██║
        ██║     ██║  ██║╚██████╔╝██████╔╝╚██████╔╝   ██║   ╚██████╔╝
        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝
{RESET}""")
    print(f"{AMARELO}{'═' * 60}{RESET}")

    time.sleep(0.5)

    print(f"""
  {NEGRITO}ID:{RESET}         #99  {VERMELHO}[CLASSIFICADO]{RESET}
  {NEGRITO}PRODUTO:{RESET}    ACTION FIGURE — Megan Fox Hiper-Realista™
  {NEGRITO}EDIÇÃO:{RESET}     Transformers: Revenge of the Fallen (2009)
  {NEGRITO}ESCALA:{RESET}     1:1  {VERMELHO}(tamanho real){RESET}
  {NEGRITO}MATERIAL:{RESET}   Silicone grau médico + IA generativa embutida
  {NEGRITO}ORIGEM:{RESET}     {VERMELHO}ALTAMENTE IMPORTADO{RESET} (Fábrica clandestina, Macau)
  {NEGRITO}PREÇO:{RESET}      R$ 14.999,99
  {NEGRITO}ESTOQUE:{RESET}    1 unidade  {AMARELO}(única no mundo){RESET}
  {NEGRITO}STATUS:{RESET}     {VERMELHO}{BLINK}⚠ VENDA PROIBIDA — INTERPOL CIENTE ⚠{RESET}
    """)

    print(f"{AMARELO}{'═' * 60}{RESET}")
    time.sleep(1.2)


# =============================================================================
# ATO 2: ALERTA — A POLÍCIA ESTAVA MONITORANDO
# =============================================================================

def _ato2_alerta_policia():
    """
    A revirada. A polícia estava monitorando o acesso ao produto ID 99.
    Interceptação de conexão em andamento.
    """
    time.sleep(0.5)
    _digitar("\n[SISTEMA] Registrando consulta no log de auditoria...", 0.03, CIANO)
    time.sleep(1.0)

    # O alerta chega como uma "interrupção" inesperada
    print(f"\n\n{VERMELHO}{NEGRITO}")
    print("  ██╗███╗   ██╗████████╗███████╗██████╗  ██████╗███████╗██████╗ ████████╗ ██████╗ ")
    print("  ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗")
    print("  ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██║     █████╗  ██████╔╝   ██║   ██║   ██║")
    print("  ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██║     ██╔══╝  ██╔═══╝    ██║   ██║   ██║")
    print("  ██║██║ ╚████║   ██║   ███████╗██║  ██║╚██████╗███████╗██║        ██║   ╚██████╔╝")
    print("  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝        ╚═╝    ╚═════╝ ")
    print(f"{RESET}")

    time.sleep(0.3)

    _digitar(">>> CONEXÃO INTERCEPTADA PELA INTERPOL <<<", 0.04, VERMELHO)
    time.sleep(0.4)
    _digitar(">>> UNIDADE CIBER-CRIME BRASIL — OPERAÇÃO FOX HUNT <<<", 0.04, VERMELHO)
    time.sleep(0.8)

    print(f"\n{AMARELO}[INTERCEPTAÇÃO] Transmissão em andamento...{RESET}\n")
    time.sleep(0.5)

    # "Transmissão" da polícia chegando no terminal
    mensagens_policia = [
        ("DELTA-7 PARA BASE: temos um positivo no produto restrito #99.", CIANO),
        ("BASE PARA DELTA-7: confirme coordenadas do terminal.", CIANO),
        ("DELTA-7: IP rastreado. Localização confirmada. ETA: 4 minutos.", VERMELHO),
        ("BASE: autorizado uso de força. Não deixem apagar as evidências.", VERMELHO),
        ("DELTA-7: ENTENDIDO. A caminho.", VERMELHO),
    ]

    for msg, cor in mensagens_policia:
        _digitar(f"  [RADIO] {msg}", 0.025, cor)
        time.sleep(random.uniform(0.3, 0.7))

    time.sleep(0.8)
    print(f"\n{VERMELHO}{NEGRITO}  ⚠ VOCÊ TEM MENOS DE 4 MINUTOS PARA APAGAR TUDO ⚠{RESET}\n")
    time.sleep(1.0)

    input(f"{AMARELO}  [Pressione ENTER para tentar acessar o protocolo de autodestruição...]{RESET}")


# =============================================================================
# ATO 3: MINIGAME DE HACKING — Decifrar códigos com Cifra de César
# =============================================================================

def _ato3_hacking_minigame() -> bool:
    """
    Minigame: o usuário precisa decifrar 3 códigos cifrados com César para
    desbloquear o protocolo de wipe. Reusa a lógica de crypto.py do projeto.

    Mecânica:
        - Cada rodada mostra um texto cifrado com uma chave diferente
        - O usuário digita o que acha que é o texto original
        - 3 acertos (não necessariamente consecutivos) = acesso liberado
        - 3 erros = bloqueio total (a polícia chega primeiro)

    Returns:
        bool: True se o usuário passou no minigame, False se falhou
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{VERMELHO}{NEGRITO}")
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║         PROTOCOLO DE AUTODESTRUIÇÃO — BLOQUEADO         ║")
    print("  ║      Decifre os códigos para liberar o WIPE TOTAL       ║")
    print("  ╚══════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

    time.sleep(0.5)
    _digitar("[SISTEMA] O protocolo de wipe está protegido por 3 camadas de cifra.", 0.03, CIANO)
    _digitar("[SISTEMA] Cada código usa um deslocamento diferente da Cifra de César.", 0.03, CIANO)
    _digitar("[SISTEMA] Decifre todos os 3 para liberar a autodestruição.", 0.03, AMARELO)
    time.sleep(0.8)

    # Definição dos desafios: (texto_original, chave_usada, dica)
    # O texto cifrado é gerado dinamicamente aplicando cesar_encrypt
    desafios = [
        {
            "original":  "APAGAR TUDO",
            "chave":      3,
            "dica":      "Chave: 3  |  A→D, P→S, A→D...",
            "cifrado":   "",   # preenchido abaixo
        },
        {
            "original":  "WIPE CONFIRMED",
            "chave":     13,
            "dica":      "Chave: 13  |  ROT13 clássico  (A→N, W→J...)",
            "cifrado":   "",
        },
        {
            "original":  "EXECUTE PROTOCOL ZERO",
            "chave":      7,
            "dica":      "Chave: 7  |  a mesma do inventário (E→L, X→E...)",
            "cifrado":   "",
        },
    ]

    # Importa encrypt para gerar os textos cifrados dos desafios
    from crypto import cesar_encrypt
    for d in desafios:
        d["cifrado"] = cesar_encrypt(d["original"], d["chave"])

    acertos = 0
    erros   = 0
    MAX_ERROS = 3

    for i, desafio in enumerate(desafios, start=1):
        print(f"\n{AMARELO}{'─' * 55}{RESET}")
        print(f"{NEGRITO}  CAMADA {i} DE {len(desafios)}{RESET}")
        print(f"  Código cifrado:  {VERMELHO}{NEGRITO}{desafio['cifrado']}{RESET}")
        print(f"  Dica:            {AZUL}{desafio['dica']}{RESET}")
        print(f"{AMARELO}{'─' * 55}{RESET}")

        tentativas_rodada = 2  # 2 chances por desafio
        acertou_rodada = False

        while tentativas_rodada > 0:
            resposta = input(f"\n  Sua resposta (MAIÚSCULAS): ").strip().upper()

            if resposta == desafio["original"]:
                _digitar(f"  ✔ CAMADA {i} DESBLOQUEADA!", 0.04, VERDE)
                acertos += 1
                acertou_rodada = True
                time.sleep(0.4)
                break
            else:
                tentativas_rodada -= 1
                erros += 1
                if tentativas_rodada > 0:
                    _digitar(f"  ✘ Errado. {tentativas_rodada} tentativa(s) restante(s) nesta camada.", 0.03, VERMELHO)
                else:
                    _digitar(f"  ✘ CAMADA {i} FALHOU.", 0.03, VERMELHO)

            # Bloqueio antecipado se atingiu erros totais
            if erros >= MAX_ERROS:
                break

        if erros >= MAX_ERROS:
            break  # Sai do loop de desafios

    # Resultado final do minigame
    print(f"\n{AMARELO}{'═' * 55}{RESET}")

    if acertos == len(desafios):
        _digitar("  TODAS AS CAMADAS DESBLOQUEADAS. ACESSO CONCEDIDO.", 0.04, VERDE)
        time.sleep(0.5)
        return True
    elif acertos >= 2:
        # Passou em 2 de 3 — autodestruição parcial, mas aceita
        _digitar(f"  {acertos}/3 camadas desbloqueadas. Acesso parcial liberado.", 0.04, AMARELO)
        _digitar("  Iniciando wipe de emergência com permissões reduzidas...", 0.03, AMARELO)
        time.sleep(0.5)
        return True
    else:
        _digitar("  ACESSO NEGADO. FALHA NO PROTOCOLO.", 0.04, VERMELHO)
        _digitar("  Os dados permanecem intactos. A INTERPOL já chegou.", 0.04, VERMELHO)
        time.sleep(1.0)
        return False


# =============================================================================
# ATO 4 & 5: AUTODESTRUIÇÃO + WIPE REAL DOS ARQUIVOS
# =============================================================================

def _ato4_autodestruicao(inventario: dict):
    """
    Tela dramática de autodestruição com contagem regressiva e wipe real.

    O que é apagado de verdade:
        - login.txt         (credenciais hasheadas)
        - inventario.csv    (dados cifrados)
        - security.log      (log de auditoria)

    O dicionário `inventario` em RAM também é esvaziado (inventario.clear()).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"\n{VERMELHO}{NEGRITO}")
    print("  ██╗    ██╗██╗██████╗ ███████╗    ██╗███╗   ██╗██╗ ██████╗██╗ █████╗ ██████╗  ██████╗")
    print("  ██║    ██║██║██╔══██╗██╔════╝    ██║████╗  ██║██║██╔════╝██║██╔══██╗██╔══██╗██╔═══██╗")
    print("  ██║ █╗ ██║██║██████╔╝█████╗      ██║██╔██╗ ██║██║██║     ██║███████║██║  ██║██║   ██║")
    print("  ██║███╗██║██║██╔═══╝ ██╔══╝      ██║██║╚██╗██║██║██║     ██║██╔══██║██║  ██║██║   ██║")
    print("  ╚███╔███╔╝██║██║     ███████╗    ██║██║ ╚████║██║╚██████╗██║██║  ██║██████╔╝╚██████╔╝")
    print("   ╚══╝╚══╝ ╚═╝╚═╝     ╚══════╝    ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝")
    print(f"{RESET}\n")

    time.sleep(0.5)
    _digitar("  PROTOCOLO ZERO ATIVADO. INICIANDO SEQUÊNCIA DE AUTODESTRUIÇÃO.", 0.03, VERMELHO)
    time.sleep(0.4)

    # Contagem regressiva dramática
    print(f"\n{NEGRITO}  CONTAGEM REGRESSIVA:{RESET}\n")
    for i in range(5, 0, -1):
        cor = VERMELHO if i <= 2 else AMARELO
        print(f"    {cor}{NEGRITO}  {i}...{RESET}", flush=True)
        time.sleep(0.9)

    print(f"\n    {VERMELHO}{NEGRITO}{BLINK}  ZERO. EXECUTANDO WIPE.{RESET}\n")
    time.sleep(0.5)

    # Wipe dos arquivos com barra de progresso
    arquivos_para_apagar = [
        ("login.txt",        "Credenciais de administrador"),
        ("inventario.csv",   "Banco de dados do inventário"),
        ("security.log",     "Log de auditoria e rastreamento"),
    ]

    for arquivo, descricao in arquivos_para_apagar:
        print(f"  {AMARELO}[WIPE]{RESET} {descricao} ({arquivo})")
        _barra_progresso(f"  ", total=25, cor=VERMELHO)

        if os.path.exists(arquivo):
            # Sobrescreve com zeros antes de deletar (wipe seguro)
            try:
                tamanho = os.path.getsize(arquivo)
                with open(arquivo, "wb") as f:
                    f.write(b'\x00' * tamanho)   # Sobrescreve com bytes nulos
                os.remove(arquivo)               # Depois deleta
            except Exception:
                pass   # Se não conseguir apagar, continua silenciosamente

    # Limpa o dicionário em RAM também
    inventario.clear()

    time.sleep(0.5)

    # Tela final
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{VERDE}{NEGRITO}")
    print("  ██████╗  █████╗ ██████╗  ██████╗ ███████╗    █████╗ ██████╗  █████╗  ██████╗  █████╗ ██████╗  ██████╗ ███████╗")
    print("  ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔════╝   ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔══██╗██╔═══██╗██╔════╝")
    print("  ██║  ██║███████║██║  ██║██║   ██║███████╗   ███████║██████╔╝███████║██║  ███╗███████║██║  ██║██║   ██║███████╗")
    print("  ██║  ██║██╔══██║██║  ██║██║   ██║╚════██║   ██╔══██║██╔══██╗██╔══██║██║   ██║██╔══██║██║  ██║██║   ██║╚════██║")
    print("  ██████╔╝██║  ██║██████╔╝╚██████╔╝███████║   ██║  ██║██║  ██║██║  ██║╚██████╔╝██║  ██║██████╔╝╚██████╔╝███████║")
    print("  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝")
    print(f"{RESET}\n")

    time.sleep(0.4)
    _digitar("  Todos os arquivos foram destruídos com segurança.", 0.03, VERDE)
    _digitar("  Nenhuma evidência encontrável.", 0.03, VERDE)
    _digitar("  A action figure? Nunca existiu.", 0.03, AMARELO)

    time.sleep(0.8)
    print(f"\n  {CIANO}Obrigado por usar o IN-SECURITY System.{RESET}")
    print(f"  {CIANO}Fique seguro. Ou não. Você escolheu a segunda opção.{RESET}\n")
    time.sleep(2.0)


# =============================================================================
# FINAL ALTERNATIVO: O USUÁRIO FALHOU NO MINIGAME
# =============================================================================

def _final_capturado():
    """
    Fim alternativo quando o usuário não decifra os códigos a tempo.
    A INTERPOL chega, os dados ficam intactos, game over.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"\n{VERMELHO}{NEGRITO}")
    print("  ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ ")
    print("  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗")
    print("  ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝")
    print("  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗")
    print("  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║")
    print("   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝")
    print(f"{RESET}\n")

    mensagens_finais = [
        ("DELTA-7: Invasão confirmada. Terminal sob controle.", CIANO),
        ("DELTA-7: Dados do suspeito intactos. Enviando para análise forense.", CIANO),
        ("BASE: Bom trabalho, Delta-7. Operação Fox Hunt encerrada com êxito.", VERDE),
        ("DELTA-7: O suspeito estava tentando apagar tudo, mas falhou.", AMARELO),
        ("BASE: Mandado de prisão emitido. Aguardem a viatura.", VERMELHO),
    ]

    time.sleep(0.5)
    for msg, cor in mensagens_finais:
        _digitar(f"  [RADIO] {msg}", 0.03, cor)
        time.sleep(0.5)

    print(f"\n  {VERMELHO}{NEGRITO}Você foi capturado. A action figure da Megan Fox foi confiscada.{RESET}")
    print(f"  {AMARELO}O inventário permanece intacto como evidência.{RESET}\n")
    time.sleep(2.5)


# =============================================================================
# PONTO DE ENTRADA PÚBLICO — chamado pelo main.py
# =============================================================================

def ativar_evento_secreto(inventario: dict):
    """
    Função principal do módulo. Orquestra todos os atos do easter egg.

    Fluxo completo:
        Ato 1 → Produto secreto exibido
        Ato 2 → Alerta da polícia
        Ato 3 → Minigame de hacking (retorna True/False)
        Ato 4 → Autodestruição (se passou) ou captura (se falhou)

    Após o evento (independente do resultado), o main.py deve encerrar
    o sistema pois ou os arquivos foram apagados ou a "INTERPOL chegou".

    Args:
        inventario (dict): Dicionário do inventário passado por referência
                           (será esvaziado em caso de wipe bem-sucedido)

    Returns:
        bool: True se o wipe foi executado (main deve encerrar sem salvar)
              False se o usuário falhou (main pode continuar ou encerrar)
    """
    try:
        _ato1_produto_secreto()
        _ato2_alerta_policia()
        sucesso = _ato3_hacking_minigame()

        if sucesso:
            _ato4_autodestruicao(inventario)
            return True   # Dados apagados — main deve encerrar
        else:
            _final_capturado()
            return False  # Dados intactos — main pode tratar como quiser

    except KeyboardInterrupt:
        # Se o usuário apertar Ctrl+C durante o evento, trata graciosamente
        print(f"\n\n{VERMELHO}  [SISTEMA] Evento interrompido. Retornando ao menu...{RESET}\n")
        time.sleep(1.0)
        return False
