# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Gera pacotes Anki (.apkg) a partir de CSVs de perguntas. O script e agnostico de
materia: nenhum nome de disciplina, agente, topico ou arquivo fica fixado no codigo.
Tudo o que muda de uma materia para outra vem do proprio CSV (colunas e valores) ou
dos argumentos de linha de comando. Documentacao completa em scripts/README.md.

Contrato do CSV (o unico conjunto de nomes que o script conhece):

  - "pergunta" e "resposta": obrigatorias -- sao intrinsecas a qualquer cartao.
  - "baralho" (opcional): caminho do subdeck do cartao, com niveis separados por "::"
    (o separador nativo do Anki). Ex.: "Helmintologia::Trichuris trichiura". Sem essa
    coluna, ou com o valor vazio, o cartao vai para o deck raiz do arquivo.
  - colunas cujo nome comeca com "_" (ex.: "_ordem"): viram campo do cartao, mas ficam
    ocultas na linha de metadados -- para dado de bastidor.
  - qualquer outra coluna: vira campo do cartao e aparece na linha de metadados, com o
    nome que a propria coluna tiver.

Cada CSV vira seu proprio .apkg. O deck raiz e o nome do arquivo vem do nome do CSV:
"perguntas-nucleo-dicionarios.csv" -> deck raiz "Nucleo", arquivo "Nucleo-Dicionarios.apkg".

Uso:
    python montar_deck.py                  # gera um .apkg para cada CSV encontrado
    python montar_deck.py <trecho>         # so os CSVs cujo nome contem <trecho>
    python montar_deck.py --listar         # so lista os CSVs, sem gerar nada
    python montar_deck.py --entrada DIR --saida DIR --prefixo PREFIXO
