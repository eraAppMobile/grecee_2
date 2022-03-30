import jwt as pyjwt


from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):

        request.user = None

        # `auth_header` должен быть массивом из двух элементов: 1) имя
        # заголовок аутентификации (в данном случае «Token») и 2) JWT
        # что мы должны аутентифицировать
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Недопустимый заголовок токена. Учетные данные не предоставлены. Не пытайтесь
            # аутентифицировать
            return None

        elif len(auth_header) > 2:
            # Недопустимый заголовок токена. Строка токена не должна содержать пробелов.
            # Не пытайтесь аутентифицироваться.
            return None

        # Используемая нами библиотека JWT не может обрабатывать тип `byte`, т.е.
        # обычно используется стандартными библиотеками в Python 3. Чтобы обойти это,
        # нам просто нужно расшифровать `prefix` и `token`. Это не делает для
        # чистым код, но это хорошее решение, потому что мы получим ошибку
        # если мы не расшифровали эти значения.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # Префикс заголовка auth не соответствует нашим ожиданиям. Не пытайтесь
            # аутентифицировать.
            return None

        # К настоящему времени мы уверены, что есть *шанс*, что аутентификация будет
        # преуспеть. Мы делегируем фактическую аутентификацию учетных данных
        # метод ниже
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """

        try:

            payload = pyjwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])

        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_staff:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token
