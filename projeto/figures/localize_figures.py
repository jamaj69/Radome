"""Build language-specific publication figures from the common geometry masters."""

from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageChops, ImageDraw, ImageFont

from build_paths import BUILD
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
    "fig01": (("orange: external source; blue: radomes; purple: command center; green: calibrated observations"), ("laranja: fonte externa; azul: radomes; roxo: central de comando; verde: observações calibradas")),
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
    "fig01": [
        (.50,.135,"external illuminator / emitter","iluminador / emissor externo"),
        (.185,.475,"Radome A","Radome A"),
        (.520,.475,"Radome B","Radome B"),
        (.855,.475,"Radome C","Radome C"),
        (.50,.865,"Command center","Central de comando"),
    ],
    "fig02": [(.29,.65,"HF","HF"),(.42,.78,"VHF","VHF"),(.64,.69,"UHF","UHF"),(.70,.37,"L/S/C","L/S/C"),(.40,.28,"X/Ku/Ka","X/Ku/Ka"),(.50,.52,"face core","núcleo da face")],
    "fig03": [(.252,.530,"RF aperture","abertura RF"),(.700,.152,"outer skin","pele externa"),(.700,.265,"low-loss core","núcleo de baixa perda"),(.700,.378,"inner skin","pele interna"),(.700,.491,"RF aperture / PCB","abertura RF / PCB"),(.700,.604,"shielded band modules","módulos blindados por faixa"),(.593,.739,"ADC A","ADC A"),(.806,.739,"ADC B","ADC B"),(.593,.829,"ASIC A","ASIC A"),(.806,.829,"ASIC B","ASIC B")],
    "fig04": [(.18,.78,"HF","HF"),(.27,.66,"VHF","VHF"),(.51,.54,"UHF","UHF"),(.57,.42,"aviation","aeronáutica"),(.68,.30,"L/S/C","L/S/C"),(.82,.18,"X/Ku","X/Ku"),(.89,.07,"K/Ka","K/Ka")],
    "fig05": [(.123,.196,"VHF channel","canal VHF"),(.123,.376,"UHF channel","canal UHF"),(.421,.279,"independent bands","faixas independentes"),(.779,.279,"invalid synthesis","síntese inválida"),(.123,.651,"port X","porta X"),(.123,.830,"port Y","porta Y"),(.421,.734,"coherent ADCs","ADCs coerentes"),(.779,.734,"Jones / Stokes / circular","Jones / Stokes / circular")],
    "fig06": [(.084,.331,"antenna","antena"),(.218,.331,"filter","filtro"),(.351,.331,"LNA","LNA"),(.484,.331,"converter","conversor"),(.618,.331,"ADC","ADC"),(.751,.331,"FPGA","FPGA"),(.884,.331,"events","eventos"),(.221,.750,"calibration","calibração"),(.488,.750,"clock","relógio"),(.755,.750,"control","controle")],
    "fig07": [(.130,.224,"GNSS antenna","antena GNSS"),(.130,.748,"GNSS receiver","receptor GNSS"),(.402,.486,"1 PPS + 10 MHz","1 PPS + 10 MHz"),(.673,.252,"distribution","distribuição"),(.673,.720,"HW timestamp","timestamp HW"),(.885,.486,"RF-delay cal.","calibração atraso RF")],
    "fig08": [(.13,.78,"illuminator","iluminador"),(.50,.12,"target","alvo"),(.80,.82,"receiver","receptor"),(.72,.38,"receiver","receptor"),(.50,.88,"receiver","receptor")],
    "fig09": [(.097,.260,"reference","referência"),(.097,.739,"surveillance","vigilância"),(.281,.491,"alignment","alinhamento"),(.425,.491,"detection","detecção"),(.568,.491,"association","associação"),(.712,.491,"estimation","estimação"),(.856,.491,"tracking","rastreamento"),(.440,.831,"calibration","calibração"),(.728,.831,"quality control","controle de qualidade")],
    "fig10": [(.123,.171,"concept","conceito"),(.274,.330,"simulation","simulação"),(.447,.490,"bench prototype","protótipo de bancada"),(.640,.650,"field demonstrator","demonstrador de campo"),(.825,.810,"qualification","qualificação")],
    "fig11": [(.23,.39,"dielectric RF face","face RF dielétrica"),(.49,.52,"normal boom","boom normal"),(.60,.43,"UHF Yagi — 135°","Yagi UHF — 135°"),(.56,.61,"VHF Yagi — 45°","Yagi VHF — 45°"),(.82,.10,"outer skin","pele externa"),(.82,.22,"low-loss core","núcleo de baixa perda"),(.82,.34,"inner skin","pele interna"),(.82,.465,"RF aperture / PCB","abertura RF / PCB"),(.82,.59,"shielding","blindagem"),(.82,.71,"face electronics","eletrônica da face"),(.75,.87,"VHF channel","canal VHF"),(.89,.87,"UHF channel","canal UHF")],
    "fig15": [(.08,.57,"node A","nó A"),(.92,.57,"node B","nó B"),(.50,.18,"aircraft","aeronave"),(.50,.62,"nominal 100 km baseline","linha de base nominal de 100 km"),(.29,.38,"path A / AOA cone","caminho A / cone AOA"),(.71,.38,"path B / AOA cone","caminho B / cone AOA")],
}

