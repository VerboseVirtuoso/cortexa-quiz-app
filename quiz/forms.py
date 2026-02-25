from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, Option

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter your question here...',
                'class': 'vibrant-textarea'
            }),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']
        widgets = {
            'option_text': forms.TextInput(attrs={
                'placeholder': 'Option text',
                'class': 'vibrant-input'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'vibrant-checkbox'
            }),
        }

OptionFormSet = inlineformset_factory(
    Question, 
    Option, 
    form=OptionForm,
    extra=4, 
    can_delete=False,
    min_num=4, 
    validate_min=True,
    max_num=4, 
    validate_max=True
)

class BaseOptionFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        correct_answers = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE'):
                if form.cleaned_data.get('is_correct'):
                    correct_answers += 1
        
        if correct_answers == 0:
            raise forms.ValidationError("You must mark exactly one option as correct.")
        if correct_answers > 1:
            raise forms.ValidationError("You can only mark one option as correct.")

OptionFormSet = inlineformset_factory(
    Question, 
    Option, 
    form=OptionForm,
    formset=BaseOptionFormSet,
    extra=4, 
    can_delete=False,
    min_num=4, 
    validate_min=True,
    max_num=4, 
    validate_max=True
)
