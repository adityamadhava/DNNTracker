"""Context processors so base template always has streak_days."""


def streak(request):
    try:
        from .firebase import get_streak
        data = get_streak()
        return {"streak_days": data.get("streak_days", 0)}
    except Exception:
        return {"streak_days": 0}
