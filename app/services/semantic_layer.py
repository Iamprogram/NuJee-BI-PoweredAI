SEMANTIC_METRICS = {
    "revenue": {
        "expression": "SUM(amount)",
        "table": "sales",
        "grain": "day",
        "description": "Total sales revenue",
    },
    "orders": {
        "expression": "COUNT(*)",
        "table": "sales",
        "grain": "day",
        "description": "Order count",
    },
}


ALLOWED_DIMENSIONS = {"date", "region", "product"}


def get_metric(metric_name: str) -> dict:
    key = metric_name.lower().strip()
    if key not in SEMANTIC_METRICS:
        raise ValueError(f"Unknown metric: {metric_name}")
    return SEMANTIC_METRICS[key]
