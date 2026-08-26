from pathlib import Path
import re

p = Path('agendar4.html')
s = p.read_text(encoding='utf-8')

# ===== CORREÇÃO ESTRUTURAL =====
# Havia vários </div> extras entre o card Carpete e o Total. Isso fazia as etapas
# seguintes escaparem do container correto e aparecerem abaixo da etapa atual.
carpete_end = (
    '<div class="carpete-info"><strong>⚠️ Informação importante</strong>'
    '<span>O carpete será higienizado no local, com processo de higienização a seco. '
    'O tempo de secagem pode ser de até 8 horas.</span></div></div>'
)
if carpete_end not in s:
    raise SystemExit('ERRO: final do card Carpete não encontrado')

# Do fim do carpete até o Total, deixa somente:
# fecha service-card + fecha service-mobile-grid.
pattern = re.escape(carpete_end) + r'(?:\s*</div>)+\s*(<div class="total"><strong>Total</strong><strong id="total">R\$ 0,00</strong></div>)'
m = re.search(pattern, s, flags=re.S)
if not m:
    raise SystemExit('ERRO: não foi possível normalizar o fechamento do grid')
canonical = carpete_end + '\n</div>\n</div>\n' + m.group(1)
s = s[:m.start()] + canonical + s[m.end():]

# ===== CSS: somente uma etapa ocupa a tela =====
layout_css = '''
/* ===== Layout dados do cliente Seven ===== */
#s1 .service-mobile-grid{display:grid!important;width:100%!important}
#s1 .service-mobile-grid + .total{display:flex!important;width:100%!important;box-sizing:border-box!important;clear:both!important;margin:14px 0 0!important}
#s1 .total ~ .field{display:block!important;width:100%!important;max-width:none!important;box-sizing:border-box!important;clear:both!important;margin:14px 0!important}
#s1 .total ~ .field input,#s1 .total ~ .field textarea{display:block!important;width:100%!important;box-sizing:border-box!important}
#s1 #next1{display:block!important;width:100%!important;clear:both!important;margin-top:16px!important}

/* ===== Navegação por telas ===== */
.content>.step{display:none!important}
.content>.step.active{display:block!important}
.content>#ok{display:none!important}
.content>#ok.active{display:block!important}
.content{position:relative!important}
@media(max-width:700px){
  .content>.step.active,.content>#ok.active{min-height:calc(100svh - 110px)}
}
'''
marker='/* ===== Layout dados do cliente Seven ===== */'
if marker not in s:
    s=s.replace('</style>',layout_css+'</style>',1)
else:
    s=re.sub(r'/\* ===== Layout dados do cliente Seven ===== \*/.*?(?=</style>)',layout_css.strip()+'\n',s,flags=re.S)

# Remove controlador antigo; o próprio show(n) do módulo já faz a navegação correta.
s=re.sub(r'\s*<script id="sevenStepScreenController">.*?</script>\s*','\n',s,flags=re.S)

# Ajusta show(n) para rolar até o topo visual logo após trocar de etapa.
old_show="function show(n){clearError();document.querySelectorAll('.step').forEach(x=>x.classList.remove('active'));$('s'+n).classList.add('active');window.scrollTo(0,0)}"
new_show="function show(n){clearError();document.querySelectorAll('.step').forEach(x=>x.classList.remove('active'));$('ok')?.classList.remove('active');$('s'+n).classList.add('active');requestAnimationFrame(()=>window.scrollTo({top:0,left:0,behavior:'auto'}))}"
if old_show in s:
    s=s.replace(old_show,new_show,1)
elif new_show not in s:
    raise SystemExit('ERRO: função show(n) não encontrada')

# Ao finalizar, oculta qualquer etapa antes de mostrar a confirmação.
old_ok="document.querySelectorAll('.step').forEach(x=>x.classList.remove('active'));$('ok').classList.add('active')"
new_ok="document.querySelectorAll('.step').forEach(x=>x.classList.remove('active'));$('ok').classList.add('active');requestAnimationFrame(()=>window.scrollTo({top:0,left:0,behavior:'auto'}))"
s=s.replace(old_ok,new_ok)

required=['id="s1"','id="s2"','id="s3"','id="s4"','id="ok"','id="next1"','function show(n)']
for item in required:
    if item not in s:
        raise SystemExit('ERRO: faltando '+item)

# Validação estrutural: Total deve aparecer imediatamente depois do fechamento do grid.
if not re.search(r'</div>\s*</div>\s*<div class="total"><strong>Total</strong>', s):
    raise SystemExit('ERRO: estrutura do grid/Total continua inválida')

p.write_text(s,encoding='utf-8')
print('Corrigido: Continuar agora troca para uma tela única, sem exibir a etapa anterior')
