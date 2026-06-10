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
    course = Course.objects.create(
        name="Introduction to Python",
        description="Learn the basics of Python programming",
        pub_date=datetime.now().date()
    )
    print(f"Created course: {course.name}")
    
    # Create lesson
    lesson = Lesson.objects.create(
        title="Python Basics",
        order=1,
        course=course,
        content="Learn about Python basics"
    )
    print(f"Created lesson: {lesson.title}")
    
    # Create question
    q = Question.objects.create(
        course=course,
        lesson=lesson,
        question_text="What is Python?",
        grade=1
    )
    print(f"Created question: {q.question_text}")
    
    # Create choices
    Choice.objects.create(question=q, choice_text="A programming language", is_correct=True)
    Choice.objects.create(question=q, choice_text="A snake", is_correct=False)
    print("Created choices")
    
    # Create user
    user = User.objects.create_user(username='testuser', password='testpass123')
    print(f"Created user: {user.username}")
    
    # Create enrollment
    Enrollment.objects.create(user=user, course=course)
    print("Created enrollment")
    
    print("\nDatabase populated successfully!")
