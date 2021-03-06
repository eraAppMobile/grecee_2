from datetime import datetime

import jwt as pyjwt
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, User
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.html import format_html


class Viq(models.Model):
    qid = models.IntegerField(db_column='QId', blank=True, null=True)
    objecttype = models.IntegerField(db_column='ObjectType', blank=True, null=True)
    categoryid = models.IntegerField(db_column='CategoryId', blank=True, null=True)
    questionid = models.TextField(db_column='QuestionId', blank=True, null=True)
    commentid = models.TextField(db_column='CommentId', blank=True, null=True)
    parentid = models.TextField(db_column='ParentId', blank=True, null=True)
    parenttype = models.TextField(db_column='ParentType', blank=True, null=True)
    displayindex = models.IntegerField(db_column='DisplayIndex', blank=True, null=True)
    displaylevel = models.IntegerField(db_column='DisplayLevel', blank=True, null=True)
    objectid = models.TextField(db_column='ObjectId', blank=True, null=True)
    parentcategory = models.TextField(db_column='ParentCategory', blank=True, null=True)
    globaldisplayindex = models.IntegerField(db_column='GlobalDisplayIndex', blank=True, null=True)
    children = models.IntegerField(db_column='Children', blank=True, null=True)
    displaycode = models.TextField(db_column='DisplayCode', blank=True, null=True)
    internaldisplaycode = models.TextField(db_column='InternalDisplayCode', blank=True, null=True)
    id = models.AutoField(db_column='Id', blank=True, primary_key=True)
    showafterid = models.IntegerField(db_column='ShowAfterId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VIQ'



class Questionpoolnew(models.Model):
    questionid = models.TextField(db_column='questionid', blank=True, primary_key=True)
    questioncode = models.TextField(db_column='questioncode', blank=True, null=True)
    question = models.TextField(db_column='question', blank=True, null=True)
    comment = models.TextField(db_column='comment', blank=True, null=True)
    categoryid = models.TextField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    categorycode = models.TextField(db_column='CategoryCode', blank=True, null=True)  # Field name made lowercase.
    origin = models.IntegerField(db_column='Origin', blank=True, null=True)  # Field name made lowercase.
    origincode = models.TextField(db_column='OriginCode', blank=True, null=True)  # Field name made lowercase.
    categorynewid = models.TextField(db_column='CategoryNewID', blank=True, null=True)  # Field name made lowercase.
    defaultdisplayindex = models.TextField(db_column='DefaultDisplayIndex', blank=True, null=True)
    creationinfo = models.TextField(db_column='CreationInfo', blank=True, null=True)  # Field name made lowercase.
    conceptuallink = models.TextField(db_column='ConceptualLink', blank=True, null=True)  # Field name made lowercase.
    questiontypeid = models.IntegerField(db_column='QuestionTypeID', blank=True, null=True)
    parentid = models.TextField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'questionpoolnew'


class Viqinfo(models.Model):
    qid = models.AutoField(db_column='QId', blank=True, primary_key=True)
    title = models.TextField(db_column='Title', blank=True, null=True)
    comments = models.TextField(db_column='Comments', blank=True, null=True)
    author = models.TextField(db_column='Author', blank=True, null=True)
    finalized = models.TextField(db_column='Finalized', blank=True, null=True)
    registrationdate = models.TextField(db_column='RegistrationDate', blank=True, null=True)
    numofquestions = models.IntegerField(db_column='NumOfQuestions', blank=True, null=True)
    viqgui = models.TextField(db_column='VIQGUI', blank=True, null=True)
    effectivedate = models.TextField(db_column='EffectiveDate', blank=True, null=True)
    version = models.TextField(blank=True, null=True)
    securitycolumn = models.TextField(db_column='SecurityColumn', blank=True, null=True)
    visible = models.TextField(db_column='Visible', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VIQinfo'


class Inspectiontypes(models.Model):
    inspectiontypeid = models.AutoField(db_column='InspectionTypeId', blank=True, primary_key=True)
    inspectiontype = models.TextField(db_column='InspectionType', blank=True, null=True)
    inspectioncode = models.TextField(db_column='InspectionCode', blank=True, null=True)
    bitreport = models.TextField(db_column='bitReport', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'InspectionTypes'


class Vessel(models.Model):
    vesselname = models.TextField(db_column='VesselName', blank=True, null=True)
    vesselid = models.AutoField(db_column='VesselId', blank=True, primary_key=True)
    imo = models.TextField(db_column='IMO', blank=True, null=True)
    flag = models.TextField(db_column='FLAG', blank=True, null=True)
    deliverydate = models.TextField(db_column='DeliveryDate', blank=True, null=True)
    grosstonage = models.TextField(db_column='GrossTonage', blank=True, null=True)
    deadweight = models.TextField(db_column='DeadWeight', blank=True, null=True)
    locked = models.IntegerField(db_column='Locked', blank=True, null=True)
    fleetid = models.IntegerField(db_column='FleetId', blank=True, null=True)
    vesselcode = models.TextField(db_column='VesselCode', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Vessel'


class Inspectionsource(models.Model):
    inspectionsourceid = models.AutoField(db_column='InspectionSourceId', blank=True, primary_key=True)
    majorocimfid = models.TextField(db_column='MajorOCIMFId', blank=True, null=True)
    sourcename = models.TextField(db_column='SourceName', blank=True, null=True)
    sourcecode = models.TextField(db_column='SourceCode', blank=True, null=True)
    countrycode = models.TextField(db_column='CountryCode', blank=True, null=True)
    usedid = models.TextField(db_column='UsedId', blank=True, null=True)
    typecode = models.TextField(db_column='TypeCode', blank=True, null=True)
    printcode = models.TextField(db_column='PrintCode', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'InspectionSource'


class Vettinginfo(models.Model):
    inspectorname = models.TextField(db_column='InspectorName', blank=True, null=True)
    inspectorsirname = models.TextField(db_column='InspectorSirName', blank=True, null=True)
    port = models.TextField(db_column='Port', blank=True, null=True)
    country = models.TextField(db_column='Country', blank=True, null=True)
    vetdate = models.TextField(db_column='VetDate', blank=True, null=True)
    vettime = models.TextField(db_column='VetTime', blank=True, null=True)
    password = models.TextField(db_column='Password', blank=True, null=True)
    comments = models.TextField(db_column='Comments', blank=True, null=True)
    vesselname = models.TextField(db_column='VesselName', blank=True, null=True)
    vettingcode = models.TextField(db_column='VettingCode', blank=True, null=True)
    vetid = models.AutoField(db_column='VetId', blank=True, primary_key=True)
    qid = models.IntegerField(db_column='QId', blank=True, null=True)
    vetgui = models.TextField(db_column='VetGUI', blank=True, null=True)
    inspectiontypeid = models.IntegerField(db_column='InspectionTypeId', blank=True, null=True)
    vesselid = models.IntegerField(db_column='VesselId', blank=True, null=True)
    countryid = models.TextField(db_column='CountryId', blank=True, null=True)
    portid = models.TextField(db_column='PortId', blank=True, null=True)
    companyrepresentativename = models.TextField(db_column='CompanyRepresentativeName', blank=True, null=True)
    registrationdate = models.TextField(db_column='RegistrationDate', blank=True, null=True)
    majorid = models.TextField(db_column='MajorId', blank=True, null=True)
    registername = models.TextField(db_column='RegisterName', blank=True, null=True)
    answered = models.IntegerField(db_column='Answered', blank=True, null=True)
    negative = models.TextField(db_column='Negative', blank=True, null=True)
    positive = models.TextField(db_column='Positive', blank=True, null=True)
    sourceid = models.TextField(db_column='SourceId', blank=True, null=True)
    userid = models.TextField(db_column='UserId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VettingInfo'


class Answer(models.Model):
    answer = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=False, default=datetime.today, blank=True, null=True)
    questionid = models.TextField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    questioncode = models.TextField(blank=True, null=True)
    categoryid = models.IntegerField(blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    categorynewid = models.TextField(blank=True, null=True)
    briefcase_answer = models.ForeignKey('Briefcase', on_delete=models.CASCADE,
                                         related_name='briefcase', blank=True, null=True)

    def __str__(self):
        return f'question id:{self.questionid}, question: {self.question}'


def user_directory_path(instance , name):
    # ????????, ???????? ?????????? ???????????????????????? ???????????????? MEDIA_ROOT/user_username
    return 'Inspector_{0}/{1}/{2}'.format(
        name, 'question_id_' + str(instance.answer_image.questionid), 'photo_question_id_'
                                                                      + str(instance.answer_image.questionid) + '.png'
    )


class Image(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    answer_image = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='images')

    def image_img(self):
        if self.image:
            return format_html(
                u'<a href="{0}" target="_blank"><img src="{0}" width="200"/></a></a>'.format(self.image.url)
            )
        else:
            return 'no photography'

    image_img.short_description = 'Photography'
    image_img.allow_tags = True

    def __str__(self):
        return self.image.url


@receiver(pre_delete, sender=Image)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)


class Briefcase(models.Model):

    InspectorName = models.TextField(blank=True, null=True)
    InspectionTypes = models.TextField(blank=True, null=True)
    InspectionSource = models.TextField(blank=True, null=True)
    vessel = models.CharField(max_length=255, blank=True, null=True)
    port = models.CharField(max_length=255, blank=True, null=True)
    name_case = models.TextField(max_length=255)
    date_of_creation = models.DateTimeField(auto_now_add=False, default=datetime.today, blank=True, null=True)
    date_in_vessel = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.name_case


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('?????????????????? ?????? ???????????????????????? ???????????? ???????? ??????????????????????')

        if not email:
            raise ValueError('???????????? ?????????? ?????????????????????? ?????????? ???????????? ???????? ????????????????????')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """
        ?????????????? ?? ???????????????????? `User` ?? ?????????????? ?????????????????????? ??????????,
        ???????????? ???????????????????????? ?? ??????????????.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
        ?????????????? ?? ???????????????????? ???????????????????????? ?? ??????????????
        ?????????????????????????????????? (????????????????????????????).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('?????????????????????????????????? ???????????? ?????????? is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('?????????????????????????????????? ???????????? ?????????? is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    ???????????????????? ?????? ???????????????????????????????? ?????????? User.
    ?????????????????? ?????? ????????????????????????, ?????????? ?????????????????????? ?????????? ?? ????????????.
    """

    username = models.CharField(db_index=True, max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
        )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, verbose_name='administrator')
    is_active = models.BooleanField(default=True)

    # ???????????????? `USERNAME_FIELD` ???????????????? ??????, ?????????? ???????? ???? ?????????? ???????????????????????? ?????? ??????????.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    # ???????????????? Django, ?????? ?????????? UserManager, ???????????????????????? ????????,
    # ???????????? ?????????????????? ?????????????????? ?????????? ????????.
    objects = UserManager()


    def __str__(self):
        """
        ???????????????????? ?????????????????? ?????????????????????????? ?????????? `User`.
        ?????? ???????????? ????????????????????????, ?????????? ?? ?????????????? ?????????????????? `User`.
        """
        return self.username

    @property
    def token(self):

        token = pyjwt.encode({
            'id': self.pk,
            'email': self.email

        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def get_full_name(self):
        """
        ???????? ?????????? ?????????????????? Django ?????? ?????????? ??????????, ?????? ?????????????????? ??????????????????????
        ??????????. ???????????? ?????? ?????? ?????????????? ????????????????????????, ???? ?????????????????? ???? ????
        ???????????????????? ????, ?????????? ???????????????????? username.
        """
        return self.username
