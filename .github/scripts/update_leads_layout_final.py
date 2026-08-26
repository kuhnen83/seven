from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenLeadsLayoutFinal">.*?</style>\s*','\n',s,flags=re.S)

css=r'''
<style id="sevenLeadsLayoutFinal">
/* Correção final: Leads centralizados na área útil e colados ao topo */
#sevenProtectedPanel.authorized{position:relative!important}
#sevenLeadsScreen{
  display:none!important;
  position:relative!important;
  width:auto!important;
  max-width:none!important;
  min-height:0!important;
  margin:0!important;
  padding:10px 24px 24px!important;
  box-sizing:border-box!important;
  background:#f5f7fa!important;
  text-align:left!important;
}
#sevenLeadsScreen[style*="display: block"],#sevenLeadsScreen.seven-visible{display:block!important}
#sevenLeadsScreen .seven-screen-header{
  width:100%!important;
  max-width:1040px!important;
  margin:0 auto 8px!important;
  padding:0!important;
  justify-content:flex-start!important;
  align-items:flex-start!important;
  text-align:left!important;
}
#sevenLeadsScreen .seven-screen-title{width:100%!important;text-align:left!important}
#sevenLeadsScreen .seven-screen-title h1{margin:0!important;padding:0!important;font-size:24px!important}
#sevenLeadsScreen .seven-screen-title p{margin:3px 0 0!important}
.seven-leads-toolbar{
  width:100%!important;
  max-width:1040px!important;
  margin:8px auto 10px!important;
  justify-content:flex-start!important;
}
.seven-leads-toolbar input{width:min(100%,560px)!important;max-width:560px!important}
.seven-leads-grid{
  width:100%!important;
  max-width:1040px!important;
  margin:0 auto!important;
  padding:0!important;
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:12px!important;
  align-items:start!important;
}
.seven-lead-card{width:100%!important;min-width:0!important;margin:0!important}
@media(max-width:1000px){.seven-leads-grid{grid-template-columns:1fr!important}}
@media(max-width:800px){
 #sevenLeadsScreen{padding:8px 14px 18px!important}
 #sevenLeadsScreen .seven-screen-header,.seven-leads-toolbar,.seven-leads-grid{max-width:100%!important}
}
@media(max-width:480px){
 #sevenLeadsScreen{padding:6px 10px 16px!important}
 #sevenLeadsScreen .seven-screen-title h1{font-size:21px!important}
}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)

# Garante classe visível apenas quando a tela de Leads está ativa e força topo real.
s=s.replace("if($('sevenLeadsScreen'))$('sevenLeadsScreen').style.display='none'","if($('sevenLeadsScreen')){$('sevenLeadsScreen').style.display='none';$('sevenLeadsScreen').classList.remove('seven-visible')}")
s=s.replace("if($('sevenLeadsScreen'))$('sevenLeadsScreen').style.display='block';renderLeads();requestAnimationFrame(()=>{window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0})","if($('sevenLeadsScreen')){$('sevenLeadsScreen').style.display='block';$('sevenLeadsScreen').classList.add('seven-visible')}renderLeads();window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0;requestAnimationFrame(()=>{window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0})")

p.write_text(s,encoding='utf-8')
print('Layout final de Meus Leads aplicado')
