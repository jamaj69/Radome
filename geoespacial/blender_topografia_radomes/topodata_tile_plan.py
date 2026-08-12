"""Planejamento puro de blocos sobrepostos de uma folha TOPODATA."""


def starts(length, cells):
    """Inícios de blocos que compartilham a borda, sem lacunas."""
    if length < 2 or cells < 2:
        raise ValueError("Uma folha e um bloco precisam ter pelo menos duas células")
    return list(range(0, length - 1, cells))


def windows(width, height, cells):
    """Janelas [coluna, linha, largura, altura] com até ``cells`` quadrículas."""
    return [
        (column, row, min(cells + 1, width - column), min(cells + 1, height - row))
        for row in starts(height, cells)
        for column in starts(width, cells)
    ]
