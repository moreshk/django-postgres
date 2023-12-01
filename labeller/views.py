from django.shortcuts import render, redirect
import yfinance as yf
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from .models import Course, Lesson
from .models import Course
from labeller.models import UserLessonProgress
from django.urls import reverse
from users.models import GlobalSettings

def fetch_data():
    ticker = os.getenv('TICKER', '^GSPC')
    days = os.getenv('DAYS', '7')
    interval = os.getenv('INTERVAL', '1h')
    data = yf.download(tickers=ticker, period=f'{days}d', interval=interval)
    data = data.drop(columns=['Volume'])  # Drop the 'Volume' column
    data['Date'] = data.index  # Add 'Date' column from index
    data['Date'] = data['Date'].apply(lambda x: x.isoformat())  # Convert all Timestamps to strings
    
    return data.reset_index(drop=True).to_dict('records')  # Drop the original index

@login_required
def candlestick_view(request):
    if request.user.user_type != 'LABELLER':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    if 'data' not in request.session:
        request.session['data'] = fetch_data()
        request.session['index'] = 0
    
    index = request.session['index']
    candlestick = request.session['data'][index]

    # Debug prints
    print(f"Date: {candlestick['Date']}, Type: {type(candlestick['Date'])}")
    print(f"Close: {candlestick['Close']}, Type: {type(candlestick['Close'])}")
    print(f"High: {candlestick['High']}, Type: {type(candlestick['High'])}")
    print(f"Low: {candlestick['Low']}, Type: {type(candlestick['Low'])}")
    print(f"Open: {candlestick['Open']}, Type: {type(candlestick['Open'])}")

    is_last = index == len(request.session['data']) - 1
    # candlestick['Date'] = candlestick['Date'].isoformat()
    # print(f"After isoformat: {candlestick['Date']}, Type: {type(candlestick['Date'])}")
    return render(request, 'labeller/candlestick.html', {
        'candlestick': candlestick,
        'index': index,
        'total': len(request.session['data']),
    })

@login_required
def back_view(request):
    if request.session['index'] > 0:
        request.session['index'] -= 1
    return redirect('candlestick_view')

@login_required
def forward_view(request):
    if request.session['index'] < len(request.session['data']) - 1:
        request.session['index'] += 1
    return redirect('candlestick_view')


@csrf_exempt
def check_doji(request):
    if request.method == 'POST':
       
        index = request.session['index']
        candlestick = request.session['data'][index]
        user_choice = request.POST.get('choice')
        is_doji = abs(candlestick['Open'] - candlestick['Close']) <= 0.0005 * candlestick['Open']  # Check if the difference is not more than 0.1%
        is_correct = (user_choice == 'doji' and is_doji) or (user_choice == 'not_doji' and not is_doji)
        if is_correct:
            request.user.token += 1
            request.user.save()
        return JsonResponse({'is_correct': is_correct, 'token': request.user.token})
    
    
@login_required
def referred_users_view(request):
    referred_users = CustomUser.objects.filter(referred_by=request.user)
    referral_link = request.build_absolute_uri(reverse('register_with_referral', args=[request.user.referral_code]))

    # Fetch the bonuses from the GlobalSettings
    global_settings = GlobalSettings.objects.first()
    referred_user_bonus = global_settings.referred_user_bonus

    total_referral_bonus = referred_users.count() * referred_user_bonus
    return render(request, 'labeller/referred_users.html', {
        'referred_users': referred_users,
        'referral_link': referral_link,
        'referral_slots': request.user.referral_slots,
        'total_referral_bonus': total_referral_bonus,
        'referred_user_bonus': referred_user_bonus,  # Pass the bonus to the template
    })

