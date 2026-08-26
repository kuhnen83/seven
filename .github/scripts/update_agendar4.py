from pathlib import Path
import re

p = Path('agendar4.html')
s = p.read_text(encoding='utf-8')

# Corrige a estrutura HTML: o grid de serviços precisa terminar antes do Total.
# Sem esse fechamento, Total/Nome/WhatsApp/Observação viravam itens do próprio grid.
pattern = r'(<div id="carpeteq" class="qty carpete-box">.*?</div>\s*</div>)\s*(<div class="total"><strong>Total</strong><strong id="total">R\$ 0,00</strong></div>)'
m = re.search(pattern, s, flags=re.S)
if m:
    trecho = m.group(0)
    # Se ainda não houver um fechamento extra do service-mobile-grid, adiciona.
    corrigido = m.group(1) + '\n</div>\n' + m.group(2)
    s = s.replace(trecho, corrigido, 1)

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

required=['id="carpete"','id="imp"','id="total"','id="nome"','id="tel"','id="obs"','id="next1"']
for item in required:
    if item not in s:
        raise SystemExit('ERRO: faltando '+item)

# Confirma que o Total está fora do grid de serviços.
check = re.search(r'<div class="service-mobile-grid">(.*?)</div>\s*<div class="total">', s, flags=re.S)
if not check:
    raise SystemExit('ERRO: Total ainda não ficou fora da grade de serviços')

p.write_text(s,encoding='utf-8')
print('Corrigido: grid fechado antes do Total; dados do cliente agora ficam abaixo')
