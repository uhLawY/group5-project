from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import UserRegisterForm , FlexcamPostForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Profile, Routines , FlexcamPost, WorkoutExercise, Workout
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, "gymmy/landing.html", {})

def about(request):
    return render(request, 'gymmy/aboutpage.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome Back! {username}!')
            return redirect('homepage')
        else:
            messages.success(request,('There was an error logging in!'))
            return redirect('login')
    else:
        return render(request, 'gymmy/login.html', {})

def signup_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'gymmy/signup.html', {'form':form}) 
        

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('homepage')


@login_required
def profile_user(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        

        
        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile Has Been Updated!')
            return redirect('profile')

            
    else:
        u_form = UserUpdateForm(instance=request.user)
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        

    context = {
        'u_form': u_form,
        'p_form': p_form,
       
    }
    return render(request, 'gymmy/profile.html', context)

@login_required
def profile_front(request):
    return render(request, 'gymmy/profile_front.html')

@login_required
def see_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect('profile_front')
    else:
        return render(request, 'gymmy/see_profile.html', {'user': user})



def my_workouts(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'gymmy/my_workouts.html', {'workouts': workouts})



def routines(request):
    query = request.GET.get('input-box')
    if query:
        routines = Routines.objects.filter(routine__icontains=query) | Routines.objects.filter(description__icontains=query)
    else:
        routines = Routines.objects.all()
    
    if request.method == 'POST':

        routine_id = request.POST.get('routine_id')
        routine = get_object_or_404(Routines, id=routine_id)

        new_workout_name = request.POST.get('new_workout_name', '').strip()
        selected_workout_id = request.POST.get('workout')

        if new_workout_name and selected_workout_id:
            messages.error(request, 'Please choose either to select an existing workout or create a new one, not both.')
        elif not new_workout_name and not selected_workout_id:
            messages.error(request, 'Please select an existing workout or enter a new workout name.')
        elif new_workout_name:
            workout = Workout.objects.create(user=request.user, name=new_workout_name)
            reps = int(request.POST.get('reps', 1))
            sets = int(request.POST.get('sets', 1))
            WorkoutExercise.objects.create(
                workout=workout,
                routine=routine,
                reps=reps,
                sets=sets
            )
            messages.success(request, f'New workout "{workout.name}" created and exercise added successfully!')
        else:
            try:
                workout = Workout.objects.get(id=selected_workout_id, user=request.user)
                reps = int(request.POST.get('reps', 1))
                sets = int(request.POST.get('sets', 1))
                WorkoutExercise.objects.create(
                    workout=workout,
                    routine=routine,
                    reps=reps,
                    sets=sets
                )
                messages.success(request, f'Exercise added to "{workout.name}" successfully!')
            except Workout.DoesNotExist:
                messages.error(request, 'Selected workout does not exist. Please try again.')
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'gymmy/routines.html', {'routines': routines, 'workouts': workouts})

def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, f'Workout "{workout.name}" has been deleted successfully!')
        return redirect('my_workouts')
    else:
        messages.error(request, 'Invalid request. Please try again.')
        return redirect('my_workouts')

def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(WorkoutExercise, id=exercise_id, workout__user=request.user)  
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, f'Exercise "{exercise.routine.routine}" has been deleted successfully from workout "{exercise.workout.name}"!')
        return redirect('my_workouts')
    else:
        messages.error(request, 'Invalid request. Please try again.')
        return redirect('my_workouts')

@login_required
def add_to_favourite(request, routine_id):
    routine = get_object_or_404(Routines, id=routine_id)
    
    if routine.favorites.filter(id=request.user.id).exists():
        routine.favorites.remove(request.user)
        added = False
    else:
        routine.favorites.add(request.user)
        added = True
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'added': added})
    
    return redirect('routines')



@login_required
def favourite_routines(request):
    favourite_routines = Routines.objects.filter(favorites=request.user)
    favourite_routine_ids = favourite_routines.values_list('id', flat=True)
    
    return render(request, 'gymmy/favourite_routines.html', {
        'favourite_routines': favourite_routines,
        'favourite_routine_ids': favourite_routine_ids,
    })





@login_required
def flexcam(request):
    posts_list = FlexcamPost.objects.all()
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'gymmy/flexcam.html', {'posts': posts})

@login_required
def new_flexcam_post(request):
    if request.method == 'POST':
        form = FlexcamPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('flexcam')
    else:
        form = FlexcamPostForm()
    return render(request, 'gymmy/new_flexcam_post.html', {'form': form})

def like_flexcam_post(request, post_id):
    post = get_object_or_404(FlexcamPost, id=post_id)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'like_count': post.likes.count()})
    
    return redirect('flexcam')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(FlexcamPost, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('flexcam')
    else:
        form = CommentForm()
    return render(request, 'gymmy/add_comment.html', {'form': form, 'post': post})
