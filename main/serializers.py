from venv import create

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from rest_framework import serializers

from main.models import Answer, Viqinfo, Vessel, Inspectiontypes, Inspectionsource, Vettinginfo, Questionpoolnew, \
    Briefcase, Image


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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionpoolnew
        fields = (
            'questionid',
            'questioncode',
            'question',
            'comment',
            'categoryid',
            'origin',
            'categorynewid'
        )


class QuestionListSerializer(serializers.Serializer):
    question = QuestionSerializer(read_only=True, many=True)


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token and Fullname
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)


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

        full_name = f"{user.name or ''} {user.lastname or ''}".strip()

        return {
                'token': user.token,
                'full_name': full_name,
            }


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')
            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "png" if extension == "png" else extension

        return extension


class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Image
        fields = ('image',)


class AnswerSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Answer
        fields = (
            'answer',
            'comment',
            'questionid',
            'question',
            'questioncode',
            'categoryid',
            'categorynewid',
            'origin',
            'images',
        )


class BriefCaseDataBaseSerializer(serializers.ModelSerializer):
    briefcase = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Briefcase
        fields = (
            'name_case',
            'InspectorName',
            'InspectionTypes',
            'InspectionSource',
            'vessel',
            'port',
            'date_in_vessel',
            'briefcase',
        )


    def create(self, validated_data):
        user = self.context['user_id']

        answers = validated_data.pop('briefcase')
        name = user.lastname
        new_briefcase = Briefcase.objects.create(**validated_data)
        for answer in answers:
            images = answer.pop('images')
            new_answer = Answer.objects.create(**answer, briefcase_answer=new_briefcase)

            for image in images:
                for order_dict in image.items():
                    image_var = order_dict[1].open().read()
                    Image.objects.create(image=ContentFile(image_var, name='' + name), answer_image=new_answer)

        LogEntry.objects.log_action(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(Briefcase).pk,
            object_id=new_briefcase.id,
            object_repr=new_briefcase.name_case,
            action_flag=ADDITION if create else CHANGE)
        return new_briefcase


#регистрация юзеров тут скрыта
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
