from onlinecourse_app.models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment
from django.contrib.auth.models import User
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinecourse.settings')
django.setup()


# Create a test course
course = Course.objects.create(
    name="Introduction to Python",
    description="Learn the basics of Python programming",
    pub_date=datetime.now().date()
)

# Create lessons
lesson1 = Lesson.objects.create(
    title="Introduction to Variables",
    order=1,
    course=course,
    content="Learn about variables and data types"
)

lesson2 = Lesson.objects.create(
    title="Control Flow",
    order=2,
    course=course,
    content="Learn about if statements and loops"
)

# Create questions
question1 = Question.objects.create(
    course=course,
    lesson=lesson1,
    question_text="What is a variable?",
    grade=1
)

question2 = Question.objects.create(
    course=course,
    lesson=lesson1,
    question_text="Which of these is not a data type?",
    grade=1
)

# Create choices for question 1
Choice.objects.create(
    question=question1,
    choice_text="A named container that stores a value",
    is_correct=True
)

Choice.objects.create(
    question=question1,
    choice_text="A type of loop",
    is_correct=False
)

Choice.objects.create(
    question=question1,
    choice_text="A function parameter",
    is_correct=False
)

# Create choices for question 2
Choice.objects.create(
    question=question2,
    choice_text="int",
    is_correct=False
)

Choice.objects.create(
    question=question2,
    choice_text="str",
    is_correct=False
)

Choice.objects.create(
    question=question2,
    choice_text="variable",
    is_correct=True
)

Choice.objects.create(
    question=question2,
    choice_text="float",
    is_correct=False
)

# Create a test user (learner)
try:
    user = User.objects.get(username='testuser')
except User.DoesNotExist:
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

# Create an enrollment
enrollment, created = Enrollment.objects.get_or_create(
    user=user,
    course=course,
    defaults={'mode': 'audit'}
)

print("Test data created successfully!")
print(f"Course: {course.name}")
print(f"Lessons: {course.lesson_set.count()}")
print(f"Questions: {course.question_set.count()}")
print(f"Test user: {user.username}")
