# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Gera pacotes Anki (.apkg) a partir de QUALQUER CSV de perguntas encontrado direto em
docs/material-gerado/ (sem entrar em subpastas -- uma eventual subpasta de material
arquivado de outra disciplina nao e conteudo ativo e nao deve ser descoberta aqui). O
script e agnostico de disciplina, de nome de coluna e atemporal: nenhum nome de
disciplina, item ou arquivo fica fixado no codigo. O contrato estavel e minimo:

  1. o nome do arquivo comeca com "perguntas-" e termina em ".csv";
  2. existe uma coluna "pergunta" e uma coluna "resposta" -- os dois unicos nomes de
     coluna que o script realmente exige, porque sao intrinsecos a qualquer cartao de
     revisao, nao especificos de nenhuma disciplina.

Qualquer outra coluna (disciplina, agente, tipo_pergunta, fonte, ordem, ou qualquer nome
que a disciplina preferir) e opcional e vira campo do cartao automaticamente, com o nome
que a propria coluna tiver -- nao exige nenhuma mudanca neste script. Uma coluna tem um
papel especial, mas so se existir: uma coluna "disciplina" (se presente) organiza os
cartoes em subdecks por valor distinto; se ausente, todos os cartoes desse CSV vao para
um unico deck.

Cada cartao tambem tem um campo Imagem, sempre vazio neste script -- reservado para
quando algum mecanismo de imagem (manual ou automatico) vier a preenche-lo, sem exigir
mudar o modelo do cartao.

Cada arquivo processado vira seu proprio pacote .apkg (nomeado a partir do proprio nome
do arquivo). O modelo de nota (campos e template do cartao) e construido a partir do
cabecalho de cada CSV -- CSVs com conjuntos de coluna diferentes ganham modelos
diferentes automaticamente, cada um com ID deterministico a partir do proprio conjunto
de colunas.

Uso:
    python montar_deck.py              # gera um .apkg para cada CSV encontrado
    python montar_deck.py <trecho>     # gera so os .apkg cujo nome de arquivo contem <trecho>
    python montar_deck.py --listar     # so lista os CSVs que seriam processados, sem gerar nada
