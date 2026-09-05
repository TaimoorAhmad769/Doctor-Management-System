from rest_framework.permissions import BasePermission #Django REST Framework package 


class IsAdminOrDoctorOwner(BasePermission):
    """
    Admin → can access any Doctor.
    Doctor → can access only their own Doctor record.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Admin → any doctor
        if request.user.groups.filter(name="Admin").exists():
            return True

        # Doctor → only their own doctor record
        if request.user.groups.filter(name="Doctor").exists():
            return obj.user == request.user

        return False



class IsAdminOrRelevantPatient(BasePermission):
    """
    Admin → can access any Patient.
    Doctor → can access patients who have an appointment with them.
    Patient → can access only their own Patient record.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Admin → any patient
        if request.user.groups.filter(name="Admin").exists():
            return True

        # Patient → only their own patient record
        if request.user.groups.filter(name="Patient").exists():
            return obj.user == request.user

        # Doctor → only their own patients
        if request.user.groups.filter(name="Doctor").exists():
            return obj.appointment_set.filter(
                doctor__user=request.user
            ).exists()

        return False




class IsAdminOrRelevantAppointment(BasePermission):
    """
    Admin → can access any Appointment.
    Doctor → can access appointments assigned to them.
    Patient → can access their own appointments.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Admin → any appointment
        if request.user.groups.filter(name="Admin").exists():
            return True

        # Doctor → only their appointments
        if request.user.groups.filter(name="Doctor").exists():
            return obj.doctor.user == request.user

        # Patient → only their appointments
        if request.user.groups.filter(name="Patient").exists():
            return obj.patient.user == request.user

        return False