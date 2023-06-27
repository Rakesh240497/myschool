from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm, SignUpForm, TeacherClassForm, ResetPasswordForm, StudentClassForm, MarksForm, AddMarksForm
from django.contrib.auth.models import User
from .models import Teacher, Student, TeacherClass, StudentClass, Marks



# Create your views here.
def usercreation(request):
    form = SignUpForm()
    if request.method == 'POST': 
        form = SignUpForm(request.POST)
        if form.is_valid():
            youare = form.cleaned_data.get('youare')
            if youare == "Student":
                username = form.cleaned_data.get('username')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                dateofbirth = form.cleaned_data.get('dateofbirth')
                Student.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, dateofbirth=dateofbirth)
            if youare == "Teacher":
                username = form.cleaned_data.get('username')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                dateofbirth = form.cleaned_data.get('dateofbirth')
                Teacher.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, dateofbirth=dateofbirth)
            form.save()
            messages.success(request, 'Your account as been created')
            # username = form.cleaned_data.get('username')
            # raw_pass = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_pass)
            # login(request, user)
            return HttpResponse('Your account has been created succesfully <a href="login">Click Here to login</a>')
    context = {'form': form}
    return render(request, 'singup.html', context) 


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=raw_password)
                check1 = Teacher.objects.filter(username=username).exists()
                check2 = Student.objects.filter(username=username).exists()
                # print(check1, check2)
                if user is not None and check1:
                    auth_login(request, user)
                    tea_details = Teacher.objects.get(username=username)
                    query = TeacherClass.objects.filter(teacher=username)
                    print(query)
                    context = {
                        'details': tea_details,
                        'teaches': query.values_list('assigned', flat=True)
                    }
                    return render(request, "teacher/teacherhome.html", context)
                if user is not None and check2:
                    auth_login(request, user)
                    stu_details = Student.objects.get(username=username)
                    context = {'details': stu_details}
                    return render(request, "student/studenthome.html", context)
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Form is not valid')
        except Exception as e:
            messages.error(request, 'Something went wrong: {}'.format(str(e)))
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'signin.html', context)


def requests(request):
    return HttpResponse('%s' %(request.user.username))

def logout(request):
    auth_logout(request)
    return render(request, "logout.html")

def check(request):
    if request.user.is_autheticated():
        return HttpResponse('%s' %(request.user.username))

def teacherhome(request, username=None):
    username = request.user.username
    tea_details = Teacher.objects.get(username=username)
    query = TeacherClass.objects.filter(teacher=username)
    # print(query)
    context = {
        'details': tea_details,
        'teaches': query.values_list('assigned', flat=True)
    }
    return render(request, "teacher/teacherhome.html", context)

def studenthome(request, username=None):
    username = request.user.username
    tea_details = Student.objects.get(username=username)
    # query = TeacherClass.objects.filter(assigned=username)
    # print(query)
    context = {
        'details': tea_details,
        # 'class': query.values_list('assigned', flat=True)
    }
    return render(request, "student/studenthome.html", context)

def resetpassword(request):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('newpassword')
            password2 = form.cleaned_data.get('confirmpassword')
            if password1 != password2:
                messages.error(request, "Both passwords are not the same")
            else:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(password1)
                    user.save()
                    messages.success(request, "Password has been updated")
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, "User does not exist")
        else:
            messages.error(request, "Form is not valid")
    
    context = {
        'form': form,
        'messages': messages.get_messages(request),
    }
    return render(request, 'resetpassword.html', context)





def admin_login(request):
    form = TeacherClassForm()
    context = {'form': form}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login Sussesfull')
            return render(request, "teacher/teacherclass.html", context)
        else:
            messages.error(request, 'Enter Valid Creadentials')
    return render(request, "admin.html")




def addteacher(request):
    form = TeacherClassForm()
    context = {'form': form}
    
    if request.method == 'POST':
        form = TeacherClassForm(request.POST)
        
        try:
            if form.is_valid():
                check1 = form.cleaned_data['teacher']
                check2 = form.cleaned_data['assigned']
                query = TeacherClass.objects.filter(teacher=check1)
                
                if 'checklist' in request.POST:
                    context = {'form': form}
                    if query.exists():
                        assigned_classes = query.values_list('assigned', flat=True)
                        context['list'] = assigned_classes
                    else:
                        messages.error(request, 'Teacher does not exist')
                    return render(request, "teacher/teacherclass.html", context)
                
                if query.exists():
                    if check2 not in query.values_list('assigned', flat=True):
                        form.save()
                        messages.success(request, 'Teacher assigned successfully')
                    else:
                        messages.error(request, 'Teacher has already been assigned to this class')
                else:
                    messages.error(request, 'Teacher does not exist')
                    
                return render(request, "teacher/teacherclass.html", context)
        
        except Exception as e:
            messages.error(request, 'Something went wrong: {}'.format(str(e)))
    
    return render(request, "teacher/teacherclass.html", context)



