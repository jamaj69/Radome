# Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos
## Projeto conceitual revisado para sensoriamento eletromagnetico passivo, radiogoniometria e localizacao multiestatica

> Revisao tecnica do documento-base `RadomeBrasil.pdf`. Documento conceitual para pesquisa, simulacao e prototipagem; desempenho deve ser confirmado por ensaios.

## Resumo

O documento-base propunha uma rede de radomes geodesicos multifacetados, instalados em pontos afastados, com antenas de banda larga em cada face, digitalizacao local, sincronizacao por fibra optica e processamento central para localizacao tridimensional. A ideia nuclear - uma rede passiva, coerente e multiestatica - e tecnicamente defensavel. Entretanto, a formulacao original misturava escalas eletromagneticas incompatíveis, atribuía a cada face uma cobertura de HF a Ka, tratava polarizacao circular como requisito universal e extrapolava a precisao de White Rabbit para coerencia de fase em dezenas de gigahertz.

Este projeto revisado substitui a antena unica de espectro total por uma abertura conformal multifaixa composta por subsistemas independentes: HF, VHF/UHF, L/S/C, X/Ku e K/Ka. Cada subsistema possui duas portas ortogonais coerentes, permitindo sintetizar RHCP, LHCP, polarizacao linear ou eliptica no dominio digital. Em HF, a direcao nao e atribuida a uma face isolada; explora-se diversidade de padroes, loops e dipolos cruzados e, quando viavel, modos caracteristicos da plataforma. Em micro-ondas, tiles phased-array executam varredura eletronica com sobreposicao entre faces.

A rede utiliza canais de referencia e vigilancia, cancelamento do sinal direto, funcao de ambiguidade cruzada, estimacao AOA/TDOA/FDOA e fusao estatistica. White Rabbit e apropriado para distribuicao deterministica de tempo e frequencia, mas deve ser acompanhado de calibracao de toda a cadeia analogica e de osciladores locais de baixo jitter. O resultado e uma arquitetura verificavel por etapas, com limites declarados e plano de demonstracao em tres nos antes de qualquer expansao territorial.

## Palavras-chave

radome conformal; antena multifaixa; radar passivo; radiogoniometria; polarimetria; TDOA; FDOA; White Rabbit; phased array; HF.

## 1. Escopo e natureza do projeto

O presente texto e uma revisao tecnica do arquivo RadomeBrasil.pdf [1]. Preservam-se a topologia distribuida, a digitalizacao na borda, o uso de fibra optica e a fusao multiestatica. Corrigem-se as partes que contrariavam limites de abertura, largura de banda, coerencia e propagacao.

O projeto e conceitual: define arquitetura, interfaces, requisitos mensuraveis e etapas de verificacao. Nao fixa marcas comerciais, locais de implantacao, frequencias protegidas ou desempenho operacional. Valores apresentados como metas devem ser validados em simulacao eletromagnetica, bancada, camara anecoica e campanhas de campo.

A aplicacao cientifica abrange monitoramento do espectro, radiogoniometria, deteccao passiva de emissores, observacao de reflexoes por iluminadores de oportunidade, rastreio cooperativo, astronomia e vigilancia de objetos aereos ou espaciais, observadas as normas de telecomunicacoes, privacidade e seguranca.

## 2. Diagnostico do documento-base

O documento original descreve corretamente o fluxo antena-ADC-FPGA-fibra-central e reconhece a necessidade de canais de referencia e vigilancia. Tambem acerta ao propor sobreposicao angular entre faces. Os problemas aparecem quando a cobertura espectral e tratada como se um mesmo painel, LNA e ADC fossem adequados de 3 MHz a 40 GHz, e quando a precisao de sincronismo e convertida diretamente em precisao espacial sem orçamento de incerteza.

| Item | Decisao na revisao | Justificativa tecnica |
| --- | --- | --- |
| Rede de varios radomes | Mantida | A diversidade espacial permite AOA/TDOA/FDOA e melhora a geometria da estimacao. |
| Digitalizacao proxima da antena | Mantida com particionamento | Reduz perdas de cabo, mas cada subfaixa exige cadeia RF e taxa de amostragem proprias. |
| Uma antena por face de HF a Ka | Substituida | A razao espectral supera 13.000:1; abertura, substrato, alimentacao e espacamento de elementos sao incompatíveis. |
| Polarizacao circular fixa | Substituida por dual-pol coerente | Duas componentes ortogonais preservam qualquer estado de polarizacao e geram RHCP/LHCP digitalmente. |
| Diretividade de cada face em HF | Rejeitada | Uma face de poucos metros e eletricamente pequena em HF; a direcao vem de diversidade modal e de rede. |
| White Rabbit como garantia de fase em Ka | Corrigida | WR oferece tempo subnanosegundo, mas coerencia de portadora em Ka exige jitter e calibracao muito mais rigorosos. |
| Juntas com espessura lambda/2 universal | Rejeitada | Uma junta sintonizada em uma frequencia nao e transparente em quatro decadas; exige otimizacao full-wave e medicao angular. |
| Precisao metrica por dias de holdover | Rejeitada como promessa | O erro depende do oscilador, temperatura, propagacao e geometria; deve ser expresso como covariancia medida. |

## 3. Requisitos funcionais e criterios de sucesso

