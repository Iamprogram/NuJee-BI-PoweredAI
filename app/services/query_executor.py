from app.database import get_connection


def run_sql(sql: str) -> tuple[list[str], list[dict]]:
    with get_connection() as conn:
        cur = conn.execute(sql)
        columns = [c[0] for c in cur.description]
        rows = [dict(r) for r in cur.fetchall()]
    return columns, rows
