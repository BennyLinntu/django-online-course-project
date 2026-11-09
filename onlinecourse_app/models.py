from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Course(models.Model):
    name = models.CharField(max_length=100, default="Online course")
    image = models.ImageField(upload_to="course_images/", blank=True)
    description = models.TextField()
    pub_date = models.DateField(default=timezone.now)
    instructors = models.ManyToManyField("Instructor", blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Enrollment",
        related_name="courses",
        blank=True,
    )
    total_enrollment = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-pub_date", "name"]

    def __str__(self):
        return self.name

    @property
    def lesson_count(self):
        return self.lessons.count()

    @property
    def question_count(self):
        return self.questions.count()


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson")
    order = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons"
    )
    content = models.TextField()

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "order"], name="unique_lesson_order"
            )
        ]

    def __str__(self):
        return f"{self.course.name}: {self.title}"


class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_profiles",
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Learner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learner_profile",
    )
    STUDENT = "student"
    DEVELOPER = "developer"
    DATA_SCIENTIST = "data_scientist"
    DATABASE_ADMIN = "dba"
    OCCUPATION_CHOICES = [
        (STUDENT, "Student"),
        (DEVELOPER, "Developer"),
        (DATA_SCIENTIST, "Data Scientist"),
        (DATABASE_ADMIN, "Database Admin"),
    ]
    occupation = models.CharField(
        max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT
    )
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Enrollment(models.Model):
    AUDIT = "audit"
    HONOR = "honor"
    BETA = "beta"
    COURSE_MODES = [
        (AUDIT, "Audit"),
        (HONOR, "Honor"),
        (BETA, "Beta"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    date_enrolled = models.DateField(default=timezone.now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_enrollment"
            )
        ]
        ordering = ["-date_enrolled"]

    def __str__(self):
        return f"{self.user.username} → {self.course.name}"


class Question(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="questions"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="questions"
    )
    question_text = models.CharField(max_length=300)
    grade = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["lesson__order", "id"]

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class ExamAttempt(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="attempts"
    )
    choices = models.ManyToManyField(Choice, blank=True, related_name="attempts")
    score = models.FloatField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-submitted_at", "-id"]

    def __str__(self):
        return f"{self.enrollment} — {self.score:.0f}%"