@login_required
def training(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Retrieve the UserLessonProgress object for the user and course, or create a new one if it doesn't exist
    user_lesson_progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user, 
        course=course,
        defaults={'lesson': course.lesson_set.order_by('step_id').first()}
    )

    message = None
    correct_answer = None
    selected_option = None
    correct_answer_image = None
    if request.method == 'POST':
        selected_option = int(request.POST.get('user_option'))  # Convert the selected option to an integer
        correct_answer_image = user_lesson_progress.lesson.correct_answer_image
        if selected_option == user_lesson_progress.lesson.correct_answer:
            message = 'Correct!'
        else:
            correct_answer = user_lesson_progress.lesson.user_options[user_lesson_progress.lesson.correct_answer - 1]
            message = f'Wrong! The correct answer is "{correct_answer}".'

    first_step_id = course.lesson_set.order_by('step_id').first().step_id
    last_step_id = course.lesson_set.order_by('-step_id').first().step_id
    is_last_lesson = user_lesson_progress.lesson.step_id == last_step_id
    has_completed_course = course in request.user.completed_courses.all()

    return render(request, 'labeller/training.html', {
        'lesson': user_lesson_progress.lesson, 
        'course': course, 
        'message': message,
        'first_step_id': first_step_id,
        'last_step_id': last_step_id,
        'correct_answer': correct_answer,
        'selected_option': selected_option,
        'correct_answer_image': correct_answer_image,
        'is_last_lesson': is_last_lesson,
        'has_completed_course': has_completed_course
    })

@login_required
def courses_view(request):
    if request.user.user_type != 'LABELLER':
        return redirect('home')
    courses = Course.objects.filter(lesson__isnull=False).distinct()
    return render(request, 'labeller/courses.html', {'courses': courses})

@login_required
def previous_lesson(request, course_id):
    # Retrieve the current lesson for the user in this course
    current_lesson = UserLessonProgress.objects.get(user=request.user, course_id=course_id).lesson

    # Find the previous lesson in the course
    previous_lesson = Lesson.objects.filter(course_id=course_id, step_id__lt=current_lesson.step_id).order_by('-step_id').first()

    if previous_lesson is not None:
        # Update the user's progress to the previous lesson
        UserLessonProgress.objects.filter(user=request.user, course_id=course_id).update(lesson=previous_lesson)

    # Redirect to the training view
    return redirect('training', course_id=course_id)

def next_lesson(request, course_id):
    # Retrieve the current lesson for the user in this course
    current_lesson = UserLessonProgress.objects.get(user=request.user, course_id=course_id).lesson
    print("Current Lesson",current_lesson)
    # Find the next lesson in the course
    next_lesson = Lesson.objects.filter(course_id=course_id, step_id__gt=current_lesson.step_id).order_by('step_id').first()
    print("Next Lesson", next_lesson)
    if next_lesson is not None:
        # Update the user's progress to the next lesson
        UserLessonProgress.objects.filter(user=request.user, course_id=course_id).update(lesson=next_lesson)

    # Redirect to the training view
    return redirect('training', course_id=course_id)


@login_required
def claim_bonus(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course not in request.user.completed_courses.all():
        request.user.token += course.completion_token_bonus
        request.user.completed_courses.add(course)
        request.user.save()
        messages.success(request, f'Congratulations! You earned {course.completion_token_bonus} tokens.')
    return redirect('training', course_id=course_id)

def label_task_view(request):
    # Fetch the last 180 days of data for NSEI
    data = yf.download('^NSEI', period='6mo')
    # Remove rows where 'Open', 'High', 'Low', and 'Close' are all NaN
    data = data.dropna(subset=['Open', 'High', 'Low', 'Close'])
    # Reset the index to move the Date from index to columns
    data.reset_index(inplace=True)
    # Convert the 'Date' column to a shorter string format
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')  # Include the year in the format
    # Convert the data to a format that can be used in the template
    data_list = data.values.tolist()
    # Print the data to the console
    print(data[['Open', 'High', 'Low', 'Close']])
    return render(request, 'labeller/label_task.html', {'data': data_list})

