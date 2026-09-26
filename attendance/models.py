from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.roll_number} - {self.user.username}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class AttendanceSession(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE
    )

    date = models.DateField()
    section = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.date}"


class AttendanceRecord(models.Model):

    STATUS_CHOICES = [
        ("P", "Present"),
        ("A", "Absent"),
    ]

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="records"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "student"],
                name="unique_student_attendance"
            )
        ]

    def __str__(self):
        return f"{self.student.roll_number} - {self.get_status_display()}"