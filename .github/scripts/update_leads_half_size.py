from pathlib import Path
import re
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenLeadsHalfSize">.*?</style>\s*','\n',s,flags=re.S)
css=r'''
<style id="sevenLeadsHalfSize">
/* Meus Leads: cards aproximadamente 50% mais compactos */
#sevenLeadsScreen .seven-leads-grid{max-width:560px!important;gap:6px!important}
#sevenLeadsScreen .seven-lead-card{max-width:560px!important;border-radius:8px!important}
#sevenLeadsScreen .seven-lead-top{padding:7px 9px!important}
#sevenLeadsScreen .seven-lead-name{font-size:13px!important}
#sevenLeadsScreen .seven-lead-status{font-size:8px!important;padding:3px 6px!important}
#sevenLeadsScreen .seven-lead-data{padding:2px 9px 4px!important;gap:0 8px!important}
#sevenLeadsScreen .seven-lead-field,#sevenLeadsScreen .seven-lead-field.full{padding:4px 0!important;font-size:10px!important;line-height:1.2!important}
#sevenLeadsScreen .seven-lead-field small{font-size:7px!important;margin-bottom:1px!important}
#sevenLeadsScreen .seven-lead-actions{padding:3px 9px 7px!important;gap:5px!important}
#sevenLeadsScreen .seven-lead-actions button,#sevenLeadsScreen .seven-lead-actions a{min-height:29px!important;padding:5px 7px!important;font-size:9px!important}
#sevenLeadsScreen .seven-lead-top div[style]{font-size:9px!important;margin-top:1px!important}
@media(max-width:800px){#sevenLeadsScreen .seven-leads-grid,#sevenLeadsScreen .seven-lead-card{max-width:520px!important}}
@media(max-width:600px){
 #sevenLeadsScreen .seven-leads-grid,#sevenLeadsScreen .seven-lead-card{max-width:100%!important}
 #sevenLeadsScreen .seven-lead-data{grid-template-columns:1fr 1fr!important}
}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Cards de Meus Leads reduzidos em aproximadamente 50%')
