from typing import Dict


def detect_missing_data(environment) -> Dict:
    """
    Determine whether enough environmental information is available
    for meaningful multi-metric reasoning.
    """

    if environment is None:
        return {
            "missing": True,
            "missing_fields": [
                "biodiversity",
                "soil_organic_carbon",
                "water_availability",
                "land_use"
            ],
            "message": (
                "To provide a grounded environmental recommendation, "
                "please provide at least biodiversity, soil organic "
                "carbon, water availability, or land-use information."
            )
        }

    fields = [
        "soil_organic_carbon",
        "soil_ph",
        "soil_moisture",
        "biodiversity",
        "water_availability",
        "land_use",
        "pollution"
    ]

    available = []

    for field in fields:
        if isinstance(environment, dict):
            value = environment.get(field)
        else:
            value = getattr(environment, field, None)

        if value is not None:
            available.append(field)

    if len(available) < 2:
        missing = [
            field for field in fields
            if field not in available
        ][:3]

        return {
            "missing": True,
            "missing_fields": missing,
            "available_fields": available,
            "message": (
                "I need at least two environmental variables "
                "to perform multi-metric reasoning. Please provide "
                "additional soil, biodiversity, water, land-use, "
                "or pollution information."
            )
        }

    return {
        "missing": False,
        "missing_fields": [],
        "available_fields": available,
        "message": "Sufficient environmental information available."
    }