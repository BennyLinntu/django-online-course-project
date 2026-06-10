#!/usr/bin/env python
import os
import sys
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinecourse.settings')
    django.setup()

    from django.contrib.auth.models import User
    from onlinecourse_app.models import Course, Lesson, Question, Choice, Enrollment
    from datetime import datetime

    # Create course
    course, created = Course.objects.get_or_create(
        name="Introduction to Python",
        defaults={
            "description": "Learn the basics of Python programming",
            "pub_date": datetime.now().date()
        }
    )
    print(f"{'Created' if created else 'Found'} course: {course.name}")

    # Create lesson
    lesson, created = Lesson.objects.get_or_create(
        title="Python Basics",
        course=course,
        defaults={
            "order": 1,
            "content": "Learn about Python basics"
        }
    )
    print(f"{'Created' if created else 'Found'} lesson: {lesson.title}")

    # Create question
    q, created = Question.objects.get_or_create(
        course=course,
        lesson=lesson,
        question_text="What is Python?",
        defaults={"grade": 1}
    )
    print(f"{'Created' if created else 'Found'} question: {q.question_text}")

    # Create choices
    c1, _ = Choice.objects.get_or_create(
        question=q, choice_text="A programming language", defaults={"is_correct": True})
    c2, _ = Choice.objects.get_or_create(
        question=q, choice_text="A snake", defaults={"is_correct": False})
    print("Choices set up")

    # Create user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    print(f"{'Created' if created else 'Found'} user: {user.username}")

    # Create enrollment
    Enrollment.objects.create(user=user, course=course)
    print("Created enrollment")

    print("\nDatabase populated successfully!")
