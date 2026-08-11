# Pré-seleção continental baseada na BC250

Execução inicial realizada sobre a BC250 2025 do IBGE:

- 127 pontos cotados de entrada;
- 75 candidatos após afastamento mínimo de 10 km;
- 97 picos nomeados usados para identificação por proximidade;
- 5.623 registros continentais de cidades e capitais;
- raio logístico exploratório de 250 km;
- oito setores azimutais para favorecer cidades distribuídas ao redor.

Os primeiros candidatos pela pontuação exploratória são:

| Ordem | Referência próxima | Cota IBGE (m) | Cidade mais próxima | Distância (km) | Pontuação |
|---:|---|---:|---|---:|---:|
| 1 | Pico da Bandeira | 2.891,3 | Alto Caparaó | 7,7 | 0,964 |
| 2 | Pedra da Mina | 2.798,0 | Passa Quatro | 13,3 | 0,946 |
| 3 | Agulhas Negras | 2.791,0 | Itatiaia | 15,8 | 0,943 |
| 4 | Pico dos Marins | 2.420,7 | Marmelópolis | 7,5 | 0,855 |
| 5 | Pedra Alta | 2.095,0 | São José do Barreiro | 7,1 | 0,772 |
| 6 | Pedra do Selado | 2.082,0 | Camanducaia | 18,4 | 0,770 |
| 7 | Morro Tira Chapéu | 2.088,0 | São José do Barreiro | 16,3 | 0,752 |
| 8 | Pico do Barbado | 2.033,3 | Piatã | 21,9 | 0,720 |
| 9 | Pico Paraná | 1.922,0 | Antonina | 21,7 | 0,710 |
| 10 | Morro da Boa Vista | 1.827,0 | Urubici | 17,2 | 0,700 |

Pico da Neblina e Monte Roraima continuam na lista, respectivamente nas posições
13 e 19. Suas grandes cotas são contrabalançadas nesta triagem pela baixa
densidade de cidades. Isso não os elimina: a etapa com MDE poderá recuperar sua
prioridade por área visível e importância regional.

## Limitações obrigatórias

- a BC250 contém poucos pontos altimétricos e concentra registros no Sudeste;
- proximidade não significa visada;
- não há ainda curvatura terrestre, bloqueio por relevo ou zona de Fresnel;
- a classificação não representa cobertura nacional nem define implantação;
- os 75 pontos servem para orientar recortes e validar o pipeline do MDE.

`candidates.geojson` abre diretamente no QGIS em SIRGAS 2000 (EPSG:4674).
`candidates.csv` preserva a tabela completa e a ordem da triagem.
