# RADOME — Roadmap de correções técnicas e documentais

**Data-base:** 8 de agosto de 2026
**Escopo:** inconsistências encontradas entre documentos, figuras, scripts, modelo Blender e revisão bibliográfica
**Regra:** nenhuma solução arquitetural deve ser apresentada como desempenho demonstrado antes do gate experimental correspondente.

## Estado dos gates

| Gate | Estado inicial | Resultado esperado |
|---|---|---|
| C0 — baseline documental | Aprovado com bloqueios | Fonte, versionamento, parâmetros e ADRs aprovados; conflitos seguem bloqueados para C1–C3 |
| C1 — polarimetria correta | Aprovado no nível arquitetural | Síntese restrita a duas portas coerentes na mesma faixa; Yagis VHF/UHF declaradas single-pol independentes |
| C2 — geometria consistente | Reaberto pela ADR-012 | Faces externas de 2 m e células rasas verificadas; faltam corte modular, juntas/corredores, tolerâncias e nova interface civil |
| C3 — cobertura espectral | Em andamento; arquitetura e triagem aprovadas | Lacunas deliberadas, cadeia aeronáutica e protocolos definidos; faltam orçamento RF, enlace e sítio |
| C4 — modelo 3D sincronizado | Bloqueado pelo fechamento de C2 e C3 | Blender e figuras gerados a partir dos parâmetros aprovados |
| C5 — consistência científica | Em aberto | Novidade, referências e limites formulados com evidência apropriada |
| C6 — qualidade editorial | Em andamento; edições separadas implantadas | Conteúdo equivalente entre as edições independentes e compilação sem avisos relevantes |

## Onda 0 — congelar a baseline

**Prioridade:** imediata.
**Dependências:** nenhuma.

1. [x] Declarar `projeto/projetov1.tex` como documento técnico autoritativo e classificar os PDFs/Markdown anteriores como histórico.
2. [x] Resolver a nomenclatura “RADOME V1” versus “geometria V3”: adotar versão do documento e revisão da arquitetura como campos distintos.
3. [x] Criar uma tabela central de parâmetros com valor, unidade, estado (`proposto`, `derivado`, `simulado`, `medido`, `histórico` ou `em conflito`), fonte, responsabilidade e validação.
4. [x] Registrar decisões em um log curto de arquitetura, evitando que números retornem por cópia de documentos históricos.
5. [x] Realizar a revisão formal da baseline e aprovar as entradas iniciais com bloqueios explícitos em `projeto/PARAMETERS.md`.

**Gate C0:** todos os valores quantitativos do artigo apontam para a tabela central ou são marcados explicitamente como exemplo conceitual.

## Onda 1 — corrigir a polarimetria

**Prioridade:** crítica.
**Dependências:** C0.

1. [x] Remover a síntese RHCP/LHCP e Stokes feita pela combinação da Yagi VHF com a Yagi UHF: elas observam faixas diferentes.
2. [x] Decidir, por faixa, entre:
   - antena dual-polarizada com duas portas coerentes na mesma frequência;
   - par de antenas ortogonais da mesma faixa;
   - recepção de polarização única, explicitamente limitada.
3. [x] Manter as Yagis VHF/UHF cruzadas apenas como integração mecânica, diversidade espectral e diversidade de orientação avaliada separadamente.
4. [x] Atualizar `04_multiband_polarimetry.tex`, `09_literature_review.tex`, `10_conclusion.tex`, `fig05_polarimetria.png` e seu gerador.
5. [x] Definir como evidência obrigatória amplitude, fase, isolamento, cross-pol, matriz de Jones e deriva por frequência, ângulo e temperatura.

**Gate C1:** toda equação polarimétrica recebe entradas simultâneas, coerentes e na mesma frequência; figura, texto e hardware proposto concordam.

## Onda 2 — reconstruir a geometria paramétrica

**Prioridade:** crítica.
**Dependências:** C0; pode ocorrer em paralelo com a Onda 1.