O requisito principal nao deve ser “receber tudo simultaneamente”, mas “cobrir um conjunto definido de subfaixas com canais coerentes, calibrados e selecionaveis”. A cobertura instantanea e limitada por numero de conversores, largura de banda de processamento e vazao da rede. A cobertura sintonizavel pode ser muito maior.

Cada deteccao deve transportar, alem de frequencia e potencia, o instante de chegada, fase relativa, estado de polarizacao, direcao estimada, largura de banda, Doppler, identificador da cadeia RF e indicadores de qualidade.

| Categoria | Meta conceitual | Metodo de verificacao |
| --- | --- | --- |
| Cobertura angular | Hemisferio superior sem lacunas persistentes; sobreposicao entre faces | Medicao OTA com fonte em malha angular e mapa de ganho ativo |
| Polarizacao | Dois canais ortogonais calibrados; sintese RHCP/LHCP e Stokes | Fonte polarimetrica conhecida e erro de razao axial |
| Sincronismo | Timestamp subnanosegundo na rede optica; erro ponta a ponta caracterizado | Time interval counter, loopback optico e injecao RF comum |
| Direcao de chegada | Estimativa com covariancia e calibracao por frequencia | Campanha com emissores de posicao conhecida |
| Radar passivo | Canal de referencia e vigilancia simultaneos | Alvo cooperativo e iluminador conhecido |
| Resiliencia | Holdover local e dados armazenados sem prometer coerencia ilimitada | Teste de perda de fibra e curva de erro versus tempo |
| Radome | Perda e erro de apontamento medidos para TE/TM, incidencia e umidade | Painel-amostra em espaco livre e camara climatica |

## 4. Arquitetura de sistema revisada

Cada estacao e um no sensor coerente. O no recebe sinais diretos de emissores, sinais emitidos por objetos e sinais refletidos. A rede central nao “triangula qualquer energia” automaticamente: ela associa observacoes da mesma forma de onda, identifica ou estima o iluminador e escolhe o modelo adequado - emissor direto, reflexao bistatica, interferometria ou rastreio orbital.

A topologia recomendada e hierarquica. Clusters locais, com linhas de base de dezenas de quilometros, atendem alvos de baixa altitude e iluminadores regionais. Clusters regionais, com centenas de quilometros, ampliam a cobertura. Linhas de base continentais ou oceanicas sao mais adequadas a HF, sinais de alta altitude e objetos espaciais, desde que haja campo de visada e iluminador comum.

![Figura 1 - Arquitetura distribuida: iluminadores, objeto, nos receptores, rede de tempo/dados e centro de fusao.](figures/fig01_arquitetura_rede.png)

## 5. Radome geodesico e distribuicao das aberturas

O radome deve ser entendido como plataforma mecanica e eletromagnetica, nao como um conjunto de faces identicas. Nas faixas em que uma face tem dimensao comparavel a varios comprimentos de onda, ela pode conter um subarray direcional. Em HF, toda a plataforma e eletricamente pequena ou moderada, e a separacao por face perde significado.

A configuracao proposta usa uma casca dielétrica com setores funcionais. Tiles de micro-ondas podem ser repetidos em muitas faces; sensores HF/VHF podem ocupar anéis, elementos centrais ou excitadores distribuidos. A selecao das faces ativas depende da direcao desejada, do acoplamento e do padrao ativo de cada elemento. Arranjos conformais esfericos e dodecaedricos demonstram que cobertura angular extensa e polarizacao circular sao possiveis quando os elementos e as fases sao projetados conjuntamente [7].

![Figura 2 - Zonamento funcional de uma plataforma quase esferica. As cores indicam familias de subsistemas, nao divisorias eletromagneticas rigidas.](figures/fig02_zonamento_radome.png)

## 5.1 Geometria preliminar

Nao se recomenda fixar faces de 2,3 m antes de definir a frequencia inferior de cada tile, o angulo de varredura, a carga de vento e o metodo de manutencao. Para um demonstrador, um domo de 4 a 6 m pode acomodar dezenas de tiles de VHF a Ka e sensores de baixa frequencia internos ou periféricos. A escala HF deve ser avaliada pelo raio da menor esfera que envolve a plataforma e pelo parametro ka = 2 pi a/lambda.

Para phased arrays, o espacamento dos elementos deve evitar lobos de grade na frequencia mais alta e no maior angulo de varredura. Como regra conservadora, usa-se d proximo ou inferior a lambda_min/2; em varredura ampla, o limite e ainda menor. Por isso, a densidade de elementos cresce fortemente em Ku/Ka e nao pode ser compartilhada geometricamente com HF.

## 5.2 Parede do radome, juntas e estrutura

Uma parede A-sandwich de peles dielétricas e nucleo de baixa densidade e um ponto de partida, mas sua espessura nao pode ser escolhida por uma unica condicao lambda/2. Paredes compostas podem ser otimizadas para duas ou tres janelas de transmissao [17], e o projeto mecanico e eletromagnetico deve ser multiobjetivo [18].

As peles devem usar materiais de baixa tangente de perdas, como tecido de quartzo ou GFRP qualificado, com resina apropriada; fibra de carbono e estruturas metalicas continuas devem ser evitadas nas aberturas de micro-ondas. Juntas, parafusos, vedacao, pintura, agua superficial e salinidade precisam entrar no modelo. A caracterizacao deve cobrir polarizacoes TE/TM, angulos de 0 a pelo menos 60 graus, temperatura, chuva e envelhecimento.

