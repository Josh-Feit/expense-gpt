from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings
from functools import wraps

from .models import *
from .forms import *

import openai
openai.api_key = settings.OPENAI_API_KEY

def login_required(f):
    @wraps(f)
    def g(request, *args, **kwargs):
        if request.user.is_authenticated:
            return f(request, *args, **kwargs)
        else:
            return redirect('/login')
    return g

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('transactions')
    
class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('transactions')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

@login_required
def actionList(request):
    transactions = Transaction.objects.all().filter(user=request.user)
    balance = Transaction.calculate_balance(transactions)
    form = GPTEntryForm()
    response = ""
    if request.method == 'POST':
        form = GPTEntryForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data.get("input")
            if "GPT_Invest_Entry" in request.POST:
                input = "What are some smart ways to invest $" + str(balance) + "?" 
            if "GPT_Fun_Entry" in request.POST:
                input = "What are some ways to spend $" + str(balance) + "?" 
            if "GPT_Taxes_Entry" in request.POST:
                input = "How much will I have to pay in taxes if I make $" + str(balance) + " a month?" 
            response = openai.Completion.create(
                model="text-curie-001",
                prompt=input,
                temperature=0.5,
                max_tokens=1648
            )
            print(response['choices'][0]['text'])
            response = response['choices'][0]['text']
    context = {'transactions':transactions, 'balance':balance, 'form':form, 'response':response}
    pass
    return render(request, 'base/home.html', context)

@login_required
def createAction(request):
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.user = request.user
            action.save()
        return redirect('/')
    context = {'form':form}
    pass
    return render(request, 'base/add.html', context)

@login_required
def updateAction(request, pk):
    action = Transaction.objects.get(id=pk)
    form = TransactionForm(instance=action)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=action)
        if form.is_valid():
            action = form.save(commit=False)
            action.user = request.user
            action.save()
        return redirect('/')

    context = {'form':form}
    pass
    return render(request, 'base/update.html', context)

@login_required
def deleteAction(request, pk):
    action = Transaction.objects.get(id=pk)
    action.delete()
    pass
    return redirect('/')