from django.urls import path
from .views import (
    DoctorListCreateAPIView,
    DoctorDetailAPIView,
    PatientListCreateAPIView,
    PatientDetailAPIView,
    AppointmentListCreateAPIView,
    AppointmentDetailAPIView
)


urlpatterns = [
    path(
        "doctors/",
        DoctorListCreateAPIView.as_view(),
        name="doctor-list-create"
    ),

    path(
        "doctors/<int:pk>/",
        DoctorDetailAPIView.as_view(),
        name="doctor-detail"
    ),
    path(
    "patients/",
    PatientListCreateAPIView.as_view(),
    name="patient-list-create"
    ),
    
    path(
    "patients/<int:pk>/",
    PatientDetailAPIView.as_view(),
    name="patient-detail"
    ),

    path(
    "appointments/",
    AppointmentListCreateAPIView.as_view(),
    name="appointment-list-create"
    ),

     path(
        'appointments/<int:pk>/',
        AppointmentDetailAPIView.as_view()
    ),
]