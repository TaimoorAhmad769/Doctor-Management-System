from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from .models import Doctor, Patient, Appointment
from .serializers import (
    DoctorSerializer,
    PatientSerializer,
    AppointmentSerializer
)

from .permissions import (
    IsAdminOrDoctorOwner,
    IsAdminOrRelevantPatient,
    IsAdminOrRelevantAppointment,
)


# =========================================================
# DOCTOR APIs
# =========================================================


class DoctorListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Admin → see all doctors
        if request.user.groups.filter(name="Admin").exists():

            doctors = Doctor.objects.all()

        # Doctor → see only themselves
        elif request.user.groups.filter(name="Doctor").exists():

            doctors = Doctor.objects.filter(
                user=request.user
            )

        # Patient → can see all doctors
        elif request.user.groups.filter(name="Patient").exists():

            doctors = Doctor.objects.all()

        else:

            return Response(
                {"detail": "You do not have a valid role."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DoctorSerializer(
            doctors,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        # Only Admin can create doctors
        if not request.user.groups.filter(
            name="Admin"
        ).exists():

            return Response(
                {"detail": "Only Admins can create doctors."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DoctorSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DoctorDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrDoctorOwner
    ]

    def get(self, request, pk):

        doctor = get_object_or_404(
            Doctor,
            pk=pk
        )

        self.check_object_permissions(
            request,
            doctor
        )

        serializer = DoctorSerializer(
            doctor
        )

        return Response(serializer.data)

    def put(self, request, pk):

        doctor = get_object_or_404(
            Doctor,
            pk=pk
        )

        self.check_object_permissions(
            request,
            doctor
        )

        # Only Admin can modify doctors
        if not request.user.groups.filter(
            name="Admin"
        ).exists():

            return Response(
                {"detail": "Only Admins can update doctors."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DoctorSerializer(
            doctor,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        doctor = get_object_or_404(
            Doctor,
            pk=pk
        )

        self.check_object_permissions(
            request,
            doctor
        )

        # Only Admin can modify doctors
        if not request.user.groups.filter(
            name="Admin"
        ).exists():

            return Response(
                {"detail": "Only Admins can update doctors."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DoctorSerializer(
            doctor,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        doctor = get_object_or_404(
            Doctor,
            pk=pk
        )

        self.check_object_permissions(
            request,
            doctor
        )

        # Only Admin can delete doctors
        if not request.user.groups.filter(
            name="Admin"
        ).exists():

            return Response(
                {"detail": "Only Admins can delete doctors."},
                status=status.HTTP_403_FORBIDDEN
            )

        doctor.delete()

        return Response(
            {"message": "Doctor deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================================================
# PATIENT APIs
# =========================================================


class PatientListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        # Admin → see all patients
        if request.user.groups.filter(
            name="Admin"
        ).exists():

            patients = Patient.objects.all()

        # Doctor → see only their patients
        elif request.user.groups.filter(
            name="Doctor"
        ).exists():

            patients = Patient.objects.filter(
                appointment__doctor__user=request.user
            ).distinct()

        # Patient → see only themselves
        elif request.user.groups.filter(
            name="Patient"
        ).exists():

            patients = Patient.objects.filter(
                user=request.user
            )

        else:

            return Response(
                {"detail": "You do not have a valid role."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PatientSerializer(
            patients,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        # Admin can create any patient
        if request.user.groups.filter(
            name="Admin"
        ).exists():

            serializer = PatientSerializer(
                data=request.data
            )

        # Patient can create their own patient record
        elif request.user.groups.filter(
            name="Patient"
        ).exists():

            data = request.data.copy()

            data["user"] = request.user.id

            serializer = PatientSerializer(
                data=data
            )

        else:

            return Response(
                {
                    "detail":
                    "Only Admins or Patients can create patient records."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PatientDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRelevantPatient
    ]

    def get(self, request, pk):

        patient = get_object_or_404(
            Patient,
            pk=pk
        )

        self.check_object_permissions(
            request,
            patient
        )

        serializer = PatientSerializer(
            patient
        )

        return Response(
            serializer.data
        )

    def put(self, request, pk):

        patient = get_object_or_404(
            Patient,
            pk=pk
        )

        # Admin → can update any patient
        if request.user.groups.filter(
            name="Admin"
        ).exists():

            serializer = PatientSerializer(
                patient,
                data=request.data
            )

        # Patient → can update only themselves
        elif (
            request.user.groups.filter(name="Patient").exists()
            and patient.user == request.user
        ):

            serializer = PatientSerializer(
                patient,
                data=request.data
            )

        else:

            return Response(
                {"detail": "You cannot update this patient."},
                status=status.HTTP_403_FORBIDDEN
            )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        patient = get_object_or_404(
            Patient,
            pk=pk
        )

        # Admin → can update any patient
        if request.user.groups.filter(
            name="Admin"
        ).exists():

            serializer = PatientSerializer(
                patient,
                data=request.data,
                partial=True
            )

        # Patient → can update themselves
        elif (
            request.user.groups.filter(name="Patient").exists()
            and patient.user == request.user
        ):

            serializer = PatientSerializer(
                patient,
                data=request.data,
                partial=True
            )

        else:

            return Response(
                {"detail": "You cannot update this patient."},
                status=status.HTTP_403_FORBIDDEN
            )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        patient = get_object_or_404(
            Patient,
            pk=pk
        )

        # Only Admin can delete patients
        if not request.user.groups.filter(
            name="Admin"
        ).exists():

            return Response(
                {"detail": "Only Admins can delete patients."},
                status=status.HTTP_403_FORBIDDEN
            )

        patient.delete()

        return Response(
            {"message": "Patient deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================================================
# APPOINTMENT APIs
# =========================================================


class AppointmentListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        # Admin → all appointments
        if request.user.groups.filter(
            name="Admin"
        ).exists():

            appointments = Appointment.objects.all()

        # Doctor → only their appointments
        elif request.user.groups.filter(
            name="Doctor"
        ).exists():

            appointments = Appointment.objects.filter(
                doctor__user=request.user
            )

        # Patient → only their appointments
        elif request.user.groups.filter(
            name="Patient"
        ).exists():

            appointments = Appointment.objects.filter(
                patient__user=request.user
            )

        else:

            return Response(
                {"detail": "You do not have a valid role."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        # Admin → can create any appointment
        if request.user.groups.filter(
            name="Admin"
        ).exists():

            serializer = AppointmentSerializer(
                data=request.data
            )

        # Patient → can create appointment for themselves
        elif request.user.groups.filter(
            name="Patient"
        ).exists():

            patient = get_object_or_404(
                Patient,
                user=request.user
            )

            data = request.data.copy()

            # Force the appointment to belong to logged-in patient
            data["patient"] = patient.id

            serializer = AppointmentSerializer(
                data=data
            )

        else:

            return Response(
                {
                    "detail":
                    "Only Admins and Patients can create appointments."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AppointmentDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRelevantAppointment
    ]

    def get(self, request, pk):

        appointment = get_object_or_404(
            Appointment,
            pk=pk
        )

        self.check_object_permissions(
            request,
            appointment
        )

        serializer = AppointmentSerializer(
            appointment
        )

        return Response(
            serializer.data
        )

    def put(self, request, pk):

        appointment = get_object_or_404(
            Appointment,
            pk=pk
        )

        self.check_object_permissions(
            request,
            appointment
        )

        serializer = AppointmentSerializer(
            appointment,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        appointment = get_object_or_404(
            Appointment,
            pk=pk
        )

        self.check_object_permissions(
            request,
            appointment
        )

        serializer = AppointmentSerializer(
            appointment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        appointment = get_object_or_404(
            Appointment,
            pk=pk
        )

        self.check_object_permissions(
            request,
            appointment
        )

        # Only Admin can delete appointments
        if not request.user.groups.filter(
            name="Admin"
        ).exists():

            return Response(
                {"detail": "Only Admins can delete appointments."},
                status=status.HTTP_403_FORBIDDEN
            )

        appointment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )