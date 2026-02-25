from django.contrib import admin
from .models import Quiz, Question, Option, Attempt, QuizAttempt, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('question_text',)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('option_text',)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total_questions', 'submitted_at')
    list_filter = ('quiz', 'submitted_at')
    readonly_fields = ('submitted_at',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'percentage', 'created_at')
    list_filter = ('quiz', 'created_at')
