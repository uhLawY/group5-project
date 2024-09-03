from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name="homepage"),
    path('about/',views.about, name="about"),
    path('login/',views.login_user, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('signup/',views.signup_user, name="signup"),
    path('profile/',views.profile_user, name="profile"),
    path('routines/',views.routines, name="routines"),
    path('profile_front/', views.profile_front, name="profile_front"),
    path('routines/<int:routine_id>/favourite/', views.add_to_favourite, name='add_to_favourite'),
    path('my-favourites/', views.favourite_routines, name='favourite_routines'),
    path('flexcam/', views.flexcam, name='flexcam'),
    path('new-flexcam-post/', views.new_flexcam_post, name='new_flexcam_post'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment')
    ]


    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)