from django.contrib import admin
from django.contrib.admin import (
    ModelAdmin,
    StackedInline,
    TabularInline,
    AdminSite,
    site,
    register,
    SimpleListFilter,
)
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment


class LessonInline(StackedInline):
    model = Lesson
    extra = 5


class QuestionInline(StackedInline):
    model = Question
    extra = 5


class ChoiceInline(StackedInline):
    model = Choice
    extra = 5


class CourseAdmin(ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class LessonAdmin(ModelAdmin):
    list_display = ['title']
    inlines = [QuestionInline]


class QuestionAdmin(ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
