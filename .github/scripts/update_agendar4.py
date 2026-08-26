from pathlib import Path
import re

p = Path('agendar4.html')
s = p.read_text(encoding='utf-8')

# Corrige a estrutura HTML: o grid de serviços precisa terminar antes do Total.
pattern = r'(<div id="carpeteq" class="qty carpete-box">.*?</div>\s*</div>)\s*(<div class="total"><strong>Total</strong><strong id="total">R\$ 0,00</strong></div>)'
m = re.search(pattern, s, flags=re.S)
if m:
    trecho = m.group(0)
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

/* ===== Etapas em telas individuais ===== */
.step{display:none!important}
.step.active{display:block!important;animation:sevenStepIn .18s ease-out}
@keyframes sevenStepIn{from{opacity:.25;transform:translateY(8px)}to{opacity:1;transform:none}}
@media(max-width:700px){
  .content{padding-top:18px!important}
  .step.active{min-height:calc(100svh - 120px)}
}
'''
marker='/* ===== Layout dados do cliente Seven ===== */'
if marker not in s:
    s=s.replace('</style>',layout_css+'</style>',1)
else:
    s=re.sub(r'/\* ===== Layout dados do cliente Seven ===== \*/.*?(?=</style>)',layout_css.strip()+'\n',s,flags=re.S)

# Controlador adicional: sempre que uma etapa nova recebe "active",
# remove "active" das demais e leva o usuário ao topo do conteúdo.
step_script = '''
<script id="sevenStepScreenController">
(function(){
  let changing=false;
  function topOfContent(){
    const spacer=document.querySelector('.seven-menu-spacer');
    const y=spacer?spacer.getBoundingClientRect().bottom+window.scrollY:0;
    window.scrollTo({top:Math.max(0,y-4),behavior:'smooth'});
  }
  function activateOnly(target){
    if(changing||!target||!target.classList.contains('step'))return;
    changing=true;
    document.querySelectorAll('.step.active').forEach(el=>{if(el!==target)el.classList.remove('active')});
    changing=false;
    setTimeout(topOfContent,20);
  }
  function start(){
    const steps=[...document.querySelectorAll('.step')];
    const observer=new MutationObserver(list=>{
      for(const m of list){
        if(m.type==='attributes'&&m.attributeName==='class'&&m.target.classList.contains('active')){
          activateOnly(m.target);
        }
      }
    });
    steps.forEach(el=>observer.observe(el,{attributes:true,attributeFilter:['class']}));
    const initial=steps.find(el=>el.classList.contains('active'));
    if(initial)activateOnly(initial);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
</script>
'''
if 'id="sevenStepScreenController"' not in s:
    s=s.replace('</body>',step_script+'\n</body>',1)

required=['id="carpete"','id="imp"','id="total"','id="nome"','id="tel"','id="obs"','id="next1"','sevenStepScreenController']
for item in required:
    if item not in s:
        raise SystemExit('ERRO: faltando '+item)

check = re.search(r'<div class="service-mobile-grid">(.*?)</div>\s*<div class="total">', s, flags=re.S)
if not check:
    raise SystemExit('ERRO: Total ainda não ficou fora da grade de serviços')

p.write_text(s,encoding='utf-8')
print('Agendamento atualizado: cada etapa agora aparece em uma tela separada')
