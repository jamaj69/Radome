# RADOME — Registro de decisões de arquitetura

## ADR-001 — Fonte técnica autoritativa

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** `projetov1.tex`, seus capítulos incluídos e a bibliografia associada formam o documento técnico autoritativo.
- **Consequência:** documentos anteriores permanecem como histórico e não prevalecem em caso de conflito.
- **Histórico principal:** `Radome2.pdf`, `RadomeBrasil.pdf`, `RADOME V3.md`, `RADOME V3 — Arquitetura Eletrônica Distribuída Revisada.md`, `Projeto_Radomes_Multifaixa_Revisado.md`, `projeto_tecnico_radome_consolidado.md` e seus PDFs derivados.

## ADR-002 — Versionamento independente

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** usar dois identificadores independentes: versão do documento e revisão da arquitetura.
- **Baseline atual:** documento 1.1; arquitetura 3, conceitual.
- **Consequência:** “RADOME V1” deixa de ser usado como identificador ambíguo do sistema completo. Uma nova compilação editorial pode alterar a versão documental sem alterar a arquitetura, e vice-versa.

## ADR-003 — Registro central de parâmetros

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** `PARAMETERS.md` controla valores quantitativos, estado da evidência, fonte, responsabilidade e gate de validação.
- **Consequência:** números copiados de documentos históricos não retornam ao documento vigente sem revisão explícita.

## ADR-004 — Conflitos não são requisitos

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** parâmetros incompatíveis permanecem visíveis com estado `Em conflito` até resolução pelo gate apropriado.
- **Consequência:** raio, lado de face, apoio civil, lacunas espectrais e polarimetria não podem orientar fabricação enquanto seus conflitos estiverem abertos.

## ADR-005 — Aprovação condicionada da baseline C0

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** aprovar a baseline documental para orientar as ondas de correção, preservando bloqueios explícitos sobre parâmetros `Em conflito`.
- **Escopo da aprovação:** hierarquia documental, versionamento, IDs, estados de evidência e responsabilidades.
- **Fora do escopo:** aprovação de fabricação, desempenho ou resolução técnica dos conflitos C1–C3.
- **Distinções obrigatórias:** o cenário aeronáutico ilustrativo usa dois nós, enquanto o demonstrador-alvo usa três; os 90° entre as Yagis VHF e UHF representam orientação mecânica entre faixas diferentes, não duas componentes polarimétricas coerentes do mesmo sinal.

## ADR-006 — Polarimetria restrita à mesma faixa

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** Jones, Stokes, RHCP e LHCP somente podem ser calculados a partir de duas portas simultâneas, ortogonais e coerentes na mesma frequência.
- **Aplicação ao demonstrador:** as Yagis VHF e UHF atuais são canais independentes de polarização única; sua montagem a 90° oferece diversidade mecânica/orientacional entre faixas, não polarimetria.
- **Expansão futura:** uma faixa poderá receber antena dual-polarizada ou par cruzado na mesma faixa, com cadeias coerentes e calibração de amplitude/fase.
- **Evidência exigida:** matriz de Jones, isolamento, cross-pol, equilíbrio de amplitude, fase relativa e deriva versus frequência, ângulo e temperatura.

## ADR-007 — LPDA VHF como candidata de banda larga

- **Data:** 8 de agosto de 2026
- **Estado:** proposta para simulação
- **Decisão:** adotar uma LPDA de 11 elementos, τ = 0,86, σ = 0,16 e elemento máximo de 2 m como baseline de simulação para aproximadamente 72–320 MHz.
- **Motivo:** uma Yagi convencional com elemento máximo de 2 m seria predominantemente estreita e centrada na parte baixa de VHF.
- **Limite:** a LPDA não substitui a Yagi no modelo físico atual até que ganho realizado, impedância, padrão, cargas e integração sejam validados.
- **Fonte dimensional:** `antenna_designs/lpda_vhf_72_320.md`.

## ADR-008 — Mastro polarimétrico de quatro canais

- **Data:** 8 de agosto de 2026
- **Estado:** proposta para simulação
- **Decisão:** avaliar dois canais VHF ortogonais a 0°/90° e dois canais UHF ortogonais a 45°/135° em um mastro estrutural comum, mantendo quatro booms e cadeias RF eletricamente independentes.
- **Calibração:** estimar o campo por faixa com a inversão regularizada de uma matriz complexa 2×2 dependente de frequência, direção e temperatura.
- **Limite:** a rotação UHF de 45° não garante isolamento; quatro portas, acoplamento e padrões embarcados devem ser resolvidos como uma única estrutura eletromagnética.
- **Fonte:** `antenna_designs/dual_band_quad_polarization_mast.md`.

## ADR-009 — Malha geodésica C2 preliminar