1. [x] Definir formalmente o poliedro base e o método de subdivisão/projeção.
2. [x] Separar aresta da macroface, dimensões das subfaces, raio circunscrito, diâmetro e altura do segmento cortado.
3. [x] Recalcular `V`, `E` e `F` para o envelope fechado e para a estrutura efetivamente cortada.
4. [x] Definir o corte em coordenada geométrica (`ângulo polar` ou `z/R`), evitando a ambiguidade de “latitude 35° S”.
5. [x] Dimensionar o anel de apoio e compatibilizá-lo com a base de concreto; ampliar a base ou especificar uma transição estrutural.
6. [x] Produzir verificação automática de Euler, comprimentos, raio do apoio e envelope da base.

**Gate C2:** um arquivo de parâmetros reproduz todas as dimensões publicadas e passa verificações geométricas e de apoio sem valores manuais conflitantes.

### Revisão tetraédrica ADR-012

A exigência posterior de faces externas equiláteras de 2 m tornou incompatível a projeção esférica que produzia duas classes de corda. O novo verificador preserva 80 faces por subdivisão planar das macrofaces e testa dois casos: tetraedros regulares com seis arestas de 2 m, que geram 120 interpenetrações, e células tetraédricas rasas com altura de 0,75 m, que não colidem. A candidata rasa possui 240 paredes Faraday independentes, 120 corredores intercelulares e núcleo interno livre com raio mínimo de 2,2730 m. O render `fig16_tetrahedral_face_cluster.png` mostra sete faces contíguas, bases tangentes locais, antenas ortogonais, caixas ADC/ASIC blindadas, núcleo reservado e rotas de energia/fibra.

O C2 é reaberto porque o corte circular, o anel de apoio e a transição civil anteriores pertencem à candidata projetada. O novo gate exige selecionar módulos inteiros para a borda inferior, dimensionar juntas e corredores com espessuras e folgas reais, comprovar continuidade Faraday e recalcular a fundação.

## Onda 3 — fechar o plano espectral e os experimentos

**Prioridade:** alta.
**Dependências:** C0 e decisão preliminar de C1.

1. [x] Resolver as lacunas espectrais: 323–470 MHz e 860–960 MHz permanecem deliberadamente sem cobertura no primeiro demonstrador.
2. [x] Atribuir ADS-B 1090ES e UAT 978 MHz a uma abertura aeronáutica dedicada de 960–1215 MHz, com preselectors, ADCs e canais FPGA independentes; a Yagi de 470–860 MHz não cobre esses serviços.
3. [x] Separar três experimentos, com observáveis, verdade-terreno, estimador e métricas próprios:
   - emissor direto cooperativo ADS-B;
   - transmissores conhecidos para calibração;
   - reflexão biestática de alvo com canal de referência e vigilância.
4. [ ] Fechar os parâmetros de aquisição e RF:
   - [x] baselines de triagem de 8 MS/s para os dois canais aeronáuticos e 25 MS/s para os canais UHF;
   - [x] I/Q de 16+16 bits, janelas brutas de 10 s e vazões/volumes reproduzidos por `projeto/spectral/verify_c3_acquisition_budget.py`;
   - [ ] largura ocupada por forma de onda, clock/ENOB de implementação, faixa dinâmica, NF e IP3 após campanha RFI e orçamento em cascata.
5. [ ] Reavaliar a baseline nominal de 100 km:
   - [x] triagem de horizonte com Terra efetiva: aproximadamente 542 km para estação a 1000 m e aeronave a 10000 m;
   - [ ] fechar terreno, diagramas, margem de enlace, visibilidade comum, GDOP, coordenadas e regulamentação dos sítios reais.

### Evidência C3 já produzida

- `ADR-010`: lacunas deliberadas e cadeia aeronáutica dedicada;
- `ADR-011`: protocolos experimentais independentes;
- `RF-007`–`RF-015` e `EXP-006`–`EXP-010` em `projeto/PARAMETERS.md`;
- Figura 4 regenerada com a faixa aeronáutica e as lacunas explícitas;
- `projeto/spectral/verify_c3_acquisition_budget.py`: 512, 800 e 1600 Mbit/s por nó; 0,64, 1,00 e 2,00 GB por nó em janelas de 10 s;
- artigo bilíngue recompilado, sem erros fatais ou referências indefinidas na passagem final.

