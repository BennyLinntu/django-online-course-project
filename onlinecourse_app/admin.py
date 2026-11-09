from django.contrib import admin

from .models import (
    Choice,
    Course,
    Enrollment,
    Instructor,
    Learner,
    Lesson,
    Question,
    ExamAttempt,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    ordering = ("order",)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "pub_date", "total_enrollment", "lesson_count")
    list_filter = ("pub_date",)
    search_fields = ("name", "description")
    inlines = [LessonInline]
    filter_horizontal = ("instructors",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "content")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "lesson", "grade")
    list_filter = ("course", "lesson")
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("choice_text",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "mode", "rating", "date_enrolled")
    list_filter = ("mode", "course")
    search_fields = ("user__username", "course__name")


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment",
        "score",
        "correct_count",
        "total_questions",
        "submitted_at",
    )
    list_filter = ("submitted_at",)
    readonly_fields = ("submitted_at",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation")
    list_filter = ("occupation",)
    search_fields = ("user__username",)


admin.site.site_header = "OnlineCourse administration"
admin.site.site_title = "OnlineCourse admin"
admin.site.index_title = "Manage courses, lessons and exams"
