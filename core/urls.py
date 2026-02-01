from django.urls import re_path

from core import views


app_name = 'core'

urlpatterns = [
    # Login urls
    re_path(
        r'^hello/$',
        views.hello,
        name='hello'
    ),
    re_path(
        r'^user/create/$',
        views.create_user,
        name='create_user'
    ),
    re_path(
        r'user/get/',
        views.get_user,
        name='get_user'
    ),
]
