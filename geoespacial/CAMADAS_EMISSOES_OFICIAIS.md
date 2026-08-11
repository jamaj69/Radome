# Inventário de camadas oficiais de emissões

**Reanálise:** 10 de agosto de 2026.

## Critério de prontidão

Uma camada de emissores somente fica pronta para gerar uma aresta analítica
`illuminates` quando permite recuperar ou derivar, com proveniência explícita:

1. identidade, tipo e estado operacional da estação;
2. longitude, latitude e código IBGE municipal;
3. altitude do terreno e altura do centro radiante;
4. frequência central, sentido de transmissão e largura necessária/canalizada;
5. potência Tx ou ERP/EIRP;
6. polarização, ganho, azimute, elevação e abertura do diagrama;
7. data/ciclo da fonte e vínculo com o registro original.

Ausência de qualquer item não elimina a estação do inventário. Ela reduz o
nível de uso: localização, diversidade espectral, horizonte geométrico ou
modelo RF completo.

## Matriz reavaliada

| Camada oficial | Localização | Altitude/altura | Espectro | Potência/diagrama | Integração atual | Lacuna decisiva |
|---|---|---|---|---|---|---|
| SMP 2G/3G/4G/5G — Anatel | coordenadas e município | altitude de terreno preliminar; sem altura radiante no recurso dedicado | Tx/Rx, faixa, tecnologia e largura ITU por registro | ausentes no recurso SMP dedicado | esquema canônico: 105.726 sítios, 282.623 proxies de antena e 3.284.526 emissões sem perdas | revisar 23 conflitos municipais e buscar parâmetros radiométricos complementares |
| TV/RTV/GTVD/RTVD/FM/RTRFM/OM — Anatel | coordenadas e município | HCI existe, unidade/semântica por serviço ainda não fechada | centro e canal; largura não declarada no CSV | ERP existe, unidade/semântica ainda não fechada | licenciadas C4 integradas por sítio | congelar atos de canalização e normalizar ERP/HCI |
| VOR/DVOR — DECEA/ICA | 77/77 | elevação 76/77; altura de antena 0/77 | frequência 77/77, 112–117,7 MHz | potência e diagrama ausentes | baixada e inventariada | recortar Brasil, ligar município e obter potência/altura por AIP/ROTAER ou outra fonte oficial |
| NDB — DECEA/ICA | 24/24 | elevação 19/24 | frequência 24/24, 114,3–407 kHz; banda de emissão 1/24 | potência/diagrama ausentes | baixada e inventariada | completar elevação e parâmetros RF oficiais |
| DME — DECEA/ICA | 173/173 | elevação 158/173 | canal 173/173; portadora UHF ainda não derivada | potência/diagrama ausentes | baixada e inventariada | versionar tabela oficial canal--frequência e reconciliar DME pareados |
| ILS/LOC e relações `navaids` — DECEA/ICA | 124/124 | elevação 30/124 | frequência ausente na visão agregada | ausentes | baixada como relação | obter componentes/frequências oficiais e evitar contar o mesmo conjunto duas vezes |
| SARC — Anatel | 4.228 emissões ativas em 2.362 sítios | preservada quando disponível | 1.466 com frequência; designação/largura ausentes | ganho/diagrama preservados; potência ausente | esquema canônico; nenhuma quantitativamente pronta | buscar complemento oficial e não criar `illuminates` quantitativo |
| Banda larga fixa/SCM — Anatel | 1.850 emissões Tx ativas em 973 sítios | 1.849 com altura | frequência e potência em 1.850; duas sem designação | 1.849 atendem presença mínima de frequência/potência/altura | esquema canônico, enlaces não pareados | validar parâmetros e parear somente após auditoria das demais bases |
| Telefonia fixa/STFC — Anatel | 589/589 coordenadas e municípios | indisponível | indisponível | indisponível | auditado; não pronto para RF | manter como infraestrutura até complemento oficial |
| SLE — Anatel | 115.458/119.058 coordenadas válidas; código IBGE em todas as linhas | 118.968 com altura | 118.954 frequências úteis; 118.968 designações decodificáveis | 118.968 com potência; ganho disponível em apenas 578 | auditado; 59.484 Tx ativos e 118.490 linhas móveis; sem pareamento | não converter móveis em sítios fixos; definir integração após SLP/STEL |
| SLP/Mosaico-STEL — Anatel | campos de coordenada e município no pacote geral | campo de altura de antena | frequência e designação de emissão | potência, polarização, ganho, azimute, elevação e abertura disponíveis no esquema | pacote baixado; arquivos de cerca de 5 GB ainda não classificados | inventariar serviços e reconciliar pontas somente com evidência explícita |
| Radioamador — Anatel | município, sem coordenada precisa no recurso atual | ausente | frequências declaradas de forma agregada | ausentes | baixado, não integrado | baixa prioridade e atividade temporal desconhecida |
| Estações marítimas — Anatel | predominantemente móveis; arquivo sem coordenada geográfica útil | ausente | frequências/potências agregadas | incompletos | baixado, não integrado | separar estações costeiras fixas de embarcações móveis |
| Estações terrenas/VSAT — Anatel | fonte oficial identificada | a auditar | a auditar | a auditar | não baixada | adquirir base “Estações Terrenas em Bloco” e cruzar com SLP/SCM/STFC |
| Radares meteorológicos — Cemaden/SIPAM/INMET e parceiros | lista oficial com coordenadas identificada | a auditar | banda S/C/X em parte da fonte | potência/diagrama não confirmados | fonte identificada, não estruturada | adquirir tabela oficial e separar radares ativos de sensores passivos |
| Radares aeronáuticos civis — DECEA | sem camada pública estruturada confirmada | — | — | — | pendente | localizar fonte pública oficial sem inferir radar por aeródromo |
| Radares e emissores militares — FAB/Defesa | sem camada pública estruturada confirmada | — | — | — | `blocked_public_source` | cadastrar somente informação oficialmente publicável |

