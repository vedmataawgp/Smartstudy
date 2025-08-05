from django import forms
from .models import Doubt
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class DoubtSubmissionForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter doubt title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your doubt in detail'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'title',
            'description',
            Field('image', help_text='Optional: Upload an image if it helps explain your doubt'),
            Submit('submit', 'Submit Doubt', css_class='btn btn-primary')
        )

class DoubtResolutionForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['resolution']
        widgets = {
            'resolution': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Provide detailed resolution'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Resolve Doubt', css_class='btn btn-success'))