"""

import argparse
import csv
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

import genanki

# Nomes de coluna do contrato (ver docstring e scripts/README.md). Sao os unicos nomes
# que o script conhece; nenhum deles e especifico de materia.
COLUNA_PERGUNTA = "pergunta"
COLUNA_RESPOSTA = "resposta"
COLUNA_BARALHO = "baralho"
PREFIXO_OCULTA = "_"
SEPARADOR_BARALHO = "::"
CAMPO_IMAGEM = "Imagem"

# Padroes de pasta relativos a raiz do projeto (a pasta acima de scripts/). Podem ser
# trocados na linha de comando com --entrada e --saida.
RAIZ = Path(__file__).resolve().parent.parent
ENTRADA_PADRAO = RAIZ / "docs" / "material-gerado"
SAIDA_PADRAO = RAIZ / "anki-decks"
PREFIXO_PADRAO = "perguntas-"


def id_estavel(texto, minimo=1_000_000_000, maximo=1_999_999_999):
    """ID deterministico de 10 digitos a partir de um texto: o mesmo texto sempre gera
    o mesmo ID, entao reimportar o .apkg atualiza os decks e modelos existentes no Anki
    em vez de duplicar."""
    digest = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    return minimo + (int(digest, 16) % (maximo - minimo))


def campo_anki(nome_coluna):
    """Nome de coluna do CSV -> nome de campo do Anki (ex.: "tipo_pergunta" ->
    "TipoPergunta"). Sem espaco nem acento, pra nao arriscar problema de sintaxe no
    template do Anki. So formata para leitura -- nao muda o que a coluna significa."""
    sem_acento = unicodedata.normalize("NFKD", nome_coluna).encode("ascii", "ignore").decode("ascii")
    return "".join(p.capitalize() for p in re.split(r"[_\s]+", sem_acento) if p) or "Campo"


def nomes_a_partir_do_arquivo(caminho_csv: Path, prefixo: str):
    """"perguntas-nucleo-dicionarios.csv" -> deck raiz "Nucleo", arquivo de saida
    "Nucleo-Dicionarios". Tira o prefixo (se existir) e capitaliza cada parte separada
    por hifen -- funciona para qualquer nome de arquivo novo."""
    nome = caminho_csv.stem
    if prefixo and nome.startswith(prefixo):
        nome = nome[len(prefixo):]
    partes = [p for p in nome.split("-") if p] or [caminho_csv.stem]
    return partes[0].capitalize(), "-".join(p.capitalize() for p in partes)


def construir_modelo(colunas_extra, rotulo):
    """Monta o modelo de nota com Pergunta, Resposta e Imagem (sempre vazio, reservado
    para quando houver imagens), mais um campo por coluna extra do CSV. Colunas com o
    prefixo de oculta viram campo, mas nao entram na linha de metadados. O ID do modelo
    vem do conjunto de colunas: o mesmo formato de CSV sempre reusa o mesmo modelo."""
    campos_extra = [campo_anki(c) for c in colunas_extra]
    if CAMPO_IMAGEM in campos_extra or len(set(campos_extra)) != len(campos_extra):
        raise ValueError(
            f"{rotulo}: nomes de coluna colidem entre si ou com o campo reservado "
            f'"{CAMPO_IMAGEM}" depois de convertidos para campo do Anki -- renomeie no CSV.'
        )
    visiveis = [campo_anki(c) for c in colunas_extra if not c.startswith(PREFIXO_OCULTA)]
    linha_meta = "".join(
        f'{{{{#{c}}}}}<span class="meta-item">{{{{{c}}}}}</span>{{{{/{c}}}}}' for c in visiveis
    )
    return genanki.Model(
        id_estavel("modelo::" + (",".join(colunas_extra) or "minimo")),
        f"Nucleo Multidisciplina - {rotulo}",
        fields=[{"name": "Pergunta"}, {"name": "Resposta"}, {"name": CAMPO_IMAGEM}]
        + [{"name": c} for c in campos_extra],
        templates=[{
            "name": "Cartao Padrao",
            "qfmt": f'<div class="meta">{linha_meta}</div><div class="pergunta">{{{{Pergunta}}}}</div>',
            "afmt": (
                '{{FrontSide}}<hr id="answer">'
                '<div class="resposta">{{Resposta}}</div>'
                f'{{{{#{CAMPO_IMAGEM}}}}}<div class="imagem">{{{{{CAMPO_IMAGEM}}}}}</div>{{{{/{CAMPO_IMAGEM}}}}}'
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


def caminho_do_deck(raiz, valor_baralho):
    """Deck raiz + caminho da coluna baralho (niveis separados por "::"). Espacos
    sobrando em volta de cada nivel sao removidos; o texto de cada nivel fica como
    esta no CSV (nada de capitalizar -- nomes cientificos e siglas sao preservados)."""
    niveis = [n.strip() for n in (valor_baralho or "").split(SEPARADOR_BARALHO) if n.strip()]
    return SEPARADOR_BARALHO.join([raiz] + niveis)


def montar_pacote(caminho_csv: Path, pasta_saida: Path, prefixo: str):
    raiz, nome_saida = nomes_a_partir_do_arquivo(caminho_csv, prefixo)

    with open(caminho_csv, encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        colunas = leitor.fieldnames or []
        faltando = [c for c in (COLUNA_PERGUNTA, COLUNA_RESPOSTA) if c not in colunas]
        if faltando:
            raise ValueError(
                f"{caminho_csv.name}: faltam as colunas obrigatorias {faltando} "
                f"(colunas encontradas: {colunas})."
            )
        colunas_extra = [c for c in colunas if c not in (COLUNA_PERGUNTA, COLUNA_RESPOSTA, COLUNA_BARALHO)]
        modelo = construir_modelo(colunas_extra, nome_saida)

        decks = {}
        vistas = {}
        for numero_linha, linha in enumerate(leitor, start=2):
            pergunta = (linha.get(COLUNA_PERGUNTA) or "").strip()
            resposta = (linha.get(COLUNA_RESPOSTA) or "").strip()
            if not pergunta or not resposta:
                raise ValueError(f"{caminho_csv.name}, linha {numero_linha}: pergunta ou resposta vazia.")
            if pergunta in vistas:
                raise ValueError(
                    f"{caminho_csv.name}: a pergunta da linha {numero_linha} repete a da linha "
                    f"{vistas[pergunta]} -- cada pergunta identifica um cartao e precisa ser unica."
                )
            vistas[pergunta] = numero_linha

            # O identificador da nota vem do arquivo + pergunta: corrigir so a resposta
            # (ou uma coluna extra) atualiza o mesmo cartao no Anki ao reimportar, em vez
            # de criar um duplicado. Mudar o texto da pergunta cria um cartao novo.
            nota = genanki.Note(
                model=modelo,
                fields=[pergunta, resposta, ""] + [(linha.get(c) or "").strip() for c in colunas_extra],
                guid=genanki.guid_for(nome_saida, pergunta),
            )
            nome_deck = caminho_do_deck(raiz, linha.get(COLUNA_BARALHO))
            if nome_deck not in decks:
                decks[nome_deck] = genanki.Deck(id_estavel(nome_deck), nome_deck)
            decks[nome_deck].add_note(nota)

    if not decks:
        print(f"{caminho_csv.name}: nenhum cartao (so o cabecalho) -- nenhum .apkg gerado.")
        return

    pasta_saida.mkdir(parents=True, exist_ok=True)
    caminho_saida = pasta_saida / f"{nome_saida}.apkg"
    genanki.Package(list(decks.values())).write_to_file(caminho_saida)

    print(f"Deck gerado: {caminho_saida}")
    for nome, deck in decks.items():
        print(f"  {nome}: {len(deck.notes)} cartoes")
    print(f"  Total de cartoes: {sum(len(d.notes) for d in decks.values())}")


def descobrir_csvs(pasta_entrada: Path, prefixo: str, filtro=None):
    """CSVs cujo nome comeca com o prefixo, direto na pasta de entrada (sem entrar em
    subpastas). `filtro`, se dado, mantem so os arquivos cujo nome contem o trecho."""
    candidatos = sorted(pasta_entrada.glob(f"{prefixo}*.csv"))
    if filtro:
        candidatos = [c for c in candidatos if filtro.lower() in c.name.lower()]
    return candidatos


def main(argv=None):
    parser = argparse.ArgumentParser(description="Gera pacotes Anki (.apkg) a partir de CSVs de perguntas.")
    parser.add_argument("filtro", nargs="?", help="gera so os CSVs cujo nome contem este trecho")
    parser.add_argument("--listar", action="store_true", help="so lista os CSVs encontrados, sem gerar nada")
    parser.add_argument("--entrada", type=Path, default=ENTRADA_PADRAO, help=f"pasta dos CSVs (padrao: {ENTRADA_PADRAO})")
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO, help=f"pasta dos .apkg (padrao: {SAIDA_PADRAO})")
    parser.add_argument("--prefixo", default=PREFIXO_PADRAO, help=f'prefixo dos CSVs (padrao: "{PREFIXO_PADRAO}")')
    args = parser.parse_args(argv)

    csvs = descobrir_csvs(args.entrada, args.prefixo, args.filtro)
    if not csvs:
        alvo = f" com filtro {args.filtro!r}" if args.filtro else ""
        raise SystemExit(f"nenhum CSV '{args.prefixo}*.csv' encontrado em {args.entrada}{alvo}")

    print(f"CSVs encontrados ({len(csvs)}): {', '.join(c.name for c in csvs)}")
    if args.listar:
        return
    for caminho in csvs:
        montar_pacote(caminho, args.saida, args.prefixo)


if __name__ == "__main__":
    sys.exit(main())
