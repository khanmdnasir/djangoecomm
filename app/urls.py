# from app.forms import LoginForm
from django.urls import path
from app import views
from .forms import AuthenticationForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
    path('', views.home,name='home'),
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    path('accounts/password_change',PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm),name="changepassword"),
    path('accounts/password_change/done',PasswordChangeDoneView.as_view(template_name='app/passChangeDone.html'),name="password_change_done"),
    path('accounts/password_reset/',PasswordResetView.as_view(template_name="app/password_reset.html",form_class=MyPasswordResetForm),name="password_reset"),
    path('accounts/password_reset/done/',PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"),name="password_reset_done"),
    path('accounts/reset/done/',PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"),name="password_reset_complete"),
    path('accounts/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html",form_class=MySetPasswordForm),name="password_reset_confirm"),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobileData'),
    path('login/',views.login_view,name='login'),
    # path('accounts/login/', LoginView.as_view(template_name='app/login.html',authentication_form=AuthenticationForm), name='login'),
    path('accounts/logout/',LogoutView.as_view(),name='logout'),
    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationView, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    
]
