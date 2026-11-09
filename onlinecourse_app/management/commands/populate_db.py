"""Create a useful demo catalogue without touching real data."""

from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from onlinecourse_app.models import (
    Choice,
    Course,
    Enrollment,
    Instructor,
    Lesson,
    Question,
)


COURSES = [
    {
        "name": "Introduction to Python",
        "description": (
            "Start from zero and learn the ideas that make Python readable: "
            "variables, types, conditionals, loops and functions."
        ),
        "instructor": ("Ada", "Lovelace", "ada"),
        "lessons": [
            (
                1,
                "Variables and values",
                "A variable is a name bound to a value. Learn how Python stores "
                "numbers, strings and booleans, and why names matter.",
            ),
            (
                2,
                "Control flow",
                "Use if, elif and else to make decisions. Then repeat work with "
                "for and while loops.",
            ),
            (
                3,
                "Functions",
                "Package reusable behaviour into functions with parameters, "
                "return values and sensible names.",
            ),
        ],
        "questions": [
            (
                1,
                "What is a variable?",
                1,
                [
                    ("A named reference to a value", True),
                    ("A type of loop", False),
                    ("A Python keyword only", False),
                    ("A function parameter", False),
                ],
            ),
            (
                3,
                "Which keyword sends a value back from a function?",
                1,
                [
                    ("return", True),
                    ("yield", False),
                    ("print", False),
                    ("break", False),
                ],
            ),
        ],
    },
    {
        "name": "Web Development Foundations",
        "description": (
            "Understand how a browser, HTTP and a server fit together, then build "
            "a small page with HTML, CSS and a little JavaScript."
        ),
        "instructor": ("Grace", "Hopper", "grace"),
        "lessons": [
            (
                1,
                "How the web works",
                "Follow a request from the address bar to a server and back. "
                "Meet DNS, HTTP methods and status codes.",
            ),
            (
                2,
                "HTML and CSS",
                "Structure content with semantic HTML, then make it readable and "
                "responsive with modern CSS.",
            ),
            (
                3,
                "JavaScript in the browser",
                "Respond to clicks, read input and update the page without a "
                "full reload.",
            ),
        ],
        "questions": [
            (
                1,
                "Which HTTP method usually retrieves a page?",
                1,
                [
                    ("GET", True),
                    ("POST", False),
                    ("DELETE", False),
                    ("PATCH", False),
                ],
            ),
            (
                2,
                "Which HTML element is best for the main page heading?",
                1,
                [
                    ("<h1>", True),
                    ("<div>", False),
                    ("<span>", False),
                    ("<p>", False),
                ],
            ),
        ],
    },
    {
        "name": "Data Thinking with SQL",
        "description": (
            "Ask better questions of tabular data. Practise SELECT, WHERE, joins "
            "and aggregation with small, realistic examples."
        ),
        "instructor": ("Ada", "Lovelace", "ada"),
        "lessons": [
            (
                1,
                "Tables and rows",
                "Learn how relational data is organised and what a primary key "
                "is for.",
            ),
            (
                2,
                "Filtering and sorting",
                "Use WHERE to narrow a result set and ORDER BY to make it useful.",
            ),
            (
                3,
                "Joins and aggregates",
                "Combine tables with JOIN, then summarise with COUNT, SUM and "
                "GROUP BY.",
            ),
        ],
        "questions": [
            (
                2,
                "Which clause filters rows before grouping?",
                1,
                [
                    ("WHERE", True),
                    ("HAVING", False),
                    ("ORDER BY", False),
                    ("LIMIT", False),
                ],
            ),
            (
                3,
                "Which function counts rows in a group?",
                1,
                [
                    ("COUNT()", True),
                    ("SUM()", False),
                    ("AVG()", False),
                    ("MAX()", False),
                ],
            ),
        ],
    },
]


class Command(BaseCommand):
    help = "Populate the database with demo courses, lessons, exams and a demo learner."

    def handle(self, *args, **options):
        instructors = {}
        for first_name, last_name, username in {
            ("Ada", "Lovelace", "ada"),
            ("Grace", "Hopper", "grace"),
        }:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": f"{username}@example.com",
                },
            )
            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
            instructors[username], _ = Instructor.objects.get_or_create(
                user=user, defaults={"full_time": True}
            )

        for spec in COURSES:
            course, _ = Course.objects.get_or_create(
                name=spec["name"],
                defaults={
                    "description": spec["description"],
                    "pub_date": date.today(),
                },
            )
            course.description = spec["description"]
            course.pub_date = course.pub_date or date.today()
            course.save(update_fields=["description", "pub_date"])
            course.instructors.set([instructors[spec["instructor"][2]]])

            lessons = {}
            for order, title, content in spec["lessons"]:
                lesson, _ = Lesson.objects.get_or_create(
                    course=course,
                    order=order,
                    defaults={"title": title, "content": content},
                )
                lesson.title = title
                lesson.content = content
                lesson.save(update_fields=["title", "content"])
                lessons[order] = lesson

            for lesson_order, text, grade, choices in spec["questions"]:
                question, _ = Question.objects.get_or_create(
                    course=course,
                    question_text=text,
                    defaults={
                        "lesson": lessons[lesson_order],
                        "grade": grade,
                    },
                )
                question.lesson = lessons[lesson_order]
                question.grade = grade
                question.save(update_fields=["lesson", "grade"])

                for choice_text, is_correct in choices:
                    Choice.objects.get_or_create(
                        question=question,
                        choice_text=choice_text,
                        defaults={"is_correct": is_correct},
                    )

        demo, created = User.objects.get_or_create(
            username="demo",
            defaults={"first_name": "Demo", "last_name": "Learner"},
        )
        if created:
            demo.set_password("demo12345")
            demo.save(update_fields=["password"])

        for course in Course.objects.all():
            Enrollment.objects.get_or_create(
                user=demo, course=course, defaults={"mode": Enrollment.AUDIT}
            )
            course.total_enrollment = course.enrollments.count()
            course.save(update_fields=["total_enrollment"])

        self.stdout.write(self.style.SUCCESS("Demo catalogue is ready."))
        self.stdout.write(
            f"{Course.objects.count()} courses, {Lesson.objects.count()} lessons, "
            f"{Question.objects.count()} questions."
        )
        self.stdout.write("Demo login: demo / demo12345")
