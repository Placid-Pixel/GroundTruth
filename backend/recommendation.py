from typing import Dict, List


def ground_recommendations(
    recommendations: List[Dict],
    evidence: List[Dict]
) -> List[Dict]:
    """
    Attach the strongest retrieved scientific evidence to each
    recommendation using metric overlap and semantic relevance.
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

            if not overlap:
                continue

            similarity = document.get(
                "similarity_score",
                0.0
            ) or 0.0

            # Stronger weight for metric overlap, while still
            # considering semantic retrieval similarity.
            metric_score = len(overlap)

            combined_score = (
                metric_score * 0.7
                + similarity * 0.3
            )

            scored_evidence.append({
                "id": document.get("id"),
                "source": document.get("source"),
                "year": document.get("year"),
                "title": document.get("title"),
                "supporting_metrics": list(overlap),
                "similarity_score": similarity,
                "evidence_score": round(
                    combined_score,
                    4
                )
            })

        # Strongest evidence first.
        scored_evidence.sort(
            key=lambda item: item["evidence_score"],
            reverse=True
        )

        # Keep only the strongest three pieces of evidence.
        grounded.append({
            **recommendation,
            "evidence": scored_evidence[:3]
        })

    return grounded