# Space available inside each coloured functional block.  Every tuple is
# (width fraction, height fraction, maximum lines).  Keeping this geometry
# separate from the translated strings lets each language compose its text
# without changing the common diagram master.
INSIDE_BLOCKS = {
    "fig01": [(.27,.095,2),(.17,.120,2),(.17,.120,2),(.17,.120,2),(.30,.100,2)],
    "fig03": [(.14,.18,2),(.36,.050,1),(.36,.050,1),(.36,.050,1),(.36,.050,1),(.36,.050,1),(.12,.068,1),(.12,.068,1),(.12,.068,1),(.12,.068,1)],
    "fig05": [(.13,.105,2),(.13,.105,2),(.16,.105,2),(.23,.105,2),(.13,.105,2),(.13,.105,2),(.16,.105,2),(.23,.105,2)],
    "fig06": [(.075,.115,2),(.075,.115,2),(.075,.115,1),(.075,.115,2),(.075,.115,1),(.075,.115,1),(.075,.115,2),(.085,.115,2),(.085,.115,2),(.085,.115,2)],
    "fig07": [(.12,.130,2),(.12,.130,2),(.12,.130,2),(.12,.130,2),(.12,.130,2),(.095,.130,3)],
    "fig09": [(.095,.130,2),(.095,.130,2),(.085,.130,2),(.085,.130,2),(.085,.130,2),(.085,.130,2),(.085,.130,2),(.12,.130,2),(.12,.130,2)],
    "fig10": [(.12,.100,2),(.20,.100,2),(.25,.100,2),(.24,.100,2),(.20,.100,2)],
}

