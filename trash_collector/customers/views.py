from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .models import Customer
from .forms import customer_forms, change_pickup_form
from django.contrib import messages
from django.http import JsonResponse
import json
from django.urls import reverse


# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user
    # It will be necessary while creating a customer/employee to assign the logged-in user as the user foreign key
    # This will allow you to later query the database using the logged-in user,
    # thereby finding the customer/employee profile that matches with the logged-in user.
    return render(request, 'customers/index.html')

# ADD CHECK TO MAKE SURE APP CANT BREAK IF DAY_INPUT IS NOT INPUTTED
def customer_signup(request):
    user = request.user
    day_input = request.POST.get('day_of_week')
    customer = Customer.objects.filter(user_id=user.id)
    if customer.exists():
        return redirect("/customers/")
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        if customer_name is None:
            messages.error(request, 'Please complete all fields!')
            return redirect('/customers/customer/')
        customer_address = request.POST.get('customer_address')
        if customer_address is None:
            messages.error(request, 'Please complete all fields!')
            return redirect('/customers/customer/')
        customer_zip_code = request.POST.get('customer_zip_code')
        if customer_zip_code is None:
            messages.error(request, 'Please complete all fields!')
            return redirect('/customers/customer/')
        customer_weekly_pickup_day = day_input
        if day_input is None:
            messages.error(request, 'Please complete all fields!')
            return redirect('/customers/customer/')
        new_customer = Customer(name=customer_name, customer_address=customer_address,
                                customer_zip_code=customer_zip_code, weekly_pickup_day=customer_weekly_pickup_day,
                                user=request.user)
        new_customer.save()

        return redirect('/customers/')
    else:
        return render(request, 'customers/customer_signup_information.html')


def customer_validation(request):
    user = request.user
    customer = Customer.objects.filter(user_id=user.id)
    context = {
        'customer': customer,
        'user': user
    }
    return render(request, "customers/base.html", context)


def customer_account_info(request):
    user = request.user
    customer = Customer.objects.filter(user_id=user.id)
    if not customer.exists():
        messages.error(request, 'You must register first!')
        return redirect("/customers/customer")
    customer_info = Customer.objects.get(user_id=user.id)
    form = customer_forms(request.POST, instance=customer_info)
    if form.is_valid():
        form.save()
        messages.success(request, 'successfully saved')
        return redirect('/customers/account_info')
    context = {
        'form': form,
        'customer_info': customer_info
    }
    return render(request, "customers/account_info.html", context)


def change_pickup_day(request):
    user = request.user
    day_input = request.POST.get('day_of_week')
    customer = Customer.objects.filter(user_id=user.id)
    if not customer.exists():
        messages.error(request, 'You must register first!')
        return redirect("/customers/customer")
    customer_info = Customer.objects.get(user_id=user.id)
    form = change_pickup_form(request.POST, instance=customer_info)
    if form.is_valid():
        if day_input is not None:
            customer_info.weekly_pickup_day = day_input
        form.save()
        messages.success(request, 'successfully saved')
        return redirect('/customers/weekly_pickup/')
    context = {
        'form': form,
        'customer_info': customer_info
    }
    return render(request, "customers/customer_change_pickup_day.html", context)


def complete_purchase(request):
    body = json.loads(request.body)
    print('BODY:', body)
    customer = Customer.objects.get(id=body['customer_id'])
    if customer.customer_balance > 0:
        customer.customer_balance = 0
        customer.save()
        return redirect('/customers/account_info/')
    else:
        return redirect('/customers/account_info/')
