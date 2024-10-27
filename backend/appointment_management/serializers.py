from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Appointment,
    Availability,
    Club,
    Match,
    Notification,
    Preference,
    Referee,
    Relative,
    Venue,
    PasswordReset
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['venue_id', 'venue_name', 'capacity', 'location']

class ClubSerializer(serializers.ModelSerializer):
    home_venue = VenueSerializer(read_only=True)

    class Meta:
        model = Club
        fields = ['club_id', 'club_name', 'home_venue', 'contact_name', 'contact_phone_number']

    def create(self, validated_data):
        return Club.objects.create(**validated_data)

class ClubWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['club_id', 'club_name', 'home_venue', 'contact_name', 'contact_phone_number']

class RefereeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Referee
        fields = [
            'referee_id', 'username', 'email', 'first_name', 'last_name',
            'gender', 'age', 'location', 'zip_code', 'phone_number',
            'experience_years', 'level'
        ]

class RefereeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee
        fields = [
            'referee_id', 'first_name', 'last_name', 'gender', 'age',
            'location', 'zip_code', 'phone_number', 'experience_years', 'level'
        ]

class MatchSerializer(serializers.ModelSerializer):
    home_club = ClubSerializer(read_only=True)
    away_club = ClubSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    referee = RefereeSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ['match_id', 'referee', 'home_club', 'away_club', 'venue', 'match_date', 'match_time', 'level']

class MatchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['match_id', 'referee', 'home_club', 'away_club', 'venue', 'match_date', 'match_time', 'level']

class AppointmentSerializer(serializers.ModelSerializer):
    referee = RefereeSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    match = MatchSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['appointment_id', 'referee', 'venue', 'match', 'distance', 'appointment_date', 'appointment_time', 'status']

class AppointmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'referee', 'venue', 'match', 'distance', 'appointment_date', 'appointment_time', 'status']

class AvailabilitySerializer(serializers.ModelSerializer):
    referee = RefereeSerializer(read_only=True)

    class Meta:
        model = Availability
        fields = ['availableID', 'referee', 'date', 'start_time', 'end_time', 'duration', 'availableType', 'weekday']

class AvailabilityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['availableID', 'referee', 'date', 'start_time', 'end_time', 'duration', 'availableType', 'weekday']

class NotificationSerializer(serializers.ModelSerializer):
    referee = RefereeSerializer(read_only=True)
    match = MatchSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['notification_id', 'referee', 'match', 'notification_type', 'date']

class NotificationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_id', 'referee', 'match', 'notification_type', 'date']

class PreferenceSerializer(serializers.ModelSerializer):
    referee = RefereeSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = Preference
        fields = ['preference_ID', 'referee', 'venue']

class PreferenceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['preference_ID', 'referee', 'venue']

class RelativeSerializer(serializers.ModelSerializer):
    referee = RefereeSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Relative
        fields = ['relative_id', 'referee', 'club', 'relative_name', 'relationship', 'age']

class RelativeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relative
        fields = ['relative_id', 'referee', 'club', 'relative_name', 'relationship', 'age']

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = ['user', 'reset_token', 'token_created']
        read_only_fields = ['user', 'reset_token', 'token_created']