from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('subject/<int:subject_id>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('lecture/<int:lecture_id>/', views.LectureDetailView.as_view(), name='lecture_detail'),
    path('lecture/<int:lecture_id>/complete/', views.MarkLectureCompleteView.as_view(), name='mark_complete'),
    path('enrollment/', views.EnrollmentView.as_view(), name='enrollment'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
]