from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('quiz/new/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:pk>/edit/', views.QuizUpdateView.as_view(), name='quiz_update'),
    path('quiz/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('quiz/<int:pk>/add-question/', views.QuestionCreateView.as_view(), name='add_question'),
    path('quiz/<int:pk>/start/', views.QuizStartView.as_view(), name='quiz_start'),
    path('quiz/<int:pk>/submit/', views.QuizSubmitView.as_view(), name='quiz_submit'),
    path('question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
]