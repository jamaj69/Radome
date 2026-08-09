"""Build language-specific publication figures from the common geometry masters."""

from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FIGURES = [f"fig{i:02d}" for i in range(1, 17)]
TITLES = {
    "fig01": ("Distributed sensing architecture", "Arquitetura distribuída de sensoriamento"),
    "fig02": ("Hybrid functional zoning", "Zoneamento funcional híbrido"),
    "fig03": ("Face module and electromechanical layers", "Módulo de face e camadas eletromecânicas"),
    "fig04": ("Spectral partition", "Particionamento espectral"),
    "fig05": ("Cross-band diversity and valid polarimetry", "Diversidade entre faixas e polarimetria válida"),
    "fig06": ("RF acquisition and edge processing chain", "Cadeia de aquisição RF e processamento de borda"),
    "fig07": ("Timing and end-to-end calibration", "Sincronismo e calibração ponta a ponta"),
    "fig08": ("Bistatic and multistatic geometry", "Geometria biestática e multiestática"),
    "fig09": ("Passive multistatic processing flow", "Fluxo de processamento multiestático passivo"),
    "fig10": ("Staged development roadmap", "Roteiro de desenvolvimento por etapas"),
    "fig11": ("Triangular face, normal boom and RF layers", "Face triangular, boom normal e camadas RF"),
    "fig12": ("Exploded three-dimensional face assembly", "Montagem tridimensional explodida da face"),
    "fig13": ("External radome and antenna assembly", "Conjunto externo do radome e antenas"),
    "fig14": ("Internal radome inspection view", "Vista interna de inspeção do radome"),
    "fig15": ("Two-node aircraft validation scenario", "Cenário aeronáutico de validação com dois nós"),
    "fig16": ("Tetrahedral face cluster and local orientation", "Conjunto de faces tetraédricas e orientação local"),
}

KEYS = {
    "fig01": (("orange: source/target; blue: stations; purple: fusion; green: data links"), ("laranja: fonte/alvo; azul: estações; roxo: fusão; verde: enlaces de dados")),
    "fig02": (("colours: band families; white centre: shared services"), ("cores: famílias de faixas; centro branco: serviços compartilhados")),
    "fig03": (("triangle: RF aperture; bars: material/electronic layers; lower blocks: independent channels"), ("triângulo: abertura RF; barras: camadas materiais/eletrônicas; blocos inferiores: canais independentes")),
    "fig04": (("bars: proposed band families; blank intervals: deliberate coverage gaps"), ("barras: famílias de faixas propostas; intervalos brancos: lacunas deliberadas de cobertura")),
    "fig05": (("top: invalid cross-band synthesis; bottom: coherent same-band pair"), ("acima: síntese inválida entre faixas; abaixo: par coerente na mesma faixa")),
    "fig06": (("upper row: signal chain; lower blocks: calibration, timing and control inputs"), ("linha superior: cadeia de sinal; blocos inferiores: calibração, sincronismo e controle")),
    "fig07": (("left: time references; centre: disciplined clock; right: distribution and RF-delay calibration"), ("esquerda: referências de tempo; centro: relógio disciplinado; direita: distribuição e calibração de atraso RF")),
    "fig08": (("orange: illuminator; grey: target; blue: receivers; red: reflected paths"), ("laranja: iluminador; cinza: alvo; azul: receptores; vermelho: caminhos refletidos")),
    "fig09": (("reference and surveillance channels feed detection, association, estimation and tracking"), ("canais de referência e vigilância alimentam detecção, associação, estimação e rastreamento")),
    "fig10": (("successive bars: concept, simulation, bench prototype, field demonstrator and qualification"), ("barras sucessivas: conceito, simulação, protótipo de bancada, demonstrador de campo e qualificação")),
    "fig11": (("dark axis: outward face normal; orange/blue: orthogonal Yagis at 45°/135°; right: layer stack"), ("eixo escuro: normal externa da face; laranja/azul: Yagis ortogonais a 45°/135°; direita: pilha de camadas")),
    "fig12": (("boom follows the outward normal; orange/blue elements are orthogonal in the tangent plane"), ("o boom segue a normal externa; elementos laranja/azul são ortogonais no plano tangente")),
    "fig13": (("radome overview with exploded triangular face and normal combined-Yagi boom"), ("vista geral do radome com face triangular explodida e boom normal das Yagis combinadas")),
    "fig14": (("transparent shell exposes structural paths, service trunks and shielded modules"), ("a casca transparente expõe caminhos estruturais, troncos de serviço e módulos blindados")),
    "fig15": (("two radomes define the baseline; coloured paths and cones represent independent observables"), ("dois radomes definem a linha de base; caminhos e cones coloridos representam observáveis independentes")),
    "fig16": (("green arrows: outward normals/booms; orange/cyan: orthogonal 45°/135° tangent directions"), ("setas verdes: normais externas/booms; laranja/ciano: direções tangentes ortogonais de 45°/135°")),
}

