from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='list'),
    path('<int:quiz_id>/', views.QuizDetailView.as_view(), name='detail'),
    path('<int:quiz_id>/start/', views.StartQuizView.as_view(), name='start'),
    path('<int:quiz_id>/submit/', views.SubmitQuizView.as_view(), name='submit'),
    path('attempt/<int:attempt_id>/results/', views.QuizResultsView.as_view(), name='results'),
    path('my-attempts/', views.MyAttemptsView.as_view(), name='my_attempts'),
]