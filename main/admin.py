from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django import forms
from django.utils.safestring import mark_safe

from main.models import Answer, User, Image


class GalleryInline(admin.TabularInline):
    model = Image
    readonly_fields = ['image_img',]
    fields = ['image_img',]
    extra = 0
    can_delete = False



@admin.register(Answer)
class Answer(admin.ModelAdmin):

    inlines = [
        GalleryInline,
    ]

    save_as = True

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['InspectorName',
                    'answer',
                    'comment',
                    'date_of_creation',
                    'questionid',
                    'questioncode',
                    'categoryid',
                    'origin',
                    'categorynewid',
                    'vessel',
                    'port',
                    'InspectionTypes',
                    'InspectionSource',
                    'date_in_vessel',
                    ]
        return self.readonly_fields
    # узнать как изменить отображение полей (изменить на горизонтально или еще какой-либо удобный вариант)
    def has_add_permission(self, request):
        return False


class UserCreationForm(forms.ModelForm):
    """Форма для создания новых пользователей. Включает в себя все необходимые
    поля."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'email')

    def clean_password2(self):
        # проверка паролей, ввел ли пользователь два раза один пароль
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # сохранение пароля в хешированном формате
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Форма для обновления пользователей. Включает все поля на
    пользователя, но заменяет поле пароля на admin
    поле отображения хэша пароля.
    """
    # смена пароля в админке
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active', 'is_staff')

    def clean_password(self):
        # удалит все что введет пользователь
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # Формы для добавления и изменения пользовательских экземпляров
    form = UserChangeForm
    add_form = UserCreationForm

    # Поля, которые будут использоваться при отображении модели пользователя.
    list_display = ('email', 'name', 'lastname', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('name', 'lastname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username', 'name', 'lastname')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)

admin.site.unregister(Group)
