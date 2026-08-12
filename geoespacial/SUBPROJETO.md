# Subprojeto de seleção geoespacial

## Vinculação ao projeto principal

Este diretório é um subprojeto científico e reprodutível do projeto principal
RADOME. O produto principal continua sendo o artigo técnico bilíngue, cujas
edições autoritativas são `projeto/radome-pt-br.tex` e
`projeto/radome-en.tex`. O subprojeto geoespacial não é uma publicação
independente: ele produz a evidência, os métodos, as tabelas e as figuras que
sustentarão a seleção de sítios descrita no artigo.

No artigo, a interface inicial é o capítulo de infraestrutura e validação de
cada idioma:

- `projeto/chapters/pt-BR/08_infrastructure_validation.tex`;
- `projeto/chapters/en/08_infrastructure_validation.tex`.

Resultados de cobertura, iluminação ou número de sítios somente poderão entrar
nesses capítulos depois de passarem pelo gate de integração abaixo.

## Missão e limites

A missão é selecionar, de forma auditável, o menor conjunto de sítios
continentais capaz de atender aos requisitos de cobertura e conectividade da
rede, considerando relevo, cidades, logística e iluminadores de oportunidade.
Arquipélagos e ilhas oceânicas permanecem estudos posteriores e independentes.

O subprojeto produz triagem e evidência de engenharia; não concede autorização
de implantação e não transforma cobertura geométrica em alegação de detecção.

## Documentos de controle

- `REQUISITOS_GEOLOCALIZACAO.md`: contrato normativo e instruções do usuário;
- `ROADMAP_GEOESPACIAL.md`: inventário, fases, estados e gates;
- `METODOLOGIA_ARTIGO.md`: texto intermediário para futura redação científica;
- `HEURISTICA_MALHA_TRIANGULAR.md`: linha experimental de tesselação cooperativa;
- `data/manifests/`: proveniência, datas, URLs, licenças e hashes;
- `reports/`: auditorias e resultados pequenos;
- `outputs/`: produtos derivados volumosos e regeneráveis;
- scripts e testes: execução reproduzível do método.

`POLITICA_REPRODUTIBILIDADE.md` é obrigatória: toda manipulação autoritativa das
bases pertence a scripts Python versionados.

## Gate de integração com o artigo

Uma afirmação quantitativa geoespacial só pode ser incorporada às duas edições
do artigo quando possuir:

1. fonte oficial e versão ou data de aquisição;
2. manifesto com hash dos arquivos de entrada;
3. configuração e comando reproduzíveis;
4. relatório de ausências, conflitos, descartes e limitações;
5. produto tabular ou geográfico que permita auditoria;
6. commit Git que reúna método, evidência e resultado;
7. redação equivalente em português e inglês, seguida da compilação dos dois
   documentos autoritativos.

## Visualização topográfica e WebGL

`blender_topografia_radomes/` é uma camada de comunicação e inspeção, não uma
fonte de decisão operacional. Ela preserva uma malha local TOPODATA a 30 m por
vértice e uma cena regional subamostrada para os três marcadores atuais. O modo
regional recebe uma moldura WGS84, seleciona/baixa/valida/extrai automaticamente
as folhas ZN necessárias, aplica Blue Marble por UV equiretangular geográfico e
renderiza na proporção da moldura, sem uma moldura artificial de fundo.

O Brasil não deve ser materializado em uma única malha ou PNG a 30 m: seriam
bilhões de vértices/pixels e centenas de gigabytes a terabytes de memória de
trabalho. Para navegação interativa na internet, a evolução aprovada é um
visualizador WebGL paginado por blocos, com LOD, streaming e descarte de tiles
fora do campo de visão. CesiumJS com quantized-mesh ou 3D Tiles é o candidato
preferencial; Blender permanece destinado a renders estáticos. Essa evolução não
autoriza inferências sobre visada, RF, implantação ou desempenho operacional.

## Marcos ativos: M2E e M3

O fechamento das emissões oficiais (M2E) e a infraestrutura aeronáutica (M3)
são trilhas acopladas. M2E é detalhado em `CAMADAS_EMISSOES_OFICIAIS.md`; M3
mantém o seguinte pacote:

1. baixar e congelar por ciclo AIRAC as 14 camadas selecionadas no WFS do
   DECEA, das quais VOR, NDB, DME e `navaids` já foram adquiridas;
2. reconciliar aeródromos e pistas de ANAC, IBGE BC250 e DECEA por ICAO, CIAD,
   nome e distância;
3. integrar helipontos, obstáculos OPEA, VOR, NDB e demais auxílios à navegação;
4. etiquetar cada objeto com código IBGE e preservar a proveniência por registro;
5. separar explicitamente aeródromo, auxílio RF, radar e instalação militar,
   sem inferir uso militar apenas pelo nome.

O gate M3 exige proveniência oficial por objeto, conflitos quantificados e um
grafo reconciliado município--infraestrutura aeronáutica. M2E fecha em paralelo
a classificação de radioenlaces no pacote geral Anatel, a auditoria de conflitos
e a co-localização de emissores; ele não bloqueia a aquisição versionada das
camadas DECEA, mas antecede qualquer aresta RF quantitativa `illuminates`.
