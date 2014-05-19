from django.conf import settings
from django.contrib.auth.models import User

from oncourse.api.decorators import authenticate
from oncourse.api.models import AccessToken
from oncourse.api.views import ApiView, ApiConsumerAuthentication


class UserRegistrationView(ApiView):

    authentication = [ApiConsumerAuthentication()]

    @authenticate
    def post(self, request, *args, **kwargs):

        try:
            data = self.deserialise(request)
        except ValueError:
            return self.bad_request()

        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['username'],
            password=data['password'],
        )

        try:
            access_token = user.access_tokens.get(
                consumer__key=settings.MASTER_OAUTH_KEY,
                consumer__secret=settings.MASTER_OAUTH_SECRET
            )
        except AccessToken.DoesNotExist:
            return self.unauthorized()
        else:
            token = access_token.token

        return self.json({'token': token})
