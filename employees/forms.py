from django import forms

from .models import Employee

class UserForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not name or not email or not confirm_password or not password:
            raise forms.ValidationError('Fill all the fields!')
        if password != confirm_password:
            raise forms.ValidationError("Passwords doesn't match!")

class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs['class'] = 'css_class' 
    class Meta:
        model = Employee
        exclude = ['user','details','working','work_log_id']
        help_texts = {
                'date_of_birth': ('format = yyyy-mm-dd'),
        }

class WorkForm(forms.Form):
    worked_on = forms.CharField(max_length=200)
    work_description = forms.CharField(widget=forms.Textarea, required=False)
    work_file = forms.FileField(
        required=False,
        help_text='upload work files'
    )