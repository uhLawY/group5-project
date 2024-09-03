from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm ,  CustomPasswordResetForm, AddToWorkoutForm
from django.contrib.auth.models import User
from .models import Profile, Routines, WorkoutExercise, Workout
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
        
    workouts = Workout.objects.filter(user=request.user).prefetch_related('exercises__routine')
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'workouts': workouts,  # Add workouts to the context
    }
    return render(request, 'gymmy/profile.html', context)


def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password1']

            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been successfully updated!')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'gymmy/reset_password.html', {'form': form})




def routines(request):
    query = request.GET.get('input-box')
    if query:
        routines = Routines.objects.filter(routine__icontains=query) | Routines.objects.filter(description__icontains=query)
    else:
        routines = Routines.objects.all()
    
    if request.method == 'POST':
        # Handle the form submission for adding routines to workouts
        routine_id = request.POST.get('routine_id')
        routine = get_object_or_404(Routines, id=routine_id)

        new_workout_name = request.POST.get('new_workout_name', '').strip()
        selected_workout_id = request.POST.get('workout')

        # Check if both fields are filled or both are empty
        if new_workout_name and selected_workout_id:
            messages.error(request, 'Please choose either to select an existing workout or create a new one, not both.')
        elif not new_workout_name and not selected_workout_id:
            messages.error(request, 'Please select an existing workout or enter a new workout name.')
        elif new_workout_name:
            # Create a new workout
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
            # Add to an existing workout
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

    return render(request, 'gymmy/routines.html', {'routines': routines})

    

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

def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, f'Workout "{workout.name}" has been deleted successfully!')
        return redirect('profile')
    else:
        messages.error(request, 'Invalid request. Please try again.')
        return redirect('profile')

def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(WorkoutExercise, id=exercise_id, workout__user=request.user)  
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, f'Exercise "{exercise.routine.routine}" has been deleted successfully from workout "{exercise.workout.name}"!')
        return redirect('profile')
    else:
        messages.error(request, 'Invalid request. Please try again.')
        return redirect('profile')