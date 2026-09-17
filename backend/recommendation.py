from typing import Dict, List


def ground_recommendations(
    recommendations: List[Dict],
    evidence: List[Dict]
) -> List[Dict]:
    """
    Attach retrieved scientific evidence to recommendations.

    Evidence is selected by overlap between recommendation metrics
    and metrics contained in retrieved documents.
    """

    grounded = []

    for recommendation in recommendations:

        recommendation_metrics = set(
            recommendation.get("metrics_impacted", [])
        )

        matching_evidence = []

        for document in evidence:
            document_metrics = set(
                document.get("metrics", [])
            )

            overlap = recommendation_metrics.intersection(
                document_metrics
            )

            if overlap:
                matching_evidence.append({
                    "id": document.get("id"),
                    "source": document.get("source"),
                    "year": document.get("year"),
                    "title": document.get("title"),
                    "supporting_metrics": list(overlap),
                    "similarity_score": document.get(
                        "similarity_score"
                    )
                })

        grounded.append({
            **recommendation,
            "evidence": matching_evidence
        })

    return grounded
