from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Course, Enrollment, Lesson, Question, ExamAttempt


class CourseFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="learner", password="StrongPass123!"
        )
        cls.course = Course.objects.create(
            name="Introduction to Python",
            description="Learn Python from scratch.",
        )
        cls.lesson_one = Lesson.objects.create(
            course=cls.course,
            order=1,
            title="Variables",
            content="A variable stores a value.",
        )
        cls.lesson_two = Lesson.objects.create(
            course=cls.course,
            order=2,
            title="Functions",
            content="Functions package reusable behaviour.",
        )
        cls.q1 = Question.objects.create(
            course=cls.course,
            lesson=cls.lesson_one,
            question_text="What is a variable?",
            grade=2,
        )
        cls.q2 = Question.objects.create(
            course=cls.course,
            lesson=cls.lesson_two,
            question_text="Which keyword returns a value?",
            grade=3,
        )
        cls.q1_correct = Choice.objects.create(
            question=cls.q1, choice_text="A named value", is_correct=True
        )
        cls.q1_wrong = Choice.objects.create(
            question=cls.q1, choice_text="A loop", is_correct=False
        )
        cls.q2_correct = Choice.objects.create(
            question=cls.q2, choice_text="return", is_correct=True
        )
        cls.q2_wrong = Choice.objects.create(
            question=cls.q2, choice_text="print", is_correct=False
        )

    def test_catalogue_is_public_and_searchable(self):
        response = self.client.get(reverse("course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Introduction to Python")

        response = self.client.get(reverse("course_list"), {"q": "Python"})
        self.assertContains(response, "Introduction to Python")

        response = self.client.get(reverse("course_list"), {"q": "Astrophysics"})
        self.assertContains(response, "No courses match that search")

    def test_course_detail_requires_login(self):
        response = self.client.get(
            reverse("course_details", args=[self.course.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_opening_course_creates_enrollment(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("course_details", args=[self.course.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Enrollment.objects.filter(user=self.user, course=self.course).exists()
        )
        self.assertContains(response, "Variables")
        self.assertContains(response, "What is a variable?")

    def test_submit_creates_one_weighted_attempt(self):
        self.client.force_login(self.user)
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        response = self.client.post(
            reverse("submit", args=[self.course.id]),
            {
                f"question_{self.q1.id}": self.q1_correct.id,
                f"question_{self.q2.id}": self.q2_correct.id,
            },
        )
        self.assertRedirects(
            response, reverse("show_exam_result", args=[self.course.id])
        )
        attempt = ExamAttempt.objects.get(enrollment=enrollment)
        self.assertEqual(attempt.score, 100.0)
        self.assertEqual(attempt.correct_count, 2)
        self.assertEqual(attempt.total_questions, 2)
        self.assertEqual(attempt.choices.count(), 2)

    def test_submit_scores_partial_and_unanswered(self):
        self.client.force_login(self.user)
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        response = self.client.post(
            reverse("submit", args=[self.course.id]),
            {f"question_{self.q1.id}": self.q1_correct.id},
        )
        self.assertEqual(response.status_code, 302)
        attempt = ExamAttempt.objects.get(enrollment=enrollment)
        self.assertEqual(attempt.score, 40.0)
        self.assertEqual(attempt.correct_count, 1)
        self.assertEqual(attempt.choices.count(), 1)

    def test_result_page_shows_latest_attempt(self):
        self.client.force_login(self.user)
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        first = ExamAttempt.objects.create(
            enrollment=enrollment,
            score=40,
            correct_count=1,
            total_questions=2,
        )
        first.choices.set([self.q1_correct])
        latest = ExamAttempt.objects.create(
            enrollment=enrollment,
            score=100,
            correct_count=2,
            total_questions=2,
        )
        latest.choices.set([self.q1_correct, self.q2_correct])

        response = self.client.get(
            reverse("show_exam_result", args=[self.course.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100.0%")
        self.assertContains(response, "Passed")
        self.assertContains(response, "Your answer")

    def test_submit_rejects_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("submit", args=[self.course.id]))
        self.assertEqual(response.status_code, 405)

    def test_enrollment_is_unique(self):
        Enrollment.objects.create(user=self.user, course=self.course)
        with self.assertRaises(Exception):
            Enrollment.objects.create(user=self.user, course=self.course)

    def test_models_use_expected_related_names(self):
        self.assertEqual(self.course.lesson_count, 2)
        self.assertEqual(self.course.question_count, 2)
        self.assertEqual(self.q1.choices.count(), 2)
        self.assertEqual(str(self.lesson_one), "Introduction to Python: Variables")
