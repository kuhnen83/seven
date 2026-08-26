from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenLeadsSingleColumn">.*?</style>\s*','\n',s,flags=re.S)

css=r'''
<style id="sevenLeadsSingleColumn">
/* Meus Leads: um cliente embaixo do outro */
#sevenLeadsScreen .seven-leads-grid{
  display:grid!important;
  grid-template-columns:1fr!important;
  gap:10px!important;
  width:100%!important;
  max-width:760px!important;
  margin:0 auto!important;
}
#sevenLeadsScreen .seven-lead-card{
  width:100%!important;
  max-width:760px!important;
  margin:0 auto!important;
}
@media(max-width:800px){
 #sevenLeadsScreen .seven-leads-grid,#sevenLeadsScreen .seven-lead-card{max-width:100%!important}
}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Meus Leads ajustado para coluna única')
