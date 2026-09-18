from typing import Dict, List


def analyze_environment(
    soil_organic_carbon: float | None = None,
    soil_ph: float | None = None,
    soil_moisture: float | None = None,
    biodiversity: float | None = None,
    water_availability: float | None = None,
    land_use: str | None = None,
    pollution: float | None = None,
    temperature: float | None = None,
    rainfall: float | None = None,
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
        # Climate stress and biodiversity
    if (
        temperature is not None
        and biodiversity is not None
        and temperature >= 30
        and biodiversity < 50
    ):
        findings.append({
            "relationship": "temperature_biodiversity",
            "variables": [
                "temperature",
                "biodiversity"
            ],
            "observation": (
                "Higher temperature conditions combined with "
                "low biodiversity may indicate increased climate "
                "stress on species and ecosystems."
            )
        })

        recommendations.append({
            "action": (
                "Increase native vegetation, shade cover, and "
                "habitat refuges to reduce heat stress."
            ),
            "reasoning": (
                "Vegetation can provide cooler microhabitats and "
                "refuge conditions, while maintaining habitat quality "
                "can support species under climate stress."
            ),
            "metrics_impacted": [
                "temperature",
                "biodiversity",
                "species distribution",
                "ecosystem functioning"
            ],
            "time_horizon": "short-to-medium-term"
        })

    # Rainfall + water availability + biodiversity
    if (
        rainfall is not None
        and water_availability is not None
        and biodiversity is not None
        and rainfall < 500
        and water_availability < 40
        and biodiversity < 50
    ):
        findings.append({
            "relationship": "rainfall_water_biodiversity",
            "variables": [
                "rainfall",
                "water availability",
                "biodiversity"
            ],
            "observation": (
                "Low rainfall and low water availability combined "
                "with low biodiversity may indicate drought-related "
                "ecological stress."
            )
        })

        recommendations.append({
            "action": (
                "Improve landscape water retention and maintain "
                "ecological water availability during dry periods."
            ),
            "reasoning": (
                "Maintaining water availability can reduce drought "
                "stress and support vegetation productivity and "
                "species survival."
            ),
            "metrics_impacted": [
                "rainfall",
                "water availability",
                "species survival",
                "ecosystem functioning"
            ],
            "time_horizon": "short-to-medium-term"
        })

    return {
        "findings": findings,
        "recommendations": recommendations
    }