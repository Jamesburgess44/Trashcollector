from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.apps import apps
from .models import Employee
import calendar
from datetime import date
# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')
    return render(request, 'employees/index.html')


def employee_signup(request):
    if request.method == 'POST':
        employee_name = request.POST.get('name')
        employee_zip_code = request.POST.get('employee_zip_code')
        new_employee = Employee(name=employee_name, employee_zip_code=employee_zip_code, user=request.user)
        new_employee.save()

        return redirect('/employees/')
    else:
        return render(request, 'employees/employee_signup_information.html')


# TODO: make url link, add to index?html page to give place for table to populate,
# def employee_landing_view():
# table_of_customers = []
# identify specific employee to use zip
# identify all customers
# sql search
#      cust zip == this_employee_zip
#       (cust pickup day OR one time pickup == today) AND... cust_account_active = True
#
#
def employee_home_view(request):
    user = request.user
    active_employee = Employee.objects.get(user_id=user.id)
    customer_model = apps.get_model('customers.Customer')
    all_customers = customer_model.objects.all()
    curr_date = date.today()
    day_of_the_week = calendar.day_name[curr_date.weekday()]
    todays_customers = []
    for customer in all_customers:
        if customer.customer_zip_code == active_employee.employee_zip_code and (customer.weekly_pickup_day or customer.onetime_pickup_date == day_of_the_week) and customer.start_suspension_date is None:
            todays_customers.append(customer)
    context = {
        "todays_customers": todays_customers
    }
    return render(request, 'employees/index.html', context)



