from typing import Dict, List


def analyze_environment(
    soil_organic_carbon: float | None = None,
    soil_ph: float | None = None,
    soil_moisture: float | None = None,
    biodiversity: float | None = None,
    water_availability: float | None = None,
    land_use: str | None = None,
    pollution: float | None = None,
) -> Dict:
    """
    Multi-metric environmental reasoning layer.

    The engine connects environmental variables rather than
    generating recommendations from a single metric.
    """

    findings: List[Dict] = []
    recommendations: List[Dict] = []

    # Soil carbon + biodiversity
    if (
        soil_organic_carbon is not None
        and biodiversity is not None
    ):
        if soil_organic_carbon < 2 and biodiversity < 40:
            findings.append({
                "relationship": "soil_health_biodiversity",
                "variables": [
                    "soil organic carbon",
                    "biodiversity"
                ],
                "observation": (
                    "Low soil organic carbon combined with low "
                    "biodiversity indicates a potential soil-habitat "
                    "degradation pattern."
                )
            })

            recommendations.append({
                "action": "Introduce diverse cover crops and retain organic residues.",
                "reasoning": (
                    "Increasing organic inputs can support soil "
                    "organic carbon while vegetation diversity can "
                    "provide additional habitat and resources."
                ),
                "metrics_impacted": [
                    "soil organic carbon",
                    "soil structure",
                    "habitat diversity",
                    "species richness"
                ],
                "time_horizon": "medium-term"
            })

    # Water + biodiversity
    if (
        water_availability is not None
        and biodiversity is not None
    ):
        if water_availability < 40 and biodiversity < 50:
            findings.append({
                "relationship": "water_biodiversity",
                "variables": [
                    "water availability",
                    "biodiversity"
                ],
                "observation": (
                    "Low water availability may constrain "
                    "vegetation productivity and species survival."
                )
            })

            recommendations.append({
                "action": (
                    "Restore natural water retention features and "
                    "maintain ecological water availability."
                ),
                "reasoning": (
                    "Improving water availability can reduce "
                    "water-related ecological stress and support "
                    "vegetation and species survival."
                ),
                "metrics_impacted": [
                    "water availability",
                    "vegetation productivity",
                    "species survival"
                ],
                "time_horizon": "short-to-medium-term"
            })

    # Land use + biodiversity + soil
    if (
        land_use is not None
        and biodiversity is not None
        and soil_organic_carbon is not None
    ):
        agricultural_land = land_use.lower() in [
            "cropland",
            "agriculture",
            "farmland",
            "monoculture"
        ]

        if agricultural_land:
            findings.append({
                "relationship": "land_use_soil_biodiversity",
                "variables": [
                    "land use",
                    "soil organic carbon",
                    "biodiversity"
                ],
                "observation": (
                    "Simplified agricultural land use can reduce "
                    "habitat diversity while intensive management "
                    "may also affect soil condition."
                )
            })

            recommendations.append({
                "action": (
                    "Integrate trees, hedgerows, or habitat strips "
                    "into agricultural areas."
                ),
                "reasoning": (
                    "Increasing vegetation structure can provide "
                    "habitat while improving landscape connectivity "
                    "and potentially supporting soil protection."
                ),
                "metrics_impacted": [
                    "habitat connectivity",
                    "biodiversity",
                    "soil organic carbon"
                ],
                "time_horizon": "medium-to-long-term"
            })

    # Pollution + biodiversity
    if (
        pollution is not None
        and biodiversity is not None
    ):
        if pollution > 60 and biodiversity < 50:
            findings.append({
                "relationship": "pollution_biodiversity",
                "variables": [
                    "pollution",
                    "biodiversity"
                ],
                "observation": (
                    "Elevated pollution together with low biodiversity "
                    "suggests increased ecological stress."
                )
            })

            recommendations.append({
                "action": (
                    "Identify and reduce major local pollution sources "
                    "and establish vegetated buffer zones where appropriate."
                ),
                "reasoning": (
                    "Reducing pollutant exposure can decrease ecological "
                    "stress on sensitive organisms."
                ),
                "metrics_impacted": [
                    "pollution",
                    "species survival",
                    "ecosystem health"
                ],
                "time_horizon": "short-to-medium-term"
            })

    return {
        "findings": findings,
        "recommendations": recommendations
    }