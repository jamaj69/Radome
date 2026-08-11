# Auditoria de tecnologia e espectro das estações Anatel

## Conclusão

A base dedicada de estações SMP permite identificar por registro a geração, a
tecnologia, a frequência central de transmissão da ERB e a largura necessária
da emissão. A base de radiodifusão permite identificar serviço, canal e
frequência central, mas não contém designação de emissão nem largura ocupada;
portanto, o intervalo espectral exato de cada rádio ou TV não pode ser obtido
somente desse CSV.

Esta auditoria processou os arquivos locais verificados em 10 de agosto de 2026:

- 3.284.526 registros de estações SMP;
- 35.126 registros de radiodifusão, dos quais 18.285 têm status `C4 — Canal
  Licenciado`.

Contagens abaixo são registros de licenciamento, não quantidades de torres
físicas. Um sítio pode possuir setores, portadoras, tecnologias e gerações
múltiplas.

## SMP

| Geração declarada | Tecnologia | Registros | Faixas declaradas mais frequentes | Centros Tx observados |
|---|---|---:|---|---:|
| 2G | GSM, CDMA, EDGE | 731.538 | 1800, 850, 900 MHz | 785,5–2.690 MHz |
| 3G | WCDMA | 664.536 | 850, 2100, 900 MHz | 778–3.450 MHz |
| 4G | LTE | 1.639.455 | 1800, 2500, 700, 2100 MHz | 464,5–3.450 MHz |
| 5G | NR | 241.188 | 3500, 2300, 2100 MHz; 26 GHz | 778–25.900 MHz |
| não informada | `N/I` ou `NA` | 7.809 | 700, 2500, 2300 MHz | 788–3.450 MHz |

Os campos relevantes são `Geração`, `Tecnologia`, `Tipo de Tecnologia 5G`,
`Faixa Estação`, `Subfaixa Estação`, `FreqTxMHz`, `FreqRxMHz` e `Designação
Emissão`. Para 5G, o cadastro contém 224.028 registros `SA-NSA`, 2.820 `NSA`, 39
`SA` e 14.301 sem subtipo informado.

Todas as 3.284.526 designações de emissão tiveram o prefixo de largura
necessária decodificado. Exemplos:

- `200KG7W`: 200 kHz;
- `5M00G7W`: 5 MHz;
- `10M0G7W`: 10 MHz;
- `100MG7W`: 100 MHz.

Para cada registro, o produto derivado calcula o intervalo preliminar
`FreqTxMHz ± largura_necessária/2`. Esse intervalo representa a largura
necessária declarada, não a máscara espectral completa nem emissões espúrias. O
campo `FreqRxMHz` representa a portadora recebida pela ERB e não deve ser
contado como emissão da torre. Foram encontrados valores Rx nulos ou não
positivos; eles são marcados como indisponíveis, nunca como frequência física.

As amplitudes totais da tabela são apenas mínimos e máximos observados, não
faixas contínuas. A análise por estação deve usar os centros, designações e
intervalos individualizados no produto derivado.

## Rádio e televisão

| Serviço | Interpretação | Registros C4 | Centros licenciados normalizados |
|---|---|---:|---:|
| FM | geradora FM | 3.658 | 76,1–107,9 MHz |
| RTRFM | retransmissora FM | 266 | 76,1–107,9 MHz |
| OM | onda média AM | 220 | 0,540–1,590 MHz |
| RTVD | retransmissora de TV digital | 13.165 | 177–695 MHz |
| GTVD | geradora de TV digital | 609 | 177–695 MHz |
| ECRD | estação complementar de radiodifusão | 367 | 82,9–683 MHz |

TV, TVA, RTV e PBTVD não possuem registros `C4` no arquivo atual; são canais
vagos, planejados ou mantidos em outros estados cadastrais e não entram como
iluminadores ativos. O valor de OM é armazenado em kHz na fonte e foi convertido
para MHz; FM e famílias de TV são armazenadas em MHz.

O cadastro de radiodifusão não contém tecnologia/modulação, designação de
emissão ou largura necessária por registro. Canal e frequência central são
suficientes para localização espectral nominal, mas os limites ocupados exigem
uma tabela regulatória versionada por serviço e tecnologia. Até essa integração,
o grafo não deve inventar largura de 200 kHz para FM ou 6 MHz para TV em cada
registro, mesmo quando esses valores sejam compatíveis com a canalização
regulatória geral.

## Produtos e reprodução

O script `audit_anatel_spectrum.py` gera:

- `reports/anatel_spectrum_summary.json`: resumo versionado da auditoria;
- `outputs/anatel_spectrum/smp_emissions.csv.gz`: emissão SMP individualizada;
- `outputs/anatel_spectrum/broadcast_emissions.csv.gz`: frequência central de
  cada registro de radiodifusão, com limitação espectral explícita.

```bash
/home/python/pyenv/bin/python audit_anatel_spectrum.py \
  --smp data/raw/anatel/estacoes_smp.zip \
  --broadcast data/raw/anatel/estacoes_radiodifusao.zip \
  --output-dir outputs/anatel_spectrum \
  --report reports/anatel_spectrum_summary.json
```

Próximo gate: incorporar esses atributos aos nós `torre_smp` e
`radiodifusao`, preservando emissões múltiplas por sítio, e baixar os atos
técnicos vigentes para completar a largura canalizada de rádio e televisão.

## Referências regulatórias para o próximo gate

- [Anatel — frequências autorizadas do SMP](https://www.gov.br/anatel/pt-br/regulado/outorga/telefonia-movel/frequencias-autorizadas);
- [Anatel — serviços de radiodifusão](https://www.gov.br/anatel/pt-br/regulado/radiodifusao/servicos-de-radiodifusao);
- [Anatel — regulamentação da radiodifusão](https://www.gov.br/anatel/pt-br/regulado/radiodifusao/regulamentacao);
- [Anatel — painel de estações de TV, FM e OM](https://www.gov.br/anatel/pt-br/assuntos/noticias/anatel-publica-painel-de-dados-sobre-servicos-de-radiodifusao).
