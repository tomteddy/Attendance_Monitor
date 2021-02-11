from django.shortcuts import render, redirect
from employees.models import User, Employee, Company, Work_log
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def homepage(request):
    employee_list = []
    count = 1
    users = User.objects.all()
    for user in users:
        if Employee.objects.filter(user=user).exists():
            employee = Employee.objects.get(user=user)
            employee.name = user.name
            employee.email = user.email
            employee.sl = count
            employee_list.append(employee)
            count = count + 1
            
    if request.method == 'POST' and request.POST['form'] == 'email':
        emp_email = request.POST.get('emp_email', False)
        emp_user = User.objects.get(email = emp_email)
        request.session['name'] = emp_user.name
        emp = Employee.objects.get(user=emp_user)
        request.session['position'] = emp.position
        worklogs = Work_log.objects.filter(employee = emp)
        count = 1
        for log in worklogs:
            log.sl = count
            count = count + 1
        return render(request, 'emp_dates.html', {'logs':worklogs, 'name': emp_user.name})

    if request.method == 'POST' and request.POST['form'] == 'profile_show':
        emp_email = request.POST.get('emp_email', False)
        emp_user = User.objects.get(email = emp_email)
        emp = Employee.objects.get(user=emp_user)
        emp.comp = emp.company.name
        worklogs = Work_log.objects.filter(employee = emp)
        return render(request, 'emp_profile.html', {'logs':worklogs, 'user': emp_user, 'details': emp})


    if request.method == 'POST' and request.POST['form'] == 'worklogid':
        log_id = request.POST.get('work_log_id', False)
        log = Work_log.objects.get(work_log_id = log_id)
        name = request.session.get('name')
        position = request.session.get('position')
        log.name = name
        log.position = position
        return render(request, 'work_log.html', {'log':log})

    return render(request, 'admin_home.html', {'employee_list':employee_list})

def logoutadmin(request):
    logout(request)
    return redirect('index')