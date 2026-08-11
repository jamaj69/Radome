# Terreno, curvatura e Fresnel dos candidatos

Esta triagem usa Mapzen Terrarium z8, amostragem de 1 km, altura máxima
cadastral por ponta e a menor frequência recíproca. É deliberadamente otimista
quanto à altura e preliminar quanto ao MDE; nenhuma aresta foi criada.

| Estado | k=1 | k=4/3 |
|---|---:|---:|
| 60% de Fresnel livre | 218 | 228 |
| visada livre, Fresnel obstruído | 69 | 66 |
| terreno/curvatura obstruído | 40 | 33 |
| terreno ausente | 1 | 1 |

Os 328 candidatos precisam ser recalculados com TOPODATA ou MDE oficial de
resolução adequada, amostragem mais fina e alturas físicas verificadas. O
resultado atual é triagem de sensibilidade e mantém `pairing_status` como
`not_performed`.
