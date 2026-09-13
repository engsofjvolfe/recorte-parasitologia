# Avisos de licença

Este projeto usa duas licenças diferentes, para dois tipos de arquivo diferentes, mais
uma exceção para material de terceiros. Leia esta página inteira antes de reusar qualquer
coisa daqui. Se não compreender alguma coisa, busque ajuda com um agente de IA ou na internet.

## 1. Código (scripts Python) — GPL-3.0

O script Python deste repositório —
[`scripts/montar_deck.py`](scripts/montar_deck.py) — está sob a
**GNU General Public License v3.0**. Texto completo em [`LICENSE`](LICENSE). Resumindo:
você pode usar, estudar, modificar e redistribuir o código livremente, mas qualquer
trabalho derivado dele também precisa continuar sob GPL-3.0 (copyleft) e vir com o
código-fonte disponível. O script é agnóstico de disciplina: descobre os CSVs pelo
próprio schema, sem nome de disciplina fixado no código.

## 2. Conteúdo gerado — CC BY-NC-SA 4.0

**Regra geral: tudo neste repositório que não é código Python (item 1) nem material de
terceiros (item 3) está sob CC BY-NC-SA 4.0** — isso inclui, hoje, o dicionário de
gatilhos, a ficha determinística e a biologia fundamental (em
[`docs/material-gerado/`](docs/material-gerado/)), os CSVs de perguntas, os documentos de proposta de plataforma
em [`docs/proposta-plataforma/`](docs/proposta-plataforma/), e os documentos de
navegação da raiz (`README.md`, `INDICE.md`, `MANUAL.md`, este `NOTICE.md`). A regra é
por categoria, não por lista fechada de arquivos — um arquivo novo do mesmo tipo (mais
conteúdo, mais um relatório) já nasce coberto, sem precisar editar este aviso.

Está tudo sob **Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0
Internacional (CC BY-NC-SA 4.0)**. Texto completo em
[`LICENSE-CONTENT.txt`](LICENSE-CONTENT.txt). Resumindo: você pode usar, adaptar e
redistribuir esse conteúdo, desde que dê crédito, **não use para fins comerciais** e
mantenha qualquer versão adaptada sob a mesma licença.

## 3. Material de terceiros — fora de qualquer licença deste projeto

Os PDFs em [`docs/material-base/`](docs/material-base/) (`ASCARIS_E_ASCARIDIASE.pdf`,
`GEOHELMINTOS.pdf`, `HELMINTOS_I.pdf`, `ANCILOSTOMIDEOS.pdf`) - não versionados e não aparecem aqui, nem mesmo sua pasta -, **não são cobertos por
nenhuma das licenças acima**. São material de aula de uma disciplina de graduação de
Parasitologia — quem mantém este repositório não é o autor desses PDFs e não tem
autorização para relicenciá-los. Por isso:

- Essa pasta está no [`.gitignore`](.gitignore) e **nunca deve ser versionada, publicada
  ou redistribuída** junto com o restante do projeto — fica só localmente.
- Se você recebeu este projeto com essa pasta preenchida, trate como material pessoal de
  estudo, não como parte do pacote de código aberto.

## Como creditar

Se for reusar o conteúdo (item 2), credite como: "Núcleo de Parasitologia —
Helmintologia, licenciado sob CC BY-NC-SA 4.0", com link para este repositório.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