"""

import csv
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

import genanki


def _raiz_projeto(inicio: Path) -> Path:
    """Sobe a arvore de pastas a partir de `inicio` ate achar a raiz do projeto,
    identificada pela presenca de `docs/material-gerado/` (a pasta onde o conteudo de
    qualquer disciplina sempre nasce). Isso deixa o script robusto a reorganizacoes de
    pasta, inclusive renomear a propria pasta-raiz do projeto."""
    for candidata in (inicio, *inicio.parents):
        if (candidata / "docs" / "material-gerado").is_dir():
            return candidata
    raise FileNotFoundError(
        f"nao encontrei a raiz do projeto (docs/material-gerado/) subindo a partir de {inicio}"
    )


BASE = _raiz_projeto(Path(__file__).resolve().parent)
MATERIAL_GERADO = BASE / "docs" / "material-gerado"
SAIDA_DIR = BASE / "anki-decks"

# Colunas com papel de bastidor: se existirem, viram campo do cartao (pra nao perder a
# informacao), mas nao aparecem na linha de metadados do cartao -- so pra nao poluir a
# tela com numero de ordem ou citacao de fonte toda vez. Nao sao exigidas; um CSV sem
# nenhuma das duas funciona normalmente.
COLUNAS_SO_CAMPO = {"ordem", "fonte"}


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sem_acento.lower()


def campo_anki(nome_coluna):
    """Nome de coluna do CSV -> nome de campo do Anki (ex.: "tipo_pergunta" ->
    "TipoPergunta"). Sem espaco, pra nao arriscar problema de sintaxe no template do
    Anki. So formata para leitura -- nao muda o que a coluna significa, e nao presume
    nenhum nome especifico de coluna."""
    return "".join(p.capitalize() for p in re.split(r"[_\s]+", nome_coluna) if p) or "Campo"


def construir_modelo(colunas_extra, rotulo):
    """Monta um genanki.Model com campos Pergunta, Resposta e Imagem, mais um campo pra
    cada coluna extra que o CSV realmente tiver -- nenhum nome de coluna (nem "agente",
    nem "disciplina") e exigido pra isso funcionar. CSVs com conjuntos de coluna
    diferentes ganham modelos diferentes, cada um com ID deterministico a partir do
    proprio conjunto de colunas, entao o mesmo "formato" de CSV sempre reusa o mesmo
    modelo ao reimportar."""
    if "imagem" in {c.lower() for c in colunas_extra}:
        raise ValueError(
            f'coluna "imagem" colide com o campo de imagem do modelo de cartao -- renomeie essa coluna no CSV ({rotulo}).'
        )

    campos_extra = [campo_anki(c) for c in colunas_extra]
    campos_visiveis = [
        campo_anki(c) for c in colunas_extra if c.lower() not in COLUNAS_SO_CAMPO
    ]
    assinatura = ",".join(colunas_extra) or "minimo"
    model_id = id_estavel("modelo::" + assinatura)

    linha_meta = "".join(
        f"{{{{#{c}}}}}<span class=\"meta-item\">{{{{{c}}}}}</span>{{{{/{c}}}}}"
        for c in campos_visiveis
    )

    return genanki.Model(
        model_id,
        f"Nucleo Multidisciplina - {rotulo}",
        fields=[{"name": "Pergunta"}, {"name": "Resposta"}, {"name": "Imagem"}]
        + [{"name": c} for c in campos_extra],
        templates=[{
            "name": "Cartao Padrao",
            "qfmt": f'<div class="meta">{linha_meta}</div><div class="pergunta">{{{{Pergunta}}}}</div>',
            "afmt": (
                '{{FrontSide}}<hr id="answer">'
                '<div class="resposta">{{Resposta}}</div>'
                '{{#Imagem}}<div class="imagem">{{Imagem}}</div>{{/Imagem}}'
            ),
        }],
        css="""
        .card { font-family: Arial, sans-serif; font-size: 18px; text-align: center; color: #1a1a1a; }
        .meta { color: #888; font-size: 13px; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 8px; }
        .meta-item:not(:last-child)::after { content: " • "; }
        .pergunta { font-weight: 600; }
        .resposta { margin-top: 10px; }
        .imagem img { max-width: 90%; max-height: 320px; margin-top: 14px; border-radius: 6px; }
        """,
    )


def id_estavel(nome, minimo=1_000_000_000, maximo=1_999_999_999):
    """ID deterministico de 10 digitos a partir do nome do deck: o mesmo nome sempre
    gera o mesmo ID, sem precisar cadastrar cada disciplina manualmente no codigo.
    Reimportar o mesmo .apkg atualiza os cartoes existentes no Anki em vez de duplicar
    o deck, desde que o nome do deck nao mude."""
    digest = hashlib.sha256(nome.encode("utf-8")).hexdigest()
    return minimo + (int(digest, 16) % (maximo - minimo))


def descobrir_csvs(filtro=None):
    """Lista os CSVs de perguntas prontos para virar deck: qualquer perguntas-*.csv
    direto dentro de docs/material-gerado/ (nao entra em subpastas -- uma eventual
    subpasta de material arquivado de outra disciplina nao e ativa e nao deve ser
    descoberta aqui). `filtro`, se dado, mantem so arquivos cujo nome contenha o trecho
    (case-insensitive)."""
    candidatos = sorted(MATERIAL_GERADO.glob("perguntas-*.csv"))
    if filtro:
        alvo = filtro.lower()
        candidatos = [c for c in candidatos if alvo in c.name.lower()]
    return candidatos


def nomes_a_partir_do_arquivo(caminho_csv: Path):
    """"perguntas-nucleo-dicionarios.csv" -> familia "Nucleo", nome de saida
    "Nucleo-Dicionarios". Tira o prefixo generico "perguntas" (se existir) e capitaliza
    cada palavra separada por hifen -- funciona pra qualquer nome de arquivo novo, nao
    so pros padroes ja conhecidos (nucleo/fundamentos)."""
    partes = [p for p in caminho_csv.stem.split("-") if p]
    if partes and partes[0].lower() == "perguntas":
        partes = partes[1:]
    if not partes:
        partes = [caminho_csv.stem]
    familia = partes[0].capitalize()
    nome_saida = "-".join(p.capitalize() for p in partes)
    return familia, nome_saida


def montar_pacote(caminho_csv: Path):
    familia, nome_saida = nomes_a_partir_do_arquivo(caminho_csv)

    decks = {}  # chave de deck normalizada -> genanki.Deck, criado sob demanda
    total_cartoes = 0

    with open(caminho_csv, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        colunas = leitor.fieldnames or []
        if "pergunta" not in colunas or "resposta" not in colunas:
            raise ValueError(
                f'{caminho_csv.name}: precisa ter uma coluna "pergunta" e uma '
                f'"resposta" -- sao os dois unicos nomes de coluna exigidos '
                f"(colunas encontradas: {colunas})."
            )
        colunas_extra = [c for c in colunas if c not in ("pergunta", "resposta")]
        modelo = construir_modelo(colunas_extra, nome_saida)
        tem_disciplina = "disciplina" in colunas

        for linha in leitor:
            disciplina = linha.get("disciplina", "").strip()

            nota = genanki.Note(
                model=modelo,
                fields=[linha["pergunta"].strip(), linha["resposta"].strip(), ""]
                + [linha[c].strip() for c in colunas_extra],
            )

            if tem_disciplina:
                chave_deck = normalizar(disciplina)
                nome_deck = f"{familia}::{disciplina.capitalize()}" if disciplina else familia
            else:
                chave_deck, nome_deck = "", familia
            if chave_deck not in decks:
                decks[chave_deck] = genanki.Deck(id_estavel(nome_deck), nome_deck)
            decks[chave_deck].add_note(nota)
            total_cartoes += 1

    caminho_saida = SAIDA_DIR / f"{nome_saida}.apkg"
    pacote = genanki.Package(list(decks.values()))
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    pacote.write_to_file(caminho_saida)

    print(f"Deck gerado: {caminho_saida}")
    print(f"  Subdecks: {', '.join(d.name for d in decks.values())}")
    print(f"  Total de cartoes: {total_cartoes}")


if __name__ == "__main__":
    args = sys.argv[1:]
    listar_apenas = "--listar" in args
    filtro = next((a for a in args if not a.startswith("--")), None)

    csvs = descobrir_csvs(filtro)
    if not csvs:
        alvo_desc = f" com filtro {filtro!r}" if filtro else ""
        raise SystemExit(f"nenhum CSV 'perguntas-*.csv' encontrado em {MATERIAL_GERADO}{alvo_desc}")

    print(f"CSVs encontrados ({len(csvs)}): {', '.join(c.name for c in csvs)}")
    if listar_apenas:
        raise SystemExit(0)

    for caminho in csvs:
        montar_pacote(caminho)
