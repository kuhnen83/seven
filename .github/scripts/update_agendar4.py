from pathlib import Path
import re

p = Path('agendar4.html')
s = p.read_text(encoding='utf-8')

# Mantém todo o conteúdo já gerado e aplica apenas o layout solicitado.
layout_css = '''
/* ===== Layout dados do cliente Seven ===== */
#s1.active{display:block!important}
#s1 .service-mobile-grid{display:grid!important;width:100%!important}
#s1 .service-mobile-grid + .total{display:flex!important;width:100%!important;box-sizing:border-box!important;clear:both!important;margin:14px 0 0!important}
#s1 .total ~ .field{display:block!important;width:100%!important;max-width:none!important;box-sizing:border-box!important;clear:both!important;margin:14px 0!important}
#s1 .total ~ .field input,#s1 .total ~ .field textarea{display:block!important;width:100%!important;box-sizing:border-box!important}
#s1 #next1{display:block!important;width:100%!important;clear:both!important;margin-top:16px!important}
@media(min-width:701px){#s1 .total ~ .field{width:100%!important}}
@media(max-width:700px){#s1 .total ~ .field{width:100%!important;margin:12px 0!important}}
'''
marker='/* ===== Layout dados do cliente Seven ===== */'
if marker not in s:
    s=s.replace('</style>',layout_css+'</style>',1)
else:
    s=re.sub(r'/\* ===== Layout dados do cliente Seven ===== \*/.*?(?=</style>)',layout_css.strip()+'\n',s,flags=re.S)

# Valida que os campos e serviços essenciais continuam presentes.
required=['id="carpete"','id="imp"','id="total"','id="nome"','id="tel"','id="obs"','id="next1"']
for item in required:
    if item not in s:
        raise SystemExit('ERRO: faltando '+item)

p.write_text(s,encoding='utf-8')
print('Layout atualizado: Nome, WhatsApp e Observação em linhas abaixo do Total')
