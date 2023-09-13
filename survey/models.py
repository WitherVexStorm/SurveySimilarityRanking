from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Survey(models.Model):
    survey_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    survey_name = models.CharField(unique=True, max_length=30)
    
    def get_id(self):
        return self.survey_name.split(':')[0]

    def __str__(self):
        return self.survey_name

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.survey.survey_name.split(':')[0] + '@' + self.text

class Answer(models.Model):
    class MultipleChoiceAnswer(models.IntegerChoices):
        NONE = 0, 'NONE'
        ONE = 1, 'ONE'
        TWO = 2, 'TWO'
        THREE = 3, 'THREE'
        FOUR = 4, 'FOUR'
        FIVE = 5, 'FIVE'
        SIX = 6, 'SIX'
        SEVEN = 7, 'SEVEN'
        EIGHT = 8, 'EIGHT'
        NINE = 9, 'NINE'
        TEN = 10, 'TEN'
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.IntegerField(choices=MultipleChoiceAnswer.choices, default=MultipleChoiceAnswer.NONE)

    def __str__(self):
        return f'{ self.question } -> { self.answer }'

class Similarity(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user_1 = models.ForeignKey(User, related_name='user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='user_2', on_delete=models.CASCADE)
    value = models.FloatField(default=0)

    def __str__(self):
        return self.user_1.username + ' - ' + self.user_2.username + ' = ' + str(self.value)