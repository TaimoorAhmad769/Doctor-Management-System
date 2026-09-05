from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default="Scheduled")

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"