# Independent typographic profiles are intentional.  English and Portuguese
# continue to share geometry, colours and engineering content, but they do not
# have to share line lengths or annotation offsets.
LANGUAGE_LAYOUTS = {
    "en": {
        "title_width": .90,
        "key_width": .92,
        "floating_width": .30,
        "title_scale": 1.00,
        "key_scale": 1.00,
        "annotation_scale": 1.00,
        "offsets": {},
    },
    "pt-BR": {
        "title_width": .86,
        "key_width": .88,
        "floating_width": .27,
        "title_scale": .96,
        "key_scale": .96,
        "annotation_scale": .98,
        "offsets": {
            # Longer Portuguese callouts need a little more separation from
            # the central aircraft paths and the neighbouring receiver label.
            "fig15": {3: (0, .025), 4: (-.015, 0), 5: (.015, 0)},
        },
    },
}


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def source_for(prefix):
    matches = sorted(BUILD.glob(f"{prefix}_*"))
    matches = [p for p in matches if p.suffix.lower() in {".png", ".pdf"} and p.parent == BUILD]
    if not matches:
        raise FileNotFoundError(f"{prefix} in {BUILD}")
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
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_text(draw, text, preferred_font, available_width, available_height, max_lines):
    """Return the largest readable multiline setting that fits a region."""
    minimum_size = max(12, round(preferred_font.size * .62))
    for size in range(preferred_font.size, minimum_size - 1, -1):
        candidate = font(size, True)
        lines = wrap(draw, text, candidate, available_width)
        if not lines or len(lines) > max_lines:
            continue
        label = "\n".join(lines)
        spacing = max(2, candidate.size // 6)
        bbox = draw.multiline_textbbox(
            (0, 0), label, font=candidate, spacing=spacing, align="center"
        )
        if bbox[2] - bbox[0] <= available_width and bbox[3] - bbox[1] <= available_height:
            return candidate, label, spacing, bbox
    raise ValueError(f"label does not fit its layout region: {text!r}")


def draw_label(draw, centre, text, text_font, canvas_size, width_fraction):
    """Draw a padded box whose centre follows the centre of the rendered glyphs."""
    canvas_width, canvas_height = canvas_size
    max_text_width = max(160, int(canvas_width * width_fraction))
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


def draw_text_in_block(draw, centre, text, text_font, canvas_size, block):
    """Fit and centre text directly inside an existing coloured diagram block."""
    canvas_width, canvas_height = canvas_size
    width_fraction, height_fraction, max_lines = block
    candidate, label, spacing, bbox = fit_text(
        draw,
        text,
        text_font,
        canvas_width * width_fraction,
        canvas_height * height_fraction,
        max_lines,
    )
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    cx, cy = centre
    # Centre the visible ink, compensating for the font's left/top bearings.
    origin_x = cx - text_width / 2 - bbox[0]
    origin_y = cy - text_height / 2 - bbox[1]
    draw.multiline_text(
        (origin_x, origin_y),
        label,
        font=candidate,
        fill="#263746",
        spacing=spacing,
        align="center",
    )


for lang, index in (("en", 0), ("pt-BR", 1)):
    layout = LANGUAGE_LAYOUTS[lang]
    destination = ROOT / lang
    destination.mkdir(exist_ok=True)
    for prefix in FIGURES:
        source = source_for(prefix)
        image = load_image(source)
        width, height = image.size
        title_font = font(round(max(24, width // 42) * layout["title_scale"]), True)
        key_font = font(round(max(18, width // 58) * layout["key_scale"]))
        scratch = ImageDraw.Draw(image)
        annotation_font = font(round(max(18, width // 62) * layout["annotation_scale"]), True)
        for annotation_index, (x, y, english, portuguese) in enumerate(ANNOTATIONS.get(prefix, [])):
            label = english if index == 0 else portuguese
            dx, dy = layout["offsets"].get(prefix, {}).get(annotation_index, (0, 0))
            blocks = INSIDE_BLOCKS.get(prefix)
            if blocks:
                draw_text_in_block(
                    scratch,
                    (width * (x + dx), height * (y + dy)),
                    label,
                    annotation_font,
                    image.size,
                    blocks[annotation_index],
                )
            else:
                draw_label(
                    scratch,
                    (width * (x + dx), height * (y + dy)),
                    label,
                    annotation_font,
                    image.size,
                    layout["floating_width"],
                )
        title_lines = wrap(scratch, TITLES[prefix][index], title_font, width * layout["title_width"])
        key_lines = wrap(scratch, KEYS[prefix][index], key_font, width * layout["key_width"])
        title_spacing = max(3, title_font.size // 6)
        title_bbox = scratch.multiline_textbbox(
            (0, 0), "\n".join(title_lines), font=title_font,
            spacing=title_spacing, align="center"
        )
        title_height = title_bbox[3] - title_bbox[1]
        key_height = len(key_lines) * (key_font.size + 8)
        panel_height = max(150, 38 + title_height + key_height + 24)
        output = Image.new("RGB", (width, height + panel_height), "white")
        output.paste(image, (0, panel_height))
        draw = ImageDraw.Draw(output)
        draw.multiline_text(
            (width / 2, 18), "\n".join(title_lines), font=title_font,
            fill="#17324d", spacing=title_spacing, align="center", anchor="ma"
        )
        y = 28 + title_height
        for line in key_lines:
            draw.text((width / 2, y), line, font=key_font, fill="#52606d", anchor="ma")
            y += key_font.size + 8
        draw.line((45, panel_height - 8, width - 45, panel_height - 8), fill="#c8d1d7", width=2)
        output.save(destination / source.with_suffix(".png").name, optimize=True)

print("Generated localized figure sets in figures/en and figures/pt-BR")
