import json
from pathlib import Path

from app.ai.client import openai_client


DATASET_PATH = (
    Path(__file__).parent
    / "data"
    / "classification_examples.json"
)


def load_dataset() -> list[dict]:
    with DATASET_PATH.open() as file:
        return json.load(file)


def run_eval() -> None:
    examples = load_dataset()

    total = len(examples)

    intent_correct = 0
    priority_correct = 0
    customer_lookup_correct = 0
    knowledge_search_correct = 0
    sentiment_correct = 0

    errors = []

    for example in examples:
        result = openai_client.classify_email(
            subject=example["subject"],
            body=example["body"],
        )

        expected_intent = example["expected_intent"]
        actual_intent = result.intent.value

        expected_priority = example["expected_priority"]
        actual_priority = result.priority.value

        expected_customer_lookup = (
            example["expected_customer_lookup"]
        )
        actual_customer_lookup = (
            result.requires_customer_lookup
        )

        expected_knowledge_search = (
            example["expected_knowledge_search"]
        )
        actual_knowledge_search = (
            result.requires_knowledge_search
        )

        expected_sentiment = example[
            "expected_sentiment"
        ]

        actual_sentiment = result.sentiment.value

        if actual_sentiment == expected_sentiment:
            sentiment_correct += 1

        if actual_intent == expected_intent:
            intent_correct += 1

        if actual_priority == expected_priority:
            priority_correct += 1

        if (
            actual_customer_lookup
            == expected_customer_lookup
        ):
            customer_lookup_correct += 1

        if (
            actual_knowledge_search
            == expected_knowledge_search
        ):
            knowledge_search_correct += 1

        if actual_intent != expected_intent:
            errors.append(
                {
                    "id": example["id"],
                    "subject": example["subject"],
                    "expected": expected_intent,
                    "actual": actual_intent,
                }
            )

        print(
            f"[{example['id']}] "
            f"{example['subject']} "
            f"→ {actual_intent}"
        )

    print()
    print("=== SupportFlow Classification Eval ===")
    print()
    print(f"Total: {total}")

    print(
        f"Intent accuracy: "
        f"{intent_correct}/{total} "
        f"({intent_correct / total:.1%})"
    )

    print(
        f"Priority accuracy: "
        f"{priority_correct}/{total} "
        f"({priority_correct / total:.1%})"
    )

    print(
        f"Customer lookup accuracy: "
        f"{customer_lookup_correct}/{total} "
        f"({customer_lookup_correct / total:.1%})"
    )

    print(
        f"Knowledge search accuracy: "
        f"{knowledge_search_correct}/{total} "
        f"({knowledge_search_correct / total:.1%})"
    )

    print(
        f"Sentiment accuracy: "
        f"{sentiment_correct}/{total} "
        f"({sentiment_correct / total:.1%})"
    )

    if errors:
        print()
        print("Intent errors:")

        for error in errors:
            print(
                f"#{error['id']} "
                f"{error['subject']} "
                f"| expected={error['expected']} "
                f"| actual={error['actual']}"
            )


if __name__ == "__main__":
    run_eval()