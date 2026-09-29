# Manual de Uso — Núcleo de Parasitologia

Este manual explica como usar este material, do jeito mais rápido possível. Não é
documentação técnica — é um guia para quem só quer estudar (ou ajudar a melhorar o
material) sem precisar entender a estrutura interna do projeto inteiro.

## Antes de tudo: isto foi feito por uma pessoa só, à mão

Todo o material deste projeto — texto ou resposta — foi selecionado e escrito de forma
**manual e subjetiva** por quem organizou o projeto. Não é uma revisão sistemática, não
passou por banca revisora, e não foi gerado por um processo automatizado e determinístico.
Na prática, isso quer dizer:

- **Pode ter erro em qualquer parte** — texto ou resposta.
- **A escolha de quais assuntos entraram, e a profundidade de cada um, foi um julgamento
  pessoal** de quem organizou o material — não uma cobertura garantidamente completa ou
  objetiva do tema.
- **É esperado que partes do material original em PDF não estejam representadas aqui.**
  Faltar alguma coisa não é (necessariamente) erro — pode só não ter sido considerado
  prioritário para o recorte deste material.

Use este material como **apoio de revisão**, não como fonte única de verdade. Sempre
confira com o material oficial da sua disciplina antes de uma prova ou qualquer decisão
importante. E se achar algo errado ou faltando, veja como colaborar no
[Nível 4](#nível-4--erros-e-como-colaborar) abaixo.

Está organizado em níveis. Comece pelo Nível 1. Só desça pros próximos se quiser entender
mais ou ajudar a corrigir alguma coisa.

---

## Nível 1 — Só quero estudar agora

1. Abra o Anki no computador ou celular (programa gratuito de revisão espaçada —
   baixe em [apps.ankiweb.net](https://apps.ankiweb.net) se ainda não tiver).
2. Importe os dois arquivos de `anki-decks/` — são arquivos `.apkg`, o formato que o
   Anki usa pra empacotar um baralho pronto (arraste pro Anki, ou use Arquivo >
   Importar dentro do Anki, um de cada vez):
   - `Nucleo-Dicionarios.apkg` — os agentes do núcleo, cada um no seu próprio subgrupo.
   - `Fundamentos-Helmintos.apkg` — a base teórica geral (classificação, morfologia,
     ciclo de vida, geo-helmintos), separada do primeiro.
3. Pronto. No `Nucleo-Dicionarios.apkg` você vai ver o grupo **Helmintologia**, com um
   subgrupo por agente. No `Fundamentos-Helmintos.apkg` você vai ver o mesmo grupo, mas
   organizado por tópico de biologia geral em vez de por agente.

Os cartões de cada agente são **atômicos**: um fato por cartão, com resposta curta, e a
pergunta sempre nomeia o agente (e a fase ou o contexto), para que agentes parecidos não se
confundam. Cobrem os 11 eixos da ficha determinística (agente, classificação, morfologia,
ciclo biológico, transmissão, fatores de risco, patogenia, manifestações clínicas,
diagnóstico, tratamento, profilaxia — ver
[docs/material-gerado/parasitologia-especial-determinismo.md](docs/material-gerado/parasitologia-especial-determinismo.md)),
e nenhum cartão traz o que a ficha não diz. Cada cartão guarda, escondido, o trecho literal
da aula ou do documento oficial que sustenta a resposta. Conteúdo que as fontes dizem só do
grupo aparece como do grupo ("Geo-helmintíases (inclui a tricuríase)"), e minúcias de
laboratório ficam só na ficha.

Já os cartões de fundamentos não seguem esse molde por agente — a maioria é tipo
**Conceito** (uma pergunta direta sobre um conceito de biologia geral), com algumas
**Vinheta (estrutura)** também, descrevendo um achado ou cenário genérico (não um caso
clínico de um agente específico) para você identificar a estrutura ou o fenômeno
biológico por trás. Nenhum cartão tem imagem por enquanto.

### Se você editar as planilhas de pergunta e quiser atualizar o baralho

As perguntas/respostas de cada cartão ficam guardadas em arquivos `.csv` dentro de
`docs/material-gerado/` — um CSV é só uma planilha em formato de texto simples (uma
linha por pergunta, colunas separadas por vírgula); dá pra editar direto no VSCode como
qualquer arquivo de texto, ou abrir no Excel/Google Sheets se preferir. Depois de
editar, para gerar de novo os arquivos `.apkg`:

1. No VSCode, abra o terminal: menu **Terminal → Novo Terminal** (ou o atalho `` Ctrl+` ``).
2. Só na primeira vez: digite `pip install genanki` e aperte Enter (instala a biblioteca
   que o script usa para montar o baralho).
3. Se mexeu na planilha do núcleo por agente, digite `python scripts/verificar_trechos.py`
   e aperte Enter: ele confere se cada cartão continua sustentado pelo trecho da fonte e
   lista o que não estiver (precisa da pasta `docs/material-base/` preenchida).
4. Digite exatamente `python scripts/montar_deck.py` e aperte Enter.
5. Aguarde a mensagem terminar — ela mostra quantos cartões foram gerados. Os arquivos
   `.apkg` dentro de `anki-decks/` são substituídos pelos novos; importe de novo no
   Anki (passo 2 do início desta seção) para ver as mudanças.

Se o terminal disser algo como "python não é reconhecido" ou "command not found", o
Python não está instalado no computador — isso precisa ser resolvido antes (fora do
escopo deste manual).

---

## Nível 2 — De onde isso veio

O projeto tem duas pastas de conteúdo bem diferentes:

**`docs/material-base/`** — o material geral, "cru". São os PDFs originais das aulas de
uma disciplina de graduação de parasitologia. É a fonte bruta de tudo que foi gerado
nesse projeto, mas **nunca é versionada nem redistribuída junto com o resto do
repositório** — são arquivos de terceiros, ficam só localmente (ver
[NOTICE.md](NOTICE.md)). Se você recebeu este projeto sem essa pasta preenchida, os
outros dois níveis abaixo não exigem que você tenha os PDFs — o material de
`docs/material-gerado/` já é autossuficiente.

Onde a aula não trata de um assunto (por exemplo, diagnóstico, tratamento e profilaxia do
*Schistosoma*, que os slides não cobrem), o material usa **documentos oficiais** —
Ministério da Saúde, OMS e CDC. Esses documentos também ficam só localmente, em
`docs/material-base/fontes-oficiais/`, e cada cartão guarda, em campos ocultos, o
documento e o trecho literal de onde veio a resposta. A lista completa das fontes — as
aulas e os documentos oficiais —, em ABNT, está em [docs/FONTES.md](docs/FONTES.md).

**`docs/material-gerado/`** — o conteúdo dos PDFs (e, onde a aula não trata, dos
documentos oficiais) reescrito e reorganizado em texto corrido, mais claro. Isso não é
só "matéria-prima do deck" — é, por si só, material de estudo completo. Dá pra estudar
só lendo os arquivos `.md` (texto simples com formatação leve — abre em qualquer editor,
inclusive o próprio VSCode, e fica bem legível), sem depender de nenhum deck. São três
documentos principais (a subpasta `resumos/` traz ainda versões condensadas deles, em
tópicos, esquemas e tabelas):

- **Dicionário de gatilhos** — conta cada helmintíase como uma historinha em cadeia: você
  entra em contato com o agente de um jeito → ele entra no corpo por tal porta → percorre
  tal ciclo dentro do hospedeiro → isso causa tal sintoma → por isso o tratamento é esse.
  Bom para **entender o porquê**, não só decorar.
- **Ficha determinística** — os mesmos agentes, mas em tabela seca e direta, sempre nos
  mesmos eixos, não importa o agente. Bom para **revisão de véspera de prova**.
- **Biologia fundamental dos helmintos** — os conceitos gerais que vêm antes de entrar em
  agente específico (classificação, morfologia, ciclo de vida, estratégias de
  transmissão e a epidemiologia dos geo-helmintos como grupo), cobrindo o conteúdo das
  aulas introdutórias dos PDFs originais.

Resumindo:

```
PDF da faculdade   →   .md reescrito e organizado   →   CSV   →   cartão do Anki
(material-base)        (material-gerado — já é         (mesma pasta)  (anki-decks/*.apkg)
                         material de estudo completo)
```

---

## Nível 3 — Quero achar um agente específico rápido

Se você já sabe o agente que quer revisar (ex.: "quero reler sobre Ascaris agora"), não
precisa abrir o documento inteiro e procurar. Abra o **[INDICE.md](INDICE.md)**, clique no
documento que quer (dicionário para a versão "historinha", ficha para a versão "ficha
seca") — cada um desses documentos tem seu próprio índice interno, logo no topo, com um
link por agente, que leva direto pro trecho certo.

---

## Nível 4 — Erros e como colaborar

Como já dito lá em cima, este material é curadoria manual de uma pessoa só — texto ou
resposta podem estar errados, incompletos ou desatualizados, ainda que a maior parte seja transcrição quase que literal do material utilizado em aula. Se notar isso estudando, vale
reportar.

### Como colaborar

Encontrou um erro — de texto ou de resposta — ou tem uma sugestão melhor? Mande um e-mail
para **lixotrashlixo@proton.me**. Para facilitar incorporar sua sugestão rápido, inclua:

1. **No assunto do e-mail:** o nome do agente + qual parte está errada — por exemplo:
   `Ascaris - Tratamento`.
2. **No corpo do e-mail:**
   - O que está errado, especificamente (ex.: "o texto diz X, mas o correto é Y").
   - Se tiver uma sugestão melhor, mande ela pronta.

Não precisa formalidade nem justificativa longa — quanto mais direto o e-mail, mais
rápido dá pra revisar e corrigir.

---

## Quer saber mais

Este manual cobre só o essencial. Para detalhes técnicos (estrutura de pastas, licença de
uso, avisos sobre o material ter sido feito para uma grade curricular específica), veja o
**[README.md](README.md)**.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt). Ver [NOTICE.md](NOTICE.md) para detalhes.*
