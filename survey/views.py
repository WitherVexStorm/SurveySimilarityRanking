from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Question, Answer, Survey, Similarity
from django.contrib.auth.models import User
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# surveys = [
#     {
#         "id": "S001",
#         "questions": [
#             ["How much do you like Userfacet?", 1],
#             ["How much do you like frontend?", 0],
#             ["How much do you like backend?", 2],
#             ["How much do you like fullstack?", 0],
#             ["How much do you like Userfacet?", 3],
#             ["How much do you like frontend?", 0],
#             ["How much do you like backend?", 4],
#             ["How much do you like fullstack?", 0],
#             ["How much do you like Userfacet?", 5],
#             ["How much do you like frontend?", 0],
#             ["How much do you like backend?", 6],
#             ["How much do you like fullstack?", 0],
#             ["How much do you like Userfacet?", 7],
#             ["How much do you like frontend?", 0],
#             ["How much do you like backend?", 8],
#             ["How much do you like fullstack?", 0],
#             ["How much do you like Userfacet?", 9],
#             ["How much do you like frontend?", 0],
#             ["How much do you like backend?", 10],
#             ["How much do you like fullstack?", 0]
#         ]
#     }
# ]

# Create your views here.
def list_surveys(request):
    context = { 'surveys': Survey.objects.all() }
    print(context)
    return render(request, 'survey/list_surveys.html', context = context)

@staff_member_required
def create_survey(request):
    if request.method == 'POST':
        print(request.POST)
        new_survey = Survey.objects.create(survey_name=f'#S{(Survey.objects.count() + 1):04}:{request.POST.get("survey-name")}')
        print(new_survey)
        for i in range(1, 21):
            print(Question.objects.create(survey=new_survey, text=request.POST.get('question-' + str(i))))
        messages.success(request, 'Survey id ' + new_survey.get_id() + ' added successfully!')
        return redirect('list-surveys')
    return render(request, 'survey/create_survey.html')

MULTIPLE_CHOICES = [ { 'label': i, 'value': i, 'name': i } for i in range(1, 21) ]
@login_required
def fill_survey(request):
    print(request.method)
    if request.method == 'POST':
        print(request.POST)
        user_ids = Answer.objects.filter(question__in=Question.objects.filter(survey=Survey.objects.get(survey_id=request.GET.get('survey-id')))).values_list('user').distinct()
        requested_survey = Survey.objects.get(survey_name=request.POST.get('survey-name'))
        print(requested_survey)
        current_answers = []
        for question_id, response in request.POST.items():
            if question_id not in ['csrfmiddlewaretoken', 'survey-name']:
                current_answers.append(Answer.objects.create(question=Question.objects.get(question_id=question_id), user=request.user, answer=int(response)))
        cosine_matrix = { current_answers[0].user.username: current_answers }
        user_list = [ current_answers[0].user ]
        for id in user_ids:
            user = User.objects.get(id=id[0])
            user_list.append(user)
            cosine_matrix[user.username] = [ response.answer for response in Answer.objects.filter(user=user) ]
        print(cosine_matrix)
        print(cosine_matrix.values())
        result_matrix = cosine_similarity(list(cosine_matrix.values()))
        print(result_matrix)
        for similarity, user_2 in zip(result_matrix[0], user_list):
            Similarity.objects.create(user_1=user_list[0], user_2=user_2, survey=requested_survey, value=similarity)
        # print(Answer.objects.order_by('user').distinct('user'))
        # context = { 'survey': { 'name': requested_survey.survey_name, 'questions': [ [question, MULTIPLE_CHOICES ] for question in Question.objects.filter(survey=requested_survey)] } }
        return redirect('list-surveys')
    elif request.method == 'GET':
        print(request.GET.get('survey-id'))
        requested_survey = Survey.objects.get(survey_id=request.GET.get('survey-id'))
        print(requested_survey)
        context = { 'survey': { 'name': requested_survey.survey_name, 'questions': [ [question, MULTIPLE_CHOICES ] for question in Question.objects.filter(survey=requested_survey)] } }
    # print(context)
    return render(request, 'survey/fill_survey.html', context)

def find_similarity(request):
    print(request.GET.get('survey-id'))
    user_ids = Answer.objects.filter(question__in=Question.objects.filter(survey=Survey.objects.get(survey_id=request.GET.get('survey-id')))).values_list('user').distinct()
    user_list = [ User.objects.get(id=id[0]) for id in user_ids ]
    simililarities = Similarity.objects.filter(survey=Survey.objects.get(survey_id=request.GET.get('survey-id')))
    similarity_matrix = []
    print(user_list)
    for index1, user_1 in enumerate(user_list):
        similarity_row = [ [user_list[index1]], [] ]
        for index2, user_2 in enumerate(user_list):
            if index1 >= index2:
                print(user_1, ' - ', user_2)
                similarity_row[1].append(round(simililarities.get(user_1=user_1, user_2=user_2).value * 100, 2))
            else:
                print(user_1, ' - ', user_2)
                similarity_row[1].append(round(simililarities.get(user_1=user_2, user_2=user_1).value * 100, 2))
        similarity_matrix.append(similarity_row)
    context = { 
        'similarity_matrix': similarity_matrix, 
        'similarity_matrix_header': [None] + user_list, 
        'survey_id': request.GET.get('survey-id')
    }
    print(context)
    return render(request, 'survey/find_similarity.html', context=context)

def find_similarity_to(request):
    user_ids = Answer.objects.filter(question__in=Question.objects.filter(survey=Survey.objects.get(survey_id=request.GET.get('survey-id')))).values_list('user').distinct()
    user_list = [ User.objects.get(id=id[0]) for id in user_ids ]
    simililarities = Similarity.objects.filter(survey=Survey.objects.get(survey_id=request.GET.get('survey-id')))
    user_index = user_list.index(User.objects.get(id=request.GET.get('user-id')))
    similarity_row = []
    for index, other_user in enumerate(user_list):
        similarity_row.append([other_user])
        if user_index >= index:
            print(user_list[user_index], ' - ', other_user)
            similarity_row[index].append(round(simililarities.get(user_1=user_list[user_index], user_2=other_user).value * 100, 2))
        else:
            print(user_list[user_index], ' - ', other_user)
            similarity_row[index].append(round(simililarities.get(user_1=other_user, user_2=user_list[user_index]).value * 100, 2))
    context = { 
        'user_list': user_list, 
        'similarity_row': similarity_row, 
        'current_user': user_list[user_index], 
        'survey_id': request.GET.get('survey-id') 
    }
    print(context)
    return render(request, 'survey/find_similarity_to.html', context=context)