from django.shortcuts import render,redirect
from django.http import Http404, HttpResponse
from .models import TiposExames,PedidosExames,SolicitacaoExame
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def solicitar_exames(request):
    
    tiposexames=TiposExames.objects.all()
    
    if request.method == 'GET':
        return render(request, 'solicitar_exames.html',{"tiposexames":tiposexames})
    
    elif request.method == 'POST':
        exames_id=request.POST.getlist('exames')
        solicitar_exames=TiposExames.objects.filter(id__in=exames_id)
       
        total=0
        for exames in solicitar_exames:
            if exames.disponivel:
                total +=exames.preco
           
        print('total',total) 
        
        return render(request,'solicitar_exames.html',{"tiposexames":tiposexames,'solicitacao':solicitar_exames,'total':total})
    
def fechar_pedido(request):    
    exames_id=request.POST.getlist('exames') 
    solicitacao_exames=TiposExames.objects.filter(id__in=exames_id)
    
    pedido_exames=PedidosExames(
        usuario=request.user,
        data=datetime.now()
    )
    pedido_exames.save()
    
    for exame in solicitacao_exames:
        solicitacao_exames_temp=SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status='E',
             
        )
        solicitacao_exames_temp.save()
        pedido_exames.exames.add(solicitacao_exames_temp)
    pedido_exames.save()
    
    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect('gerenciar_pedidos')

@login_required
def gerenciar_pedidos(request):
    pedidos_exames=PedidosExames.objects.filter(usuario=request.user)
    
    return render(request,'gerenciar_pedidos.html',{'pedidos_exames':pedidos_exames})
@login_required
def cancelar_pedido(request,pedido_id):
    print('pedido',pedido_id)
    
    pedido=get_object_or_404(PedidosExames,id=pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request,constants.DEBUG,'Esse pedido não é seu')
        return redirect('gerenciar_pedidos')
        
    pedido.agendado=False
    pedido.save()
    messages.add_message(request,constants.SUCCESS,'Pedido Cancelado com sucesso ')
    return redirect('gerenciar_pedidos')

def gerenciar_exames(request):
    
   exames=SolicitacaoExame.objects.filter(usuario=request.user)
   
   return render(request,'gerenciar_exames.html',{"exames":exames})          

def permitir_abrir_exame(request,exame_id):
    
    exame=get_object_or_404(SolicitacaoExame,id=exame_id)
    
    if not  exame.requer_senha:
        if not exame.resultado:
            messages.add_message(request, constants.DEBUG, 'Não existe resultado em PDF')
            return redirect('gerenciar_exames')
        return redirect(exame.resultado.url)
    
    return redirect('solicitar_senha_exame',exame.id)

def solicitar_senha_exame(request,exame_id):
    
    exame=get_object_or_404(SolicitacaoExame,id=exame_id)
    
    if request.method =='GET':
            return render(request,'solicitar_senha_exame.html',{'exame':exame})
    
    elif request.method == 'POST':
            senha= request.POST.get('senha')
            
            if exame.senha == senha:
                if not exame.resultado:
                    messages.add_message(request, constants.DEBUG, 'Não existe resultado em PDF')
                    return redirect('gerenciar_exames')
                return redirect(exame.resultado.url)
            else:
                messages.add_message(request, constants.DEBUG, 'Senha Invalida')
                print('teste10000')
                return redirect('solicitar_senha_exame',exame.id)
            