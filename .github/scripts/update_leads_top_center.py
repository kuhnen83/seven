from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenLeadsTopCenterFix">.*?</style>\s*','\n',s,flags=re.S)

css=r'''
<style id="sevenLeadsTopCenterFix">
/* Meus Leads: conteúdo centralizado e iniciado no topo */
#sevenLeadsScreen{
  display:block;
  width:100%!important;
  max-width:none!important;
  margin:0!important;
  padding:8px 16px 20px!important;
  box-sizing:border-box!important;
  text-align:center!important;
  overflow-x:hidden!important;
}
#sevenLeadsScreen .seven-screen-header{
  max-width:900px!important;
  margin:0 auto 8px!important;
  padding:0!important;
  text-align:center!important;
  align-items:center!important;
  justify-content:center!important;
}
#sevenLeadsScreen .seven-screen-title{
  width:100%!important;
  text-align:center!important;
  margin:0!important;
  padding:0!important;
}
#sevenLeadsScreen .seven-screen-title h1{margin:0!important;padding:0!important}
#sevenLeadsScreen .seven-screen-title p{margin:3px 0 0!important}
.seven-leads-toolbar{
  width:100%!important;
  max-width:900px!important;
  margin:8px auto 10px!important;
  justify-content:center!important;
}
.seven-leads-grid{
  width:100%!important;
  max-width:900px!important;
  margin:0 auto!important;
  padding:0!important;
  align-content:start!important;
}
.seven-lead-card{text-align:left!important;width:100%!important;box-sizing:border-box!important}
@media(max-width:800px){
 #sevenLeadsScreen{padding:6px 10px 16px!important}
 #sevenLeadsScreen .seven-screen-header{margin-bottom:6px!important}
 .seven-leads-toolbar{margin:6px auto 8px!important}
 .seven-leads-grid{max-width:100%!important}
}
@media(max-width:480px){
 #sevenLeadsScreen{padding:4px 8px 14px!important}
 .seven-lead-card{border-radius:10px!important}
}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)

# Ao entrar em Leads, garante topo absoluto após a tela ficar visível.
s=s.replace("else if(name==='leads'){if($('sevenLeadsScreen'))$('sevenLeadsScreen').style.display='block';renderLeads()}","else if(name==='leads'){if($('sevenLeadsScreen'))$('sevenLeadsScreen').style.display='block';renderLeads();requestAnimationFrame(()=>{window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0})}")

p.write_text(s,encoding='utf-8')
print('Meus Leads centralizado e movido para o topo')
