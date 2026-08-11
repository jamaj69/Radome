# Requisitos preservados para geolocalização dos radomes

Este documento registra as instruções do usuário que governam a análise
geoespacial. Ele é uma fonte normativa intermediária para a futura seção de
metodologia do artigo. Resultados exploratórios não alteram estes requisitos;
qualquer mudança deve ser registrada explicitamente, com justificativa e data.

## Escopo territorial

1. A otimização ativa cobre somente o território continental brasileiro.
2. Arquipélagos e ilhas oceânicas não participam da restrição de conectividade
   visual da rede continental.
3. Cada grupo de ilhas oceânicas próximas terá um único radome, cujo ótimo
   local será escolhido posteriormente em estudo independente.
4. Não se deve somar os casos insulares à contagem mínima continental antes dos
   respectivos estudos locais.

## Objetivo primário

1. Instalar o menor número possível de radomes que cubra o território do escopo.
2. A quantidade de radomes tem precedência sobre pontuações secundárias.
3. Se a cobertura total não for demonstrável, apresentar a curva entre número
   de sítios, fração coberta e lacunas, sem declarar cobertura nacional.

## Relevo, visada e conectividade

1. Priorizar linhas de maior altitude, cumeadas, máximos locais e pontos de
   interesse de defesa do espaço aéreo.
2. Um radome em local alto recebe maior peso quando cobre maior área.
3. Deve haver visada direta entre pelo menos dois radomes da rede continental;
   na formulação operacional, nenhum sítio continental selecionado pode ficar
   isolado.
4. Curvatura terrestre, refração padrão e relevo intermediário devem ser
   considerados. A zona de Fresnel será avaliada por faixa em fase posterior.
5. Raios baseados somente no horizonte são limites superiores, não cobertura ou
   visada confirmada.

## Cidades, municípios e logística

1. Favorecer locais altos com cidades próximas e distribuídas ao redor, mesmo
   que as cidades estejam abaixo do radome.
2. Não existe distância logística máxima eliminatória. Mais cidades abaixo e ao
   redor do sítio aumentam sua pontuação.
3. Cada município é um nó próprio identificado pelo código IBGE de sete dígitos.
4. O nó municipal possui `x` longitude, `y` latitude e `z` altitude da sede.
5. O tamanho visual do nó representa a área municipal. População é atributo
   separado e pode sustentar outra visualização ou ponderação explícita.
6. Torres e demais objetos devem receber código municipal e uma relação
   `located_in` com o nó correspondente.

## Grafo de infraestrutura e iluminadores

1. A pré-seleção deve representar capitais, aeroportos e comandos aéreos como
   possíveis candidatos ou referências, quando houver fonte oficial.
2. O raio visual de um candidato depende de altitude, topografia, curvatura da
   Terra e altitude-alvo.
3. Cada nó candidato deve informar o número de cidades próximas ou visíveis
   dentro de seu raio, distinguindo claramente proximidade de visibilidade.
4. Incorporar torres celulares, estações de rádio, FM, televisão e repetidoras,
   radares e infraestrutura aeronáutica como fontes potenciais de iluminação.
5. A existência de uma estação licenciada não demonstra que ela esteja ativa,
   radiando continuamente ou gerando ecos detectáveis. Status regulatório,
   frequência, ERP, polarização, altura, diagrama, terreno e geometria biestática
   devem ser preservados para filtragem posterior.
6. Bases e comandos militares só podem ser classificados quando uma fonte
   pública oficial sustentar a classificação.

## Reprodutibilidade e publicação

1. Manter scripts, configurações, documentação, hashes e relatórios suficientes
   para incorporar o processo de escolha ao artigo.
2. Preservar a origem, a data, a versão e a confiança de cada atributo.
3. Separar arquivos brutos, produtos derivados e resultados versionados.
4. Registrar hipóteses ainda dependentes de simulação ou medição e não converter
   diagramas ou modelos geométricos em alegações de desempenho operacional.
5. A futura redação metodológica deverá existir nas edições portuguesa e
   inglesa, mantendo equivalência técnica.

## Decisões operacionais derivadas

Estas decisões implementam os requisitos sem substituí-los:

- código IBGE é a chave canônica de integração municipal;
- aresta `located_in` liga infraestrutura ao município;
- `C4 — Canal Licenciado` é o filtro inicial de radiodifusão ativa;
- registros SMP e de radiodifusão são agregados por sítio, preservando os
  registros de origem e marcas de conflito;
- altitude Terrarium é preliminar e deve ser substituída pelo TOPODATA;
- cobertura eletromagnética e detectabilidade são fases posteriores ao grafo
  geométrico e ao inventário de iluminadores.
