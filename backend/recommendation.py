from typing import Dict, List


def calculate_evidence_strength(
    overlap_count: int,
    recommendation_metric_count: int
) -> str:
    """
    Classify evidence based on how much of the recommendation's
    impacted metrics are supported by the retrieved document.
    """

    if recommendation_metric_count == 0:
        return "insufficient"

    coverage = overlap_count / recommendation_metric_count

    if coverage >= 0.5:
        return "direct"
    elif coverage > 0:
        return "related"
    else:
        return "insufficient"


def ground_recommendations(
    recommendations: List[Dict],
    evidence: List[Dict]
) -> List[Dict]:
    """
    Attach scientifically relevant evidence to each recommendation.

    Evidence ranking combines:
    1. Metric overlap
    2. Semantic similarity

    Evidence strength:
    - direct: supports at least 50% of recommendation metrics
    - related: supports at least one metric
    - insufficient: supports none
    """

    grounded = []

    for recommendation in recommendations:

        recommendation_metrics = set(
            recommendation.get("metrics_impacted", [])
        )

        scored_evidence = []

        for document in evidence:

            document_metrics = set(
                document.get("metrics", [])
            )

            overlap = recommendation_metrics.intersection(
                document_metrics
            )

            # Ignore documents that have no relationship
            # with the recommendation.
            if not overlap:
                continue

            similarity = document.get(
                "similarity_score",
                0.0
            ) or 0.0

            # Normalize metric overlap to 0-1.
            metric_overlap_score = (
                len(overlap) / len(recommendation_metrics)
                if recommendation_metrics
                else 0.0
            )

            # Final evidence score is normalized to approximately 0-1.
            combined_score = (
                metric_overlap_score * 0.7
                + similarity * 0.3
            )

            evidence_strength = calculate_evidence_strength(
                len(overlap),
                len(recommendation_metrics)
            )

            scored_evidence.append({
                "id": document.get("id"),
                "source": document.get("source"),
                "year": document.get("year"),
                "title": document.get("title"),
                "document_type": document.get("document_type"),
                "source_url": document.get("source_url"),
                "supporting_metrics": sorted(overlap),
                "similarity_score": round(
                    similarity,
                    4
                ),
                "evidence_score": round(
                    combined_score,
                    4
                ),
                "evidence_strength": evidence_strength
            })

        # Strongest evidence first.
        scored_evidence.sort(
            key=lambda item: item["evidence_score"],
            reverse=True
        )

        grounded.append({
            **recommendation,
            "evidence": scored_evidence[:3]
        })

    return grounded