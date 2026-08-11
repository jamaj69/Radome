# Grafo continental aumentado de candidatos

O produto incorpora os 1.484 candidatos TOPODATA das lacunas aos 131 candidatos
de capitais e aeroportos, totalizando 1.615 vértices candidatos no grafo
geoespacial de 125.330 nós.

Com altura arquitetural provisória de 15 m, alvo a 3.000 m e raio terrestre
efetivo `k=4/3`, foram encontrados 45.137 pares dentro do limite geométrico de
curvatura. Eles geram 90.274 arcos dirigidos, todos explicitamente não
operacionais e pendentes de terreno intermediário, visada e Fresnel. O grafo
continua com zero arestas operacionais. Duas execuções produziram GraphML e CSV
gzip byte a byte idênticos.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/build_augmented_candidate_graph.py \
  --input-graph geoespacial/outputs/candidate_ranking/graph.graphml \
  --gap-candidates geoespacial/outputs/topodata_gap_candidates/gap_candidates.csv.gz \
  --output-dir geoespacial/outputs/augmented_candidate_graph \
  --report geoespacial/reports/augmented_candidate_graph/summary.json
```

O limite de curvatura não comprova cobertura territorial, conectividade visual,
implantação ou iluminação RF.
