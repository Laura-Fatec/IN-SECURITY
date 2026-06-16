# IN-SECURITY — Secure Inventory System v1.0

O projeto IN-SECURITY — Secure Inventory System v1.0 é um sistema de gerenciamento de inventário desenvolvido na linguagem Python, com o objetivo de aplicar conceitos de programação modular, estrutura de dados, manipulação de arquivos, algoritmos de busca e ordenação, além de mecanismos básicos de segurança da informação.

---

## 👥 Integrantes
- Deysi Ticona - deysi.ticona@aluno.cps.sp.gov.br
- Laura Alves Silva - deysi.ticona@aluno.cps.sp.gov.br
- Lucas Negrelli - lucas.chareta@cps.aluno.sp.gov.br
- Luiz Henrique - luiz.dias5@aluno.cps.sp.gob.br
- Obed Sarmiento - obed.sarmiento@aluno.cps.sp.gov.br
- Renato Miranda - renato.assis@cps.aluno.sp.gov.br

---

## Como executar

```bash
python main.py
```

---

## Arquivos do projeto

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada, menu, orquestração geral |
| `auth.py` | Login, logout, alteração de credenciais, log de segurança |
| `crypto.py` | SHA-256 para senhas; Cifra de César para dados do CSV |
| `inventory.py` | CRUD de produtos + leitura/escrita do CSV cifrado |
| `sorting.py` | Bubble Sort (≤100 itens) e Merge Sort (>100 itens) |
| `search.py` | Busca linear (nome parcial) e busca binária (nome exato) |
| `stats.py` | Relatório estatístico do estoque |

## Arquivos gerados em tempo de execução

| Arquivo | Conteúdo |
|---|---|
| `login.txt` | Hash SHA-256 do usuário e senha do admin |
| `inventario.csv` | Produtos cifrados com Cifra de César |
| `security.log` | Log de auditoria de todos os eventos de acesso |

---

## Segurança implementada

### Senhas — SHA-256 (hashing unidirecional)
- A senha nunca é armazenada em texto puro
- Ao fazer login, a senha digitada é hasheada e comparada com o hash salvo
- Mesmo com acesso ao `login.txt`, um atacante não consegue recuperar a senha original

### Dados do inventário — Cifra de César (criptografia simétrica)
- Todos os campos do CSV são cifrados individualmente com deslocamento 7
- O arquivo `inventario.csv` é ilegível sem a função de descriptografia
- Números e símbolos passam sem alteração (preserva estrutura)

### Proteção contra força bruta
- Máximo de 3 tentativas de login consecutivas
- Cada tentativa registrada no `security.log` com timestamp
- Bloqueio total após esgotar as tentativas

### Auditoria completa
- Todos os eventos são gravados em `security.log`:
  - Criação do sistema (primeiro admin)
  - Login bem-sucedido
  - Falhas de login (com contagem de tentativas restantes)
  - Bloqueio por tentativas excedidas
  - Alteração de credenciais

---

## Algoritmos de busca e ordenação

### Ordenação automática
| Volume | Algoritmo | Complexidade |
|---|---|---|
| ≤ 100 produtos | Bubble Sort | O(n²) |
| > 100 produtos | Merge Sort | O(n log n) |

### Busca
| Tipo | Algoritmo | Quando usar |
|---|---|---|
| Por ID | Acesso direto ao dict | Sempre O(1) |
| Por nome parcial | Busca Linear | Quando lembra parte do nome |
| Por nome exato | Busca Binária | Quando sabe o nome completo |
