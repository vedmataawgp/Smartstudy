from django.urls import path
from . import views

app_name = 'batches'

urlpatterns = [
    # Batch URLs
    path('', views.BatchListView.as_view(), name='list'),
    path('<int:batch_id>/', views.BatchDetailView.as_view(), name='detail'),
    path('<int:batch_id>/enroll/', views.EnrollBatchView.as_view(), name='enroll'),
    path('<int:batch_id>/purchase/', views.PurchaseBatchView.as_view(), name='purchase'),
    path('my-batches/', views.MyBatchesView.as_view(), name='my_batches'),
    path('order/<str:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    # Subject and Lecture URLs
    path('subject/<int:subject_id>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('lecture/<int:lecture_id>/', views.LectureDetailView.as_view(), name='lecture_detail'),
    
    # DPP URLs
    path('dpp/<int:dpp_id>/', views.DPPDetailView.as_view(), name='dpp_detail'),
    path('dpp/<int:dpp_id>/start/', views.StartDPPView.as_view(), name='start_dpp'),
    path('dpp/attempt/<int:attempt_id>/', views.TakeDPPView.as_view(), name='take_dpp'),
    path('dpp/results/<int:attempt_id>/', views.DPPResultsView.as_view(), name='dpp_results'),
    path('dpp/solution/<int:solution_id>/', views.DPPSolutionView.as_view(), name='dpp_solution'),
    
    # Comment URLs
    path('comment/add/', views.AddCommentView.as_view(), name='add_comment'),
    path('comment/<int:comment_id>/toggle-like/', views.ToggleCommentLikeView.as_view(), name='toggle_comment_like'),
    
    # Referral URLs
    path('validate-referral/', views.ValidateReferralView.as_view(), name='validate_referral'),
]