def addstudent(request):
    form = StudentClassForm()
    context = {'form': form}
    if request.method == 'POST':
        form = StudentClassForm(request.POST)
        try:
            if form.is_valid():
                check1 = request.POST.get('student')
                check2 = request.POST.get('assignclass')
                temp = request.user.username
                query2 = TeacherClass.objects.filter(teacher=temp)
                query = StudentClass.objects.filter(student=check1)
                if not query2:
                    messages.error(request, "No class assinged to you yet, you don't have the permission to assign classes")
                elif query2.exists():
                    if check2 not in query2.values_list('assigned', flat=True):
                        messages.error(request, "Please assign students to classes you have been assigned.!")
                    elif query.exists():
                        if len(query.values_list('assignclass', flat=True))>0:
                            messages.error(request,"The student is assigned to other class please check. ")
                    elif check2 not in query.values_list('assignclass', flat=True):
                            form.save()
                            # print(len(query.values_list('assignclass', flat=True)))
                            messages.success(request, 'Student Assigned Succesfully!')
                    else:
                        messages.error(request, 'Student has already added to this class')
                else :
                    form.save()
                    messages.success(request, 'Student Added!')
                return render(request, "teacher/studentclass.html", context)
        except Exception as e:
            messages.error(request, 'Something went wrong: {}'.format(str(e)))
    return render(request, "teacher/studentclass.html", context)

def selectclass(request):
    context = {}
    if request.method == 'POST':
        form = MarksForm(request.POST, request=request)
        if form.is_valid():
            temp = form.cleaned_data['classes']
            # Process successful form submission
            # return HttpResponse('success %s' % temp)
            return redirect('enter_marks', selected_class = temp)
    else:
        form = MarksForm(request=request)
        context = {'form': form}

    return render(request, "teacher/temp.html", context)

def enter_marks(request, selected_class):
    students = StudentClass.objects.filter(assignclass=selected_class)
    username_choices = [(student.student, student.student) for student in students]

    if request.method == 'POST':
        form = AddMarksForm(request.POST, username_choices=username_choices)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.total = instance.maths + instance.science + instance.labs + instance.sports
            instance.pf = True if instance.total > 35 else False
            instance.save()
            return HttpResponse('Marks saved successfully')
    else:
        form = AddMarksForm(username_choices=username_choices)

    context = {
        'form': form,
        'selected_class': selected_class,
        'students': students
    }
    return render(request, "teacher/enter_marks.html", context)

def examresults(request):
    context = {}
    try:
        query = Marks.objects.filter(username=request.user.username)
        print(query, request.user.username)
        if query:
            context = {'results': query}  # Use 'results' instead of 'result' for multiple objects
            return render(request, "student/examresults.html", context)
        else:
            return HttpResponse("Your score is not updated yet")
    except Exception as e:
        messages.error(request, 'Something went wrong: {}'.format(str(e)))

    return render(request, "student/examresults.html", context)


        

# def addmarks(request):
#     context = {}

#     if request.method == 'POST':
#         form = MarksForm(request.POST)
#         # classes = request.POST.get('class')
#         # username = request.POST.get('username')
#         # exam_type = request.POST.get('exam_type')
#         # maths = float(request.POST.get('maths'))
#         # science = float(request.POST.get('science'))
#         # labs = float(request.POST.get('labs'))
#         # sports = float(request.POST.get('sports'))
#         # marksinstance = Marks(classes=classes, username=username, exam_type=exam_type, maths=maths, science=science, labs=labs, sports=sports)
#         # marksinstance.save()
#         # messages.success(request, 'Marks added Successfully!')
#         # return redirect('addmarks')
        
#     else:
#         form = MarksForm(request=request)
#         context['form'] = form
#     return render(request, "teacher/admarks.html", context)
#     # if request.method == 'GET' and 'get_usernames' in request.GET:
#     #     username = request.user.username
#     #     print(username)
#     #     classes_choice = TeacherClass.objects.filter(teacher=username)

#     #     if not classes_choice.exists():
#     #         messages.error(request, 'There is no class assigned to you yet!')
#     #     else:
#     #         selected_class = request.GET.get('class')
#     #         print(selected_class)
#     #         query = StudentClass.objects.filter(assignclass=selected_class).values_list('student', flat=True)
#     #         context['username'] = query

#     # classes_choice = TeacherClass.objects.filter(teacher=request.user.username)
#     # if not classes_choice.exists():
#     #     messages.error(request, 'There is no class assigned to you yet!')
#     # else:
#     #     classes = classes_choice.values_list('assigned', flat=True)
#     #     context['classes'] = classes

#     # return render(request, "teacher/addmarks.html", context)


    

        
        



        