Elementos HF que explorem a estrutura como radiador entram em conflito com uma casca transparente em Ka. A solucao e separar funcoes: uma estrutura HF deliberada e esparsa, eletricamente caracterizada, e tiles de frequencia alta em janelas livres de metal.

![Figura 3 - Modulo triangular de face e corte transversal conceitual. A cadeia RF fica atras da abertura e usa fibra para dados e sincronismo.](figures/fig03_modulo_face.png)

## 6. Particionamento espectral

O espectro deve ser dividido por tecnologia de antena e por arquitetura de conversao. Arranjos ultralargos publicados atingem razoes de alguns para um, nao quatro decadas [2,3]. Solucoes de abertura compartilhada sao eficazes quando as bandas possuem razoes moderadas e elementos intercalaveis, como S/C ou K/Ka [4-6].

A tabela seguinte e uma referencia inicial. Limites exatos devem ser escolhidos conforme os sinais prioritarios, a regulamentacao e a tecnologia de conversores.

| Subfaixa | Elemento recomendado | Diretividade no no | Conversao |
| --- | --- | --- | --- |
| HF 3-30 MHz | Loops e dipolos cruzados eletricamente pequenos; excitadores de modos caracteristicos | Baixa por elemento; AOA por diversidade de padroes e rede | Amostragem direta de baixa frequencia, alto alcance dinamico |
| VHF 30-300 MHz | Dipolos/loops cruzados, log-periodicas compactas, arrays esparsos | Moderada no extremo superior | Preselecao e ADC de dezenas/centenas de MS/s |
| UHF 0,3-1 GHz | Arrays dual-pol, espirais ou elementos vetoriais | Beamforming por setor | Amostragem direta ou IF baixa |
| L/S/C 1-8 GHz | Sinuous, espiral, Vivaldi ou TCDA | Varredura eletronica multi-octava | DDC apos ADC ou downconversion |
| X/Ku 8-18 GHz | Tiles de patches, slots ou dipolos acoplados | Alta, com varredura ampla | Super-heterodino coerente |
| K/Ka 18-40 GHz | Tiles Rx dedicados, dual-pol, baixo perfil | Alta; feixes multiplos possiveis | Conversao local para IF e ADC por sub-banda |

![Figura 4 - Particionamento por subfaixas. A escala logaritmica evidencia a impossibilidade de uma cadeia unica.](figures/fig04_particionamento_espectro.png)

## 7. Subsistema HF: correcao mais importante

Em 3 MHz o comprimento de onda e aproximadamente 100 m; em 30 MHz, 10 m. Uma face de 1 a 2 m e eletricamente pequena e nao fornece feixe estreito. Antenas pequenas podem ser adaptadas, mas sofrem limitacoes de eficiencia, largura de banda e estabilidade.

A literatura mostra uma abordagem mais adequada: usar excitadores pequenos para acoplar modos caracteristicos de uma plataforma maior, selecionando padroes com diversidade angular e de polarizacao [8-10]. Em um radome predominantemente dielétrico, esses modos nao surgem automaticamente; seria necessario um esqueleto condutor intencional, um plano de terra ou um conjunto de loops/dipolos distribuidos. Essa estrutura deve ser isolada eletromagneticamente dos tiles de frequencia alta.

Para recepcao somente, o baixo ganho de antena pode ser compensado por LNA de baixo ruido, desde que o front-end suporte sinais fortes fora de banda. O requisito principal e linearidade: filtros comutados, limitadores e alto ponto de interceptacao sao mais importantes que ganho excessivo. A estimacao de AOA em HF deve usar um manifold calibrado da estacao, algoritmos como MUSIC/ML e modelos de propagacao ionosferica; nao se deve interpretar todo atraso como caminho em espaco livre.

## 8. VHF/UHF e bandas de radiodifusao

VHF e UHF sao as faixas mais favoraveis para um primeiro demonstrador. O tamanho do radome permite diversidade espacial real, os sinais de FM e TV digital podem atuar como iluminadores, e os conversores sao acessiveis. Um conjunto de 8 a 24 elementos dual-pol distribuidos na casca pode formar feixes, nulos e estimativas de direcao.

FM oferece alta potencia e cobertura, mas largura de banda limitada e, portanto, resolucao de atraso relativamente pobre. Sinais digitais de radiodifusao oferecem maior largura de banda e melhor funcao de ambiguidade. Sistemas multi-iluminador FM/DAB/DVB-T ja foram construidos e avaliados [14].

O demonstrador deve reservar canais de referencia dedicados, apontados ou beamformados para cada transmissor de oportunidade, e canais de vigilancia cobrindo o volume de interesse. A referencia nao pode ser apenas uma copia atrasada ou saturada do canal de vigilancia.

## 9. L/S/C, X/Ku e K/Ka

Entre 1 e 8 GHz, elementos sinuous, espirais, Vivaldi e arrays fortemente acoplados podem oferecer largura multi-octava [2,3]. A escolha depende de perfil, polarizacao, impedancia ativa e scan blindness. Para cobertura conformal, o padrao ativo do elemento deve ser medido sobre a curvatura real.

