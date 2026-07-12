from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text", "is_public"]  # Додали поля text та галочку is_public
        labels = {
            "text": "",
            "is_public": "",
        }
        # Додаємо стилі Bootstrap, щоб галочка та інпут виглядали красиво
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter topic name..."}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input", "style": "position: static; margin-top: 0;"}),
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {"text": ""}
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Write your entry here..."}),
        }
    