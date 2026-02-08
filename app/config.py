from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    db_path: str = "data/bi.db"
    confidence_threshold: float = 0.55


settings = Settings()
