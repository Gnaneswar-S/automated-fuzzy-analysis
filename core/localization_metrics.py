def calculate_localization_metrics(results):
    """
    Calculates Precision, Recall, and F1
    for top-1 defective-rule localization.
    """

    true_positive = 0
    false_positive = 0
    false_negative = 0

    for result in results:
        evaluation = result["evaluation"]

        actual_rule = (
            evaluation["ground_truth"]["target_rule"]
        )

        predicted_rule = (
            evaluation["prediction"]["localized_rule"]
        )

        if predicted_rule == actual_rule:
            true_positive += 1
        else:
            false_positive += 1
            false_negative += 1

    precision = (
        true_positive /
        (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else 0.0
    )

    recall = (
        true_positive /
        (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else 0.0
    )

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = (
            2 * precision * recall
            / (precision + recall)
        )

    return {
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": round(precision * 100, 2),
        "recall": round(recall * 100, 2),
        "f1_score": round(f1 * 100, 2)
    }