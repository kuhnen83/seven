from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenLeadsFixedScreen">.*?</style>\s*','\n',s,flags=re.S)

css=r'''
<style id="sevenLeadsFixedScreen">
/* Tela independente de Leads: ocupa exatamente a área à direita do menu */
#sevenLeadsScreen{
  display:none!important;
  position:fixed!important;
  top:0!important;
  left:250px!important;
  right:0!important;
  bottom:0!important;
  width:auto!important;
  height:auto!important;
  min-height:0!important;
  max-width:none!important;
  margin:0!important;
  padding:18px 28px 28px!important;
  overflow-y:auto!important;
  overflow-x:hidden!important;
  box-sizing:border-box!important;
  background:#f5f7fa!important;
  z-index:1200!important;
}
#sevenLeadsScreen.seven-visible,
#sevenLeadsScreen[style*="display: block"]{display:block!important}
#sevenLeadsScreen .seven-screen-header,
#sevenLeadsScreen .seven-leads-toolbar,
#sevenLeadsScreen .seven-leads-grid{
  width:100%!important;
  max-width:1100px!important;
  margin-left:auto!important;
  margin-right:auto!important;
  box-sizing:border-box!important;
}
#sevenLeadsScreen .seven-screen-header{
  margin-top:0!important;
  margin-bottom:10px!important;
  padding:0!important;
  justify-content:center!important;
  align-items:center!important;
  text-align:center!important;
}
#sevenLeadsScreen .seven-screen-title{
  width:100%!important;
  text-align:center!important;
  margin:0!important;
  padding:0!important;
}
#sevenLeadsScreen .seven-screen-title h1{margin:0!important;padding:0!important}
#sevenLeadsScreen .seven-screen-title p{margin:4px 0 0!important}
#sevenLeadsScreen .seven-leads-toolbar{
  margin-top:8px!important;
  margin-bottom:12px!important;
  justify-content:center!important;
}
#sevenLeadsScreen .seven-leads-toolbar input{
  width:min(100%,620px)!important;
  max-width:620px!important;
}
#sevenLeadsScreen .seven-leads-grid{
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:12px!important;
  padding:0!important;
  align-items:start!important;
}
#sevenLeadsScreen .seven-lead-card{width:100%!important;min-width:0!important;margin:0!important;text-align:left!important}
@media(max-width:1000px){
 #sevenLeadsScreen .seven-leads-grid{grid-template-columns:1fr!important;max-width:720px!important}
}
@media(max-width:800px){
 #sevenLeadsScreen{left:76px!important;padding:12px 14px 20px!important}
 #sevenLeadsScreen .seven-screen-header,#sevenLeadsScreen .seven-leads-toolbar,#sevenLeadsScreen .seven-leads-grid{max-width:100%!important}
}
@media(max-width:480px){
 #sevenLeadsScreen{left:64px!important;padding:10px 9px 16px!important}
 #sevenLeadsScreen .seven-screen-title h1{font-size:20px!important}
 #sevenLeadsScreen .seven-screen-title p{font-size:11px!important}
}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)

# Quando abrir leads, garante o scroll da própria tela no topo.
s=s.replace("renderLeads();window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0;requestAnimationFrame(()=>{window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0})", "renderLeads();const leads=$('sevenLeadsScreen');if(leads)leads.scrollTop=0;window.scrollTo(0,0);requestAnimationFrame(()=>{if(leads)leads.scrollTop=0;window.scrollTo(0,0)})")

p.write_text(s,encoding='utf-8')
print('Meus Leads fixado no topo e centralizado na área útil')
