from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required
from exames.models import SolicitacaoExame
from django.shortcuts import get_object_or_404
staff_member_required
def gerenciar_clientes(request):
    clientes=User.objects.filter(is_staff=False)
    nome_completo = request.GET.get('nome')
    email = request.GET.get('email')

    if email:
        clientes = clientes.filter(email__contains = email)
    if nome_completo:
        print('nome_completo',nome_completo)
        clientes = clientes.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__contains=nome_completo)
   
    return render(request,'gerenciar_cliente.html',{'clientes':clientes})
staff_member_required
def cliente(request,cliente_id): 
    cliente=get_object_or_404(User,id=cliente_id)
    exames=SolicitacaoExame.objects.filter(usuario=cliente)
    return render(request,'cliente.html',{'cliente':cliente,'exames':exames})

staff_member_required
def exame_cliente(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    return render(request, 'exame_cliente.html', {'exame': exame})

@staff_member_required 
def proxy_pdf(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    print(exame)
    response = exame.resultado.open()
    return FileResponse(response)