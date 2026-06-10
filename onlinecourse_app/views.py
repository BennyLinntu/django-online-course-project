from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse_app/course_details_bootstrap.html', {'course': course})


@login_required
def submit(request, course_id):
    """Handle exam submission"""
    if request.method == 'POST':
        try:
            enrollment = Enrollment.objects.get(
                user=request.user, course_id=course_id)
        except Enrollment.DoesNotExist:
            return HttpResponseRedirect(f'/onlinecourse/course/{course_id}/')

        # Clear previous submissions
        Submission.objects.filter(enrollment=enrollment).delete()

        total_questions = 0
        correct_answers = 0
        choices_selected = []

        for key, value in request.POST.items():
            if key.startswith('question_'):
                try:
                    question_id = int(key.split('_')[1])
                    choice_id = int(value)

                    question = Question.objects.get(pk=question_id)
                    choice = Choice.objects.get(pk=choice_id)

                    submission = Submission(enrollment=enrollment)
                    submission.save()
                    submission.choices.add(choice)
                    
                    choices_selected.append({
                        'question_id': question_id,
                        'choice_id': choice_id,
                        'choice_text': choice.choice_text,
                        'is_correct': choice.is_correct
                    })

                    total_questions += 1
                    if choice.is_correct:
                        correct_answers += 1
                except (Question.DoesNotExist, Choice.DoesNotExist, ValueError):
                    continue

        score = (correct_answers / total_questions) * \
            100 if total_questions > 0 else 0

        # Store comprehensive result in session
        request.session['exam_result'] = {
            'score': score,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'choices': choices_selected
        }

        return HttpResponseRedirect(reverse('show_exam_result', args=[course_id]))
    else:
        # Redirect GET requests to course details
        return HttpResponseRedirect(reverse('course_details', args=[course_id]))


@login_required
def show_exam_result(request, course_id):
    """Display exam results"""
    result = request.session.get('exam_result')
    if not result:
        raise Http404("Exam result not found.")

    course = get_object_or_404(Course, pk=course_id)

    # Get user's submissions for the exam
    try:
        enrollment = Enrollment.objects.get(user=request.user, course_id=course_id)
        submissions = Submission.objects.filter(enrollment=enrollment)
    except Enrollment.DoesNotExist:
        raise Http404("No enrollment found for this course.")

    # Prepare detailed result information
    questions = Question.objects.filter(course_id=course_id)
    result_details = []
    
    for question in questions:
        question_result = {
            'question': question,
            'user_choice': None,
            'is_correct': False
        }
        
        # Find user's choice for this question
        for choice_info in result.get('choices', []):
            if choice_info['question_id'] == question.id:
                question_result['user_choice'] = choice_info['choice_text']
                question_result['is_correct'] = choice_info['is_correct']
                break
        
        result_details.append(question_result)

    return render(request, 'onlinecourse_app/exam_result.html', {
        'result': result,
        'course': course,
        'submissions': submissions,
        'result_details': result_details
    })
