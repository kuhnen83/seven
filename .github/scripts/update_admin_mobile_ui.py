from pathlib import Path

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
marker='</style>\n''\'\n\'\'\'\ns=s.replace(\'</head>\',style+'

# Este complemento é aplicado pelo workflow depois do menu base.
css=r'''
<style id="sevenAdminMobileUI">
/* Leads: ficha vertical, leitura rápida e organizada */
#sevenLeadsScreen{max-width:1180px!important;margin:0 auto!important}
.seven-leads-toolbar{justify-content:center}.seven-leads-toolbar input{width:min(100%,620px)!important;max-width:620px!important}
.seven-leads-grid{grid-template-columns:repeat(2,minmax(300px,1fr));gap:16px;max-width:1050px;margin:0 auto}
.seven-lead-card{padding:0;overflow:hidden;border-radius:16px;box-shadow:0 4px 16px #0b17300a}
.seven-lead-top{padding:16px 18px;margin:0;background:#f8fafc;align-items:center}
.seven-lead-name{font-size:18px}.seven-lead-data{display:flex!important;flex-direction:column;gap:0;padding:5px 18px 10px}
.seven-lead-field,.seven-lead-field.full{display:grid!important;grid-template-columns:120px minmax(0,1fr);align-items:start;gap:12px;padding:9px 0;border-bottom:1px solid #eef2f6;font-size:13px;grid-column:auto!important}
.seven-lead-field:last-child{border-bottom:0}.seven-lead-field small{font-size:10px;margin:0;color:#607086;line-height:1.45}.seven-lead-actions{padding:0 18px 16px;margin-top:3px}.seven-lead-actions button,.seven-lead-actions a{min-height:40px;display:flex;align-items:center;justify-content:center;flex:1;font-size:12px}

/* Carteira: tudo centralizado e com largura confortável */
#sevenWalletScreen{max-width:1180px!important;margin:0 auto!important;text-align:center}
#sevenWalletScreen .seven-screen-header{justify-content:center;flex-direction:column;text-align:center;margin-bottom:20px}
#sevenWalletScreen .seven-screen-title{text-align:center;width:100%}
#sevenWalletScreen .seven-month-controls{justify-content:center;margin:0 auto}
.seven-wallet-grid{max-width:980px;margin:0 auto 18px;justify-content:center}
.seven-wallet-kpi{text-align:center;border-left:1px solid var(--seven-line)!important;border-top:5px solid #1976d2;padding:20px 12px}
.seven-wallet-kpi.paid{border-top-color:#20a45a}.seven-wallet-kpi.pending{border-top-color:#f59e0b}.seven-wallet-kpi.clients{border-top-color:#7c4dff}
.seven-wallet-kpi strong{font-size:24px}.seven-wallet-list{max-width:980px;margin:0 auto;text-align:left}.seven-wallet-list h3{text-align:center}

@media(max-width:800px){
 #sevenLeadsScreen,#sevenWalletScreen{width:100%!important;max-width:100%!important}
 .seven-leads-grid{grid-template-columns:1fr;max-width:620px}
 #sevenWalletScreen .seven-screen-header{align-items:center!important}
 .seven-wallet-grid{grid-template-columns:repeat(2,minmax(0,1fr));width:100%;gap:10px}
 .seven-wallet-kpi{padding:15px 8px;min-width:0}.seven-wallet-kpi small{font-size:9px}.seven-wallet-kpi strong{font-size:19px;overflow-wrap:anywhere}
 .seven-wallet-list{width:100%;padding:14px}.seven-wallet-row{text-align:center;grid-template-columns:1fr;gap:5px;padding:14px 4px}
}
@media(max-width:560px){
 #sevenLeadsScreen,#sevenWalletScreen{padding:16px 10px!important}
 .seven-screen-title h1{text-align:center}.seven-screen-title p{text-align:center}
 .seven-leads-toolbar{width:100%}.seven-leads-toolbar input{font-size:16px!important;width:100%!important}
 .seven-lead-card{border-radius:13px}.seven-lead-top{padding:14px}.seven-lead-data{padding:4px 14px 8px}
 .seven-lead-field,.seven-lead-field.full{grid-template-columns:92px minmax(0,1fr);gap:8px;padding:8px 0;font-size:12px}.seven-lead-field small{font-size:9px}
 .seven-lead-actions{padding:0 14px 14px;flex-direction:column}.seven-lead-actions button,.seven-lead-actions a{width:100%;min-height:44px}
 .seven-wallet-grid{grid-template-columns:1fr 1fr!important;gap:8px}.seven-wallet-kpi{border-radius:12px;padding:13px 6px}.seven-wallet-kpi strong{font-size:17px;margin-top:6px}.seven-wallet-kpi small{font-size:8px;line-height:1.25}
 .seven-month-controls{width:100%;justify-content:space-between!important}.seven-month-controls button{min-width:44px;min-height:44px}.seven-month-label{font-size:13px;min-width:0;flex:1}
 .seven-wallet-list{border-radius:12px;padding:12px 10px}.seven-wallet-list h3{font-size:16px}.seven-wallet-row{font-size:12px}
}
</style>
'''
# Remove complemento antigo se existir.
import re
s=re.sub(r'\s*<style id="sevenAdminMobileUI">.*?</style>\s*','\n',s,flags=re.S)
s=s.replace('</head>',css+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Leads reorganizados e carteira centralizada/responsiva')
