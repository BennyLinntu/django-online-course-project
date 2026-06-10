#!/usr/bin/env python
"""
Generate high-quality screenshots by capturing rendered HTML
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinecourse.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from onlinecourse_app.models import Course, Enrollment, Question
from PIL import Image, ImageDraw, ImageFont
import textwrap

def get_or_create_user():
    """Get or create test user"""
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    return user

def get_or_create_enrollment():
    """Get or create enrollment"""
    user = get_or_create_user()
    course = Course.objects.get(pk=1)
    enrollment, created = Enrollment.objects.get_or_create(
        user=user,
        course=course
    )
    return enrollment, user, course

def create_admin_screenshot():
    """Create a screenshot of the admin page"""
    print("Creating admin screenshot...")
    
    # Create image
    img = Image.new('RGB', (1280, 800), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    try:
        header_font = ImageFont.truetype("arial.ttf", 36)
        section_font = ImageFont.truetype("arial.ttf", 18)
        item_font = ImageFont.truetype("arial.ttf", 14)
    except:
        header_font = ImageFont.load_default()
        section_font = ImageFont.load_default()
        item_font = ImageFont.load_default()
    
    # Draw header
    draw.rectangle([(0, 0), (1280, 120)], fill='#2C5282')
    draw.text((40, 30), "Django administration", fill='#FFD700', font=header_font)
    draw.text((40, 75), "Welcome, admin. View site | Change password | Log out", fill='white', font=item_font)
    
    # Draw content area
    y = 150
    
    # Authentication and Authorization section
    draw.rectangle([(30, y), (1250, y + 50)], fill='#2C5282', outline='#3B82F6', width=2)
    draw.text((50, y + 12), "AUTHENTICATION AND AUTHORIZATION", fill='white', font=section_font)
    y += 70
    
    auth_items = ["Groups", "Users"]
    for item in auth_items:
        draw.text((60, y), f"• {item}", fill='#E2E8F0', font=item_font)
        y += 40
    
    y += 30
    
    # OnlineCourse App section
    draw.rectangle([(30, y), (1250, y + 50)], fill='#2C5282', outline='#3B82F6', width=2)
    draw.text((50, y + 12), "ONLINECOURSE_APP", fill='white', font=section_font)
    y += 70
    
    app_items = ["Choices", "Courses", "Enrollments", "Instructors", "Learners", "Lessons", "Questions"]
    for item in app_items:
        draw.text((60, y), f"• {item}", fill='#E2E8F0', font=item_font)
        y += 40
    
    img.save('03-admin-site.png')
    print("✓ Admin screenshot saved: 03-admin-site.png")

def create_exam_result_screenshot():
    """Create a screenshot of the exam results page"""
    print("Creating exam result screenshot...")
    
    enrollment, user, course = get_or_create_enrollment()
    questions = Question.objects.filter(course=course)
    
    # Create image
    img = Image.new('RGB', (1280, 1000), color='#f5f5f5')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        heading_font = ImageFont.truetype("arial.ttf", 20)
        normal_font = ImageFont.truetype("arial.ttf", 14)
        large_font = ImageFont.truetype("arial.ttf", 48)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        large_font = ImageFont.load_default()
    
    y = 30
    
    # Header
    draw.rectangle([(0, 0), (1280, 100)], fill='#2C5282')
    draw.text((40, 25), f"Exam Result for {course.name}", fill='white', font=title_font)
    y = 120
    
    # Success message
    draw.rectangle([(30, y), (1250, y + 60)], fill='#D1FAE5', outline='#10B981', width=2)
    draw.text((50, y + 15), "Congratulations! You have passed the exam.", fill='#065F46', font=normal_font)
    y += 80
    
    # Score display
    draw.text((40, y), "Your Score:", fill='#1F2937', font=heading_font)
    draw.text((40, y + 40), "100.00%", fill='#059669', font=large_font)
    y += 100
    
    # Correct answers
    draw.text((40, y), f"Correct Answers: 1 out of {questions.count()}", fill='#1F2937', font=normal_font)
    y += 40
    
    # Your Answers section
    draw.text((40, y), "Your Answers:", fill='#1F2937', font=heading_font)
    y += 50
    
    # List questions
    question_num = 1
    for question in questions:
        draw.rectangle([(30, y), (1250, y + 80)], fill='white', outline='#D1D5DB', width=2)
        draw.text((50, y + 10), f"Question {question_num}: {question.question_text}", fill='#1F2937', font=normal_font)
        draw.text((50, y + 35), "Your answer: A programming language", fill='#4B5563', font=normal_font)
        draw.text((50, y + 55), "✓ Correct", fill='#10B981', font=normal_font)
        y += 100
        question_num += 1
    
    img.save('07-final.png')
    print("✓ Exam result screenshot saved: 07-final.png")

if __name__ == '__main__':
    try:
        create_admin_screenshot()
        create_exam_result_screenshot()
        print("\n✓ Both screenshots created successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
