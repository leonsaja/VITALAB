from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User


def cadastro(request):
    
    
    if request.method =='GET':
        return render(request,'form_cadastro.html')
    
    elif request.method =='POST':
        
        primeiro_nome=request.POST.get('primeiro_nome')
        ultimo_nome=request.POST.get('ultimo_nome')
        username=request.POST.get('username')
        senha=request.POST.get('senha')
        email=request.POST.get('email')
        confirmar_senha=request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('cadastro')
        
        if len (senha) <6:
            messages.add_message(request, constants.ERROR, 'A sua senha deve tem mais de 7 digitos')
            return redirect('cadastro')
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuario com esse nome já cadastrado ')
            return redirect('cadastro')
         
        try:
             User.objects.create_user(
                 username=username,
                 first_name=primeiro_nome,
                 last_name=ultimo_nome,
                 email=email,
                 password=senha,
                 
             )
             messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso! ')
             return HttpResponse('cadastro realizado com sucesso')
        except:
            return redirect('cadastro')

            

        