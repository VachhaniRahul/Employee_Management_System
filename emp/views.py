from django.shortcuts import render, get_object_or_404
from .models import Employee, Role, Department
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    return render(request, 'all_emp.html', context)

def add_emp(request):
    

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

        return HttpResponse("New Employee Added Succesfully !!")
    return render(request, 'add_emp.html')

def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id = emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Succesfully !!")
        except:
            return HttpResponse("Please Enter a Valid EMP ID")

    emps = Employee.objects.all()
    context = {
        'emps':emps
    }

    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        print(name)
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        print(emps)
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