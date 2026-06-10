#!/usr/bin/env python
"""
Test the complete exam workflow to verify views and urls are working correctly
"""
from onlinecourse_app.models import Course, Lesson, Question, Choice, Enrollment
from django.test import Client
from django.contrib.auth.models import User
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinecourse.settings')
django.setup()


def test_workflow():
    """Test the complete workflow"""
    print("=" * 60)
    print("TESTING EXAM WORKFLOW")
    print("=" * 60)

    # Get test user
    try:
        testuser = User.objects.get(username='testuser')
        print(f"✓ Test user found: {testuser.username}")
    except User.DoesNotExist:
        print("✗ Test user not found!")
        return False

    # Get course
    try:
        course = Course.objects.get(pk=1)
        print(f"✓ Course found: {course.name}")
    except Course.DoesNotExist:
        print("✗ Course not found!")
        return False

    # Check enrollment
    try:
        enrollment = Enrollment.objects.get(user=testuser, course=course)
        print(f"✓ Enrollment found for {testuser.username} in {course.name}")
    except Enrollment.DoesNotExist:
        print("✗ No enrollment found for user in course!")
        return False

    # Check questions
    questions = Question.objects.filter(course=course)
    print(f"✓ Found {questions.count()} questions in course")

    # Check choices
    for question in questions:
        choices = question.choice_set.all()
        print(f"  - Question {question.id}: {question.question_text}")
        for choice in choices:
            print(
                f"    - Choice: {choice.choice_text} (Correct: {choice.is_correct})")

    # Test client
    client = Client()

    # Test login
    print("\n" + "=" * 60)
    print("TESTING VIEWS AND URLS")
    print("=" * 60)

    # Test course_details view
    print("\n1. Testing course_details view...")
    client.login(username='testuser', password='testpass123')
    response = client.get(f'/onlinecourse/course/{course.id}/')
    if response.status_code == 200:
        print(
            f"✓ course_details view accessible (status: {response.status_code})")
    else:
        print(f"✗ course_details view failed (status: {response.status_code})")

    # Test submit view
    print("\n2. Testing submit view...")
    # Get the first correct choice
    first_question = questions.first()
    if first_question:
        correct_choice = first_question.choice_set.filter(
            is_correct=True).first()
        if correct_choice:
            post_data = {f'question_{first_question.id}': correct_choice.id}
            response = client.post(
                f'/onlinecourse/submit/{course.id}/', post_data)
            if response.status_code == 302:  # Redirect expected
                print(f"✓ submit view works (status: {response.status_code})")
                print(
                    f"  Session exam_result: {response.wsgi_request.session.get('exam_result', 'Not found')}")
            else:
                print(f"✗ submit view failed (status: {response.status_code})")

    # Test show_exam_result view
    print("\n3. Testing show_exam_result view...")
    response = client.get(f'/onlinecourse/result/{course.id}/')
    if response.status_code == 200:
        print(
            f"✓ show_exam_result view accessible (status: {response.status_code})")
    else:
        print(
            f"✗ show_exam_result view failed (status: {response.status_code})")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    return True


if __name__ == '__main__':
    test_workflow()
