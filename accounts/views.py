from typing import Any
from django import http
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreateUserForm, AccountForm
from .models import Account, AccountLogs

import datetime
from datetime import datetime

# Create your views here.

class HomePageView(LoginRequiredMixin, TemplateView):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'
    
    template_name = 'accounts/home.html'


class RegisterView(FormView):
    form_class = CreateUserForm
    template_name = 'accounts/register.html'
    success_url = '/register'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home-page')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        form.save()
        return redirect('login-page')
    
 
class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home-page')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            context = {}
            messages.info(request, 'Username OR password is incorrect')
            return render(request,'accounts/login.html',context)

    def get(self,request):
        context = {}
        return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login-page')


class AccountsListView(LoginRequiredMixin, ListView):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    template_name = 'accounts/accounts-list.html'
    model = Account
    #queryset = Account.objects.filter(owner= self.request.user)
    context_object_name = 'all_accounts'

    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset()
        data=query_set.filter(owner= self.request.user)

        return data
    
    

class AddAccountView(LoginRequiredMixin, CreateView):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    model = Account
    form_class = AccountForm
    template_name = 'accounts/add-account.html'
    success_url = reverse_lazy('accounts-list')

    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        AccountLogs.objects.create(account=self.object, old_amount=0, new_amount=self.object.amount, curency=self.object.curency, difference=self.object.amount)
        return HttpResponseRedirect(self.get_success_url())


class EditAccountView(LoginRequiredMixin, UpdateView):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        obj = self.get_object()
        if request.user != obj.owner:
            return HttpResponseRedirect("/")
        return super().dispatch(request, *args, **kwargs)

    model = Account
    form_class = AccountForm
    template_name = 'accounts/add-account.html'
    success_url = reverse_lazy('accounts-list')

    def get_initial(self):
        self.old_amount = self.object.amount

    def form_valid(self, form):
        self.object = form.save()
        AccountLogs.objects.create(account=self.object, old_amount=self.old_amount, new_amount=self.object.amount, curency=self.object.curency, difference=self.object.amount)
        return HttpResponseRedirect(self.get_success_url())
    

class SingleAccountView(LoginRequiredMixin, DetailView):
    login_url = 'login-page'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        logs = obj.account_logs.all()
        for log in logs:
            log.created_at = str(log.created_at)
        context["logs"] = logs
        return context

    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        obj = self.get_object()
        if request.user != obj.owner:
            return HttpResponseRedirect("/")
        return super().dispatch(request, *args, **kwargs)

    template_name = "accounts/single-account.html"
    model = Account

