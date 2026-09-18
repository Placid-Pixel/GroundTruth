from backend.reasoning import analyze_environment


def test_water_biodiversity_relationship():
    result = analyze_environment(
        water_availability=30,
        biodiversity=25
    )

    relationships = [
        finding["relationship"]
        for finding in result["findings"]
    ]

    assert "water_biodiversity" in relationships


def test_temperature_biodiversity_relationship():
    result = analyze_environment(
        temperature=32,
        biodiversity=25
    )

    relationships = [
        finding["relationship"]
        for finding in result["findings"]
    ]

    assert "temperature_biodiversity" in relationships


def test_rainfall_water_biodiversity_relationship():
    result = analyze_environment(
        rainfall=400,
        water_availability=30,
        biodiversity=25
    )

    relationships = [
        finding["relationship"]
        for finding in result["findings"]
    ]

    assert "rainfall_water_biodiversity" in relationships


def test_multi_metric_reasoning():
    result = analyze_environment(
        temperature=32,
        rainfall=400,
        water_availability=30,
        biodiversity=25
    )

    assert len(result["findings"]) >= 3
    assert len(result["recommendations"]) >= 3


def test_healthy_environment_has_fewer_stress_findings():
    result = analyze_environment(
        temperature=22,
        rainfall=900,
        water_availability=80,
        biodiversity=75,
        soil_organic_carbon=3.0,
        soil_ph=6.8,
        soil_moisture=50
    )

    assert len(result["findings"]) == 0