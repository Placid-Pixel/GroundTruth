from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from backend.semantic_retriever import retriever
from backend.reasoning import analyze_environment
from backend.recommendation import ground_recommendations
from backend.input_validator import detect_missing_data


class GroundTruthState(TypedDict, total=False):
    query: str
    environment: Any
    missing_data: dict
    evidence: list
    analysis: dict
    recommendations: list
    response: dict


def parse_input(state: GroundTruthState):
    return {
        "query": state.get("query", "").strip(),
        "environment": state.get("environment")
    }


def check_missing_data(state: GroundTruthState):
    result = detect_missing_data(
        state.get("environment")
    )

    return {
        "missing_data": result
    }


def route_after_validation(state: GroundTruthState):
    if state["missing_data"]["missing"]:
        return "missing"

    return "retrieve"


def retrieve_evidence(state: GroundTruthState):
    evidence = retriever.retrieve(
        state["query"],
        top_k=5
    )

    return {
        "evidence": evidence
    }


def multi_metric_analysis(state: GroundTruthState):
    environment = state["environment"]

    def get_value(field):
        if isinstance(environment, dict):
            return environment.get(field)
        return getattr(environment, field, None)

    analysis = analyze_environment(
        soil_organic_carbon=get_value("soil_organic_carbon"),
        soil_ph=get_value("soil_ph"),
        soil_moisture=get_value("soil_moisture"),
        biodiversity=get_value("biodiversity"),
        water_availability=get_value("water_availability"),
        land_use=get_value("land_use"),
        pollution=get_value("pollution"),
    )

    return {
        "analysis": analysis
    }


def generate_recommendations(state: GroundTruthState):
    grounded = ground_recommendations(
        state["analysis"]["recommendations"],
        state["evidence"]
    )

    return {
        "recommendations": grounded
    }


def validate_evidence(state: GroundTruthState):
    valid_recommendations = []

    for recommendation in state["recommendations"]:

        # Keep recommendations only when
        # scientific evidence was actually retrieved.
        if recommendation.get("evidence"):
            valid_recommendations.append(recommendation)

    return {
        "recommendations": valid_recommendations,
        "response": {
            "query": state["query"],
            "findings": state["analysis"]["findings"],
            "recommendations": valid_recommendations
        }
    }


def ask_for_information(state: GroundTruthState):
    return {
        "response": {
            "query": state["query"],
            "missing_data": state["missing_data"],
            "message": state["missing_data"]["message"],
            "recommendations": []
        }
    }


workflow = StateGraph(GroundTruthState)

workflow.add_node("parse_input", parse_input)
workflow.add_node("check_missing_data", check_missing_data)
workflow.add_node("retrieve_evidence", retrieve_evidence)
workflow.add_node("multi_metric_analysis", multi_metric_analysis)
workflow.add_node("generate_recommendations", generate_recommendations)
workflow.add_node("validate_evidence", validate_evidence)
workflow.add_node("ask_for_information", ask_for_information)

workflow.add_edge(START, "parse_input")
workflow.add_edge("parse_input", "check_missing_data")

workflow.add_conditional_edges(
    "check_missing_data",
    route_after_validation,
    {
        "missing": "ask_for_information",
        "retrieve": "retrieve_evidence"
    }
)

workflow.add_edge(
    "retrieve_evidence",
    "multi_metric_analysis"
)

workflow.add_edge(
    "multi_metric_analysis",
    "generate_recommendations"
)

workflow.add_edge(
    "generate_recommendations",
    "validate_evidence"
)

workflow.add_edge(
    "validate_evidence",
    END
)

workflow.add_edge(
    "ask_for_information",
    END
)

groundtruth_graph = workflow.compile()