Em X/Ku/Ka, a solucao robusta e usar tiles separados por banda ou aberturas compartilhadas com razao de frequencia moderada. Trabalhos em K/Ka demonstram varredura de aproximadamente mais ou menos 60 graus e elevado isolamento entre canais [4]. Arranjos triangulares intercalados sao compativeis com faces geodesicas e podem acomodar recepcao e transmissao ou duas bandas na mesma abertura [5].

Para recepcao satelital, os tiles devem ser dual-lineares ou dual-circulares, com sintese adaptativa. Satelites distintos usam polarizacoes e bandas diferentes; a estacao precisa de efemerides, frequencia Doppler prevista e apontamento. “Ouvir satelites” nao e uma unica funcao: telemetria, navegacao, radiometria e iluminacao passiva possuem orcamentos de enlace distintos.

## 10. Polarizacao: aquisicao vetorial e sintese digital

A polarizacao circular e importante para muitos enlaces satelitais, mas fixa-la fisicamente elimina flexibilidade. Cada elemento deve fornecer duas portas ortogonais com cadeias coerentes. Depois da calibracao, o processador forma RHCP e LHCP, polarizacao linear em qualquer angulo e parametros de Stokes.

Para bases locais x-y, a sintese ideal e: E_RHCP = (E_x - j E_y)/sqrt(2) e E_LHCP = (E_x + j E_y)/sqrt(2). Em uma superficie curva, cada face possui base tangencial propria; antes da combinacao global, os vetores precisam ser rotacionados para um sistema comum.

O erro de razao axial depende do desbalanceamento de amplitude, fase, acoplamento e atraso de grupo. Assim, a calibracao polarimetrica deve ser por frequencia e por angulo, nao apenas uma constante de 90 graus.

![Figura 5 - Duas portas ortogonais preservam qualquer polarizacao e permitem escolher a base no processamento.](figures/fig05_polarimetria.png)

## 11. Front-end RF, conversao e digitalizacao

Cada subfaixa possui seu proprio preseletor, limitador, LNA, conversor e ADC. Um LNA rotulado como 1-40 GHz nao substitui filtros e linearidade: sinais locais fortes podem comprimir o amplificador e mascarar ecos fracos. A protecao contra descargas, intermodulacao e aliasing deve ser projetada desde a entrada.

Amostragem direta e atraente em HF, VHF e parte de UHF. Em micro-ondas, a conversao para IF continua sendo pratica. Todos os canais que participam de beamforming ou interferometria devem compartilhar referencia de frequencia e possuir atraso de grupo calibrado.

Exemplo de vazao: quatro canais a 250 MS/s e 14 bits geram 14 Gbit/s antes de enquadramento. Um tile Ka com dezenas de elementos nao pode enviar amostras brutas continuamente por uma unica fibra comum. O FPGA local deve executar DDC, canalizacao polifasica, beamforming, deteccao, compressao sem perdas selecionada e buffer circular. Dados brutos devem ser preservados em janelas de evento para auditoria.

![Figura 6 - Cadeia RF por subfaixa com calibracao, clock comum e telemetria.](figures/fig06_cadeia_rf.png)

## 12. Sincronizacao, coerencia e holdover

White Rabbit, incorporado ao perfil de alta exatidao do IEEE 1588, e adequado para sincronizacao subnanosegundo em fibra e ja foi proposto para sistemas de aquisicao distribuidos como o SKA [11,12]. Isso suporta timestamps, alinhamento de blocos e comparacao temporal entre nos.

Entretanto, sincronismo de tempo nao e igual a coerencia de fase da portadora. O erro de fase devido a incerteza temporal e sigma_phi = 2 pi f sigma_t. A 30 GHz, 1 ps corresponde a aproximadamente 10,8 graus; 1 ns corresponde a milhares de graus. Portanto, beamforming coerente intersite em Ka nao pode depender apenas de um PPS subnanosegundo. Sao necessarios sintetizadores locais de baixo ruido, calibracao de fase, distribuicao optica de frequencia ou processamento que use observaveis de envelope/Doppler em vez de fase absoluta.

Experimentos recentes em interferometria indicam que o limite util depende do ruido de fase do equipamento White Rabbit e da calibracao de dispersao; equipamentos de baixo jitter ampliam a frequencia observavel, mas nao eliminam a necessidade de caracterizacao [13].

Em perda de fibra, um oscilador local entra em holdover. A qualidade deve ser expressa como desvio de tempo versus duracao e temperatura. Como c vezes 1 ns equivale a cerca de 0,30 m de caminho, 500 ns equivalem a 150 m; logo, nao e correto prometer precisao metrica por dias sem medir o oscilador e reestimar a covariancia.

![Figura 7 - White Rabbit e apenas um termo do orçamento de incerteza; atrasos analogicos e propagacao tambem devem ser calibrados.](figures/fig07_sincronizacao.png)

## 13. Calibracao ponta a ponta

O sistema deve possuir uma rede de calibracao que injete um tom ou ruído conhecido antes do LNA e, quando possivel, uma fonte radiada externa. A calibracao interna mede ganho e atraso da eletrônica; a externa inclui antena, radome, acoplamento e multipercurso do sitio.

