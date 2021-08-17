from django.urls import path
from .views import admin_index,all_customers,all_customers_export_as_csv,all_customers_export_as_pdf,customers_area_graph,FoodCreateView,all_menu_display_admin,single_menu_admin,edit_single_menu_admin,logout_admin,all_orders_admin,course_menu_count

urlpatterns = [

    path('admin_logout/',logout_admin,name='logout_admin'),

    path('',admin_index,name='admin_index'),
    path('all_customers/',all_customers,name='all_customers'),
    path('export_customers_csv/',all_customers_export_as_csv,name='export_customers_csv'),
    path('export_customers_pdf/',all_customers_export_as_pdf,name='export_customers_pdf'),
    path('customers_area_graph/',customers_area_graph,name='customers_area_graph'),

    path('add_food/',FoodCreateView.as_view(),name='add_food'),
    path('all_foods_admin/',all_menu_display_admin,name='all_foods_admin'),
    path('course_menu_count/',course_menu_count,name='course_menu_count'),
    path('single_food_admin/<int:id>',single_menu_admin,name='single_menu_admin'),
    path('edit_single_food_admin/<str:pk>',edit_single_menu_admin.as_view(),name='edit_single_food_admin'),


    path('all_orders_admin',all_orders_admin,name='all_orders_admin')


]