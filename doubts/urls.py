from django.urls import path
from . import views

app_name = 'doubts'

urlpatterns = [
    path('', views.DoubtListView.as_view(), name='list'),
    path('submit/', views.SubmitDoubtView.as_view(), name='submit'),
    path('<int:doubt_id>/', views.DoubtDetailView.as_view(), name='detail'),
    path('<int:doubt_id>/resolve/', views.ResolveDoubtView.as_view(), name='resolve'),
    path('my-doubts/', views.MyDoubtsView.as_view(), name='my_doubts'),
    path('teacher-dashboard/', views.TeacherDoubtDashboard.as_view(), name='teacher_dashboard'),
]