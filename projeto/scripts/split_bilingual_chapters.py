#!/usr/bin/env python3
"""Split the legacy bilingual chapters into independent language trees."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "chapters" / "legacy-bilingual"
TARGETS = {"en": ROOT / "chapters" / "en", "pt": ROOT / "chapters" / "pt-BR"}

FIGURE_CAPTIONS = {
    "fig01_arquitetura_rede.png": ("Distributed sensing architecture.", "Arquitetura distribuída de sensoriamento."),
    "fig02_zonamento_radome.png": ("Functional zoning.", "Zoneamento funcional."),
    "fig03_modulo_face.png": ("Triangular RF face module.", "Módulo triangular de face RF."),
    "fig04_particionamento_espectro.png": ("Recommended spectral partition.", "Particionamento espectral recomendado."),
    "fig05_polarimetria.png": ("Cross-band diversity versus valid same-band polarimetric acquisition.", "Diversidade entre faixas versus aquisição polarimétrica válida na mesma faixa."),
    "fig06_cadeia_rf.png": ("RF chain and edge processing.", "Cadeia RF e processamento de borda."),
    "fig07_sincronizacao.png": ("Timing and uncertainty budget.", "Sincronização e orçamento de incerteza."),
    "fig08_geometria_bistatica.png": ("Bistatic geometry.", "Geometria biestática."),
    "fig09_fluxo_processamento.png": ("Multistatic passive processing.", "Processamento passivo multiestático."),
    "fig10_roteiro.png": ("Development and validation roadmap.", "Roteiro de desenvolvimento e validação."),
    "fig11_face_yagi_camadas.pdf": ("Two-metre triangular face with crossed external VHF and UHF Yagis: orthogonal transverse elements, independent feeds and distinct scales.", "Face triangular de 2 m com Yagis VHF e UHF externas cruzadas: elementos transversais ortogonais, alimentações independentes e escalas distintas."),
    "fig13_radome_blender.png": ("Blender model of the radome and exploded face with crossed VHF/UHF Yagis.", "Modelo Blender do radome e da face explodida com Yagis VHF/UHF cruzadas."),
    "fig14_radome_interior_blender.png": ("Internal Blender inspection view with transparent shell, structural ties, service trunks and shielded modules.", "Vista interna de inspeção no Blender com casca transparente, tirantes estruturais, troncos de serviço e módulos blindados."),
    "fig15_aircraft_two_radomes_100km.png": ("Two radomes separated by 100 km receiving an aircraft transmission and fusing power, AOA, TDOA and Doppler observables.", "Dois radomes separados por 100 km recebem uma transmissão aeronáutica e fundem observáveis de potência, AOA, TDOA e Doppler."),
    "fig16_tetrahedral_face_cluster.png": ("Seven contiguous shallow tetrahedral cells with local tangent bases and a reserved internal service core.", "Sete células tetraédricas rasas contíguas com bases tangentes locais e núcleo interno de serviço reservado."),
}


def title_for(raw: str, language: str) -> str:
    parts = raw.split(" / ", 1)
    return parts[0] if language == "en" else parts[-1]


def localize_headings(text: str, language: str) -> str:
    def repl(match: re.Match[str]) -> str:
        title = title_for(match.group(1), language)
        return rf"\section{{{title}}}"
    return re.sub(r"\\subsection\*?\{([^{}]*)\}", repl, text)


def strip_figures(text: str) -> str:
    return re.sub(r"\n?\\begin\{figure\}.*?\\end\{figure\}\n?", "\n", text, flags=re.S)


def figure_blocks(source: str, language: str) -> str:
    blocks = []
    seen = set()
    for match in re.finditer(r"\\begin\{figure\}.*?\\end\{figure\}", source, flags=re.S):
        block = match.group(0)
        image = re.search(r"\\includegraphics(?:\[[^]]*\])?\{([^{}]+)\}", block)
        if not image or image.group(1) in seen:
            continue
        filename = image.group(1)
        seen.add(filename)
        caption = FIGURE_CAPTIONS.get(filename)
        if caption:
            localized = caption[0 if language == "en" else 1]
            block = re.sub(r"^\\caption.*$", lambda _: f"\\caption{{{localized}}}", block, count=1, flags=re.M)
        block = re.sub(r"\\label\{[^{}]+\}", lambda _: f"\\label{{fig:{Path(filename).stem}}}", block, count=1)
        blocks.append(block)
    return "\n\n".join(blocks)


def clean_special_cases(name: str, english: str, portuguese: str) -> tuple[str, str]:
    if name == "03_geometry_radome.tex":
        paragraph = re.search(r"\nThe Blender model makes.*?orthogonal planes\.\n", portuguese, flags=re.S)
        if paragraph:
            english += "\n" + paragraph.group(0).strip() + "\n"
            portuguese = portuguese.replace(paragraph.group(0), "\n")
    if name == "07_passive_radar.tex":
        marker = r"\\subsection\*\{Cellular towers as calibrated illuminators / Torres celulares como iluminadores calibrados\}"
        match = re.search(marker + r"(.*?)(?=\nAs torres celulares)", portuguese, flags=re.S)
        if match:
            english += "\n\\subsection*{Cellular towers as calibrated illuminators}\n" + match.group(1).strip() + "\n"
            portuguese = portuguese[:match.start()] + "\n\\subsection*{Torres celulares como iluminadores calibrados}\n" + portuguese[match.end():].lstrip()
    return english, portuguese


def split_chapter(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    chapter = re.match(r"\\chapter\{(.*?)\}\s*", source, flags=re.S)
    if not chapter:
        raise ValueError(f"No chapter title in {path}")

    if path.name == "11_detection_record.tex":
        write_detection_appendix(path.name)
        return

    body = source[chapter.end():]
    english_marker = "\\section*{English}"
    portuguese_marker = "\\section*{Português}"
    if english_marker not in body or portuguese_marker not in body:
        raise ValueError(f"Language markers not found in {path}")
    english, portuguese = body.split(portuguese_marker, 1)
    english = english.split(english_marker, 1)[1]
    english, portuguese = clean_special_cases(path.name, english, portuguese)

    for language, content in (("en", english), ("pt", portuguese)):
        content = strip_figures(content)
        content = localize_headings(content, language)
        content = content.replace("\\citep{", "\\cite{")
        content = content.replace("This article, assembled from \\texttt{projetov1.tex}, is the authoritative technical document.", "The independent English edition, assembled from \\texttt{radome-en.tex}, is one of the two authoritative technical publications.")
        content = content.replace("Este artigo, montado a partir de \\texttt{projetov1.tex}, é o documento técnico autoritativo.", "A edição independente em português brasileiro, montada a partir de \\texttt{radome-pt-br.tex}, é uma das duas publicações técnicas autoritativas.")
        figures = figure_blocks(source, language)
        output = f"\\chapter{{{title_for(chapter.group(1), language)}}}\n\n{content.strip()}\n"
        if figures:
            output += "\n" + figures + "\n"
        TARGETS[language].mkdir(parents=True, exist_ok=True)
        (TARGETS[language] / path.name).write_text(output, encoding="utf-8")


def write_detection_appendix(name: str) -> None:
    rows = {
        "en": [
            ("station\\_id", "Node identifier and calibration version"),
            ("tile\\_id/channel\\_id", "Tile, polarization port and RF chain"),
            ("timestamp\\_utc", "Time with estimated uncertainty"),
            ("frequency\\_hz/bandwidth\\_hz", "Observed centre frequency and bandwidth"),
            ("polarization", "Measured port/orientation for single-polarization channels; Jones or Stokes only for a calibrated coherent same-band pair"),
            ("aoa\\_az\\_el", "Local direction and covariance"),
            ("delay\\_doppler", "Bistatic measurements and quality"),
            ("illuminator\\_id", "Illuminator identity or hypothesis"),
            ("sync\\_state", "locked, holdover or degraded"),
            ("environment", "Temperature, humidity and radome state"),
        ],
        "pt": [
            ("station\\_id", "Identificador do nó e versão da calibração"),
            ("tile\\_id/channel\\_id", "Tile, porta de polarização e cadeia RF"),
            ("timestamp\\_utc", "Tempo com incerteza estimada"),
            ("frequency\\_hz/bandwidth\\_hz", "Frequência central e largura de banda observadas"),
            ("polarization", "Porta e orientação medidas para canais de polarização única; Jones ou Stokes somente para par coerente calibrado na mesma faixa"),
            ("aoa\\_az\\_el", "Direção local e covariância"),
            ("delay\\_doppler", "Medidas biestáticas e qualidade"),
            ("illuminator\\_id", "Identidade ou hipótese do iluminador"),
            ("sync\\_state", "travado, em holdover ou degradado"),
            ("environment", "Temperatura, umidade e estado do radome"),
        ],
    }
    titles = {"en": ("Minimum Detection Record", "Field", "Description"), "pt": ("Registro Mínimo de Detecção", "Campo", "Descrição")}
    for language in ("en", "pt"):
        title, field, description = titles[language]
        table_rows = "\n".join(rf"\texttt{{{key}}} & {value}\\" for key, value in rows[language])
        output = rf"""\chapter{{{title}}}

\small
\begin{{longtable}}{{p{{0.27\textwidth}}p{{0.58\textwidth}}}}
\toprule
\textbf{{{field}}} & \textbf{{{description}}}\\
\midrule
{table_rows}
\bottomrule
\end{{longtable}}
\normalsize
"""
        TARGETS[language].mkdir(parents=True, exist_ok=True)
        (TARGETS[language] / name).write_text(output, encoding="utf-8")


def main() -> None:
    for path in sorted(SOURCE.glob("[0-9][0-9]_*.tex")):
        split_chapter(path)


if __name__ == "__main__":
    main()
