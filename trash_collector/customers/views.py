from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Customer
from .forms import customer_forms
# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user
    # It will be necessary while creating a customer/employee to assign the logged-in user as the user foreign key
    # This will allow you to later query the database using the logged-in user,
    # thereby finding the customer/employee profile that matches with the logged-in user.
    print(user)
    return render(request, 'customers/index.html')


def customer_signup(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    form = customer_forms(request.POST, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('/accounts/login/')
    context = {
        'form': form
    }
    return render(request, "customers/customer_signup_information.html", context)
