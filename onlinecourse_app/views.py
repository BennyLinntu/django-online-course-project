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
    if request.method == 'POST':
        enrollment = Enrollment.objects.get(user=request.user, course_id=course_id)
        
        # Clear previous submissions
        Submission.objects.filter(enrollment=enrollment).delete()
        
        total_questions = 0
        correct_answers = 0
        
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                choice_id = int(value)
                
                question = Question.objects.get(pk=question_id)
                choice = Choice.objects.get(pk=choice_id)
                
                submission = Submission(enrollment=enrollment)
                submission.save()
                submission.choices.add(choice)
                
                total_questions += 1
                if choice.is_correct:
                    correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Store score in session or another model if you want to persist it
        request.session['exam_result'] = {
            'score': score,
            'total_questions': total_questions,
            'correct_answers': correct_answers
        }
        
        return HttpResponseRedirect(reverse('show_exam_result', args=[course_id]))
    else:
        # This part is not implemented as the form is in the template
        return render(request, 'onlinecourse_app/course_details_bootstrap.html')

@login_required
def show_exam_result(request, course_id):
    result = request.session.get('exam_result')
    if not result:
        raise Http404("Exam result not found.")
        
    course = get_object_or_404(Course, pk=course_id)
    
    # Get user's submissions for the exam
    enrollment = Enrollment.objects.get(user=request.user, course_id=course_id)
    submissions = Submission.objects.filter(enrollment=enrollment)
    
    return render(request, 'onlinecourse_app/exam_result.html', {
        'result': result,
        'course': course,
        'submissions': submissions
    })

