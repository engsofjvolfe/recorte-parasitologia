# `montar_deck.py` — CSV de perguntas → baralho do Anki

Transforma planilhas de perguntas (`.csv`) em pacotes do Anki (`.apkg`), prontos para
importar. O script **não sabe nada sobre a matéria**: não tem nome de disciplina, de
agente, de tópico nem de arquivo escrito no código. Tudo o que muda de uma matéria
para outra vem do próprio CSV (colunas e valores) ou dos argumentos de linha de
comando. Serve igual para parasitologia, farmacologia, direito ou qualquer outra coisa.

## Requisitos

- Python 3.9 ou mais novo.
- A biblioteca [`genanki`](https://pypi.org/project/genanki/): `pip install genanki`.

## Uso

Na raiz do projeto:

```bash
python scripts/montar_deck.py                # gera um .apkg para cada CSV encontrado
python scripts/montar_deck.py nucleo         # só os CSVs cujo nome contém "nucleo"
python scripts/montar_deck.py --listar       # só lista os CSVs que seriam processados
```

| Argumento | O que faz | Padrão |
|---|---|---|
| `filtro` (posicional, opcional) | Processa só os CSVs cujo nome contém esse trecho | todos |
| `--listar` | Lista os CSVs encontrados e sai, sem gerar nada | — |
| `--entrada DIR` | Pasta onde procurar os CSVs (sem entrar em subpastas) | `docs/material-gerado/` |
| `--saida DIR` | Pasta onde gravar os `.apkg` | `anki-decks/` |
| `--prefixo TEXTO` | Só pega CSVs cujo nome começa com esse prefixo | `perguntas-` |

Os padrões são relativos à raiz do projeto (a pasta acima de `scripts/`), e dá para
trocar todos eles na linha de comando — o script não depende da estrutura de pastas
deste repositório.

## O contrato do CSV

O CSV deve estar em UTF-8, com cabeçalho na primeira linha. O script só conhece estes
nomes de coluna:

| Coluna | Obrigatória? | Papel |
|---|---|---|
| `pergunta` | Sim | Frente do cartão. Precisa ser única dentro do arquivo (ela identifica o cartão). |
| `resposta` | Sim | Verso do cartão. |
| `baralho` | Não | Subdeck do cartão. Níveis separados por `::`, o separador do próprio Anki — ex.: `Farmacologia::Antibióticos::Penicilinas`. Vazio ou ausente = o cartão vai para o deck raiz. |
| qualquer coluna que **comece com `_`** | Não | Vira campo do cartão, mas **não aparece** na tela — para dado de bastidor (ex.: `_ordem`, `_id_interno`). |
| **qualquer outra coluna** | Não | Vira campo do cartão e **aparece** numa linha de metadados acima da pergunta, na ordem do cabeçalho. Use o nome que quiser (`agente`, `artigo`, `capítulo`, `origem`...). |

Exemplo mínimo, de outra matéria:

```csv
baralho,tema,_ordem,pergunta,resposta
"Farmacologia::Antibióticos","Penicilinas","1","Qual o mecanismo de ação das penicilinas?","Inibem a síntese da parede celular bacteriana."
"Farmacologia::Antibióticos","Penicilinas","2","Qual o principal efeito adverso grave das penicilinas?","Anafilaxia."
```

Isso gera um cartão com a linha de metadados `PENICILINAS` (a coluna `tema`), sem
mostrar a `_ordem`, dentro do subdeck `Farmacologia::Antibióticos`.

## Como os nomes são formados

- **Um `.apkg` por CSV.** O nome vem do arquivo, sem o prefixo, com cada parte
  capitalizada: `perguntas-nucleo-dicionarios.csv` → `Nucleo-Dicionarios.apkg`.
- **Deck raiz** = a primeira parte do nome: `Nucleo`. O caminho da coluna `baralho`
  fica embaixo dele: `Nucleo::Helmintologia::Trichuris trichiura`.
- O texto de cada nível do `baralho` é mantido exatamente como está no CSV (nada de
  capitalização automática — nomes científicos, siglas e acentos são preservados).
- Os nomes das colunas viram nomes de campo do Anki sem acento e sem espaço
  (`tipo_pergunta` → `TipoPergunta`). Se duas colunas virarem o mesmo nome de campo, ou
  colidirem com o campo reservado `Imagem`, o script para com uma mensagem explicando.

## Reimportar sem duplicar

- Cada cartão é identificado pelo **nome do arquivo + texto da pergunta**. Corrigir a
  resposta ou qualquer outra coluna e reimportar **atualiza** o cartão que já está no
  Anki (o histórico de revisão é mantido). Mudar o texto da pergunta cria um cartão novo.
- Decks e modelo de nota também têm ID fixo, calculado a partir do nome do deck e do
  conjunto de colunas. Se você mudar as colunas do CSV (acrescentar, remover ou
  renomear), o Anki recebe um tipo de nota novo — os cartões antigos continuam lá e
  podem ser apagados à mão.

## Campo de imagem

Todo cartão tem um campo `Imagem`, hoje sempre vazio. Ele está reservado para quando
algum mecanismo de imagem for acrescentado, sem precisar mudar o modelo do cartão. Por
isso nenhuma coluna do CSV pode se chamar `imagem`.

## Erros que o script aponta

- Falta a coluna `pergunta` ou `resposta`.
- Linha com pergunta ou resposta vazia (com o número da linha).
- Pergunta repetida dentro do mesmo arquivo (com as duas linhas).
- Nenhum CSV encontrado com o prefixo na pasta de entrada.

## `verificar_trechos.py` — conferir que o material é 100% rastreável

Confere se cada cartão está sustentado por um trecho **literal** da base de
transcrições (`docs/material-base/gerados-ocr/`). Também é agnóstico de matéria.

Para isso, o CSV usa duas colunas ocultas (começam com `_`, então não aparecem no cartão):

| Coluna | Conteúdo |
|---|---|
| `_fonte` | Onde está o trecho: `ARQUIVO § LOCAL`. `ARQUIVO` é relativo à pasta da base; `LOCAL` é o título de uma seção do arquivo (ex.: `Slide 2`) ou o ID de um bloco marcado `[ID]` (ex.: `TRI-12`). |
| `_trecho` | O texto que sustenta a resposta, copiado literalmente da fonte. |

Quando a resposta se apoia em mais de um trecho, os itens vão nas duas colunas, na
mesma ordem, separados por ` || `. Exemplo:

```csv
_fonte,_trecho
"TRICHURIS.md § Slide 3 || TRICHURIS-fontes-oficiais.md § TRI-12","Pode viver no organismo por 5 até 8 anos || The life span of the adults is about 1 year."
```

```bash
python scripts/verificar_trechos.py                       # confere todos os CSVs de perguntas
python scripts/verificar_trechos.py --citacoes DOC.md     # confere se cada [ID] citado num .md existe na base
python scripts/verificar_trechos.py --citacoes DOC.md --cobertura BASE.md   # e se todo bloco [ID] de BASE.md foi citado no .md
python scripts/verificar_trechos.py --base DIR --entrada DIR --prefixo PREFIXO
```

Para cada trecho, o script isola a seção ou o bloco indicado e exige que o texto
apareça ali literalmente (só os espaços em branco são normalizados). Sai com código 1 e
lista cada erro — arquivo inexistente, local inexistente, trecho não encontrado,
número de fontes diferente do número de trechos. CSVs sem as duas colunas são pulados,
com aviso.

O que ele **não** confere: se a resposta, em português, diz o mesmo que o trecho (inclusive
quando o trecho está em outra língua). Isso é leitura humana — por isso pergunta,
resposta e trecho ficam lado a lado na mesma linha do CSV.

## Usar em outra matéria

1. Crie os CSVs seguindo o contrato acima, com o prefixo escolhido, numa pasta qualquer.
2. Rode `python scripts/montar_deck.py --entrada <pasta dos CSVs> --saida <pasta dos decks>`.
3. Importe os `.apkg` no Anki (Arquivo > Importar).

Nada no código precisa ser editado.

---

*Código sob [GPL-3.0](../LICENSE). Ver [NOTICE.md](../NOTICE.md) para detalhes.*
