# Dual-band four-channel mast / Mastro de quatro canais em duas faixas

**Status:** proposed architecture for electromagnetic simulation; not approved for fabrication

## English

The proposed assembly uses one structural mast with four electrically independent apertures:

- VHF-X at 0° and VHF-Y at 90°;
- UHF-A at 45° and UHF-B at 135°;
- independent feed, filter, LNA, ADC and calibration path for every channel;
- a coherent clock and sampling reference shared by the two channels within each band.

Both antennas in a same-band pair must observe the same signal bandwidth simultaneously. A single UHF antenna at 45° is insufficient for full UHF polarization recovery. The 45° rotation changes the measurement basis and may help mechanical organization, but does not itself guarantee isolation.

The preferred mechanical interpretation is a common structural mast with four electrically isolated booms or balanced feed structures. VHF and UHF elements may be axially staggered, but must not share conductive paths unless the complete coupled structure is intentionally optimized. The largest UHF elements and smallest VHF-LPDA elements are close enough in electrical scale that mutual coupling must be included explicitly.

### Calibration model

For each band `b ∈ {VHF,UHF}`, the measured complex port vector is

\[
\mathbf{v}_b(f,\theta,\phi,T)
=\mathbf{C}_b(f,\theta,\phi,T)\,\mathbf{E}_b(f,\theta,\phi)+\mathbf{n}_b,
\]

and the calibrated field estimate is

\[
\widehat{\mathbf{E}}_b
=\mathbf{C}_b^{-1}(f,\theta,\phi,T)
\left[\mathbf{v}_b-\widehat{\mathbf{n}}_b\right].
\]

`C_b` is a measured 2×2 complex Jones calibration matrix containing the embedded element patterns, gain and phase imbalance, cable/front-end delay, mutual coupling, mast and platform effects. Where the matrix is poorly conditioned, a regularized pseudoinverse must replace the direct inverse and the observation must carry increased uncertainty.

For the UHF basis rotated by `ψ = 45°`, conversion to the common global basis is

\[
\begin{bmatrix}E_x\\E_y\end{bmatrix}
=
\begin{bmatrix}\cos\psi&-\sin\psi\\\sin\psi&\cos\psi\end{bmatrix}
\begin{bmatrix}E_{45}\\E_{135}\end{bmatrix}.
\]

Only after this band-specific calibration and coordinate rotation may Jones, Stokes, RHCP or LHCP quantities be formed.

### Simulation outputs required

- four-port S-parameter matrix versus frequency;
- active and realized gain of each port;
- embedded 3D element patterns with other ports terminated;
- port isolation and envelope correlation;
- axial ratio only after valid coherent same-band excitation;
- front-to-back ratio, beamwidth and cross-polarization;
- condition number of `C_b` across frequency and angle;
- sensitivity to element displacement, mast conductivity, balun, cable routing and temperature.

### Recommended simulation stack

1. **openEMS** is the preferred reproducible first implementation. Its FDTD engine supports lumped ports and near-field-to-far-field transformation, allowing a broadband four-port sweep with geometry and post-processing scripted in Python. Official documentation: <https://docs.openems.de/python/openEMS/openEMS.html>.
2. **Altair Feko** is the preferred commercial cross-check for wire antennas installed on a larger platform. Its official solver documentation includes MoM, FEM and MLFMM and specifically addresses antenna placement and coupling: <https://help.altair.com/feko/pdf/Altair_Feko_User_Guide.pdf>.
3. **Ansys HFSS** can provide a finite-element/integral-equation cross-check of S-parameters, fields and far-field polarization: <https://www.ansys.com/training-center/course-catalog/electronics/ansys-hfss-for-antenna-design>.
4. **CST Studio Suite** is another suitable commercial option; its time-domain FIT/TLM solvers are intended for broadband antenna problems and its frequency-domain solver supports multi-port systems: <https://www.3ds.com/products/simulia/cst-studio-suite/electromagnetic-simulation-solvers>.

The recommended project workflow is openEMS for automated design iterations, followed by one independent Feko, HFSS or CST model before fabrication. NEC may be used for rapid thin-wire screening, but the final four-port model must include finite booms, feeds, mast and nearby structure.

## Português

O conjunto proposto utiliza um mastro estrutural com quatro aberturas eletricamente independentes:

- VHF-X a 0° e VHF-Y a 90°;
- UHF-A a 45° e UHF-B a 135°;
- alimentação, filtro, LNA, ADC e caminho de calibração independentes para cada canal;
- clock e referência de amostragem coerentes entre os dois canais de cada faixa.

As duas antenas do mesmo par devem observar simultaneamente a mesma largura de banda. Uma única antena UHF a 45° não recupera toda a polarização UHF. A rotação de 45° altera a base de medição e pode facilitar a organização mecânica, mas não garante isolamento.

A interpretação mecânica preferencial é um mastro estrutural comum com quatro booms ou estruturas balanceadas eletricamente isoladas. Elementos VHF e UHF podem ser deslocados axialmente, mas não devem compartilhar caminhos condutivos, salvo se toda a estrutura acoplada for deliberadamente otimizada. Os maiores elementos UHF e os menores elementos da LPDA VHF possuem escalas elétricas próximas, exigindo modelagem explícita do acoplamento mútuo.

O modelo de calibração é o mesmo apresentado na seção em inglês. A matriz complexa 2×2 `C_b` inclui diagramas embarcados, desequilíbrio de ganho e fase, atrasos, acoplamento, mastro e plataforma. Quando estiver mal condicionada, deve-se usar pseudoinversa regularizada e aumentar a incerteza da observação.

Para UHF, as componentes medidas a 45°/135° são rotacionadas para a base global antes da formação de Jones, Stokes, RHCP ou LHCP.

### Resultados obrigatórios da simulação

- matriz S de quatro portas versus frequência;
- ganho ativo e realizado de cada porta;
- diagramas 3D embarcados, terminando as demais portas;
- isolamento e correlação entre portas;
- razão axial somente com excitação coerente válida na mesma faixa;
- relação frente-costas, largura de feixe e polarização cruzada;
- número de condição de `C_b` versus frequência e ângulo;
- sensibilidade a deslocamentos, condutividade do mastro, balun, cabos e temperatura.

### Ferramentas recomendadas

O fluxo recomendado é usar openEMS para iterações automatizadas e reproduzíveis, seguido por uma verificação independente em Feko, HFSS ou CST antes da fabricação. O Feko é especialmente apropriado para antenas de fio instaladas em plataformas; HFSS e CST são alternativas de alta fidelidade para a estrutura multiporta completa. NEC pode acelerar a triagem inicial de fios finos, mas não deve ser a única evidência para booms, alimentações, mastro e estrutura próxima.
