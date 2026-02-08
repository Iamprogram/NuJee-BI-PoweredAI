from statistics import mean

from app.models.schemas import InsightItem


def generate_insights(metric: str, rows: list[dict]) -> list[InsightItem]:
    if len(rows) < 3:
        return [
            InsightItem(
                type="trend",
                title=f"Insufficient data for {metric}",
                description="Need at least 3 data points for trend analysis.",
                confidence=0.5,
            )
        ]

    values = [float(r["value"]) for r in rows]
    avg = mean(values)
    last = values[-1]
    prev = values[-2]

    trend = "upward" if last >= prev else "downward"
    trend_item = InsightItem(
        type="trend",
        title=f"{metric.title()} shows {trend} trend",
        description=f"Latest value {last:.2f} vs previous {prev:.2f}.",
        confidence=0.76,
    )

    anomaly_items = []
    if abs(last - avg) > max(avg * 0.2, 1):
        anomaly_items.append(
            InsightItem(
                type="anomaly",
                title=f"Potential anomaly in {metric}",
                description=f"Latest value deviates from mean ({avg:.2f}) by more than 20%.",
                confidence=0.72,
            )
        )

    return [trend_item, *anomaly_items]
