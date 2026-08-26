from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenLeadsScrollDetailFix">.*?</style>\s*','\n',s,flags=re.S)

css=r'''
<style id="sevenLeadsScrollDetailFix">
/* Mantém o layout aprovado e corrige a rolagem da tela de Leads */
#sevenLeadsScreen{
  height:100dvh!important;
  max-height:100dvh!important;
  overflow-y:scroll!important;
  overflow-x:hidden!important;
  overscroll-behavior:contain!important;
  -webkit-overflow-scrolling:touch!important;
  touch-action:pan-y!important;
  scrollbar-gutter:stable!important;
  padding-bottom:48px!important;
}
#sevenLeadsScreen .seven-leads-grid{
  height:auto!important;
  min-height:max-content!important;
  overflow:visible!important;
  align-content:start!important;
}
#sevenLeadsScreen .seven-lead-card{
  position:relative!important;
  flex:none!important;
  overflow:visible!important;
}

/* A ficha do cliente precisa ficar acima da tela fixa de Leads e do menu */
.detail-overlay{
  z-index:12000!important;
  position:fixed!important;
  inset:0!important;
}
.detail-overlay.active{display:flex!important}
.pdf-overlay{z-index:12500!important}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)

# Garante que "Ver ficha" use uma função global acessível mesmo dentro do card gerado dinamicamente.
# Cria uma ponte segura sem substituir a função original.
bridge=r'''
<script id="sevenLeadsDetailBridge">
document.addEventListener('click',function(e){
  const btn=e.target.closest('#sevenLeadsScreen .seven-lead-actions .open');
  if(!btn)return;
  const card=btn.closest('.seven-lead-card');
  const inline=btn.getAttribute('onclick')||'';
  const m=inline.match(/abrirDetalhes\(['\"]([^'\"]+)['\"]\)/);
  if(!m)return;
  e.preventDefault();
  e.stopPropagation();
  const id=m[1];
  try{
    if(typeof window.abrirDetalhes==='function'){
      window.abrirDetalhes(id);
      const overlay=document.querySelector('.detail-overlay');
      if(overlay){overlay.classList.add('active');overlay.scrollTop=0;}
    }
  }catch(err){
    console.error('Erro ao abrir ficha do lead:',err);
    alert('Não foi possível abrir a ficha deste cliente.');
  }
},true);
</script>
'''
s=re.sub(r'\s*<script id="sevenLeadsDetailBridge">.*?</script>\s*','\n',s,flags=re.S)
pos=s.rfind('</body>')
if pos<0: raise SystemExit('body não encontrado')
s=s[:pos]+bridge+'\n'+s[pos:]

for x in ['sevenLeadsScrollDetailFix','sevenLeadsDetailBridge','z-index:12000','overflow-y:scroll']:
    if x not in s: raise SystemExit('Correção de Leads incompleta: '+x)

p.write_text(s,encoding='utf-8')
print('Rolagem e abertura da ficha em Meus Leads corrigidas')
