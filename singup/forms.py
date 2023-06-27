from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Student, Teacher, TeacherClass, StudentClass, Marks

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'style': 'width:300px'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'style': 'width:300px'}), max_length=32)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'style': 'width:300px'}), max_length=32)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'style': 'width:300px'}), max_length=64)
    dateofbirth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Date of birth', 'style': 'width:300px'}))
    youare = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:100px'}), choices=(('Teacher', 'Teacher'), ('Student', 'Student')))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'width:300px'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again', 'style': 'width:300px'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'youare', 'dateofbirth')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username', 'style': 'width:300px'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'style': 'width:300px'}))


class TeacherClassForm(forms.ModelForm):
    class Meta:
        model = TeacherClass
        fields = '__all__'

class StudentClassForm(forms.ModelForm):
     class Meta:
          model = StudentClass
          fields = ['student', 'assignclass']



class MarksForm(forms.Form):
    classes = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        teacher_username = kwargs.pop('request').user.username
        super(MarksForm, self).__init__(*args, **kwargs)

        # Set choices for classes field
        classes_choices = TeacherClass.objects.filter(teacher=teacher_username).values_list('assigned', 'assigned')
        self.fields['classes'].choices = classes_choices

# class AddMarksForm(forms.ModelForm):
#     class Meta:
#         model = Marks
#         fields = ['username', 'exam_type', 'maths', 'science', 'labs', 'sports']
#         widgets = {
#             'username': forms.Select(attrs={'class': 'form-control', 'required': False})
#         }
class AddMarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['username', 'exam_type', 'maths', 'science', 'labs', 'sports']
        widgets = {
            'username': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        username_choices = kwargs.pop('username_choices')
        super(AddMarksForm, self).__init__(*args, **kwargs)
        self.fields['username'].choices = username_choices
        self.fields['username'].required = False  # Add this line to make the field optional




        # Set choices for username field (based on selected class)
        # if self.data.get('classes'):
        #     selected_class = self.data['classes']
        #     username_choices = StudentClass.objects.filter(assignclass=selected_class).values_list('student', 'student')
        #     self.fields['username'].choices = username_choices





class ResetPasswordForm(forms.Form):
        username = forms.CharField(label="User Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username', 'style': 'width:300px'}))
        newpassword = forms.CharField(label="New Password",  widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'style': 'width:300px'}))
        confirmpassword = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'style': 'width:300px'}))
        