**Gate C3:** cada frequência citada possui caminho de sinal completo e cada experimento possui observáveis, verdade-terreno, estimador e métrica separados.

**Bloqueios restantes do gate:** selecionar formas de onda e componentes, medir o ambiente RFI, fechar NF/IP3/faixa dinâmica e concluir os orçamentos de enlace, geometria e autorização dos sítios. Os valores atuais são baselines de capacidade e triagem, não desempenho aprovado.

## Onda 4 — sincronizar Blender, figuras e texto

**Prioridade:** alta.
**Dependências:** C1, C2 e C3.

1. Fazer o Blender consumir a geometria aprovada, incluindo raio, corte, malha, anel e base.
2. Corrigir o nome interno `4x4x2 m` ou as dimensões, mantendo uma única especificação.
3. Substituir a malha ilustrativa de anéis pela malha geodésica real, ou rotular inequivocamente o render como esquemático.
4. Gerar faces, suportes e antenas sem coordenadas independentes desenhadas manualmente.
5. Preservar a baseline `baseline_35S_concrete_base/` e criar uma nova baseline nomeada após aprovação.
6. Remover a repetição de `fig13_radome_blender.png` no artigo.

**Gate C4:** relatório automático compara parâmetros do artigo, script e `.blend`; renders e legendas descrevem a mesma configuração.

## Onda 5 — fortalecer literatura e alegações

**Prioridade:** média-alta.
**Dependências:** C1 e C3.

1. Trocar “inovação central” por “solução arquitetural proposta” até concluir busca de anterioridade específica para a montagem.
2. Auditar os 29 registros do Consensus em fontes primárias, acrescentando DOI, volume, páginas e estado editorial.
3. Verificar especialmente registros de 2025–2026 e os que possuem venue ou resumo incompletos.
4. Separar claramente revisão narrativa via Consensus de uma eventual revisão sistemática.
5. Criar matriz alegação–referência–evidência e marcar como hipótese tudo que ainda depende de simulação ou ensaio.

**Gate C5:** nenhuma alegação de novidade ou desempenho depende apenas do resultado do Consensus ou de um diagrama conceitual.

## Onda 6 — corrigir estrutura bilíngue e publicação

**Prioridade:** média.
**Dependências:** C1–C5 para evitar retrabalho.

1. [x] Separar o parágrafo inglês anteriormente inserido no conteúdo português do capítulo 3.
2. [x] Separar a subseção de torres celulares do capítulo 7 entre as edições inglesa e brasileira.
3. Comparar automaticamente presença de equações, figuras, ressalvas e números entre os dois idiomas.
4. Corrigir âncoras PDF duplicadas da página 1, a caixa `Overfull` do apêndice e quebras problemáticas da bibliografia.
5. Executar a sequência completa LaTeX e inspecionar o PDF final.

As edições independentes foram implantadas em `projeto/radome-en.tex` e `projeto/radome-pt-br.tex`. A edição brasileira usa `abntex2`, `babel` e `abntex2cite`; a inglesa usa `report`, `babel` e `natbib`. Os capítulos ficam em árvores próprias e os manifestos em `projeto/config/` permitem acrescentar e reordenar capítulos e seções sem alterar os arquivos mestres.

**Gate C6:** compilação final das duas edições sem erros, referências indefinidas, âncoras duplicadas ou divergências técnicas entre idiomas.

## Ordem operacional

```mermaid
flowchart LR
    C0[Onda 0: baseline] --> C1[Onda 1: polarimetria]
    C0 --> C2[Onda 2: geometria]
    C0 --> C3[Onda 3: espectro]
    C1 --> C4[Onda 4: 3D e figuras]
    C2 --> C4
    C3 --> C4
    C1 --> C5[Onda 5: literatura]
    C3 --> C5
    C4 --> C6[Onda 6: publicação]
    C5 --> C6
```

## Definição de concluído

As correções estarão concluídas quando os seis gates forem aprovados, o artigo bilíngue recompilar conforme `AGENTS.md`, as figuras forem regeneradas a partir da baseline correta e cada afirmação quantitativa estiver classificada como proposta, simulada ou medida.