# Normalized positions in the common geometry masters. These short labels make
# the diagram itself readable; the longer engineering qualification stays in
# the LaTeX caption.
ANNOTATIONS = {
    "fig01": [(.50,.07,"source / target","fonte / alvo"),(.17,.38,"node A","nó A"),(.50,.43,"node B","nó B"),(.83,.38,"node C","nó C"),(.50,.88,"distributed fusion","fusão distribuída")],
    "fig02": [(.29,.65,"HF","HF"),(.42,.78,"VHF","VHF"),(.64,.69,"UHF","UHF"),(.70,.37,"L/S/C","L/S/C"),(.40,.28,"X/Ku/Ka","X/Ku/Ka"),(.50,.52,"face core","núcleo da face")],
    "fig03": [(.24,.43,"RF aperture","abertura RF"),(.73,.15,"outer skin","pele externa"),(.73,.265,"low-loss core","núcleo de baixa perda"),(.73,.38,"inner skin","pele interna"),(.73,.49,"RF aperture / PCB","abertura RF / PCB"),(.73,.605,"shielded band modules","módulos blindados por faixa"),(.61,.73,"ADC A","ADC A"),(.82,.73,"ADC B","ADC B"),(.61,.83,"ASIC A","ASIC A"),(.82,.83,"ASIC B","ASIC B")],
    "fig04": [(.18,.78,"HF","HF"),(.27,.66,"VHF","VHF"),(.51,.54,"UHF","UHF"),(.57,.42,"aviation","aeronáutica"),(.68,.30,"L/S/C","L/S/C"),(.82,.18,"X/Ku","X/Ku"),(.89,.07,"K/Ka","K/Ka")],
    "fig05": [(.12,.24,"VHF channel","canal VHF"),(.12,.41,"UHF channel","canal UHF"),(.42,.33,"independent bands","faixas independentes"),(.79,.33,"invalid synthesis","síntese inválida"),(.12,.68,"port X","porta X"),(.12,.86,"port Y","porta Y"),(.42,.77,"coherent ADCs","ADCs coerentes"),(.79,.77,"Jones / Stokes / circular","Jones / Stokes / circular")],
    "fig06": [(.08,.33,"antenna","antena"),(.22,.33,"filter","filtro"),(.35,.33,"LNA","LNA"),(.49,.33,"converter","conversor"),(.63,.33,"ADC","ADC"),(.77,.33,"FPGA","FPGA"),(.91,.33,"events","eventos"),(.25,.75,"calibration","calibração"),(.52,.75,"clock","relógio"),(.80,.75,"control","controle")],
    "fig07": [(.13,.23,"GNSS antenna","antena GNSS"),(.13,.75,"GNSS receiver","receptor GNSS"),(.40,.54,"1 PPS + 10 MHz","1 PPS + 10 MHz"),(.68,.28,"distribution","distribuição"),(.68,.72,"HW timestamp","timestamp HW"),(.89,.49,"RF-delay cal.","calibração atraso RF")],
    "fig08": [(.13,.78,"illuminator","iluminador"),(.50,.12,"target","alvo"),(.80,.82,"receiver","receptor"),(.72,.38,"receiver","receptor"),(.50,.88,"receiver","receptor")],
    "fig09": [(.09,.25,"reference","referência"),(.09,.74,"surveillance","vigilância"),(.28,.50,"alignment","alinhamento"),(.43,.50,"detection","detecção"),(.58,.50,"association","associação"),(.73,.50,"estimation","estimação"),(.88,.50,"tracking","rastreamento"),(.48,.83,"calibration","calibração"),(.78,.83,"quality control","controle de qualidade")],
    "fig10": [(.14,.14,"concept","conceito"),(.29,.32,"simulation","simulação"),(.47,.50,"bench prototype","protótipo de bancada"),(.68,.67,"field demonstrator","demonstrador de campo"),(.87,.83,"qualification","qualificação")],
    "fig11": [(.23,.39,"dielectric RF face","face RF dielétrica"),(.49,.52,"normal boom","boom normal"),(.60,.43,"UHF Yagi — 135°","Yagi UHF — 135°"),(.56,.61,"VHF Yagi — 45°","Yagi VHF — 45°"),(.82,.10,"outer skin","pele externa"),(.82,.22,"low-loss core","núcleo de baixa perda"),(.82,.34,"inner skin","pele interna"),(.82,.465,"RF aperture / PCB","abertura RF / PCB"),(.82,.59,"shielding","blindagem"),(.82,.71,"face electronics","eletrônica da face"),(.75,.87,"VHF channel","canal VHF"),(.89,.87,"UHF channel","canal UHF")],
    "fig15": [(.08,.57,"node A","nó A"),(.92,.57,"node B","nó B"),(.50,.18,"aircraft","aeronave"),(.50,.62,"nominal 100 km baseline","linha de base nominal de 100 km"),(.29,.38,"path A / AOA cone","caminho A / cone AOA"),(.71,.38,"path B / AOA cone","caminho B / cone AOA")],
}


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def source_for(prefix):
    matches = sorted(ROOT.glob(f"{prefix}_*"))
    matches = [p for p in matches if p.suffix.lower() in {".png", ".pdf"} and p.parent == ROOT]
    if not matches:
        raise FileNotFoundError(prefix)
    return matches[0]


