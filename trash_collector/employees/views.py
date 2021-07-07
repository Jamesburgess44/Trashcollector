from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.apps import apps
from .models import Employee
import calendar
from datetime import date
from django.contrib import messages
# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')
    return render(request, 'employees/index.html')


def employee_signup(request):
    user = request.user
    employee = Employee.objects.filter(user_id=user.id)
    if employee.exists():
        return redirect("/employees/")
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
    active_employee = Employee.objects.filter(user_id=user.id)
    if not active_employee.exists():
        return redirect('/employees/employee')
    customer_model = apps.get_model('customers.Customer')
    employee_info = Employee.objects.get(user_id=user.id)
    all_customers = customer_model.objects.all()
    curr_date = date.today()
    day_of_the_week = calendar.day_name[curr_date.weekday()]
    todays_customers = []
    for customer in all_customers:
        if (customer.customer_zip_code == employee_info.employee_zip_code) and (customer.weekly_pickup_day.lower() == day_of_the_week.lower() or customer.onetime_pickup_date == day_of_the_week.lower()) and (customer.start_suspension_date is None):
            todays_customers.append(customer)
    context = {
        "todays_customers": todays_customers
    }
    return render(request, 'employees/index.html', context)

# CHOOSE BY DAY CHANGE LINE 73 TO ACTUAL DATE FOR ONETIME PICKUP DATE
def choose_by_day(request):
    days_of_week = {'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'}
    user = request.user
    day_input = request.GET.get('day_of_week')
    for day in days_of_week:
        if day.lower() == day_input.lower():
            customer_model = apps.get_model('customers.Customer')
            employee_info = Employee.objects.get(user_id=user.id)
            all_customers = customer_model.objects.all()
            search_by_day = []
            for customer in all_customers:
                if (customer.customer_zip_code == employee_info.employee_zip_code) and (
                        customer.weekly_pickup_day.lower() == day.lower() or customer.onetime_pickup_date == day.lower()) and (customer.start_suspension_date is None):
                    search_by_day.append(customer)
            context = {
                "search_by_day": search_by_day
            }
            return render(request, 'employees/search_by_day.html', context)
    else:
        return redirect('/employees/')

# MAKE SURE TO MAKE CONDITIONAL FOR IF CUSTOMER ACCOUNT IS SUSPENDED


def confirm_pickup(request, customer_id):
    employee_confirm_pickup = request.GET.get('confirm_pickup')
    customer = apps.get_model('customers.Customer')
    customer_update = customer.objects.get(user_id=customer_id)
    if customer_update.weekly_pickup_confirmed is False:
        if employee_confirm_pickup.lower() == 'yes':
            customer_update.customer_balance += 5
            customer_update.weekly_pickup_confirmed = True
            customer_update.save()
            return redirect('/employees/')
    elif employee_confirm_pickup.lower() == 'no':
        customer_update.weekly_pickup_confirmed = False
        customer_update.save()
        return redirect('/employees/')

    return redirect('/employees/')