Para cada canal, armazena-se a resposta complexa H_i(f,T,theta,phi), com dependencia de frequencia, temperatura e direcao. A matriz de acoplamento mutuo deve ser incorporada ao manifold do array. O beamformer e os algoritmos de AOA usam padroes embutidos medidos, nao padroes ideais isolados.

Os metadados de calibracao devem ser versionados e associados a cada janela de dados. Mudancas de painel, cabo, firmware, vedacao ou temperatura fora da faixa exigem nova campanha.

## 14. Geometria de sensoriamento e localizacao

Para um iluminador em T, alvo em x e receptor R_i, a medida de alcance bistatico e Delta rho_i = |x-T| + |x-R_i| - |T-R_i|. Cada medida ideal define uma elipsoide em 3D. Com varios pares iluminador-receptor, AOA e Doppler, estima-se o estado por minimos quadrados ponderados, maxima verossimilhanca ou filtro dinamico.

TDOA de emissores diretos define hiperboloides entre receptores. FDOA adiciona informacao de velocidade relativa. AOA fornece linhas ou cones de direcao. A fusao deve considerar a matriz de covariancia, a incerteza do iluminador, a sincronizacao, o modelo atmosferico e a geometria - frequentemente resumida pela diluicao geometrica de precisao.

Algoritmos de localizacao com multiplos iluminadores e restricoes podem reduzir erro em baixo SNR [15]. Experimentos recentes tambem demonstraram localizacao passiva multiestatica de objetos LEO com transmissores terrestres e um grande array receptor [16], mas esses resultados nao significam que qualquer tile pequeno tera a mesma sensibilidade.

![Figura 8 - Geometria bistatica: o atraso mede a diferenca entre caminho refletido e caminho direto de referencia.](figures/fig08_geometria_bistatica.png)

## 15. Processamento de radar passivo

O processamento inicia pela equalizacao temporal e de fase dos canais de referencia e vigilancia. Em seguida, o sinal direto e o clutter sao cancelados por filtros adaptativos ou metodos equivalentes. A funcao de ambiguidade cruzada produz um mapa atraso-Doppler, sobre o qual se aplica deteccao com controle de falso alarme.

As deteccoes de varios iluminadores e nos sao associadas por tempo, frequencia, Doppler e consistencia geometrica. A localizacao produz uma estimativa com covariancia, e um rastreador - por exemplo EKF, UKF ou fator-grafo - aplica o modelo dinamico.

O sistema deve manter a separacao entre deteccao de emissor e deteccao por reflexao. Jamming ou interferencia nao se transforma automaticamente em “iluminador melhor”: sinais sem forma de onda de referencia, saturacao ou baixa estabilidade podem apenas degradar a recepcao.

![Figura 9 - Fluxo de referencia/vigilancia ate a trilha 3D com covariancia.](figures/fig09_fluxo_processamento.png)

## 16. Rede de dados e arquitetura computacional

A rede optica deve separar tres planos: tempo/frequencia, dados cientificos e gerenciamento. O plano de tempo usa White Rabbit ou IEEE 1588 HA em topologia redundante. O plano de dados transporta amostras selecionadas, espectros, feixes e PDWs. O plano de gerenciamento coleta temperatura, estado de LNA, potencia, alarmes e versoes de calibracao.

A central nao deve receber apenas PDWs irreversiveis. Recomenda-se arquitetura de dados em tres niveis: (1) telemetria e deteccoes continuas; (2) janelas I/Q em eventos; (3) amostras brutas de campanha ou diagnostico. Buffers circulares locais permitem recuperar segundos anteriores a um gatilho.

Fibra submarina, micro-ondas e satelite podem transportar dados, mas nao sao equivalentes para sincronismo. Links assimetricos e variaveis devem ser tratados como transporte de pacotes ja carimbados. A disponibilidade de infraestrutura em cada local precisa ser levantada; nao deve ser presumida.

| Plano | Conteudo | Prioridade | Tolerancia a latencia |
| --- | --- | --- | --- |
| Tempo/frequencia | PPS, ToD, referencia de frequencia, telemetria de atraso | Critica | Baixa e deterministica |
| Dados cientificos | I/Q, espectros, feixes, PDWs, calibracao | Alta | Variavel se houver buffer e timestamp |
| Gerenciamento | temperatura, energia, alarmes, firmware | Media | Segundos |
| Contingencia | pacotes compactados por enlace alternativo | Alta para eventos | Pode ser alta; nao serve como fase de RF |

## 17. Desempenho e limites fisicos

O ganho de uma abertura de area A e aproximadamente G = eta 4 pi A/lambda^2. Para uma mesma face, o ganho cresce com o quadrado da frequencia. Isso explica por que uma face pode ser altamente direcional em Ka e quase omnidirecional em HF.

A resolucao de atraso e limitada pela largura de banda efetiva B; a escala caracteristica e c/B. Um sinal de 100 kHz possui escala quilometrica, enquanto 10 MHz permite dezenas de metros antes dos efeitos de SNR, multipercurso e geometria. A precisao de frequencia/Doppler depende do tempo de integracao coerente.

Para arrays, o ganho e a largura de feixe nao sao os unicos criterios. Devem ser medidos: VSWR ativo, eficiencia, ruido, acoplamento, razao axial, polarizacao cruzada, lobos de grade, scan blindness e deformacao causada pelo radome.

