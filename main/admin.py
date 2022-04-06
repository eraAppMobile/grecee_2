import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from django.utils.html import format_html
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django import forms

from main.models import Answer, User, Image, Briefcase

admin.site.site_header = 'Era App development. Beta 0.1 for Lonia'


# @admin.register(Image)
class GalleryInline(admin.ModelAdmin):
    model = Image
    readonly_fields = ['image_img']
    fields = ['image_img']
    extra = 0
    can_delete = False


class AnswerInline(admin.TabularInline):
    model = Answer
    list_filter = ['categorynewid']
    save_as = True
    can_delete = False
    actions = ["export_as_csv"]
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return [
                    'question',
                    'answer',
                    'comment',
                    'date_of_creation',
                    'questionid',
                    'questioncode',
                    'categoryid',
                    'origin',
                    'categorynewid',
                    'get_photo',
                    ]
        return self.readonly_fields

    def get_photo(self, obj):
        if obj.images.all():
            href_for_admin = []
            for href in obj.images.all():
                href_for_admin.append(
                    format_html(f'<a href="{href}" target="_blank"><img src="{href} " width="50"/></a</a>')
                )
            return format_html('\n'.join(href_for_admin))
        return 'no photography'
    get_photo.short_description = 'Photo'

    def has_add_permission(self, request, *args, **kwargs):
        return False


def export_to_csv(modeladmin, request, queryset):

    opts = modeladmin.model._meta
    opts_answer = Answer._meta.get_fields()
    fields = [field for field in opts.get_fields()]
    fields1 = [field for field in opts_answer]
    list_chapters = [field.name.title() for field in fields]
    list_answer = [field.name.title() for field in fields1]
    list_csv = [*list_chapters, *list_answer]


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

    writer = csv.writer(response, delimiter=";")
    writer.writerow(list_csv)

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if field.many_to_many is True or field.one_to_many is True:
                value = str("+").replace(";", "")

            if isinstance(value, datetime.datetime):
                value = value.strftime('%d.%m.%Y')
            data_row.append(value)

        for field in fields:
            try:
                if field.many_to_many is True or field.one_to_many is True:
                    value = str(" ").replace(";", "")
                    data_row.append(value)

                for answer_in_briefcase in list(getattr(obj, field.name).all().values_list()):
                    data_lite = []
                    for element_answer in answer_in_briefcase:
                        if isinstance(element_answer, datetime.datetime):
                            element_answer = element_answer.strftime('%d.%m.%Y')
                        data_lite.append(element_answer)

                    writer.writerow(data_row+data_lite)

            except AttributeError:
                continue








    # for obj in queryset:
    #     data_row = []
    #     for field in fields:
    #         if field.many_to_many == True or field.one_to_many == True:
    #             value = getattr(obj, field.name).all()
    #
    #             fields_answer = [value.query]
    #             for i in fields_answer:
    #                 print(i.model)

    # for obj in queryset:
    #     data_row = []
    #     for field in fields:
    #         value = str(getattr(obj, field.name)).replace(";", "")
    #         if isinstance(value, datetime.datetime):
    #             value = value.strftime('%d/%m/%Y')
    #         data_row.append(value)
    #     for field in fields:
    #         if field.many_to_many == True or field.one_to_many == True:
    #             if field.many_to_many == True or field.one_to_many == True:
    #                 value = str("
    #


    # value = list(getattr(obj, field.name).all().values_list()) - ответы
    # print(fields)
    # writer.writerow([field.name.title() for field in fields])



    return response


@admin.register(Briefcase)
class BriefcaseAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    inlines = [AnswerInline]
    list_display = ['name_case', 'date_of_creation', 'InspectorName', 'vessel', 'port', ]
    fields = [
                'name_case',
                'InspectorName',
                'InspectionTypes',
                'InspectionSource',
                'vessel',
                'port',
                'date_of_creation',
                'date_in_vessel',
                ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return [
                    'name_case',
                    'InspectorName',
                    'InspectionTypes',
                    'InspectionSource',
                    'vessel',
                    'port',
                    'date_of_creation',
                    'date_in_vessel',
                    ]
        return self.readonly_fields

    def has_add_permission(self, request, *args, **kwargs):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(BriefcaseAdmin, self).change_view(request, object_id,
                                                     form_url, extra_context=extra_context)


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
    password = ReadOnlyPasswordHashField(label="Password",
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
    list_display = ('email', 'name', 'lastname', 'username', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff',)
    fieldsets = [
        (None, {'fields': ('email', 'username', 'password',)}),
        ('Personal info', {'fields': ('name', 'lastname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    ]

    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         )
    ]
    search_fields = ('email', 'username', 'name', 'lastname')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)

admin.site.unregister(Group)
