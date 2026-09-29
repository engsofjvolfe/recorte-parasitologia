# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere se o material gerado e 100% rastreavel a base de transcricoes. Agnostico de
materia: nao conhece nenhum nome de disciplina, agente ou arquivo. Documentacao em
scripts/README.md.

Dois modos:

1. Cartoes (padrao): para cada CSV de perguntas com as colunas "_fonte" e "_trecho",
   cada cartao precisa ter, em "_fonte", um ou mais localizadores "ARQUIVO § LOCAL"
   e, em "_trecho", o mesmo numero de trechos, na mesma ordem, separados por " || ".
   ARQUIVO e relativo a pasta da base; LOCAL e o titulo de uma secao do arquivo (ex.:
   "Slide 2") ou o ID de um bloco marcado como [ID] (ex.: "TRI-12"). O trecho tem de
   aparecer LITERALMENTE dentro dessa secao ou bloco (so espacos sao normalizados).

2. Citacoes (--citacoes DOC.md): todo ID no formato SIGLA-NN citado entre colchetes no
   documento (so ou junto de outros, como em "[slide 2; TRI-60]")
   precisa existir como bloco em algum arquivo da base. Com --cobertura ARQUIVO (relativo
   a pasta da base; pode repetir), todo bloco [ID] desse arquivo precisa estar citado no
   documento -- para achar trecho da base que ficou de fora do material.

Uso:
    python verificar_trechos.py                          # confere os CSVs de perguntas
    python verificar_trechos.py --citacoes ficha.md      # confere as citacoes de um .md
    python verificar_trechos.py --citacoes ficha.md --cobertura base.md   # e os blocos nao citados
    python verificar_trechos.py --base DIR --entrada DIR --prefixo PREFIXO
Sai com codigo 1 se qualquer trecho ou citacao nao for encontrado.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

COLUNA_FONTE = "_fonte"
COLUNA_TRECHO = "_trecho"
SEPARADOR_ITENS = " || "
SEPARADOR_LOCAL = " § "
PADRAO_ID = re.compile(r"\[([A-Z]{2,6}-\d{2,4})\]")
# citacao no texto: um ou mais IDs dentro dos colchetes, junto de outros localizadores ("[slide 2; TRI-60]")
PADRAO_COLCHETES = re.compile(r"\[([^\[\]]+)\]")
PADRAO_SIGLA = re.compile(r"\b[A-Z]{2,6}-\d{2,4}\b")

RAIZ = Path(__file__).resolve().parent.parent
BASE_PADRAO = RAIZ / "docs" / "material-base" / "gerados-ocr"
ENTRADA_PADRAO = RAIZ / "docs" / "material-gerado"
PREFIXO_PADRAO = "perguntas-"


def normaliza(texto):
    """Tira marcadores de citacao e de bloco de codigo do markdown e junta espacos, sem
    mexer em nenhuma palavra nem pontuacao."""
    linhas, dentro = [], False
    for linha in texto.split("\n"):
        if linha.strip().startswith("```"):
            dentro = not dentro
            continue
        # ">" no comeco da linha so e marca de citacao fora de bloco de codigo; dentro, e texto ("> 20.000")
        if not dentro:
            linha = re.sub(r"^\s*>\s?", "", linha)
        linhas.append(linha)
    return re.sub(r"\s+", " ", " ".join(linhas)).strip()


def recorta(texto, local):
    """Devolve o bloco [local] (ate o proximo bloco ou titulo) ou a secao cujo titulo
    contem `local` (ate o proximo titulo de mesmo nivel ou acima)."""
    linhas = texto.split("\n")
    marca = f"[{local}]"
    # o bloco e o que comeca pela marca (ex.: "**[TRI-12] ..."); uma remissao ("Ver tambem: [TRI-12]") nao e o bloco
    cabecalhos = [i for i, linha in enumerate(linhas) if linha.lstrip("*#> ").startswith(marca)]
    for i, linha in enumerate(linhas):
        if (i in cabecalhos) if cabecalhos else (marca in linha):
            fim = next((j for j in range(i + 1, len(linhas))
                        if linhas[j].startswith("#") or PADRAO_ID.search(linhas[j])), len(linhas))
            return "\n".join(linhas[i + 1:fim])
    for i, linha in enumerate(linhas):
        m = re.match(r"^(#+)\s+(.*)$", linha)
        if m and local in m.group(2):
            nivel = len(m.group(1))
            fim = next((j for j in range(i + 1, len(linhas))
                        if re.match(r"^#{1,%d}\s" % nivel, linhas[j])), len(linhas))
            return "\n".join(linhas[i + 1:fim])
    return None