Nenhuma especificacao deve declarar “deteccao de qualquer objeto” sem orcamento de enlace. O alcance depende da potencia e forma de onda do iluminador, secao radar bistatica, distancias T-alvo e alvo-R, ganho, temperatura de sistema, perdas, integracao e probabilidade de deteccao/falso alarme.

## 18. Aspectos mecanicos, ambientais e EMC

O radome deve ser projetado para vento, vibracao, descargas atmosfericas, umidade, salinidade, UV, chuva e manutencao. A protecao contra raios nao pode criar uma gaiola metalica continua sobre as aberturas; condutores de descida e captores devem ser posicionados e simulados.

Cada tile de alta frequencia necessita placa fria ou dissipador interno. A conveccao natural em um domo fechado pode ser insuficiente; e recomendada climatizacao por setores com sensores de temperatura e condensacao. Gradientes termicos alteram fase e comprimento eletrico.

EMC interna e critica: conversores DC/DC, FPGA, enlaces digitais e clocks podem elevar o piso de ruido. O projeto deve usar blindagem compartimentada, filtros feedthrough, fibra dentro da zona sensivel e ensaios de emissao conduzida/radiada com receptores em operacao.

## 19. Implantacao em rede

A selecao de sitios deve resultar de simulacao de cobertura e nao apenas de altitude. Para cada faixa e iluminador, avaliam-se horizonte, relevo, densidade de emissores, RFI local, acesso, energia, clima e disponibilidade de fibra. Um pico alto pode ter excelente horizonte e pessimo ambiente eletromagnetico ou logistica inviavel.

A rede deve ser desenhada em clusters. Tres a cinco nos locais permitem demonstrar multilateracao; um no isolado fornece AOA e espectro, mas nao TDOA de rede. A expansao ocorre somente apos medir a contribuicao marginal de cada sitio pela matriz de informacao de Fisher ou metricas de geometria.

Para objetos espaciais, a linha de base longa pode ser vantajosa, mas a sensibilidade e o campo de visada comum dominam. Para alvos baixos, a curvatura terrestre e o bloqueio de relevo podem tornar baselines continentais irrelevantes. A topologia deve ser multiescala.

## 20. Plano de prototipagem e verificacao

O desenvolvimento recomendado comeca em VHF/UHF, onde antenas, ADCs e iluminadores de oportunidade permitem validar a cadeia completa. Somente depois se adicionam L/S/C e, em seguida, X/Ku/Ka. HF deve ser um programa paralelo de modos caracteristicos e sensores vetoriais, nao uma miniaturizacao da face de micro-ondas.

Cada fase termina em um gate com dados reproduziveis, modelo calibrado e comparacao com referencia independente.

| Fase | Entregas | Criterio de gate |
| --- | --- | --- |
| P0 - simulacao de sistema | modelo de cobertura, requisitos, orçamento de enlace e incerteza | cenarios e hipoteses rastreaveis; riscos dominantes identificados |
| P1 - tres nos VHF/UHF | arrays dual-pol, WR, canais referencia/vigilancia, TDOA/AOA | localizacao de emissor cooperativo e alvo de teste com covariancia consistente |
| P2 - tile L/S/C | tile conformal, calibracao polarimetrica, painel de radome | VSWR ativo, AR, ganho e scan medidos com e sem painel |
| P3 - X/Ku/Ka | tile de alta frequencia, LO baixo jitter, termica | feixe e polarizacao mantidos na faixa e angulos especificados |
| P4 - demonstrador integrado | radome, rede, processamento multi-iluminador | campanha externa, taxa de falso alarme e disponibilidade documentadas |

![Figura 10 - Roteiro conceitual de 24 meses; prazos dependem da infraestrutura e da disponibilidade de laboratorio.](figures/fig10_roteiro.png)

## 21. Ensaios de aceitacao recomendados

| Ensaio | Grandezas | Observacao |
| --- | --- | --- |
| S-parametros por tile | S11, acoplamento, estabilidade termica | medir elemento isolado e padrao ativo no array |
| Padrao 3D OTA | ganho, HPBW, SLL, polarizacao cruzada, AR | com radome e varios angulos de incidencia |
| Radome em espaco livre | perda de insercao, fase, erro de apontamento | TE/TM, seco/molhado, 0-60 graus |
| Coerencia de canais | ganho e fase relativos versus tempo e temperatura | inclui ADC, LO, FPGA e fibra |
| Sincronismo entre nos | offset, jitter, TDEV, holdover | relatorio de incerteza em vez de valor unico |
| AOA calibrado | erro angular e CRLB empirico | fontes conhecidas em varios azimutes/elevacoes |
| Radar passivo | cancelamento do direto, CAF, Pd/Pfa | alvo cooperativo e verdade-terreno |
| Resiliencia | perda de fibra/energia e recuperacao | sem salto de timestamps e com qualidade degradada sinalizada |

## 22. Matriz de riscos

