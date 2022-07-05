from collections import OrderedDict
from operator import itemgetter

from django.contrib.auth import authenticate
from rest_framework.validators import UniqueTogetherValidator

from main.models import Answer, Viqinfo, Vessel, Inspectiontypes, Inspectionsource, Vettinginfo

from rest_framework import serializers


class InspectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspectiontypes
        fields = ('inspectiontype',)

    def to_representation(self, data):
        data = super(InspectionTypeSerializer, self).to_representation(data)
        for obj, (key, value) in enumerate(data.items()):
            return value.strip()


class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = ('vesselname',)

    def to_representation(self, data):
        data = super(VesselSerializer, self).to_representation(data)
        for obj, (key, value) in enumerate(data.items()):
            return value.strip()


class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vettinginfo
        fields = ('port',)


    def to_representation(self, data):
        data = super(PortSerializer, self).to_representation(data)
        for obj, (key, value) in enumerate(data.items()):
            return value.title()


class InspectionSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspectionsource
        fields = ('sourcename',)

    def to_representation(self, data):
        data = super(InspectionSourceSerializer, self).to_representation(data)
        for obj, (key, value) in enumerate(data.items()):
            return value.strip()


class BriefcaseSerializer(serializers.Serializer):
    inspectiontype = InspectionTypeSerializer(read_only=True, many=True)
    vessel = VesselSerializer(read_only=True, many=True)
    sourcename = InspectionSourceSerializer(read_only=True, many=True)
    port = PortSerializer(read_only=True, many=True)





class AnswerMVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
                    'answer',
                    'comment',
                    'date_of_creation',
                    'questionid',
                    'questioncode',
                    'categoryid',
                    'origin',
                    'categorynewid')


class ChaptersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viqinfo
        fields = (
                    'qid',
                    'title',
                    )





class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }



# class RegistrationSerializer(serializers.ModelSerializer):
#     """
#     Creates a new user.
#     Email, username, and password are required.
#     Returns a JSON web token.
#     """
#
#     # The password must be validated and should not be read by the client
#     password = serializers.CharField(
#         max_length=128,
#         min_length=8,
#         write_only=True,
#     )
#
#     # The client should not be able to send a token along with a registration
#     # request. Making `token` read-only handles that for us.
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password', 'token',)
#
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)