- **Data:** 8 de agosto de 2026
- **Estado:** proposta para verificação geométrica
- **Decisão:** substituir a subdivisão provisória de 60 faces por uma malha classe I de frequência 2 derivada de um icosaedro regular.
- **Resultado topológico:** o envelope fechado passa a ter 42 vértices, 120 arestas e 80 faces triangulares, com consistência de Euler igual a 2.
- **Corte inferior:** o corte deixa de ser controlado por “latitude” textual e passa a ser registrado como $z/R=-0{,}573576$ ou ângulo polar de 125°; o segmento cortado possui 51 vértices, 124 arestas, 74 faces e Euler igual a 1.
- **Limite:** a projeção esférica gera duas classes de corda; portanto, o lado nominal de 2 m não pode ser aplicado simultaneamente a todas as faces sem declarar a regra de escala.
- **Fonte:** `geometry/verify_radome_geometry.py`.

## ADR-010 — Lacunas deliberadas e cadeia aeronáutica dedicada

- **Data:** 8 de agosto de 2026
- **Estado:** aceita no nível arquitetural
- **Decisão:** o primeiro demonstrador não buscará cobertura espectral contínua. As faixas de 323–470 MHz e 860–960 MHz ficam deliberadamente sem cadeia receptora; a margem simulada da LPDA até aproximadamente 323 MHz não cria requisito além da faixa VHF selecionada.
- **Cadeia aeronáutica:** uma abertura ou array dedicado de 960–1215 MHz alimentará dois caminhos simultâneos e independentes: preselector de serviço em 978 MHz, limitador/LNA, ADC coerente e canal FPGA UAT; e preselector de serviço em 1090 MHz, limitador/LNA, ADC coerente e canal FPGA 1090ES.
- **Separação:** a Yagi UHF de 470–860 MHz não fundamenta recepção em 978 ou 1090 MHz. A cadeia aeronáutica também não implica cobertura contínua de toda a faixa de 960–1215 MHz.
- **Limite:** topologia da abertura, larguras de filtro, NF, IP3, faixa dinâmica, taxa de amostragem e volume de dados permanecem propostos até o dimensionamento quantitativo do C3.

## ADR-011 — Protocolos experimentais independentes

- **Data:** 8 de agosto de 2026
- **Estado:** aceita no nível arquitetural
- **Decisão:** tratar como protocolos distintos o emissor direto cooperativo ADS-B, o transmissor direto conhecido usado para calibração e a reflexão biestática de alvo.
- **Regra de evidência:** cada protocolo possui observáveis, verdade-terreno, estimador e métricas próprios. Resultados de um protocolo não validam automaticamente os demais.
- **Reflexão biestática:** exige canais simultâneos de referência e vigilância, cancelamento do caminho direto e avaliação em atraso–Doppler; a mensagem ADS-B não substitui o canal de referência do iluminador.
- **Rastreabilidade:** os protocolos são controlados por `EXP-006`, `EXP-007` e `EXP-008` em `PARAMETERS.md`.

## ADR-012 — Células tetraédricas com face externa de 2 m

- **Data:** 8 de agosto de 2026
- **Estado:** proposta geométrica; reabre C2
- **Decisão:** substituir a projeção esférica da subdivisão de frequência 2 por quatro subfaces coplanares em cada macroface icosaédrica. As 80 faces externas tornam-se triângulos equiláteros de 2 m e cada uma forma uma célula tetraédrica rasa com altura normal de 0,75 m entre o centro da face e seu ápice interno local.
- **Encaixe:** cada célula possui três paredes laterais condutivas próprias. Nas 120 arestas externas compartilhadas, as paredes vizinhas partem da mesma junta e divergem para ápices distintos, formando corredores intercelulares para alimentação, fibras ópticas, ligação equipotencial e manutenção.
- **Blindagem local:** a abertura externa permanece eletromagneticamente funcional. As outras três paredes da célula formam a gaiola de Faraday, e cada canal ortogonal possui invólucro ADC/ASIC próprio, passagens filtradas e caminho térmico condutivo.
- **Resultado geométrico:** o envelope fechado mantém 80 faces e 120 arestas, com macroaresta de 4 m, raio circunscrito de 3,8042 m e inraio de 3,0230 m. As 240 arestas laterais medem 1,3769 m, os ápices vizinhos ficam separados por 0,5435–1,1547 m e permanece um núcleo interno livre com raio mínimo de 2,2730 m.
- **Incompatibilidade registrada:** tetraedros regulares com as seis arestas de 2 m produzem 120 interpenetrações. A dimensão de 2 m controla somente as três arestas da face externa; exigir seis arestas iguais é bloqueado.
- **Limite:** o corte inferior circular e o anel de apoio da ADR-009 deixam de controlar esta candidata. C2 permanece reaberto até definir uma borda formada por módulos inteiros, dimensionar juntas, corredores, caminhos térmicos e blindagem real e recalcular a interface civil.
- **Evidência:** `geometry/verify_tetrahedral_face_geometry.py`, `figures/render_tetrahedral_face_cluster_blender.py`, `fig16_tetrahedral_face_cluster.png` e `radome_tetrahedral_face_cluster.blend`.

## ADR-013 — Eixo normal das Yagis e figuras independentes de idioma

