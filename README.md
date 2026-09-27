# Núcleo de Parasitologia — Helmintologia

![Licenca codigo](https://img.shields.io/badge/C%C3%B3digo-GPL--3.0-blue)
![Licenca conteudo](https://img.shields.io/badge/Conte%C3%BAdo-CC_BY--NC--SA_4.0-blue)

## O que é isto

Um material de estudo de parasitologia médica (helmintologia). Veja o
**[INDICE.md](INDICE.md)** para navegar por todos os documentos, ou o
**[MANUAL.md](MANUAL.md)** para um guia rápido e não técnico de como usar o material. Este
README é a documentação técnica do projeto.

## Aviso importante — leia antes de usar

Este conteúdo foi construído a partir do material de parasitologia disponibilizado (ver
seção [Origem do conteúdo](#origem-do-conteúdo) abaixo) e **organizado em torno da grade
específica de uma disciplina de graduação**. Isso significa que:

- A seleção de quais agentes entraram no núcleo, qual achado clínico é "o mais cobrado"
  e qual tratamento é "a resposta esperada" reflete a ênfase **daquele curso e daquele
  professor específico, na leitura de um aluno específico** — não é necessariamente a cobertura completa da literatura
  médica, nem substitui diretrizes oficiais (OMS, sociedades médicas) ou o material
  didático original da disciplina.
- Simplificações propositais foram feitas para organizar o conteúdo em cadeias causais e
  fichas determinísticas (uma resposta "canônica" por eixo), o que pode omitir nuances,
  exceções e controvérsias que um material de referência completo traria.
- **Use como ferramenta de revisão e fixação, não como fonte primária de estudo.**
  Sempre confira fatos clinicamente relevantes com a bibliografia oficial da sua
  disciplina antes de uma prova ou de qualquer decisão clínica real.

## Proposta de plataforma futura

Este projeto também serve de protótipo para uma proposta maior: generalizar o mecanismo
usado aqui — material de aula → conteúdo estruturado → material de estudo pronto — para
qualquer disciplina, de forma colaborativa e agnóstica de matéria. A visão geral dessa
proposta (ponto de partida, no espírito do modelo V, para um futuro documento de
Requisitos formal) está em
[`docs/proposta-plataforma/01-visao-geral.md`](docs/proposta-plataforma/01-visao-geral.md).

## Origem do conteúdo

O material de parasitologia original que serve de base para este núcleo (ANCILOSTOMÍDEOS,
s.d.; ASCARIS E ASCARIDÍASE, s.d.; GEOHELMINTOS, s.d.; HELMINTOS I, s.d.; SCHISTOSOMA
MANSONI E ESQUISTOSSOMOSE, s.d.; STRONGYLOIDES E ESTRONGILOIDÍASE, s.d.; TRICHURIS E
TRICURÍASE, s.d.) está em
[`docs/material-base/`](docs/material-base/) — referências completas na seção
[Referências](#referências), ao final deste documento.

Esses PDFs são material de aula de uma universidade de Minas Gerais, obtidos por meio de
um aluno da disciplina — **não foram produzidos por quem mantém este repositório e não
estão cobertos pela licença deste projeto** (ver [Licença](#licença) abaixo). Por isso
**nunca são versionados nem redistribuídos**: ficam só localmente, fora do controle de
versão (`.gitignore`). Todo o resto (dicionário de gatilhos, ficha determinística,
biologia fundamental) foi escrito/reorganizado a partir desses PDFs, mas é conteúdo
derivado próprio deste repositório, não uma cópia do material original. A exceção são
citações curtas: cada cartão do núcleo guarda, num campo oculto, a frase literal da aula
ou do documento oficial que sustenta a resposta, com a fonte — esses trechos não estão
cobertos pela licença deste projeto (ver [`NOTICE.md`](NOTICE.md)).

Onde a aula não cobre um ponto, o material usa **fontes oficiais** (Ministério da Saúde —
Guia de Vigilância em Saúde, Formulário Terapêutico Nacional, Guia de Bolso, diretrizes da
esquistossomose —, OMS e CDC), em trechos literais reunidos em bases por agente
(`docs/material-base/gerados-ocr/*-fontes-oficiais.md`) e citados na ficha e no dicionário
como `[TRI-nn]`, `[STR-nn]`, `[ESQ-nn]`. Os documentos oficiais baixados ficam em
`docs/material-base/fontes-oficiais/`, também fora do controle de versão.

Cada PDF tem também uma **transcrição OCR integral e literal** dos seus slides, com o
mesmo nome do PDF, em `docs/material-base/gerados-ocr/`. Ela é usada só como conferência
para achar lacunas no material gerado (foi assim, por exemplo, no documento de biologia
fundamental, que inclui a seção de geo-helmintos) — não é conteúdo derivado nosso (é
cópia literal do material de terceiros), por isso fica no mesmo regime dos PDFs: **não
versionada** (`.gitignore`) e não redistribuída.

## Licença

Este projeto usa duas licenças, para duas partes diferentes, mais uma exceção — texto
completo e detalhado em [`NOTICE.md`](NOTICE.md):

| Parte | Licença | Significa que... |
|---|---|---|
| Código (`scripts/*.py`) | [GPL-3.0](LICENSE) | Pode usar/modificar/redistribuir, mas derivados também precisam ficar abertos (copyleft) |
| Conteúdo (dicionário de gatilhos, ficha determinística, biologia fundamental, resumos, `docs/proposta-plataforma/`) | [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt) | Pode usar/adaptar com crédito, **sem fins comerciais**, mantendo a mesma licença |
| PDFs em `docs/material-base/` | Nenhuma — são de terceiros | Não redistribuir; ficam fora do controle de versão (`.gitignore`) |

## Estrutura do projeto

| Arquivo | O que é |
|---|---|
| [`docs/material-gerado/perguntas-nucleo-dicionarios.csv`](docs/material-gerado/perguntas-nucleo-dicionarios.csv) | Cartões atômicos por agente (um fato ou um "por quê" por cartão), tirados da ficha determinística e do dicionário de gatilhos, com a origem de cada um (aula ou fonte oficial complementar) |
| [`docs/material-gerado/perguntas-fundamentos-helmintos.csv`](docs/material-gerado/perguntas-fundamentos-helmintos.csv) | Cartões de biologia fundamental de helmintos e do grupo dos geo-helmintos, organizados por tópico, com a origem de cada um |
| [`docs/material-gerado/dicionario-gatilhos-parasitologia.md`](docs/material-gerado/dicionario-gatilhos-parasitologia.md) | Cadeia causal didática por agente |
| [`docs/material-gerado/parasitologia-especial-determinismo.md`](docs/material-gerado/parasitologia-especial-determinismo.md) | Ficha determinística por agente |
| [`docs/material-gerado/biologia-fundamental-helmintos.md`](docs/material-gerado/biologia-fundamental-helmintos.md) | Base teórica geral: classificação, morfologia, ciclos de vida e epidemiologia dos geo-helmintos |
| [`docs/material-gerado/resumos/resumo-biologia-fundamental-helmintos.md`](docs/material-gerado/resumos/resumo-biologia-fundamental-helmintos.md) | Resumo esquemático da biologia fundamental (tópicos, esquemas e tabelas), com link de cada bloco para a seção completa do documento |
| [`docs/material-gerado/resumos/resumo-parasitologia-especial-helmintos.md`](docs/material-gerado/resumos/resumo-parasitologia-especial-helmintos.md) | Resumo esquemático dos agentes (versão condensada da ficha determinística e do dicionário de gatilhos), com links para cada agente nos dois documentos |
| [`docs/proposta-plataforma/01-visao-geral.md`](docs/proposta-plataforma/01-visao-geral.md) | Visão geral da proposta de generalizar este mecanismo para qualquer disciplina (plataforma/software futuro) |
| [`INDICE.md`](INDICE.md) | Índice com link direto para qualquer documento do projeto |
| [`MANUAL.md`](MANUAL.md) | Guia rápido e não técnico de como usar o material e como colaborar |
| [`LICENSE`](LICENSE) | Texto completo da GPL-3.0 (código) |
| [`LICENSE-CONTENT.txt`](LICENSE-CONTENT.txt) | Texto completo da CC BY-NC-SA 4.0 (conteúdo) |
| [`NOTICE.md`](NOTICE.md) | Explica qual licença cobre qual arquivo, e a exceção dos PDFs de terceiros |
| [`.gitignore`](.gitignore) | Exclui os PDFs de terceiros, caches e artefatos temporários do controle de versão |
| [`anki-decks/Nucleo-Dicionarios.apkg`](anki-decks/Nucleo-Dicionarios.apkg) | Deck pronto para importar no Anki, por agente |
| [`anki-decks/Fundamentos-Helmintos.apkg`](anki-decks/Fundamentos-Helmintos.apkg) | Deck pronto para importar no Anki, biologia fundamental |
| [`scripts/montar_deck.py`](scripts/montar_deck.py) | Gera um `.apkg` para cada CSV `perguntas-*.csv` encontrado em `docs/material-gerado/` — agnóstico de matéria, sem nada fixado no código; contrato do CSV e uso em [`scripts/README.md`](scripts/README.md) |
| [`scripts/verificar_trechos.py`](scripts/verificar_trechos.py) | Confere se cada cartão e cada citação `[ID]` dos documentos estão sustentados por um trecho literal da base de transcrições — agnóstico de matéria; uso em [`scripts/README.md`](scripts/README.md) |

Este projeto também usa um hook de commit local (`.githooks/`, copiado do projeto-modelo
`modelo-recorte-disciplina`) que verifica o formato da mensagem de commit — título mais
descrição em prosa, sem bullets. Essa pasta não é versionada aqui de propósito (é
ferramenta local de quem mantém o projeto, não conteúdo do repositório); se ela não
existir na sua cópia, veja `.githooks/README.md` no projeto-modelo para copiá-la e
ativá-la de novo.

## Como usar

1. Para estudar: importe `anki-decks/Nucleo-Dicionarios.apkg` (por agente) e
   `anki-decks/Fundamentos-Helmintos.apkg` (biologia geral) no Anki — são dois pacotes
   independentes —, ou leia os `.md` direto em `docs/material-gerado/` (ver
   [MANUAL.md](MANUAL.md)).
2. Para consultar rapidamente um agente específico: abra o [`INDICE.md`](INDICE.md),
   clique no documento que quer (dicionário ou ficha) e use o índice interno dele, logo
   no topo, para ir direto ao agente.
3. Para editar conteúdo: mude o `.md` correspondente e os cartões no CSV em
   `docs/material-gerado/` (o CSV é a fonte dos cartões), rode
   `python scripts/verificar_trechos.py` (cada cartão tem de ter trecho literal da fonte) e
   depois `python scripts/montar_deck.py` para regenerar os `.apkg` — os dois scripts são
   agnósticos de disciplina e descobrem sozinhos qualquer CSV `perguntas-*.csv` novo.

## Ver também

**[INDICE.md](INDICE.md)** — navegação completa para todos os documentos do projeto.

## Referências

Material de aula que serviu de fonte primária para o conteúdo deste projeto (ver
[Origem do conteúdo](#origem-do-conteúdo)). Sem autoria individual identificada; local,
editora e data desconhecidos:

ANCILOSTOMÍDEOS. [S.l.: s.n., s.d.]. Material de aula (slides), não publicado.
Localização: `docs/material-base/ANCILOSTOMIDEOS.pdf` (arquivo de terceiros, não
versionado neste repositório; o arquivo original recebia o nome `STRONGILOIDES.pdf`,
renomeado por não conter nenhum conteúdo sobre *Strongyloides* — os slides de
*Strongyloides* são os de `ESTRONGILOIDES.pdf`, abaixo).

ASCARIS E ASCARIDÍASE. [S.l.: s.n., s.d.]. Material de aula (slides), não publicado.
Localização: `docs/material-base/ASCARIS_E_ASCARIDIASE.pdf` (arquivo de terceiros, não
versionado neste repositório).

GEOHELMINTOS. [S.l.: s.n., s.d.]. Material de aula (slides), não publicado. Localização:
`docs/material-base/GEOHELMINTOS.pdf` (arquivo de terceiros, não versionado neste
repositório).

HELMINTOS I. [S.l.: s.n., s.d.]. Material de aula (slides), não publicado. Localização:
`docs/material-base/HELMINTOS_I.pdf` (arquivo de terceiros, não versionado neste
repositório).

SCHISTOSOMA MANSONI E ESQUISTOSSOMOSE. [S.l.: s.n., s.d.]. Material de aula (slides), não
publicado. Localização: `docs/material-base/ESQUISTOSSOMO.pdf` (arquivo de terceiros, não
versionado neste repositório; 31 slides, que terminam na forma hepatoesplênica — não
inclui diagnóstico, tratamento nem profilaxia).

STRONGYLOIDES E ESTRONGILOIDÍASE. [S.l.: s.n., s.d.]. Material de aula (slides), não
publicado. Localização: `docs/material-base/ESTRONGILOIDES.pdf` (arquivo de terceiros, não
versionado neste repositório; só 3 slides: capa, taxonomia/gerações e morfologia das
formas de vida livre).

TRICHURIS E TRICURÍASE. [S.l.: s.n., s.d.]. Material de aula (slides), não publicado.
Localização: `docs/material-base/TRICHURIS.pdf` (arquivo de terceiros, não versionado
neste repositório; só 3 slides: capa, taxonomia/transmissão e epidemiologia).

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt). Ver [NOTICE.md](NOTICE.md) para detalhes.*
