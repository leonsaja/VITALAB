from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import TiposExames,PedidosExames,SolicitacaoExame
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants

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
    return redirect('ver_pedidos')