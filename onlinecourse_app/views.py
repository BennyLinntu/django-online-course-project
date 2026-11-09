from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Choice, Course, Enrollment, Lesson, Question, ExamAttempt


def course_list(request):
    """Public catalogue of available courses."""
    query = request.GET.get("q", "").strip()
    courses = Course.objects.annotate(
        lesson_total=Count("lessons", distinct=True),
        learner_total=Count("enrollments", distinct=True),
    ).prefetch_related("instructors__user")

    if query:
        courses = courses.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(
        request,
        "onlinecourse_app/course_list.html",
        {
            "courses": courses,
            "search_query": query,
            "total_courses": Course.objects.count(),
            "total_lessons": Lesson.objects.count(),
            "total_learners": Enrollment.objects.values("user").distinct().count(),
        },
    )


@login_required
def course_details(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.order_by("order", "id")),
            Prefetch(
                "questions",
                queryset=Question.objects.select_related("lesson").prefetch_related(
                    "choices"
                ),
            ),
        ),
        pk=course_id,
    )
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course, defaults={"mode": Enrollment.AUDIT}
    )
    if created:
        course.total_enrollment = course.enrollments.count()
        course.save(update_fields=["total_enrollment"])

    latest_attempt = (
        ExamAttempt.objects.filter(enrollment=enrollment)
        .prefetch_related("choices")
        .first()
    )

    return render(
        request,
        "onlinecourse_app/course_details.html",
        {
            "course": course,
            "enrollment": enrollment,
            "latest_attempt": latest_attempt,
            "question_count": course.questions.count(),
            "total_points": sum(
                question.grade for question in course.questions.all()
            ),
        },
    )


@login_required
@require_POST
def submit(request, course_id):
    """Grade one attempt and persist every selected answer."""
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(
        user=request.user, course=course
    ).first()
    if enrollment is None:
        messages.error(request, "You need to open the course before taking the exam.")
        return redirect("course_details", course_id=course.id)

    questions = list(
        Question.objects.filter(course=course)
        .select_related("lesson")
        .prefetch_related("choices")
        .order_by("lesson__order", "id")
    )
    if not questions:
        messages.info(request, "This course does not have an exam yet.")
        return redirect("course_details", course_id=course.id)

    selected_choices = []
    correct_count = 0
    total_points = 0
    earned_points = 0
    unanswered = 0

    for question in questions:
        total_points += question.grade
        raw = request.POST.get(f"question_{question.id}")
        choice = None
        if raw:
            choice = next(
                (item for item in question.choices.all() if str(item.id) == raw),
                None,
            )
        if choice is None:
            unanswered += 1
            continue

        selected_choices.append(choice)
        if choice.is_correct:
            correct_count += 1
            earned_points += question.grade

    attempt = ExamAttempt.objects.create(
        enrollment=enrollment,
        score=round((earned_points / total_points) * 100, 2) if total_points else 0,
        correct_count=correct_count,
        total_questions=len(questions),
    )
    attempt.choices.set(selected_choices)

    if unanswered:
        messages.warning(
            request,
            f"{unanswered} question{'s' if unanswered != 1 else ''} left unanswered.",
        )

    return HttpResponseRedirect(reverse("show_exam_result", args=[course.id]))


@login_required
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(
        user=request.user, course=course
    ).first()
    if enrollment is None:
        raise Http404("You are not enrolled in this course.")

    attempt = (
        ExamAttempt.objects.filter(enrollment=enrollment)
        .prefetch_related("choices")
        .first()
    )
    if attempt is None:
        messages.info(request, "Take the exam to see your result.")
        return redirect("course_details", course_id=course.id)

    questions = list(
        Question.objects.filter(course=course)
        .select_related("lesson")
        .prefetch_related("choices")
        .order_by("lesson__order", "id")
    )
    selected_by_question = {
        choice.question_id: choice for choice in attempt.choices.all()
    }
    result_details = []

    for question in questions:
        selected = selected_by_question.get(question.id)
        correct_choice = next(
            (choice for choice in question.choices.all() if choice.is_correct),
            None,
        )
        result_details.append(
            {
                "question": question,
                "selected": selected,
                "correct_choice": correct_choice,
                "is_correct": bool(selected and selected.is_correct),
                "points": question.grade if selected and selected.is_correct else 0,
            }
        )

    return render(
        request,
        "onlinecourse_app/exam_result.html",
        {
            "course": course,
            "enrollment": enrollment,
            "attempt": attempt,
            "result_details": result_details,
            "passed": attempt.score >= 70,
            "earned_points": sum(item["points"] for item in result_details),
            "total_points": sum(question.grade for question in questions),
        },
    )