def load_image(path):
    if path.suffix.lower() == ".png":
        return Image.open(path).convert("RGB")
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "page"
        subprocess.run(["pdftoppm", "-singlefile", "-png", "-r", "180", str(path), str(target)], check=True)
        image = Image.open(target.with_suffix(".png")).convert("RGB")
        difference = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
        bbox = difference.getbbox()
        if bbox:
            left, top, right, bottom = bbox
            padding = 30
            return image.crop((max(0, left-padding), max(0, top-padding), min(image.width, right+padding), min(image.height, bottom+padding)))
        return image


def wrap(draw, text, text_font, width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=text_font)[2] <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_label(draw, centre, text, text_font, canvas_size):
    """Draw a padded box whose centre follows the centre of the rendered glyphs."""
    canvas_width, canvas_height = canvas_size
    max_text_width = max(160, int(canvas_width * .30))
    lines = wrap(draw, text, text_font, max_text_width)
    label = "\n".join(lines)
    spacing = max(3, text_font.size // 5)

    # Pillow's text bbox can start below or to the left of the drawing origin.
    # Compensating for those bearings is what centres the visible glyphs rather
    # than merely centring the font's nominal origin.
    bbox = draw.multiline_textbbox(
        (0, 0), label, font=text_font, spacing=spacing, align="center"
    )
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    padding_x = max(10, round(text_font.size * .55))
    padding_y = max(7, round(text_font.size * .38))
    box_width = text_width + 2 * padding_x
    box_height = text_height + 2 * padding_y

    cx, cy = centre
    margin = max(8, text_font.size // 3)
    cx = min(max(cx, margin + box_width / 2), canvas_width - margin - box_width / 2)
    cy = min(max(cy, margin + box_height / 2), canvas_height - margin - box_height / 2)
    left = round(cx - box_width / 2)
    top = round(cy - box_height / 2)
    right = round(left + box_width)
    bottom = round(top + box_height)

    draw.rounded_rectangle(
        (left, top, right, bottom),
        radius=max(5, text_font.size // 4),
        fill="#ffffff",
        outline="#8a9aa3",
        width=max(1, text_font.size // 16),
    )
    text_x = left + padding_x - bbox[0]
    text_y = top + padding_y - bbox[1]
    draw.multiline_text(
        (text_x, text_y),
        label,
        font=text_font,
        fill="#263746",
        spacing=spacing,
        align="center",
    )


for lang, index in (("en", 0), ("pt-BR", 1)):
    destination = ROOT / lang
    destination.mkdir(exist_ok=True)
    for prefix in FIGURES:
        source = source_for(prefix)
        image = load_image(source)
        width, height = image.size
        title_font = font(max(24, width // 42), True)
        key_font = font(max(18, width // 58))
        scratch = ImageDraw.Draw(image)
        annotation_font = font(max(18, width // 62), True)
        for x, y, english, portuguese in ANNOTATIONS.get(prefix, []):
            label = english if index == 0 else portuguese
            draw_label(
                scratch,
                (width * x, height * y),
                label,
                annotation_font,
                image.size,
            )
        key_lines = wrap(scratch, KEYS[prefix][index], key_font, width - 100)
        panel_height = max(150, 65 + len(key_lines) * (key_font.size + 8))
        output = Image.new("RGB", (width, height + panel_height), "white")
        output.paste(image, (0, panel_height))
        draw = ImageDraw.Draw(output)
        draw.text((width / 2, 18), TITLES[prefix][index], font=title_font, fill="#17324d", anchor="ma")
        y = 28 + title_font.size
        for line in key_lines:
            draw.text((width / 2, y), line, font=key_font, fill="#52606d", anchor="ma")
            y += key_font.size + 8
        draw.line((45, panel_height - 8, width - 45, panel_height - 8), fill="#c8d1d7", width=2)
        output.save(destination / source.with_suffix(".png").name, optimize=True)

print("Generated localized figure sets in figures/en and figures/pt-BR")
