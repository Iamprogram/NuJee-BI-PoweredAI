def narrate(audience: str, title: str, facts: list[str], confidence: float) -> str:
    tone = {
        "executive": "executive summary",
        "analyst": "analyst-level explanation",
        "operator": "operational recommendation",
    }.get(audience, "summary")

    bullets = " ".join(f"- {f}" for f in facts)
    return (
        f"{title}: This {tone} highlights key outcomes. {bullets} "
        f"Model confidence is {confidence:.0%}; validate before high-impact decisions."
    )
