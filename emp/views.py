from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Role, Department
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    if request.user.is_authenticated: 
        first_name = request.user.first_name 
        return render(request, 'index.html',{'first_name':first_name})
    messages.warning(request, "First Login Then Try Agin!!")
    return render(request, 'login.html')


def all_emp(request):
    if request.user.is_authenticated:
        emps = Employee.objects.all()
        context = {
            'emps':emps
        }
        return render(request, 'all_emp.html', context)
    messages.warning(request, "First Login Then Try Agin!!")
    return render(request, 'login.html')

def add_emp(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dept_id = request.POST.get('dept')
            salary = request.POST.get('salary')
            bonus = request.POST.get('bonus')
            role_id = request.POST.get('role')
            phone = request.POST.get('phone')
       
            dept = get_object_or_404(Department, id=dept_id)
            role = get_object_or_404(Role, id=role_id)


            emp = Employee(first_name=first_name, last_name=last_name, dept=dept, salary=salary, bonus=bonus, role=role, phone=phone, hire_date=datetime.now())
            emp.save()

            messages.success(request, "The New Employee is Added Succesfullly!!")
            return redirect("all_emp")
        return render(request, 'add_emp.html')
    messages.warning(request, "First Login Then Try Agin!!")
    return render(request, 'login.html')

def remove_emp(request, emp_id = 0):
    if request.user.is_authenticated:
        if emp_id:
            try:
                emp_to_be_removed = Employee.objects.get(id = emp_id)
                emp_to_be_removed.delete()
                messages.success(request, "Employee Is Remove Succesfully!!")
                return redirect('all_emp')
            except:
                return HttpResponse("Please Enter a Valid EMP ID")

        emps = Employee.objects.all()
        context = {
          'emps':emps
        }

        return render(request, 'remove_emp.html', context)
    return render(request, 'login.html')

def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
            print(emps)
            
        if dept:
            emps = emps.filter(dept__name__icontains = dept)

        if role:
            emps = emps.filter(role__name = role)

        context = {
            "emps" : emps
        }
        return render(request, 'all_emp.html', context)

    return render(request, 'filter_emp.html')


def update_emp(request,id):
    emp = Employee.objects.get(id=id)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = request.POST['salary']
        bonus = request.POST['bonus']
        phone = request.POST['phone']

        emp = Employee.objects.get(id=id)
        emp.first_name = first_name
        emp.last_name = last_name
        emp.salary = salary
        emp.bonus = bonus
        emp.phone = phone
        emp.save()
        messages.success(request, "Employee Is Updated Succesfully!!")
        return redirect('all_emp')
    return render(request, 'update_emp.html', {'emp':emp})
        

def Login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser  = User.objects.create_user(username, email, pass1)
        myuser.save()

        messages.success(request, "Your Account has been Succesfully created!!")
        return redirect('signin')

    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username = username, password = pass1)
          
        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'index.html', {'first_name':username})

        else:
            messages.error(request, "Bad Creadentials!")
            return redirect('login')

    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Succesfully!!")
    return redirect('login')