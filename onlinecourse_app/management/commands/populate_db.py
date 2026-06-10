from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from onlinecourse_app.models import Course, Lesson, Question, Choice, Enrollment
from datetime import datetime


class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **options):
        # Create a test course
        course, created = Course.objects.get_or_create(
            name="Introduction to Python",
            defaults={
                'description': "Learn the basics of Python programming",
                'pub_date': datetime.now().date()
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Created course: {course.name}'))

        # Create lessons
        lesson1, created = Lesson.objects.get_or_create(
            title="Introduction to Variables",
            course=course,
            defaults={
                'order': 1,
                'content': "Learn about variables and data types"
            }
        )

        lesson2, created = Lesson.objects.get_or_create(
            title="Control Flow",
            course=course,
            defaults={
                'order': 2,
                'content': "Learn about if statements and loops"
            }
        )

        # Create questions
        question1, created = Question.objects.get_or_create(
            course=course,
            lesson=lesson1,
            question_text="What is a variable?",
            defaults={'grade': 1}
        )

        question2, created = Question.objects.get_or_create(
            course=course,
            lesson=lesson1,
            question_text="Which of these is not a data type?",
            defaults={'grade': 1}
        )

        # Create choices for question 1
        Choice.objects.get_or_create(
            question=question1,
            choice_text="A named container that stores a value",
            defaults={'is_correct': True}
        )

        Choice.objects.get_or_create(
            question=question1,
            choice_text="A type of loop",
            defaults={'is_correct': False}
        )

        Choice.objects.get_or_create(
            question=question1,
            choice_text="A function parameter",
            defaults={'is_correct': False}
        )

        # Create choices for question 2
        Choice.objects.get_or_create(
            question=question2,
            choice_text="int",
            defaults={'is_correct': False}
        )

        Choice.objects.get_or_create(
            question=question2,
            choice_text="str",
            defaults={'is_correct': False}
        )

        Choice.objects.get_or_create(
            question=question2,
            choice_text="variable",
            defaults={'is_correct': True}
        )

        Choice.objects.get_or_create(
            question=question2,
            choice_text="float",
            defaults={'is_correct': False}
        )

        # Create a test user (learner)
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com'
            }
        )

        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Created user: {user.username}'))

        # Create an enrollment
        enrollment, created = Enrollment.objects.get_or_create(
            user=user,
            course=course,
            defaults={'mode': 'audit'}
        )

        self.stdout.write(self.style.SUCCESS(
            'Test data populated successfully!'))
        self.stdout.write(f'Course: {course.name}')
        self.stdout.write(f'Lessons: {course.lesson_set.count()}')
        self.stdout.write(f'Questions: {course.question_set.count()}')
        self.stdout.write(f'Test user: {user.username}')
