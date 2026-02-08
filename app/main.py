"""Service-layer API for AI-augmented BI workflows (framework-agnostic)."""

from app.agents.forecasting_agent import forecast_linear
from app.agents.insight_agent import generate_insights
from app.agents.query_translation_agent import translate_nl_to_sql
from app.agents.report_narration_agent import narrate
from app.models.schemas import AuditEvent, QueryResult, UserContext
from app.services.governance import log_event
from app.services.query_executor import run_sql
from app.services.rls import apply_rls
from app.services.semantic_layer import get_metric


def health() -> dict:
    return {"status": "ok"}


def run_nl_query(question: str, context: UserContext) -> QueryResult:
    sql, sources, metrics, confidence = translate_nl_to_sql(question)
    safe_sql = apply_rls(sql, context)
    columns, rows = run_sql(safe_sql)
    log_event(
        AuditEvent(
            event_type="nl_query",
            user_id=context.user_id,
            role=context.role,
            prompt=question,
            sql=safe_sql,
            output=f"rows={len(rows)}",
            confidence=confidence,
        )
    )
    return QueryResult(
        sql=safe_sql,
        columns=columns,
        rows=rows,
        sources=sources,
        metrics_used=metrics,
        confidence=confidence,
    )


def generate_metric_insights(metric: str, period_days: int, context: UserContext) -> dict:
    get_metric(metric)
    sql = (
        "SELECT date, SUM(amount) AS value FROM sales "
        f"WHERE date >= date('now', '-{period_days} day') "
        "GROUP BY date ORDER BY date"
    )
    safe_sql = apply_rls(sql, context)
    _, rows = run_sql(safe_sql)
    return {"metric": metric, "insights": generate_insights(metric, rows), "evidence_query": safe_sql}


def forecast_metric(metric: str, horizon_days: int, context: UserContext) -> dict:
    get_metric(metric)
    sql = "SELECT date, SUM(amount) AS value FROM sales GROUP BY date ORDER BY date"
    safe_sql = apply_rls(sql, context)
    _, rows = run_sql(safe_sql)
    points, confidence = forecast_linear(rows, horizon_days)
    return {
        "metric": metric,
        "points": points,
        "method": "linear_trend_baseline",
        "confidence": confidence,
    }


def narrate_report(audience: str, title: str, facts: list[str], confidence: float) -> str:
    return narrate(audience, title, facts, confidence)


def record_feedback(query: str, accepted: bool, comment: str | None, context: UserContext) -> dict:
    log_event(
        AuditEvent(
            event_type="feedback",
            user_id=context.user_id,
            role=context.role,
            prompt=query,
            output=f"accepted={accepted}; comment={comment}",
            confidence=1.0,
        )
    )
    return {"status": "recorded"}