CTR, TMA, ZIDA, aeródromos, pistas e OPEA são contexto ou restrição, não
emissores por si mesmos. Satélites, aeronaves, embarcações e terminais móveis
exigem modelos temporais/órbitas/trajetórias e não devem virar sítios fixos.

## Principal descoberta da reanálise

O pacote geral `estacoes_licenciadas.zip` da Anatel já foi baixado e verificado,
mas ainda não foi explorado como camada de iluminadores. Ele contém 13 arquivos
e 10,45 GB descompactados. Nos recursos SLP, SLE, SARC, Mosaico/STEL, banda
larga fixa e telefonia fixa, o esquema oferece os atributos que faltam nas
camadas simplificadas: designação de emissão, polarização, ganho, relação
frente--costa, abertura, azimute, elevação, altura de antena, frequência e
potência do transmissor.

Isso muda a prioridade: antes de buscar um recurso separado chamado
“radioenlaces SMP”, deve-se classificar o pacote geral por serviço, classe,
direção e estação. A regulamentação da Anatel determina que radioenlaces fora
do mesmo local das estações do serviço sejam licenciados como SLP ou sucessor;
logo, SLP/STEL é uma fonte provável das pontas de enlace, mas essa hipótese deve
ser demonstrada pelos campos e registros, não apenas pelo nome do serviço.

## Novo gate de emissões oficiais — M2E

O gate M2E estará concluído quando:

- existir um esquema canônico `emissor`/`emissao` que preserve relação um-para-
  muitos entre sítio físico, antena e portadora;
- SMP e radiodifusão forem regenerados nesse esquema sem perder tecnologia,
  largura, ERP, HCI ou conflitos;
- VOR, NDB e DME brasileiros tiverem código IBGE e espectro normalizado;
- SLP/SLE/SARC/STEL forem inventariados por serviço e direção, com radioenlaces
  reconciliados em duas pontas quando possível;
- VSAT e radares meteorológicos tiverem decisão documentada de inclusão;
- cada atributo ausente ou derivado tiver fonte e confiança explícitas.

M2E não exige potência perfeita para manter um nó no grafo, mas proíbe criar
`illuminates` quantitativo quando potência, altura ou diagrama indispensáveis
forem desconhecidos.

## Sequência revisada

1. **concluído:** criar o esquema canônico sítio--antena--emissão e migrar as
   3.284.526 emissões SMP sem perdas;
2. **parcialmente concluído:** SARC, banda larga fixa, telefonia fixa e SLE
   foram auditados; faltam SLP e Mosaico/STEL;
3. **concluído:** migrar 6.078 registros ativos SARC/SCM com evidência de
   transmissão/repetição;
4. auditar SLP/STEL e parear radioenlaces somente quando demonstrável;
5. normalizar ERP/HCI e canalização de radiodifusão;
6. recortar VOR/NDB/DME ao Brasil, associar municípios e derivar DME por tabela
   oficial;
7. obter frequências/componentes ILS/LOC e decidir VSAT/radares meteorológicos;
8. somente então calcular disponibilidade e qualidade de iluminadores na Fase 6.

## Fontes oficiais adicionais identificadas

- [Anatel — Dados Abertos](https://www.gov.br/anatel/pt-br/dados/dados-abertos);
- [Anatel — Serviço Limitado Privado](https://www.gov.br/anatel/pt-br/regulado/outorga/servico-limitado-privado);
- [Anatel — Regulamento Geral de Licenciamento](https://www.gov.br/anatel/pt-br/regulado/outorga/regulamento-geral-de-licenciamento);
- [Anatel — licenciamento de estações terrenas](https://www.gov.br/anatel/pt-br/regulado/satelite/licenciamento-de-estacoes-terrenas);
- [Cemaden — Plano Diretor 2024–2027, com inventário interinstitucional de radares meteorológicos](https://www.gov.br/cemaden/pt-br/acesso-a-informacao/institucional-1/planodiretor_2024_2027_revisado_bs08.pdf).
