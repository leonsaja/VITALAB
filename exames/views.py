from django.shortcuts import render
from django.http import HttpResponse
from .models import TiposExames
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