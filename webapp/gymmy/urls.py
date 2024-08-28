from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="homepage"),
    path('about/',views.about, name="about"),
    path('login/',views.login_user, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('signup/',views.signup_user, name="signup"),
    path('profile/',views.profile_user, name="profile"),
    path('routines/',views.routinepage, name="routines")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)