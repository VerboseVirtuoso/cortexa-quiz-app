from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Quiz, Question, Option, QuizAttempt
from .forms import QuestionForm, OptionFormSet

class HomeView(ListView):
    model = Quiz
    template_name = 'quiz/home.html'
    context_object_name = 'quizzes'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Quiz.objects.filter(is_active=True)
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
            
        return queryset.order_by('-created_at')

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['title', 'description', 'is_active']
    template_name = 'quiz/quiz_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Quiz created successfully! Now let's add your first question.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_question', kwargs={'pk': self.object.pk})

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'

    def get(self, request, *args, **kwargs):
        quiz = self.get_object()
        leaderboard = QuizAttempt.objects.filter(quiz=quiz).order_by('-percentage', 'created_at')[:5]
        return render(request, self.template_name, {'quiz': quiz, 'leaderboard': leaderboard})

class QuizUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    fields = ['title', 'description', 'is_active']
    template_name = 'quiz/quiz_form.html'
    
    def test_func(self):
        quiz = self.get_object()
        return self.request.user == quiz.created_by

    def form_valid(self, form):
        messages.success(self.request, "Quiz updated successfully!")
        return super().form_valid(form)

class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    template_name = 'quiz/quiz_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        quiz = self.get_object()
        return self.request.user == quiz.created_by

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, "Quiz deleted successfully.")
        return super().delete(request, *args, **kwargs)

class RegisterView(UserPassesTestMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'quiz/register.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        return redirect('dashboard')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"Welcome to Cortexa, {self.object.username}!")
        return valid

class UserLoginView(UserPassesTestMixin, LoginView):
    template_name = 'quiz/login.html'
    redirect_authenticated_user = True
    
    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        return redirect('dashboard')

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quizzes'] = Quiz.objects.filter(created_by=self.request.user)
        context['created_quizzes'] = Quiz.objects.filter(created_by=self.request.user).annotate(avg_percentage=Avg('attempts__percentage'))
        context['user_attempts'] = QuizAttempt.objects.filter(user=self.request.user).order_by('-created_at')
        return context
class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/question_form.html'

    def test_func(self):
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        return self.request.user == quiz.created_by

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['options'] = OptionFormSet(self.request.POST)
        else:
            data['options'] = OptionFormSet()
        data['quiz'] = Quiz.objects.get(pk=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        options = context['options']
        quiz = context['quiz']
        
        if options.is_valid():
            self.object = form.save(commit=False)
            self.object.quiz = quiz
            self.object.save()
            options.instance = self.object
            options.save()
            messages.success(self.request, "Question added successfully!")
            
            if 'save_and_add' in self.request.POST:
                return redirect('add_question', pk=quiz.pk)
            return redirect('quiz_detail', pk=quiz.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/question_form.html'

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.quiz.created_by

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['options'] = OptionFormSet(self.request.POST, instance=self.object)
        else:
            data['options'] = OptionFormSet(instance=self.object)
        data['quiz'] = self.object.quiz
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        options = context['options']
        
        if options.is_valid():
            self.object = form.save()
            options.instance = self.object
            options.save()
            messages.success(self.request, "Question updated successfully!")
            return redirect('quiz_detail', pk=self.object.quiz.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'quiz/question_confirm_delete.html'

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.quiz.created_by

    def get_success_url(self):
        messages.success(self.request, "Question deleted successfully!")
        return reverse_lazy('quiz_detail', kwargs={'pk': self.object.quiz.pk})

class QuizStartView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_start.html'
    context_object_name = 'quiz'

    def get_queryset(self):
        return Quiz.objects.filter(is_active=True)

class QuizSubmitView(View):
    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return redirect('home')
            
        score = 0
        for question in quiz.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    if selected_option.is_correct:
                        score += 1
                except Option.DoesNotExist:
                    pass
        total_questions = quiz.questions.count()
        percentage = (score / total_questions * 100) if total_questions > 0 else 0.0
        
        if request.user.is_authenticated:
            QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                total_questions=total_questions,
                percentage=percentage
            )
        
        return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'score': score})
