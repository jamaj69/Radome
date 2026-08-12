"""Geometria pura da cena regional TOPODATA de baixa resolução."""
import math


def regional_bounds(sites, margin_degrees):
    """Retorna a caixa geográfica dos sítios, expandida por uma margem."""
    if not sites:
        raise ValueError("A seleção regional não contém sítios")
    if margin_degrees < 0:
        raise ValueError("A margem não pode ser negativa")
    return (
        min(site["longitude"] for site in sites) - margin_degrees,
        min(site["latitude"] for site in sites) - margin_degrees,
        max(site["longitude"] for site in sites) + margin_degrees,
        max(site["latitude"] for site in sites) + margin_degrees,
    )


def axis(start, stop, spacing):
    """Amostras regulares que incluem exatamente as duas extremidades."""
    if spacing <= 0 or stop <= start:
        raise ValueError("Extensão e espaçamento regionais inválidos")
    count = math.ceil((stop - start) / spacing)
    return [start + (stop - start) * index / count for index in range(count + 1)]


def grid_shape(bounds, spacing):
    west, south, east, north = bounds
    return axis(west, east, spacing), axis(south, north, spacing)
