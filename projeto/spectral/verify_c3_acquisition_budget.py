#!/usr/bin/env python3
"""Calculate screening data rates and radio-horizon checks for C3."""

from dataclasses import dataclass
from math import sqrt


BITS_PER_BYTE = 8
EFFECTIVE_EARTH_HORIZON_FACTOR_KM = 4.12


@dataclass(frozen=True)
class CapturePath:
    name: str
    channels_per_node: int
    sample_rate_msps: float
    bits_per_i_or_q: int
    capture_seconds: float

    @property
    def data_rate_mbps_per_node(self) -> float:
        bits_per_complex_sample = 2 * self.bits_per_i_or_q
        return self.channels_per_node * self.sample_rate_msps * bits_per_complex_sample

    @property
    def capture_gb_per_node(self) -> float:
        return self.data_rate_mbps_per_node * self.capture_seconds / BITS_PER_BYTE / 1000


def radio_horizon_km(height_m: float) -> float:
    return EFFECTIVE_EARTH_HORIZON_FACTOR_KM * sqrt(height_m)


def mutual_horizon_km(first_height_m: float, second_height_m: float) -> float:
    return radio_horizon_km(first_height_m) + radio_horizon_km(second_height_m)


def main() -> None:
    node_count = 3
    paths = (
        CapturePath("UAT + 1090ES direct", 2, 8.0, 16, 10.0),
        CapturePath("Known UHF transmitter", 1, 25.0, 16, 10.0),
        CapturePath("UHF bistatic reference + surveillance", 2, 25.0, 16, 10.0),
    )

    print("C3 acquisition screening budget")
    print("Values are proposed capture baselines, not hardware performance claims.\n")
    for path in paths:
        network_gb = path.capture_gb_per_node * node_count
        print(
            f"{path.name}: {path.data_rate_mbps_per_node:.0f} Mbit/s/node, "
            f"{path.capture_gb_per_node:.2f} GB/node/capture, "
            f"{network_gb:.2f} GB/{node_count}-node capture"
        )

    station_height_m = 1000.0
    aircraft_height_m = 10000.0
    baseline_km = 100.0
    horizon_km = mutual_horizon_km(station_height_m, aircraft_height_m)
    print(
        f"\nScreening radio horizon at {station_height_m:.0f} m station and "
        f"{aircraft_height_m:.0f} m aircraft: {horizon_km:.1f} km"
    )
    print(f"Nominal {baseline_km:.0f} km baseline is geometrically screenable: {horizon_km >= baseline_km}")
    print("Terrain, antenna pattern, link margin, GDOP and regulation remain mandatory site-specific gates.")
    print("NF, IP3 and usable dynamic range remain unassigned until measured RFI and cascade budgets exist.")

    assert paths[0].data_rate_mbps_per_node == 512.0
    assert paths[2].capture_gb_per_node == 2.0
    assert horizon_km >= baseline_km


if __name__ == "__main__":
    main()