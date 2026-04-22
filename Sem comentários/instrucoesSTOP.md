# 🛑 Jogo STOP - Multiplayer em Python

Este é um jogo de **Stop**, jogável no terminal através de uma arquitetura Cliente-Servidor utilizando *Sockets* em Python.

## ˚.🎀༘⋆ Como Jogar

### 1. Iniciando o Servidor
O servidor deve ser o primeiro a ser iniciado. Ele é responsável por sortear a letra, coordenar as rodadas e calcular a pontuação de todos.

1. Abra um terminal e execute o arquivo do servidor:
   ```bash
   python serverSTOP.py
   ```
2. O terminal solicitará a quantidade de jogadores. Digite o número de pessoas que vão jogar (ex: `2` ou `3`) e pressione Enter.
3. O servidor ficará aguardando o número exato de jogadores se conectarem.

### 2. Conectando os Jogadores (Clientes)
Abra novos terminais (um para cada jogador) de acordo com a quantidade definida no servidor. Em cada um deles, execute:
```bash
python clientSTOP.py
```
***Por padrão, o jogo está configurado para rodar localmente (`localhost` / `127.0.0.1`) na porta `2223`.**

### 3. A Dinâmica da Partida
- O jogo padrão é composto por **3 rodadas**.
- No início de cada rodada, o servidor sorteia aleatoriamente uma letra do alfabeto e todos os terminais dos jogadores são liberados ao mesmo tempo.
- Cada jogador deve preencher as seguintes categorias:
  - **CEP** (Cidade, Estado ou País)
  - **Nome**
  - **Animal**
  - **Cor**
  - **Minha sogra é**
  - **Comida**
- **OBS:** O cliente já limpa as respostas automaticamente (remove acentos e deixa tudo em maiúsculo).
- Após preencher a última categoria ("Comida") e dar Enter, o jogo envia suas palavras. O servidor aguardará até que **todos** enviem suas respostas para calcular os pontos.

## ˚.🎀༘⋆ Sistema de Pontuação
A pontuação é calculada de forma automática pelo servidor, seguindo as regras abaixo:

- **0 pontos**: Se a resposta for deixada em branco ou **não começar com a letra sorteada** da rodada.
- **1 ponto**: Se a resposta for válida, mas **outro jogador escreveu exatamente a mesma palavra** na mesma categoria.
- **3 pontos**: Se a resposta for válida e **única** (nenhum outro jogador escreveu a mesma coisa).

Ao fim de cada rodada, o placar atualizado é exibido na tela de todos os jogadores, junto com quem está vencendo no momento!