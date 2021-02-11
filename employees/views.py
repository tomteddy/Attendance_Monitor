from django.shortcuts import render, redirect
from .forms import UserForm, EmployeeForm, WorkForm
from .models import User, Employee, Company, Work_log
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        email = request.user.email
        user = User.objects.get(email=email)
        if Employee.objects.filter(user=user).exists():
            emp = Employee.objects.get(user=user)
            request.session['email'] = email
            if not emp.details:
                return redirect('details')
            else:
                return redirect('homepage')
        elif user.is_superuser:
            return redirect('admin_homepage')


    if request.method == 'POST' and request.POST.get('login', False) == 'Login':
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        if User.objects.filter(email=email).exists():
            user1 = authenticate(request, email=email, password=password)
            if (user1 is not None):
                user = User.objects.get(email=email)
                if Employee.objects.filter(user=user).exists():
                    emp = Employee.objects.get(user=user)
                    request.session['email'] = email
                    if not emp.details:
                        return redirect('details')
                    else:
                        return redirect('homepage')
                elif user.is_superuser:
                    return redirect('admin_homepage')
    return render(request, 'index.html')

def logoutuser(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            if User.objects.filter(email=email).exists() == False:
                user = User.objects.create_user(name=name, email = email, password = password)
                user.save()
                user = authenticate(request, email=email,password=password)
                if (user is not None):
                    login(request,user)
                request.session['email'] = email
                return redirect('details')

    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form, 'heading': 'Signup form'})

def details(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            date_of_birth = form.cleaned_data.get('date_of_birth')
            blood_group = form.cleaned_data.get('blood_group')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')
            position = form.cleaned_data.get('position')
            company = form.cleaned_data.get('company')
            email = request.session.get('email')
            comp = Company.objects.get(name=company)

            user = User.objects.get(email=email)
            employee = Employee.objects.create(user = user,blood_group=blood_group,date_of_birth=date_of_birth,address=address,phone_number=phone_number,position=position,company=comp, details=True)
            employee.save()
            return redirect('homepage')
    else:
        form = EmployeeForm()
    return render(request, 'signup.html', {'form': form, 'heading': 'Details form'})

def homepage(request):
    email = request.session.get('email')
    user = User.objects.get(email=email)
    emp = Employee.objects.get(user=user)

    if request.method == 'POST' and request.POST.get('work', False) == 'start':
        work_log = Work_log.objects.create(employee = emp)
        log_id = work_log.work_log_id
        work_log.save()
        emp.work_log_id = log_id
        emp.working = True
        emp.save(update_fields=['work_log_id','working'])
        return redirect('homepage')

    if request.method == 'POST' and request.POST.get('work', False) == 'end':
        return redirect('end_work')
        
    if not emp.working:
        return render(request, 'homepage.html', {'work':'ended' ,'name':user.name, 'pos': emp.position})
    elif emp.working:
        return render(request, 'homepage.html', {'work':'started' ,'name':user.name, 'pos': emp.position})


def end_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            worked_on = form.cleaned_data.get('worked_on')
            work_description = form.cleaned_data.get('work_description')
            work_file = form.cleaned_data.get('work_file')
            
            email = request.session.get('email')
            user = User.objects.get(email=email)
            emp = Employee.objects.get(user=user)

            work_id = emp.work_log_id
            emp.working = False
            emp.save(update_fields=['working'])
            work_log = Work_log.objects.get(work_log_id = work_id)
            work_log.worked_on = worked_on
            work_log.work_description = work_description
            work_log.end_time = timezone.now()
            work_log.work_file = work_file
            work_log.save(update_fields=['worked_on','work_description','end_time','work_file'])
            return redirect('homepage')
            
    else:
        form = WorkForm()
    return render(request, 'signup.html', {'form': form, 'heading': 'Work form'})


