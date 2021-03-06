from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.employee_home_view, name="index"),
    path('employee/', views.employee_signup, name="employee_signup"),
    path('search_by_day/', views.choose_by_day, name="choose_by_day"),
    path('pickup_confirm/<int:customer_id>/', views.confirm_pickup, name="confirm_pickup")
]
