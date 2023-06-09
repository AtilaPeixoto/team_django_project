from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib import auth
from .utils import validacao



# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        senha = request.POST.get('senha').strip()
        confirmar_senha = request.POST.get('confirmar_senha').strip()
        
        if not validacao(request, senha, confirmar_senha):
            return redirect('cadastro.html') 
        
        if not name.strip() or not email.strip():
            messages.add_message(request, constants.ERROR, 'Campo não pode ficar em branco')  
             
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'Opa este E-mail já está cadastrado')
            return redirect('cadastro.html')    
       
        try:
            user = User.objects.create_user(username=name, email=email, password=senha)
            user.save()
             
            messages.add_message(request, constants.SUCCESS, 'Parabéns você foi cadastrado com Sucesso!')
            return render(request, 'login.html')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno. Tente novamente.')
            return render(request, 'cadastro.html')
         
    
    
    
def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        name = request.POST.get('name').strip()
        senha = request.POST.get('senha').strip()
        
        user = auth.authenticate(username=name, password=senha)
        
        if not user:
            messages.add_message(request, constants.ERROR, 'Nome de usuario e ou senha invalidos')
            return redirect('login.htm')
        
        
        auth.login(request, user)
        return redirect('home.html')
    
    
def sair(request):
    auth.logout(request)
    return redirect('login.htm')