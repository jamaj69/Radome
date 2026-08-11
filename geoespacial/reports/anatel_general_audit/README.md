# Auditoria inicial do pacote geral da Anatel

Esta etapa lê diretamente o ZIP oficial, sem extrair seus 10,45 GB, e audita os
quatro arquivos priorizados pelo gate M2E:

- `Estacoes_SARC.csv`;
- `Estacoes_Banda_Larga_Fixa.csv`;
- `Estacoes_Telefonia_Fixa.csv`;
- `Estacoes_SLE.csv`.

O relatório versionado está em `summary.json`; os registros normalizados e
reproduzíveis ficam em `outputs/anatel_general_audit/`.

## Regra de classificação RF

A direção explícita `Transmissão` ou `Recepção` tem precedência. Quando ela não
existe, somente classes exclusivamente transmissoras, exclusivamente receptoras
ou repetidoras fornecem evidência secundária. Classes fixas/base sem direção e
valores `N/I` ou `Usuário informou errado` permanecem desconhecidos. Portanto,
`active_potential_emitter_records` é um conjunto conservador de candidatos, não
uma confirmação de operação radioelétrica atual.

## Resultado

- SARC: 8.774 registros, todos com coordenadas e código IBGE; 5.926 ativos e
  4.228 ativos com evidência de transmissão/repetição. Há 4.583 frequências
  utilizáveis entre 153,02 e 12.751 MHz, mas nenhuma potência ou designação de
  emissão utilizável nessa versão.
- Banda larga fixa/SCM: 7.513 registros, todos com coordenadas e código IBGE;
  3.703 ativos e 1.850 ativos com direção de transmissão. Há 3.706 frequências
  e potências utilizáveis e 3.514 designações com largura decodificável. Os
  3.799 registros sem direção permanecem desconhecidos.
- Telefonia fixa/STFC: 589 registros, 75 ativos, todos georreferenciados, porém
  sem frequência, potência, classe ou direção utilizável; essa camada ainda não
  pode fornecer iluminadores RF.
- SLE: 119.058 registros, 118.968 ativos e 59.484 ativos com direção explícita
  de transmissão. A camada tem 115.458 coordenadas válidas e código IBGE em
  todos os registros; 118.968 linhas possuem designação decodificável, potência
  e altura, com frequências úteis entre 148 e 927,77 MHz. As 118.490 estações
  móveis e a simetria entre 59.484 linhas de recepção e 59.484 de transmissão
  exigem preservar o papel cadastral sem transformar cada registro em sítio
  fixo ou inferir automaticamente uma ponta de enlace.

Nenhum radioenlace foi pareado nesta etapa. SARC/SCM já passaram pela migração
canônica conservadora; o próximo gate audita SLP e Mosaico-STEL por streaming e
só depois define regras demonstráveis de pareamento.

## Reprodução

```bash
/home/python/pyenv/bin/python audit_anatel_general.py \
  --source data/raw/anatel/estacoes_licenciadas.zip \
  --output-dir outputs/anatel_general_audit \
  --report reports/anatel_general_audit/summary.json
```
