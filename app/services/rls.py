from app.models.schemas import UserContext


def apply_rls(sql: str, context: UserContext) -> str:
    if context.role == "executive" or not context.region:
        return sql
    if " where " in sql.lower():
        return f"{sql} AND region = '{context.region}'"
    return f"{sql} WHERE region = '{context.region}'"
