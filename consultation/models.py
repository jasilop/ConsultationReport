from django.db import models

# Create your models here.

class Consultation(models.Model):
    clinic_name = models.CharField(max_length=200)
    clinic_logo = models.ImageField(upload_to='clinic_logos/')  # Store uploaded logos
    physician_name = models.CharField(max_length=200)
    physician_contact = models.CharField(max_length=200)
    patient_first_name = models.CharField(max_length=200)
    patient_last_name = models.CharField(max_length=200)
    patient_dob = models.DateField()  # Use DateField for date of birth
    patient_contact = models.CharField(max_length=200)
    chief_complaint = models.TextField()  # Use TextField for longer text
    consultation_note = models.TextField()  # Use TextField for longer text

    def __str__(self):
        return f"Consultation with {self.patient_first_name} {self.patient_last_name}"



