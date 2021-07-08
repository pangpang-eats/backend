import typing
from apps.user.models import User, UserRole


def create_sample_user_and_get_token(api_client, phone_number) -> typing.List:
    user: User = User.objects.create_user(phone_number=phone_number,
                                          name='홍길동',
                                          password='thePas123Q',
                                          role=UserRole.CLIENT)
    response = api_client.post(
        '/api/token',
        {
            'phone_number': phone_number,
            'password': 'thePas123Q',
        },
    )
    return (user, response.data['access'])