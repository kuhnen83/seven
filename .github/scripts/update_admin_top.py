from pathlib import Path
import re
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenAdminTopFix">.*?</style>\s*','\n',s,flags=re.S)
css=r'''
<style id="sevenAdminTopFix">
/* Leads e Carteira começam sempre no topo da área administrativa */
#sevenLeadsScreen,#sevenWalletScreen{
  padding-top:16px!important;
  align-self:flex-start!important;
  min-height:100vh!important;
}
#sevenLeadsScreen .seven-screen-header,#sevenWalletScreen .seven-screen-header{
  margin-top:0!important;
  padding-top:0!important;
}
#sevenLeadsScreen .seven-screen-title,#sevenWalletScreen .seven-screen-title{
  margin-top:0!important;
  padding-top:0!important;
}
#sevenLeadsScreen .seven-screen-title h1,#sevenWalletScreen .seven-screen-title h1{
  margin-top:0!important;
}
@media(max-width:800px){
 #sevenLeadsScreen,#sevenWalletScreen{padding-top:10px!important}
}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)
# Ao trocar de menu, força a janela para o topo antes e depois da renderização.
s=s.replace("window.scrollTo({top:0,left:0,behavior:'auto'});try{sessionStorage.setItem('seven_admin_screen',name)}catch(e){}", "window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0;requestAnimationFrame(()=>{window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0});try{sessionStorage.setItem('seven_admin_screen',name)}catch(e){}")
p.write_text(s,encoding='utf-8')
print('Leads e carteira posicionados no topo')