def confere_cartoes(pasta_entrada, pasta_base, prefixo):
    csvs = sorted(pasta_entrada.glob(f"{prefixo}*.csv"))
    erros, conferidos = [], 0
    cache = {}
    for caminho in csvs:
        with open(caminho, encoding="utf-8", newline="") as f:
            leitor = csv.DictReader(f)
            if COLUNA_FONTE not in (leitor.fieldnames or []) or COLUNA_TRECHO not in leitor.fieldnames:
                print(f"{caminho.name}: sem colunas {COLUNA_FONTE}/{COLUNA_TRECHO} -- nao conferido.")
                continue
            for n, linha in enumerate(leitor, start=2):
                fontes = [x.strip() for x in (linha[COLUNA_FONTE] or "").split(SEPARADOR_ITENS) if x.strip()]
                trechos = [x.strip() for x in (linha[COLUNA_TRECHO] or "").split(SEPARADOR_ITENS) if x.strip()]
                rotulo = f"{caminho.name}, linha {n}"
                if not fontes or len(fontes) != len(trechos):
                    erros.append(f"{rotulo}: {len(fontes)} fonte(s) para {len(trechos)} trecho(s).")
                    continue
                for fonte, trecho in zip(fontes, trechos):
                    if SEPARADOR_LOCAL not in fonte:
                        erros.append(f"{rotulo}: fonte sem '{SEPARADOR_LOCAL.strip()}': {fonte!r}")
                        continue
                    arquivo, local = [p.strip() for p in fonte.split(SEPARADOR_LOCAL.strip(), 1)]
                    caminho_base = pasta_base / arquivo
                    if caminho_base not in cache:
                        if not caminho_base.exists():
                            erros.append(f"{rotulo}: arquivo da base nao existe: {arquivo}")
                            continue
                        cache[caminho_base] = caminho_base.read_text(encoding="utf-8")
                    secao = recorta(cache[caminho_base], local)
                    if secao is None:
                        erros.append(f"{rotulo}: local {local!r} nao encontrado em {arquivo}")
                    elif normaliza(trecho) not in normaliza(secao):
                        erros.append(f"{rotulo}: trecho nao encontrado em {arquivo} § {local}: {trecho[:90]!r}")
                    else:
                        conferidos += 1
    return erros, conferidos


def blocos(texto):
    """IDs dos blocos definidos no texto (linha que comeca pela marca [ID]), na ordem."""
    return [m.group(1) for m in (PADRAO_ID.match(l.lstrip("*#> ")) for l in texto.split("\n")) if m]


def confere_citacoes(documento, pasta_base, cobertura=()):
    ids_base = set()
    for arq in pasta_base.glob("*.md"):
        ids_base |= set(PADRAO_ID.findall(arq.read_text(encoding="utf-8")))
    citados = [i for c in PADRAO_COLCHETES.findall(documento.read_text(encoding="utf-8")) for i in PADRAO_SIGLA.findall(c)]
    erros = [f"{documento.name}: [{i}] nao existe na base" for i in sorted(set(citados) - ids_base)]
    for arq in cobertura:
        caminho = pasta_base / arq
        if not caminho.exists():
            erros.append(f"arquivo da base nao existe: {arq}")
            continue
        fora = [i for i in blocos(caminho.read_text(encoding="utf-8")) if i not in set(citados)]
        erros += [f"{documento.name}: bloco [{i}] de {arq} nao citado" for i in fora]
    return erros, len(citados)


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere a rastreabilidade do material gerado a base de transcricoes.")
    p.add_argument("--citacoes", type=Path, help="documento .md cujas citacoes [SIGLA-NN] serao conferidas")
    p.add_argument("--cobertura", action="append", default=[], metavar="ARQUIVO",
                   help="com --citacoes: arquivo da base cujos blocos [ID] tem de estar todos citados (pode repetir)")
    p.add_argument("--base", type=Path, default=BASE_PADRAO, help=f"pasta das transcricoes (padrao: {BASE_PADRAO})")
    p.add_argument("--entrada", type=Path, default=ENTRADA_PADRAO, help=f"pasta dos CSVs (padrao: {ENTRADA_PADRAO})")
    p.add_argument("--prefixo", default=PREFIXO_PADRAO, help=f'prefixo dos CSVs (padrao: "{PREFIXO_PADRAO}")')
    a = p.parse_args(argv)

    if a.citacoes:
        erros, total = confere_citacoes(a.citacoes, a.base, a.cobertura)
        tipo = "citacoes"
    else:
        erros, total = confere_cartoes(a.entrada, a.base, a.prefixo)
        tipo = "trechos"
    for e in erros:
        print("ERRO:", e)
    print(f"{total} {tipo} conferidos, {len(erros)} erro(s).")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
