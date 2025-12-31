def generate_audit_explanation(transaction_id, shap_values, feature_names):
    explanations = []

    # Pair feature with SHAP value
    contributions = list(zip(feature_names, shap_values))

    # Sort by absolute impact (most important first)
    contributions.sort(key=lambda x: abs(x[1]), reverse=True)

    for feature, value in contributions[:3]:  # Top 3 reasons only
        if feature == "amount_zscore":
            explanations.append(
                "The transaction amount significantly deviates from normal spending patterns."
            )

        elif feature == "vendor_txn_count":
            explanations.append(
                "The vendor has an unusually high number of transactions compared to historical behavior."
            )

        elif feature == "department_txn_count":
            explanations.append(
                "The department shows higher-than-normal transaction activity, indicating possible budget pressure."
            )

        elif feature == "day":
            explanations.append(
                "The transaction occurred close to the end of the month, a period often associated with rushed expenditures."
            )

        elif feature == "weekday":
            explanations.append(
                "The transaction timing deviates from typical working-day spending patterns."
            )

        elif feature == "month":
            explanations.append(
                "The transaction occurred during an unusual time period compared to historical data."
            )

    if not explanations:
        explanations.append(
            "The transaction shows anomalous behavior when compared with historical spending data."
        )

    return {
        "transaction_id": transaction_id,
        "audit_explanation": explanations
    }