| Risco | Impacto | Mitigacao |
| --- | --- | --- |
| Saturacao por emissores locais | perda de sensibilidade e produtos espurios | preseletores, limitadores, alto IP3, mapa RFI do sitio |
| Acoplamento entre bandas | deformacao de padrao e ruido | co-simulacao, cavidades, filtros e arranjo intercalado otimizado |
| Deriva termica | erro de fase/tempo | controle termico, sensores, calibracao continua |
| Modelo ideal de antena | AOA enviesado | padroes embutidos medidos e matriz de acoplamento |
| Vazao de dados excessiva | perda de eventos | DDC/beamforming local, buffers e politicas de retencao |
| Propagacao nao em espaco livre | erro de localizacao, especialmente HF | modelos de canal, dados meteorologicos/ionosfericos e covariancia adaptativa |
| Radome molhado ou envelhecido | perda e erro de apontamento | materiais qualificados, ensaios climaticos e recalibracao |
| Promessas de desempenho sem enlace | requisito impossivel de verificar | orcamentos por iluminador, alvo, faixa e geometria |

## 23. Conclusao

A proposta original contem um conceito valido: combinar receptores distribuidos, digitalizacao local, sincronizacao e processamento multiestatico. A correcao decisiva e abandonar a ideia de uma face universal e adotar uma abertura conformal composta por subsistemas de escalas diferentes.

Em HF, o radome deve funcionar como plataforma de diversidade modal ou hospedar sensores vetoriais; em VHF/UHF e micro-ondas, as faces podem conter arrays direcionais. A polarizacao deve ser adquirida por duas portas ortogonais e sintetizada digitalmente. White Rabbit fornece uma excelente espinha dorsal de tempo, mas nao substitui a calibracao de fase, atraso e propagacao.

O caminho de menor risco e um demonstrador de tres nos em VHF/UHF com canais de referencia e vigilancia, seguido por tiles L/S/C e K/Ka. O projeto so deve escalar territorialmente apos validar o orçamento de enlace, a geometria, a taxa de falso alarme e a estabilidade metrologica.

# Referencias

[1] **Documento-base fornecido pelo proponente** RadomeBrasil.pdf. Documento conceitual de arquitetura de radomes multifacetados, digitalizacao local, rede optica sincronizada e processamento passivo multiestatico, 2026.

