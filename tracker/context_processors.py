"""Context processors so base template always has streak_days."""
from .firebase import get_streak


def streak(request):
    data = get_streak()
    return {"streak_days": data.get("streak_days", 0)}
