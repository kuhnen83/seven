from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Remove complemento anterior, se houver.
s=re.sub(r'\s*<style id="sevenAdminCompactFix">.*?</style>\s*','\n',s,flags=re.S)

css=r'''
<style id="sevenAdminCompactFix">
/* ===== Meus Leads: versão compacta ===== */
#sevenLeadsScreen{overflow-x:hidden!important}
.seven-leads-grid{grid-template-columns:1fr!important;max-width:900px!important;margin:0 auto!important;gap:10px!important}
.seven-lead-card{padding:0!important;border-radius:12px!important;overflow:hidden!important}
.seven-lead-top{padding:12px 14px!important;margin:0!important}
.seven-lead-name{font-size:16px!important}
.seven-lead-data{display:grid!important;grid-template-columns:1fr 1fr!important;gap:0 16px!important;padding:6px 14px 8px!important}
.seven-lead-field,.seven-lead-field.full{display:block!important;grid-column:auto!important;padding:7px 0!important;border-bottom:1px solid #eef2f6!important;font-size:12px!important;line-height:1.35!important}
.seven-lead-field small{font-size:8.5px!important;margin-bottom:2px!important}
.seven-lead-actions{padding:6px 14px 12px!important;margin:0!important;display:flex!important;gap:8px!important}
.seven-lead-actions button,.seven-lead-actions a{min-height:38px!important;padding:8px 10px!important}

/* ===== Carteira: centralização real e sem conteúdo escondido ===== */
#sevenWalletScreen{box-sizing:border-box!important;width:100%!important;max-width:none!important;margin:0!important;overflow-x:hidden!important;text-align:center!important}
#sevenWalletScreen .seven-screen-header{width:100%!important;max-width:760px!important;margin:0 auto 18px!important;align-items:center!important;justify-content:center!important}
#sevenWalletScreen .seven-screen-title{width:100%!important;text-align:center!important}
#sevenWalletScreen .seven-month-controls{width:auto!important;max-width:100%!important;margin:0 auto!important;justify-content:center!important}
.seven-wallet-grid{width:100%!important;max-width:760px!important;margin:0 auto 16px!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px!important}
.seven-wallet-kpi{min-width:0!important;width:100%!important;box-sizing:border-box!important;text-align:center!important;padding:14px 8px!important}
.seven-wallet-kpi small{white-space:normal!important;line-height:1.2!important}
.seven-wallet-kpi strong{white-space:normal!important;overflow-wrap:anywhere!important;font-size:20px!important}
.seven-wallet-list{width:100%!important;max-width:760px!important;margin:0 auto!important;box-sizing:border-box!important;overflow:hidden!important;text-align:center!important}
.seven-wallet-row{width:100%!important;box-sizing:border-box!important;text-align:center!important}

@media(max-width:800px){
 #sevenProtectedPanel.authorized{padding-left:70px!important}
 #sevenWalletScreen,#sevenLeadsScreen{padding:14px 10px!important;width:100%!important;max-width:100%!important;box-sizing:border-box!important}
 .seven-wallet-grid{grid-template-columns:1fr 1fr!important;gap:8px!important}
 .seven-wallet-kpi{padding:12px 5px!important}
 .seven-wallet-kpi strong{font-size:17px!important}
 .seven-wallet-kpi small{font-size:8px!important}
 .seven-wallet-list{padding:12px 8px!important}
 .seven-wallet-row{grid-template-columns:1fr!important;gap:4px!important;padding:12px 4px!important}
}
@media(max-width:480px){
 #sevenProtectedPanel.authorized{padding-left:64px!important}
 #sevenAdminSidebar{width:64px!important}
 #sevenWalletScreen,#sevenLeadsScreen{padding:12px 8px!important}
 .seven-wallet-grid{grid-template-columns:1fr!important;max-width:360px!important}
 .seven-wallet-kpi{padding:13px 8px!important}
 .seven-wallet-kpi strong{font-size:19px!important}
 .seven-wallet-list{max-width:360px!important}
 .seven-lead-data{grid-template-columns:1fr!important}
 .seven-lead-actions{flex-direction:row!important}
}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)

# Remove Conversa registrada dos cards de leads, preservando o dado na ficha detalhada.
s=s.replace("<div class=\"seven-lead-field full\"><small>Conversa registrada</small>'+esc(a.conversation||'—')+'</div>","")
s=s.replace("<div class=\"seven-lead-field full\"><small>Observações</small>'+esc(a.notes||'—')+'</div><div class=\"seven-lead-field full\"><small>Conversa registrada</small>'+esc(a.conversation||'—')+'</div>","<div class=\"seven-lead-field full\"><small>Observações</small>'+esc(a.notes||'—')+'</div>")

# Também deixa o card mais compacto removendo quantidade e valor unitário da visão resumida.
s=s.replace("<div class=\"seven-lead-field\"><small>Quantidade</small>'+esc(a.quantity??'—')+'</div><div class=\"seven-lead-field\"><small>Valor unitário</small>'+money(a.unit_price)+'</div>","")

for required in ['sevenAdminCompactFix','sevenWalletScreen','sevenLeadsScreen']:
    if required not in s: raise SystemExit('Ajuste compacto incompleto: '+required)

p.write_text(s,encoding='utf-8')
print('Leads compactados e carteira corrigida para centralização/mobile')
