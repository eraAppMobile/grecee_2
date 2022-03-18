
from datetime import date, datetime, timedelta

import jwt as jwt
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, User
from django.core import validators
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Viq(models.Model):
    qid = models.IntegerField(db_column='QId', blank=True, null=True)  # Field name made lowercase.
    objecttype = models.IntegerField(db_column='ObjectType', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryId', blank=True, null=True)  # Field name made lowercase.
    questionid = models.TextField(db_column='QuestionId', blank=True, null=True)  # Field name made lowercase.
    commentid = models.TextField(db_column='CommentId', blank=True, null=True)  # Field name made lowercase.
    parentid = models.TextField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    parenttype = models.TextField(db_column='ParentType', blank=True, null=True)  # Field name made lowercase.
    displayindex = models.IntegerField(db_column='DisplayIndex', blank=True, null=True)  # Field name made lowercase.
    displaylevel = models.IntegerField(db_column='DisplayLevel', blank=True, null=True)  # Field name made lowercase.
    objectid = models.TextField(db_column='ObjectId', blank=True, null=True)  # Field name made lowercase.
    parentcategory = models.TextField(db_column='ParentCategory', blank=True, null=True)  # Field name made lowercase.
    globaldisplayindex = models.IntegerField(db_column='GlobalDisplayIndex', blank=True, null=True)  # Field name made lowercase.
    children = models.IntegerField(db_column='Children', blank=True, null=True)  # Field name made lowercase.
    displaycode = models.TextField(db_column='DisplayCode', blank=True, null=True)  # Field name made lowercase.
    internaldisplaycode = models.TextField(db_column='InternalDisplayCode', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='Id', blank=True, primary_key = True)  # Field name made lowercase.
    showafterid = models.IntegerField(db_column='ShowAfterId', blank=True, null=True)  # Field name made lowercase.

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
    defaultdisplayindex = models.TextField(db_column='DefaultDisplayIndex', blank=True, null=True)  # Field name made lowercase.
    creationinfo = models.TextField(db_column='CreationInfo', blank=True, null=True)  # Field name made lowercase.
    conceptuallink = models.TextField(db_column='ConceptualLink', blank=True, null=True)  # Field name made lowercase.
    questiontypeid = models.IntegerField(db_column='QuestionTypeID', blank=True, null=True)  # Field name made lowercase.
    parentid = models.TextField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'questionpoolnew'


class Viqinfo(models.Model):
    qid = models.AutoField(db_column='QId', blank=True, primary_key = True)  # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    author = models.TextField(db_column='Author', blank=True, null=True)  # Field name made lowercase.
    finalized = models.TextField(db_column='Finalized', blank=True, null=True)  # Field name made lowercase.
    registrationdate = models.TextField(db_column='RegistrationDate', blank=True, null=True)  # Field name made lowercase.
    numofquestions = models.IntegerField(db_column='NumOfQuestions', blank=True, null=True)  # Field name made lowercase.
    viqgui = models.TextField(db_column='VIQGUI', blank=True, null=True)  # Field name made lowercase.
    effectivedate = models.TextField(db_column='EffectiveDate', blank=True, null=True)  # Field name made lowercase.
    version = models.TextField(blank=True, null=True)
    securitycolumn = models.TextField(db_column='SecurityColumn', blank=True, null=True)  # Field name made lowercase.
    visible = models.TextField(db_column='Visible', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VIQinfo'


    # переработать вопросы ( создать портфель вопросов, может включать разное кол-во ответов)
class Answer(models.Model):
    InspectorName = models.TextField(blank=True, null=True)
    answer = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    date_of_creation = models.DateTimeField( auto_now_add=False, default=datetime.today, blank=True, null=True)
    questionid = models.TextField(blank=True, null=True)
    questioncode = models.TextField(blank=True, null=True)
    categoryid = models.IntegerField(blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    categorynewid = models.TextField(blank=True, null=True)
    vessel = models.CharField(max_length=255, blank=True, null=True)
    port = models.CharField(max_length=255, blank=True, null=True)
    InspectionTypes = models.TextField(blank=True, null=True)
    InspectionSource = models.TextField(blank=True, null=True)
    date_in_vessel = models.TextField(blank=True, null=True)


def user_directory_path(instance):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_username
    # вопрос по медия рут ( читал про отдельный домен что бы избежать уязвимостей xss)-спросить у Димы
    # папка не создаются -разобраться!!!
    return 'user_{0}/'.format(instance.user.username)


class Image(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='images')
    # не отображает миниатюры в админке!
    def image_img(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(no Photography)'

    image_img.short_description = 'Photography'
    image_img.allow_tags = True


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Создает и возвращает `User` с адресом электронной почты,
        именем пользователя и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Создает и возвращает пользователя с правами
        суперпользователя (администратора).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Определяет наш пользовательский класс User.
    Требуется имя пользователя, адрес электронной почты и пароль.
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

    is_active = models.BooleanField(default=True)

    # Свойство `USERNAME_FIELD` сообщает нам, какое поле мы будем использовать для входа.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    # Сообщает Django, что класс UserManager, определенный выше,
    # должен управлять объектами этого типа.
    objects = UserManager()



    def __str__(self):
        """
        Возвращает строковое представление этого `User`.
        Эта строка используется, когда в консоли выводится `User`.
        """
        return self.username

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


