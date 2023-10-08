import os
from random import choice,shuffle
from django.template.loader import render_to_string
from io import BytesIO
from django.conf import settings
from weasyprint import HTML

import string

def gerar_senha_aleatoria(tamanho):
    
    caracteres_especiais=string.punctuation
    caracteres=string.ascii_letters
    numero_list=string.digits
    
    sobra=0
    qta=tamanho // 3 
    
    if not tamanho % 3 == 0:
        sobra=tamanho - (qta*3)
        
    letras=''
    for i in range(0,qta+sobra):
        letras+=choice(caracteres)
    
    especiais=''
    for i in range(0,qta):
        especiais+=choice(caracteres_especiais)
        
    numero=''
    for i in range(0,qta):
        numero+=choice(numero_list)
    
    senha=list(numero + especiais+letras)
   
    shuffle(senha)
    return ''.join(senha)

def gerar_pdf_exames(exame, paciente, senha):

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/senha_exame.html')
    print('teste',path_template)
    template_render = render_to_string(path_template, {'exame': exame, 'paciente': paciente, 'senha': senha})

    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return path_output