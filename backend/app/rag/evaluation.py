"""RAG evaluation helpers using RAGAS metrics."""

from __future__ import annotations

from app.rag.types import EvaluationRecord


class RAGEvaluator:
    """Evaluate generated answers with a small set of RAGAS metrics."""

    def evaluate(self, records: list[EvaluationRecord]) -> dict[str, float]:
        """Run RAGAS on prepared evaluation records."""
        if not records:
            return {}

        try:
            from datasets import Dataset
            from ragas import evaluate
            from ragas.metrics import answer_relevancy, context_recall, faithfulness
        except ImportError:
            return {"error": "ragas/datasets not installed"}

        dataset = Dataset.from_dict(
            {
                "question": [record.question for record in records],
                "answer": [record.answer for record in records],
                "contexts": [record.contexts for record in records],
                "ground_truth": [record.ground_truth for record in records],
            }
        )
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_recall],
        )
        return {key: float(value) for key, value in result.items()}

