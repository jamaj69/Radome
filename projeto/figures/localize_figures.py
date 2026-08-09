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
    "fig03": [(.24,.43,"RF aperture","abertura RF"),(.73,.15,"outer skin","pele externa"),(.73,.265,"low-loss core","núcleo de baixa perda"),(.73,.38,"inner skin","pele interna"),(.73,.49,"RF aperture / PCB","abertura RF / PCB"),(.73,.605,"shielded band modules","módulos blindados por faixa"),(.61,.77,"ADC A","ADC A"),(.82,.77,"ADC B","ADC B"),(.61,.91,"ASIC A","ASIC A"),(.82,.91,"ASIC B","ASIC B")],
    "fig04": [(.18,.78,"HF","HF"),(.27,.66,"VHF","VHF"),(.51,.54,"UHF","UHF"),(.57,.42,"aviation","aeronáutica"),(.68,.30,"L/S/C","L/S/C"),(.82,.18,"X/Ku","X/Ku"),(.89,.07,"K/Ka","K/Ka")],
    "fig05": [(.12,.24,"VHF channel","canal VHF"),(.12,.41,"UHF channel","canal UHF"),(.42,.33,"independent bands","faixas independentes"),(.79,.33,"invalid synthesis","síntese inválida"),(.12,.68,"port X","porta X"),(.12,.86,"port Y","porta Y"),(.42,.77,"coherent ADCs","ADCs coerentes"),(.79,.77,"Jones / Stokes / circular","Jones / Stokes / circular")],
    "fig06": [(.08,.34,"antenna","antena"),(.22,.34,"filter","filtro"),(.35,.34,"LNA","LNA"),(.49,.34,"converter","conversor"),(.63,.34,"ADC","ADC"),(.77,.34,"FPGA","FPGA"),(.91,.34,"events","eventos"),(.25,.74,"calibration","calibração"),(.52,.74,"clock","relógio"),(.80,.74,"control","controle")],
    "fig07": [(.13,.20,"GNSS antenna","antena GNSS"),(.13,.70,"GNSS receiver","receptor GNSS"),(.40,.43,"1 PPS + 10 MHz","1 PPS + 10 MHz"),(.68,.20,"distribution","distribuição"),(.68,.70,"hardware timestamp","timestamp em hardware"),(.89,.43,"RF-delay calibration","calibração de atraso RF")],
    "fig08": [(.13,.78,"illuminator","iluminador"),(.50,.12,"target","alvo"),(.80,.82,"receiver","receptor"),(.72,.38,"receiver","receptor"),(.50,.88,"receiver","receptor")],
    "fig09": [(.09,.25,"reference","referência"),(.09,.74,"surveillance","vigilância"),(.28,.50,"alignment","alinhamento"),(.43,.50,"detection","detecção"),(.58,.50,"association","associação"),(.73,.50,"estimation","estimação"),(.88,.50,"tracking","rastreamento"),(.48,.83,"calibration","calibração"),(.78,.83,"quality control","controle de qualidade")],
    "fig10": [(.14,.14,"concept","conceito"),(.29,.32,"simulation","simulação"),(.47,.50,"bench prototype","protótipo de bancada"),(.68,.67,"field demonstrator","demonstrador de campo"),(.87,.83,"qualification","qualificação")],
    "fig11": [(.23,.39,"dielectric RF face","face RF dielétrica"),(.49,.52,"normal boom","boom normal"),(.60,.43,"UHF Yagi — 135°","Yagi UHF — 135°"),(.56,.61,"VHF Yagi — 45°","Yagi VHF — 45°"),(.82,.10,"outer skin","pele externa"),(.82,.22,"low-loss core","núcleo de baixa perda"),(.82,.34,"inner skin","pele interna"),(.82,.465,"RF aperture / PCB","abertura RF / PCB"),(.82,.59,"shielding","blindagem"),(.82,.71,"face electronics","eletrônica da face"),(.75,.87,"VHF channel","canal VHF"),(.89,.87,"UHF channel","canal UHF")],
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
            bbox = scratch.textbbox((width*x, height*y), label, font=annotation_font, anchor="mm", stroke_width=2)
            scratch.rounded_rectangle((bbox[0]-7, bbox[1]-4, bbox[2]+7, bbox[3]+4), radius=5, fill=(255,255,255,225), outline="#8a9aa3", width=1)
            scratch.text((width*x, height*y), label, font=annotation_font, fill="#263746", anchor="mm")
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
