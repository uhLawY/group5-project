from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import profile_front, copy_workout , report_flexcam_post,delete_flexcam_post
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name="homepage"),
    path('about/',views.about, name="about"),
    path('login/',views.login_user, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('signup/',views.signup_user, name="signup"),
    path('profile/',views.profile_user, name="profile"),
    path('routines/',views.routines, name="routines"),
    path('progress/',views.progress_tracker, name="progress"),
    path('profile_front/', views.profile_front, name="profile_front"),
    path('flexcam/', views.flexcam, name='flexcam'),
    path('new-flexcam-post/', views.new_flexcam_post, name='new_flexcam_post'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('like-flexcam-post/<int:post_id>/', views.like_flexcam_post, name='like_flexcam_post'),
    path('my_workouts/', views.my_workouts, name='my_workouts'),
    path('delete-workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('delete-exercise/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('profile/<str:username>/', views.see_profile, name='see_profile'),
    path('exercise/<int:routine_id>/', views.exercise_details, name='exercise_details'),
    path('my_workouts/', views.my_workouts, name='my_workouts'),
    path('my_workouts/<str:username>/', views.my_workouts, name='my_workouts_user'),
    path('progress/', views.progress_tracker, name='progress'),
    path('progress/reset/<str:date>/<str:exercise_routine>/', views.reset_progress, name='reset_progress'),
    path('top-exercises/', views.top_exercises, name='top_exercises'),
    path('copy_workout/<int:workout_id>/', copy_workout, name='copy_workout'),
    path('report-flexcam-post/<int:post_id>/', report_flexcam_post, name='report_flexcam_post'),
    path('progress/overall/', views.overallstats, name='overallstats'),
    path('delete-flexcam-post/<int:post_id>/', delete_flexcam_post, name='delete_flexcam_post'),
    ]


    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)