- **Data:** 8 de agosto de 2026
- **Estado:** aceita como premissa arquitetural e editorial
- **Orientação mecânica:** o eixo estrutural e os booms da montagem combinada VHF/UHF são colineares com o vetor normal externo ao plano da face triangular. O suporte parte do ápice interno, atravessa o centro da abertura e prossegue para fora ao longo dessa normal.
- **Orientação transversal:** os elementos VHF e UHF permanecem mutuamente ortogonais e a montagem cruzada completa é girada em 45° ao redor da normal em relação à base tangente local da face. Assim, as direções transversais nominais são 45° e 135° na base local, sem transformar os canais de faixas diferentes em um par polarimétrico coerente.
- **Regra editorial substituída em 8 de agosto de 2026:** as edições `pt-BR` e `en` usam conjuntos localizados distintos em `figures/pt-BR/` e `figures/en/`. Ambos derivam dos mesmos mestres geométricos, mas títulos, rótulos e chaves visuais aparecem no idioma da edição. Esta regra substitui a tentativa anterior de publicar imagens sem texto, cuja leitura se mostrou insuficiente.
- **Evidência:** `figures/localize_figures.py`, `figures/render_radome_blender.py`, `figures/render_tetrahedral_face_cluster_blender.py`, `figures/generate_updated_figures.py`, `figures/en/` e `figures/pt-BR/`.

## ADR-014 — Célula receptora absorvedora como hipótese de baixa observabilidade

- **Data:** 9 de agosto de 2026
- **Estado:** inovação arquitetural proposta; desempenho não demonstrado
- **Hipótese:** combinar Yagis VHF/UHF expostas, que não sofrem a perda de transmissão do casco, com uma célula piramidal interna individualmente blindada e revestida por material absorvedor. A abertura conduz a energia útil ao receptor, enquanto a terminação absorvedora proposta busca reduzir reflexões internas, acoplamento entre células e reradiação pela abertura.
- **Ressalva física:** paredes Faraday condutivas, isoladamente, refletem energia e não tornam a estação invisível. Baixa observabilidade somente pode ser alegada se a geometria, o revestimento dissipativo, as juntas, os feedthroughs, o boom e a antena externa reduzirem a seção reta radar e a reflexão da abertura nas frequências, polarizações e ângulos de interesse.
- **Evidência exigida:** modelo EM do conjunto aberto e revestido; balanço de potência incidente–refletida–absorvida–recebida; $S_{11}$ da abertura; eficácia de blindagem; acoplamento entre células; RCS monoestática e biestática angular com e sem absorvedor; ganho, ruído e padrão embarcado; ensaios OTA em câmara e campanha externa.
- **Limite operacional:** o conceito pode aumentar discrição eletromagnética por não transmitir e pode reduzir a assinatura passiva da estrutura, mas não fundamenta a palavra ``invisível'' nem capacidade de defesa aérea antes dos ensaios.
- **Anterioridade incorporada:** Oh et al. (2026) já demonstram integração em pacote de antena UHF, parede metálica de isolamento e radome GFRP de baixa perda. Portanto, parede isolante mais radome não é reivindicada como novidade; a hipótese candidata fica limitada à combinação específica de Yagis VHF/UHF externas ortogonais, boom normal à face, célula piramidal interna blindada/absorvedora e operação distribuída exclusivamente receptora.

## ADR-015 — Custo--desempenho e geometria probabilística multiestática

- **Data:** 9 de agosto de 2026
- **Estado:** hipótese arquitetural; custo e precisão não demonstrados
- **Decisão econômica:** tratar antenas externas, casco potencialmente menos exigente em transparência multifaixa, ausência de transmissor próprio e manutenção modular como fontes candidatas de redução de custo. Comparar por custo de ciclo de vida e desempenho normalizado, incluindo as penalidades de exposição ambiental e multiplicação de canais.
- **Decisão geométrica:** atraso excedente eco--referência define elipsoide biestático; AOA, potência calibrada, Doppler/FDOA e polarização coerente na mesma faixa fornecem restrições adicionais. A recepção associada do mesmo eco por múltiplas antenas/faces e por radomes sincronizados acrescenta informação ao estimador; em mínimos quadrados ponderados, a covariância não aumenta e diminui estritamente nas direções observáveis em que a nova medição não é redundante. Essa propriedade é tratada como consequência matemática da fusão e da propagação multivariada de incertezas conforme JCGM 102:2011, não com o verbo modal ``pode''.
- **Decisão temporal:** as faces de cada radome compartilham uma base temporal central, e os nós são referenciados à época comum da rede. GNSS, referência de frequência, White Rabbit, holdover local e calibração de atraso operam simultaneamente e são verificados continuamente para sustentar timestamping e associação do eco entre canais e nós.
- **Proibição:** não afirmar baixo custo, valor numérico de incerteza ou localização exata antes de orçamento rastreável e campanha com verdade-terreno. A redução de incerteza por informação válida adicional deve ser preservada como propriedade do modelo; o ensaio quantifica sua magnitude.
