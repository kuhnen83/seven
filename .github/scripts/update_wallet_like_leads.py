from pathlib import Path
import re
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<style id="sevenWalletLikeLeads">.*?</style>\s*','\n',s,flags=re.S)
css=r'''
<style id="sevenWalletLikeLeads">
/* Carteira com a mesma linguagem visual aprovada em Meus Leads */
#sevenWalletScreen{
 display:none!important;position:fixed!important;top:0!important;left:250px!important;right:0!important;bottom:0!important;
 width:auto!important;height:100dvh!important;max-height:100dvh!important;min-height:0!important;margin:0!important;
 padding:12px 18px 40px!important;box-sizing:border-box!important;background:#f5f7fa!important;z-index:1200!important;
 overflow-y:scroll!important;overflow-x:hidden!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-y!important;text-align:center!important
}
#sevenWalletScreen[style*="display: block"]{display:block!important}
#sevenWalletScreen .seven-screen-header,#sevenWalletScreen .seven-wallet-grid,#sevenWalletScreen .seven-wallet-list{width:100%!important;max-width:560px!important;margin-left:auto!important;margin-right:auto!important;box-sizing:border-box!important}
#sevenWalletScreen .seven-screen-header{margin-top:0!important;margin-bottom:8px!important;padding:0!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:7px!important}
#sevenWalletScreen .seven-screen-title{width:100%!important;text-align:center!important;margin:0!important;padding:0!important}
#sevenWalletScreen .seven-screen-title h1{font-size:20px!important;margin:0!important;padding:0!important}
#sevenWalletScreen .seven-screen-title p{font-size:10px!important;margin:3px 0 0!important}
#sevenWalletScreen .seven-month-controls{width:100%!important;max-width:300px!important;margin:0 auto!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:6px!important}
#sevenWalletScreen .seven-month-controls button{min-width:34px!important;min-height:32px!important;padding:5px 8px!important;font-size:14px!important}
#sevenWalletScreen .seven-month-label{font-size:11px!important;min-width:130px!important}
#sevenWalletScreen .seven-wallet-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:6px!important;margin-top:6px!important;margin-bottom:8px!important}
#sevenWalletScreen .seven-wallet-kpi{width:100%!important;min-width:0!important;padding:9px 6px!important;border-radius:8px!important;text-align:center!important}
#sevenWalletScreen .seven-wallet-kpi small{font-size:7px!important;line-height:1.15!important}
#sevenWalletScreen .seven-wallet-kpi strong{font-size:15px!important;line-height:1.15!important;margin-top:4px!important;overflow-wrap:anywhere!important}
#sevenWalletScreen .seven-wallet-list{padding:10px!important;border-radius:8px!important;text-align:center!important;overflow:visible!important}
#sevenWalletScreen .seven-wallet-list h3{font-size:13px!important;margin:0 0 7px!important;text-align:center!important}
#sevenWalletScreen .seven-wallet-row{display:grid!important;grid-template-columns:1fr auto!important;gap:5px 8px!important;width:100%!important;padding:7px 4px!important;text-align:left!important;font-size:10px!important;box-sizing:border-box!important}
#sevenWalletScreen .seven-wallet-row>span{font-size:9px!important;text-align:right!important}
#sevenWalletScreen .seven-wallet-row>strong{font-size:11px!important;text-align:right!important}
@media(max-width:800px){#sevenWalletScreen{left:76px!important;padding:10px 10px 32px!important}#sevenWalletScreen .seven-screen-header,#sevenWalletScreen .seven-wallet-grid,#sevenWalletScreen .seven-wallet-list{max-width:520px!important}}
@media(max-width:480px){#sevenWalletScreen{left:64px!important;padding:8px 8px 28px!important}#sevenWalletScreen .seven-screen-header,#sevenWalletScreen .seven-wallet-grid,#sevenWalletScreen .seven-wallet-list{max-width:100%!important}#sevenWalletScreen .seven-wallet-grid{grid-template-columns:1fr 1fr!important}#sevenWalletScreen .seven-wallet-kpi strong{font-size:13px!important}#sevenWalletScreen .seven-wallet-row{grid-template-columns:1fr!important;text-align:center!important}#sevenWalletScreen .seven-wallet-row>span,#sevenWalletScreen .seven-wallet-row>strong{text-align:center!important}}
</style>
'''
s=s.replace('</head>',css+'\n</head>',1)
# Garante topo ao abrir Carteira.
s=s.replace("else if(name==='carteira'){if($('sevenWalletScreen'))$('sevenWalletScreen').style.display='block';renderWallet()}","else if(name==='carteira'){if($('sevenWalletScreen'))$('sevenWalletScreen').style.display='block';renderWallet();const wallet=$('sevenWalletScreen');if(wallet)wallet.scrollTop=0;requestAnimationFrame(()=>{if(wallet)wallet.scrollTop=0})}")
p.write_text(s,encoding='utf-8')
print('Carteira ajustada para o mesmo layout compacto de Leads')
