from django.urls import path
from manager_app import views

urlpatterns = [
    path('', views.home, name="home"),

    path('delete_notification/<int:notification_id>/', views.delete_notification, name="delete_notification"),
    path('schedule/', views.schedule, name="schedule"),
    
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('register_user/', views.register_user, name="register_user"),
    
    path('profile_list/', views.profile_list, name="profile_list"),
    path('update_profile/<int:profile_id>/', views.update_profile, name="update_profile"),
    path('delete_user/<int:user_id>/', views.delete_user, name="delete_user"),
    
    path('genba_list/', views.genba_list, name="genba_list"),
    path('profile_genba/', views.profile_genba, name="profile_genba"),
    path('add_genba/', views.add_genba, name="add_genba"),
    path('delete_genba/<int:genba_id>/', views.delete_genba, name="delete_genba"),
    path('genba_details/<int:genba_id>/', views.genba_details, name="genba_details"),
    
    path('report_list/', views.report_list, name="report_list"),
    path('report_details/<int:report_id>/', views.report_details, name="report_details"),
    path('add_report/', views.add_report, name="add_report"),
    path('delete_report/<int:report_id>/', views.delete_report, name="delete_report"),

    path('export_csv/', views.export_csv, name="export_csv"),
    path('export_searched/<str:keyword>/', views.export_searched, name="export_searched"),
]