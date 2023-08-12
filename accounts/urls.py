from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'home-page'),
    path('register/', views.RegisterView.as_view(), name = 'register-page'),
    path('login/', views.LoginView.as_view(), name = 'login-page'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('accounts/', views.AccountsListView.as_view(), name = 'accounts-list'),
    path('accounts/add/', views.AddAccountView.as_view(), name = 'add-account'),
    path("accounts/<slug:slug>", views.SingleAccountView.as_view(), name = "single-account-page"),
    path("accounts/<slug:slug>/edit/", views.EditAccountView.as_view(), name = "edit-account-page"),
    path("accounts/<slug:slug>/delete/", views.DeleteAccountView.as_view(), name = "delete-account-page"),
]