[2] **LATHA, T.; RAM, G.; KUMAR, G.; CHAKRAVARTHY, M.** Review on Ultra-Wideband Phased Array Antennas. IEEE Access, v. 9, p. 129742-129755, 2021. [Link](https://consensus.app/papers/review-on-ultrawideband-phased-array-antennas-latha-ram/80537595407f5331975395f963bedff0/?utm_source=chatgpt)

[3] **MU, Y. et al.** Design of Ultrawideband Circularly Polarized Phased Array Antenna With Low VSWR and Low Axial Ratio. IEEE Antennas and Wireless Propagation Letters, v. 23, p. 1608-1612, 2024. [Link](https://consensus.app/papers/design-of-ultrawideband-circularly-polarized-phased-mu-zhao/f595f9bb5c415280a4d605fc39fa98a0/?utm_source=chatgpt)

[4] **HAO, R. S. et al.** K-/Ka-Band Shared-Aperture Phased Array With Wide Bandwidth and Wide Beam Coverage for LEO Satellite Communication. IEEE Transactions on Antennas and Propagation, v. 71, p. 672-680, 2023. [Link](https://consensus.app/papers/kkaband-sharedaperture-phased-array-with-wide-bandwidth-hao-zhang/64209be3e2545efa9385a0ea97a4786a/?utm_source=chatgpt)

[5] **FALKNER, B.; ZHOU, H.; MEHTA, A.** Shared Aperture Triangular Antenna Array for Ka-band LEO Satellite Communication. IEEE International Symposium on Antennas and Propagation and USNC-URSI, p. 1001-1002, 2023. [Link](https://consensus.app/papers/shared-aperture-triangular-antenna-array-for-kaband-leo-falkner-zhou/48bd28edb28d5b76bd139d0e795fb7cc/?utm_source=chatgpt)

[6] **XIAO, Y.; HE, L.; WEI, X.** Dual-Band Dual-Circularly Polarized Shared-Aperture Phased Array for S-/C-Band Satellite Communications. Electronics, 2025. [Link](https://consensus.app/papers/dualband-dualcircularly-polarized-sharedaperture-xiao-he/184fd8257aae541ba723ba4e9e5a77f4/?utm_source=chatgpt)

[7] **LUO, Y. et al.** Design of a wide beamwidth spherical conformal antenna array for ship-borne applications. Microwave and Optical Technology Letters, v. 65, p. 921-929, 2022. [Link](https://consensus.app/papers/design-of-a-wide-beamwidth-spherical-conformal-antenna-luo-zhao/1feaa0bda2cf52e0a408e12905853852/?utm_source=chatgpt)

[8] **MA, R.; BEHDAD, N.** Design of Platform-Based HF Direction-Finding Antennas Using the Characteristic Mode Theory. IEEE Transactions on Antennas and Propagation, v. 67, p. 1417-1427, 2019. [Link](https://consensus.app/papers/design-of-platformbased-hf-directionfinding-antennas-ma-behdad/206751f32e625ef88d6af478db454c71/?utm_source=chatgpt)

[9] **MA, R.; BEHDAD, N.** A Spatially Confined, Platform-Based HF Direction Finding Array. IEEE Transactions on Antennas and Propagation, v. 70, p. 1298-1308, 2022. [Link](https://consensus.app/papers/a-spatially-confined-platformbased-hf-direction-finding-ma-behdad/583eae4c607852b18e4e0dd5d8b3046c/?utm_source=chatgpt)

[10] **REN, K.; RANJBAR NIKKHAH, M.; BEHDAD, N.** Design of Dual-Polarized, Platform-Based HF Antennas Using the Characteristic Mode Theory. IEEE Transactions on Antennas and Propagation, v. 68, p. 5130-5141, 2020. [Link](https://consensus.app/papers/design-of-dualpolarized-platformbased-hf-antennas-using-ren-nikkhah/d5046a9ed01b54fe968e41e74fbce3ac/?utm_source=chatgpt)

[11] **JIMENEZ-LOPEZ, M. et al.** A Fully Programmable White-Rabbit Node for the SKA Telescope PPS Distribution System. IEEE Transactions on Instrumentation and Measurement, v. 68, p. 632-641, 2019. [Link](https://consensus.app/papers/a-fully-programmable-whiterabbit-node-for-the-ska-jiménez-lópez-torres-gonzález/e6c4848f58fe5bc5b57fe06061576d27/?utm_source=chatgpt)

[12] **GIRELA-LOPEZ, F. et al.** IEEE 1588 High Accuracy Default Profile: Applications and Challenges. IEEE Access, v. 8, p. 45211-45220, 2020. [Link](https://consensus.app/papers/ieee-1588-high-accuracy-default-profile-applications-and-girela-lópez-lópez-jiménez/d0d3da67454f58d897761029e19b02c3/?utm_source=chatgpt)

[13] **BOVEN, E. P. et al.** White Rabbit in radio interferometry. Experimental Astronomy, v. 61, 2026. [Link](https://consensus.app/papers/white-rabbit-in-radio-interferometry-boven-koelemeij/01fc2f652bdb51438cbf3259464a3e22/?utm_source=chatgpt)

[14] **EDRICH, M.; SCHROEDER, A.; MEYER, F.** Design and performance evaluation of a mature FM/DAB/DVB-T multi-illuminator passive radar system. IET Radar, Sonar & Navigation, v. 8, p. 114-122, 2014. [Link](https://consensus.app/papers/design-and-performance-evaluation-of-a-mature-fmdabdvbt-edrich-schroeder/d0987ab208bf51c18be5c937b6d9115c/?utm_source=chatgpt)

[15] **AUBRY, A.; CAROTENUTO, V.; DE MAIO, A.; PALLOTTA, L.** Localization in 2D PBR With Multiple Transmitters of Opportunity: A Constrained Least Squares Approach. IEEE Transactions on Signal Processing, v. 68, p. 634-646, 2020. [Link](https://consensus.app/papers/localization-in-2d-pbr-with-multiple-transmitters-of-aubry-carotenuto/07250e6397065979990b8882e394999a/?utm_source=chatgpt)

[16] **JEDRZEJEWSKI, K. et al.** Multistatic Localisation in Passive Radar System for LEO Space Objects Observation Using Terrestrial Illuminators and LOFAR Radio Telescope. IET Radar, Sonar & Navigation, 2025. [Link](https://consensus.app/papers/multistatic-localisation-in-passive-radar-system-for-leo-jędrzejewski-malanowski/898c4079a2a55858bdd3f457543c80d0/?utm_source=chatgpt)

[17] **ZHOU, L. et al.** Design and characterization for dual-band and multi-band A-sandwich composite radome walls. Composites Science and Technology, v. 149, p. 28-33, 2017. [Link](https://consensus.app/papers/design-and-characterization-for-dualband-and-multiband-zhou-wang/3dffdc18045d58418d09b2b92171b9f4/?utm_source=chatgpt)

[18] **AAMIR, M. et al.** Multi-disciplinary optimization of hybrid composite radomes for enhanced performance. Results in Engineering, 2023. [Link](https://consensus.app/papers/multidisciplinary-optimization-of-hybrid-composite-aamir-nasir/46631fb476eb5f23b4e9b2c43de56ccd/?utm_source=chatgpt)

# Apendice A - Formato minimo de registro de deteccao

| Campo | Descricao |
|---|---|
| `station_id` | Identificador do no e versao de calibracao |
| `tile_id/channel_id` | Tile, porta de polarizacao e cadeia RF |
| `timestamp_utc` | Tempo com incerteza estimada |
| `frequency_hz/bandwidth_hz` | Centro e largura de banda observada |
| `complex_amplitude` | I/Q ou amplitude/fase referenciada |
| `polarization` | Stokes ou Jones com covariancia |
| `aoa_az_el` | Direcao local e matriz de covariancia |
| `delay_doppler` | Medidas bistaticas e qualidade |
| `illuminator_id` | Identidade/hipotese do iluminador |
| `sync_state` | locked, holdover, degraded |
| `environment` | temperatura, umidade e estado do radome |

# Apendice B - Equacoes de referencia

- $\lambda=c/f$
- $ka=2\pi a/\lambda$
- $G\approx\eta 4\pi A/\lambda^2$
- $\sigma_\phi=2\pi f\sigma_t$
- $\Delta\rho_i=\|x-T\|+\|x-R_i\|-\|T-R_i\|=c\Delta\tau_i$
- $E_{RHCP}=(E_x-jE_y)/\sqrt{2}$ e $E_{LHCP}=(E_x+jE_y)/\sqrt{2}$