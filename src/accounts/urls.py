from django.urls import path
from accounts import views
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import views as auth_views


urlpatterns = [

    path('validate-username',csrf_exempt(views. UsernameValidation.as_view()),name='validate-username'),
    
    path('validate-email',csrf_exempt(views.EmailValidation.as_view()),name='validate-email'),

    path('validate-password',csrf_exempt(views.PasswordValidate.as_view()),name='validate-password'),

    path('activate/<uidb64>/<token>',views.VerificationView.as_view(),name='activate'),

    path('register/',views.signup,name='signup'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),


    # path('password_reset/',views.password_reset_request,name='password_reset'),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),name='password_reset'),

    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),name='password_reset_confirm'),

    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),name='password_reset_complete'),



    # staff user
    path('signup_staff/',views.signup_staff,name='signup_staff'),


    path('profile/',views.user_profile,name='user_profile'),

    # path('add_comment/',views.add_comment,name='add_comment'),

    # path('update_address/',views.update_address,name='update_address'),

]