import json

import settings as cfg


def load_best_score():
    try:
        with cfg.SAVE_FILE.open("r", encoding="utf-8") as save_file:
            data = json.load(save_file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return 0

    best_score = data.get("best_score", 0)
    if isinstance(best_score, int) and best_score >= 0:
        return best_score
    return 0


def save_best_score(best_score):
    cfg.SAVE_FILE.write_text(
        json.dumps({"best_score": best_score}, indent=2),
        encoding="utf-8",
    )
