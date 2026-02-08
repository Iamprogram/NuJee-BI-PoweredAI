from app.services.semantic_layer import get_metric


def translate_nl_to_sql(question: str) -> tuple[str, list[str], list[str], float]:
    q = question.lower()
    metric = "revenue" if "revenue" in q or "sales" in q else "orders"
    metric_cfg = get_metric(metric)

    if "last week" in q:
        date_filter = "date >= date('now', '-7 day')"
        confidence = 0.78
    elif "last month" in q:
        date_filter = "date >= date('now', '-30 day')"
        confidence = 0.74
    else:
        date_filter = "date >= date('now', '-14 day')"
        confidence = 0.6

    sql = (
        f"SELECT date, {metric_cfg['expression']} AS value "
        f"FROM {metric_cfg['table']} "
        f"WHERE {date_filter} GROUP BY date ORDER BY date"
    )
    return sql, [metric_cfg["table"]], [metric], confidence
