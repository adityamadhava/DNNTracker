"""
Dashboard, update progress, add notes, and filters.
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from tracker.firebase import (
    get_all_topics,
    get_topic,
    update_topic,
    toggle_subtopic,
    get_streak,
    record_study_date,
)
from tracker.topics_data import DIFFICULTY_CHOICES
from datetime import datetime


def _topic_progress(topic):
    subtopics = topic.get("subtopics") or []
    completed = topic.get("completed_subtopics") or []
    total = len(subtopics)
    if total == 0:
        return 100
    return int(100 * len(completed) / total)


def _overall_progress(topics):
    if not topics:
        return 0
    total_sub = 0
    done_sub = 0
    for t in topics:
        subs = t.get("subtopics") or []
        completed = t.get("completed_subtopics") or []
        total_sub += len(subs)
        done_sub += len(completed)
    if total_sub == 0:
        return 0
    return int(100 * done_sub / total_sub)


def _filter_topics(topics, filter_type, difficulty_filter):
    if filter_type == "completed":
        return [t for t in topics if _topic_progress(t) == 100]
    if filter_type == "pending":
        return [t for t in topics if _topic_progress(t) < 100]
    if filter_type == "difficulty" and difficulty_filter:
        return [t for t in topics if (t.get("difficulty") or "").strip() == difficulty_filter]
    return topics


@require_GET
def dashboard(request):
    filter_type = request.GET.get("filter", "all")
    difficulty_filter = request.GET.get("difficulty", "")
    topics = get_all_topics()
    for t in topics:
        t["progress_pct"] = _topic_progress(t)
    filtered = _filter_topics(topics, filter_type, difficulty_filter)
    overall = _overall_progress(topics)
    streak_data = get_streak()
    context = {
        "topics": filtered,
        "all_topics": topics,
        "overall_progress": overall,
        "progress_ring_offset": 100 - overall,
        "streak_days": streak_data.get("streak_days", 0),
        "filter": filter_type,
        "difficulty_filter": difficulty_filter,
        "difficulty_choices": DIFFICULTY_CHOICES,
    }
    return render(request, "dashboard.html", context)


@require_GET
def topic_detail(request, topic_id):
    topic = get_topic(topic_id)
    if not topic:
        return render(request, "dashboard.html", {"error": "Topic not found"})
    topic["progress_pct"] = _topic_progress(topic)
    streak_data = get_streak()
    context = {
        "topic": topic,
        "streak_days": streak_data.get("streak_days", 0),
        "difficulty_choices": DIFFICULTY_CHOICES,
    }
    return render(request, "topic_detail.html", context)


@require_http_methods(["GET", "POST"])
def update_progress(request, topic_id):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "POST required"}, status=405)
    try:
        body = request.body
        if isinstance(body, bytes):
            import json
            data = json.loads(body.decode("utf-8")) if body else {}
        else:
            data = request.POST.dict() or {}
    except Exception:
        data = getattr(request, "POST", {}) or {}
    subtopic_index = data.get("subtopic_index")
    completed = data.get("completed")
    if subtopic_index is None or completed is None:
        # Allow form-style POST
        subtopic_index = request.POST.get("subtopic_index")
        completed = request.POST.get("completed")
    if subtopic_index is not None:
        try:
            subtopic_index = int(subtopic_index)
        except (TypeError, ValueError):
            return JsonResponse({"ok": False, "error": "Invalid subtopic_index"}, status=400)
    if completed is not None and str(completed).lower() not in ("true", "false", "1", "0"):
        completed = completed == 1 or str(completed).lower() == "true"
    else:
        completed = str(completed).lower() in ("true", "1")
    if subtopic_index is None:
        return JsonResponse({"ok": False, "error": "subtopic_index required"}, status=400)
    ok = toggle_subtopic(topic_id, subtopic_index, completed)
    if not ok:
        return JsonResponse({"ok": False, "error": "Update failed"}, status=400)
    topic = get_topic(topic_id)
    # Optionally record study date for streak when marking something complete
    if completed:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        record_study_date(today)
    progress_pct = _topic_progress(topic) if topic else 0
    return JsonResponse({"ok": True, "progress_pct": progress_pct})


@require_http_methods(["GET", "POST"])
def add_notes(request, topic_id):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "POST required"}, status=405)
    notes = request.POST.get("notes", "").strip()
    if request.content_type and "application/json" in request.content_type:
        try:
            import json
            data = json.loads(request.body.decode("utf-8"))
            notes = (data.get("notes") or "").strip()
        except Exception:
            pass
    ok = update_topic(topic_id, notes=notes)
    if not ok:
        return JsonResponse({"ok": False, "error": "Update failed"}, status=400)
    return JsonResponse({"ok": True})


@require_http_methods(["GET", "POST"])
def set_difficulty(request, topic_id):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "POST required"}, status=405)
    difficulty = request.POST.get("difficulty", "").strip()
    if request.content_type and "application/json" in request.content_type:
        try:
            import json
            data = json.loads(request.body.decode("utf-8"))
            difficulty = (data.get("difficulty") or "").strip()
        except Exception:
            pass
    if difficulty and difficulty not in DIFFICULTY_CHOICES:
        return JsonResponse({"ok": False, "error": "Invalid difficulty"}, status=400)
    ok = update_topic(topic_id, difficulty=difficulty)
    if not ok:
        return JsonResponse({"ok": False, "error": "Update failed"}, status=400)
    return JsonResponse({"ok": True})


@require_GET
def overall_progress_api(request):
    """JSON endpoint for overall progress (e.g. for header)."""
    topics = get_all_topics()
    overall = _overall_progress(topics)
    streak_data = get_streak()
    return JsonResponse({
        "overall_progress": overall,
        "streak_days": streak_data.get("streak_days", 0),
    })
