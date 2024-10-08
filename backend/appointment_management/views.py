from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.conf import settings
from .models import *
from .serializers import *
from datetime import date, timezone

# Create your views here.

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    #List all appointments (GET /appointments/)
    def list(self, request):
        queryset = self.get_queryset()

        ## This code checks appointment.appointment_date for all appointment instances
        ## and switches "ongoing" and "upcoming" to "complete" on that instance if the
        ## appointment_date field is before today (signifying the appointment is over)
        ## This code is executed when list() is called. 

        ## May implement this on matches if we decide it needs it. 
        appointments = queryset
        for appointment in appointments:
            if appointment.appointment_date < date.today() and appointment.status != "cancelled":
                appointment.status = "complete"
                appointment.save()

        serializer = AppointmentSerializer(queryset, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)

    #Retrive a specific appointment (GET /appointments/ {id})
    def retrieve(self, request, pk=None):
        appointmet = get_object_or_404(self.queryset, pk=pk)
        serializer = AppointmentSerializer(appointmet)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    #Retrive a specific appointment (GET /appointments/ {id})
    def retrieve(self, request, pk=None):
        appointmet = get_object_or_404(self.queryset, pk=pk)
        serializer = AppointmentSerializer(appointmet)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    ## appointmet is a typo but I'm scared to correct it incase I break the code. 
    
    #Create new appointment (POST /appointments/)
    def create(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    #Updata an existing appointment (PUT /appointments/{id})
    def updata(self, request, pk=None):
        appointment = get_object_or_404(self.queryset, pk=pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /appointments/{id})
    def partial_update(self, request, pk=None):
        appointment = get_object_or_404(self.queryset, pk=pk)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete an appointment (DELETE /appointments/{id})
    def destroy(self, request, pk=None):
        appointment = get_object_or_404(self.queryset ,pk=pk)
        appointment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    # def appointment_list(request):
    #     appointments = Appointment.objects.all() #########



    
class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    
    #Retrieve a specific availability (GET /appointments/{id})
    def retrieve(self, request, pk=None):
        availability = get_object_or_404(self.queryset, pk=pk)
        serializer = AvailabilitySerializer(availability)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    #Create a new availability (POST /appointments/)
    def create(self, request):
        serializer = AvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Update an existing availability (PUT /appointment/{id})
    def update(self, request, pk=None):
        availability = get_object_or_404(self.queryset, pk=pk)
        serializer = AvailabilitySerializer(availability, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = self.get_queryset()
        if (request.query_params.get("referee")):
            queryset = queryset.filter(referee=request.query_params.get("referee"))
        serializer = AvailabilitySerializer(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Partial update (PATCH /availabilities/{id})
    def partial_update(self, request, pk =None):
        availability = get_object_or_404(self.queryset, pk=pk)
        serializer = AvailabilitySerializer(availability, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete an availability (DELETE /availabilities/{id})
    def destroy(self, request, pk=None):
        availability = get_object_or_404(self.queryset, pk=pk)
        availability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    #List all clubs (GET /clubs/)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ClubSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #Retrieve a specific club (GET /clubs/{id})
    def retrieve(self, request, pk=None):
        club = get_object_or_404(self.queryset, pk=pk)
        serializer = ClubSerializer(club)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create a new club (POST /clubs/)
    def create(self, request):
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Update an existing club (PUT /clubs/{id})
    def update(self, request, pk=None):
        club = get_object_or_404(self.queryset, pk=pk)
        serializer = ClubSerializer(club, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /clubs/{id})
    def partial_update(self, request, pk=None):
        club = get_object_or_404(self.queryset ,pk=pk)
        serializer = ClubSerializer(club, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a club (DELETE /clubs/{id})
    def destroy(self, request, pk=None):
        club = get_object_or_404(self.queryset, pk=pk)
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    #List all matches (GET /matches/)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = MatchSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve a specific match (GET /matches/{id})
    def retrieve(self, request, pk=None):
        match = get_object_or_404(self.queryset, pk=pk)
        serializer = MatchSerializer(match)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve qualified referees for a specific match (GET matches/qualified_referees/{id})
    @action(detail=True)
    def qualified_referees(self, request, pk=None):
        match = get_object_or_404(self.queryset, pk=pk)
        referee_availability_queryset = Referee.objects.prefetch_related('availability')
        level_qualified_set = referee_availability_queryset.filter(level__gte=match.level)
        final_availability_set = level_qualified_set.filter(availability__date=match.match_date)
        serializer = RefereeAvailabilitySerializer(final_availability_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create a new match (POST /matches/)
    def create(self, request):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Update an existing match (PUT /matches/{id})
    def update(self, request, pk=None):
        match = get_object_or_404(self.queryset, pk=pk)
        serializer = MatchSerializer(match, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /matches/{id})
    def partial_update(self, request, pk=None):
        match = get_object_or_404(self.queryset, pk=pk)
        serializer = MatchSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a match (DELETE /matches/{id})
    def destroy(self, request, pk=None):
        match = get_object_or_404(self.queryset, pk=pk)
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    #List all notifications (GET /matches/)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve a specific notification (GET /notifications/{id})
    def retrieve(self, request, pk=None):
        notification = get_object_or_404(self.queryset, pk=pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create a new notification (POST /notifications/)
    def create(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Update an existing notification (PUT /notifications/{id})
    def update(self, request, pk=None):
        notification = get_object_or_404(self.queryset, pk=pk)
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /notifications/{id})
    def partial_update(self, request, pk=None):
        notification = get_object_or_404(self.queryset, pk=pk)
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a notification (DELETE /notifications/{id})
    def destroy(self, request, pk=None):
        notification = get_object_or_404(self.queryset, pk=pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

    #List all preferences (GET /preferences/)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = PreferenceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve a specific preference (GET /preferences/{id})
    def retrieve(self, request, pk=None):
        preference = get_object_or_404(self.queryset, pk=pk)
        serializer = PreferenceSerializer(preference)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create a new preference (POST /preferences/)
    def create(self, request):
        serializer = PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Update an existing preference (PUT /preferences/{id})
    def update(self, request, pk=None):
        preference = get_object_or_404(self.queryset, pk=pk)
        serializer = PreferenceSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /preferences/{id})
    def partial_update(self, request, pk=None):
        preference = get_object_or_404(self.queryset, pk=pk)
        serializer = NotificationSerializer(preference, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a preference (DELETE /preferenes/{id})
    def destroy(self, request, pk=None):
        preference = get_object_or_404(self.queryset, pk=pk)
        preference.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RefereeViewSet(viewsets.ModelViewSet):
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer
    
    #List all the referees (GET /referees/)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = RefereeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve a specific referee (GET /referees/{id})
    def retrieve(self, request, pk=None):
        referee = get_object_or_404(self.queryset, pk=pk)
        serializer = RefereeSerializer(referee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create a new referee (POST /referees/)
    def create(self, request):
        #Ensure that each referee can only create one profile
        if Referee.objects.filter(referee_id=request.user.id).exists():
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RefereeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Update an existing referee (PUT /referees/{id})
    def update(self, request, pk=None):
        referee = get_object_or_404(self.queryset, pk=pk)
        serializer = RefereeSerializer(referee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /referees/{id})
    def partial_update(self, request, pk=None):
        referee = get_object_or_404(self.queryset, pk=pk)
        serializer = RefereeSerializer(referee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a referee (DELETE /referees/{id})
    def destroy(self, request, pk=None):
        referee = get_object_or_404(self.queryset, pk=pk)
        referee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RelativeViewSet(viewsets.ModelViewSet):
    queryset = Relative.objects.all()
    serializer_class = RelativeSerializer

    #List all relatives (GET /relatives/)
    def list(self, request):
        querryset = self.get_queryset()
        serializer = RelativeSerializer(querryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve a specific relative (GET /relatives/{id})
    def retrieve(self, request, pk = None):
        relative = get_object_or_404(self.queryset, pk=pk)
        serializer = RelativeSerializer(relative)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create new relative (POST /relatives/)
    def create(self, request):
        serializer = RelativeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Updata an existing relative (PUT /relatives/{id})
    def update(self, request, pk=None):
        relative = get_object_or_404(self.queryset, pk=pk)
        serializer = RelativeSerializer(relative, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /relatives/{id})
    def partial_update(self, request, pk=None):
        relative = get_object_or_404(self.queryset, pk=pk)
        serializer = RelativeSerializer(relative, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a relative (DELETE /relatives/{id})
    def destroy(self, request, pk=None):
        relative = get_object_or_404(self.queryset, pk=pk)
        relative.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    #List all venues (GET /venues/)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = VenueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve a specific venue (GET /venues/{id})
    def retrieve(self, request, pk=None):
        venue = get_object_or_404(self.queryset, pk=pk)
        serializer = VenueSerializer(venue)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create new venue (POST /venues/)
    def create(self, request):
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Update an existing venue (PUT /venues/{id})
    def update(self, request, pk=None):
        venue = get_object_or_404(self.queryset, pk=pk)
        serializer = VenueSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /venues/{id})
    def partial_update(self, request, pk=None):
        venue = get_object_or_404(self.queryset, pk=pk)
        serializer = VenueSerializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a venue (DELETE /venues/{id})
    def destroy(self, request, pk=None):
        venue = get_object_or_404(self.queryset, pk=pk)
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTEN)
class AppointmentManagementAppointmentViewSet(viewsets.ModelViewSet):
    queryset = AppointmentManagementAppointment.objects.all()
    serializer_class = AppointmentManagementAppointmentSerializer
    
    #List all appointment_manage_appointment (GET /appointmentmanageappointment/)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = AppointmentManagementAppointmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Retrieve a specific appointment_manage_appointment (GET /appointmentmanageappointment/{id})
    def retrieve(self, request, pk=None):
        appointment_manage_appointment = get_object_or_404(self.request, pk=pk)
        serializer = AppointmentManagementAppointmentSerializer(appointment_manage_appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create a new appointment_manage_appointment (POST /appointmentmanageappointment/)
    def create(self, request):
        serializer = AppointmentManagementAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Update an existing appointment_manage_appointment (PUT /appointmentmanageappointment/{id})
    def update(self, request, pk=None):
        appointment_manage_appointment = get_object_or_404(self.request, pk=pk)
        serializer = AppointmentManagementAppointmentSerializer(appointment_manage_appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Partial update (PATCH /appointmentmanageappointment/{id})
    def partial_update(self, request, pk=None):
        appointment_manage_appointment = get_object_or_404(self.queryset, pk=pk)
        serializer = AppointmentManagementAppointmentSerializer(appointment_manage_appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete an appointment_manage_appointment (DELETE /appointmentmanageappointment/)
    def destroy(self, request, pk=None):
        appointment_manage_appointment = get_object_or_404(self.queryset, pk=pk)
        appointment_manage_appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class AuthGroupViewSet(viewsets.ModelViewSet):
    queryset = AuthGroup.objects.all()
    serializer_class = AuthGroupSerializer

class AuthGroupPermissionsViewSet(viewsets.ModelViewSet):
    queryset = AuthGroupPermissions.objects.all()
    serializer_class = AuthGroupPermissionsSerializer

class AuthPermissionViewSet(viewsets.ModelViewSet):
    queryset = AuthPermission.objects.all()
    serializer_class = AuthPermissionSerializer

class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

class AuthUserGroupsViewSet(viewsets.ModelViewSet):
    queryset = AuthUserGroups.objects.all()
    serializer_class = AuthUserGroupsSerializer

class AuthUserUserPermissionViewSet(viewsets.ModelViewSet):
    queryset = AuthUserUserPermissions.objects.all()
    serializer_class = AuthUserUserPermissionsSerializer

class DjangoAdminLogViewSet(viewsets.ModelViewSet):
    queryset = DjangoAdminLog.objects.all()
    serializer_class = DjangoAdminLogSerializer

class DjangoContentTypeViewSet(viewsets.ModelViewSet):
    queryset = DjangoContentType.objects.all()
    serializer_class = DjangoContentTypeSerializer

class DjangoMigrationsViewSet(viewsets.ModelViewSet):
    queryset = DjangoMigrations.objects.all()
    serializer_class = DjangoMigrationsSerializer

class DjangoSessionViewSet(viewsets.ModelViewSet):
    queryset = DjangoSession.objects.all()
    serializer_class = DjangoSessionSerializer

class SysdiagramsViewSet(viewsets.ModelViewSet):
    queryset = Sysdiagrams.objects.all()
    serializer_class = SysdiagramsSerializer