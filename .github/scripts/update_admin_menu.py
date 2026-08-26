from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Remove versão anterior, se houver, para manter atualização idempotente.
s=re.sub(r'\s*<style id="sevenAdminMenuStyle">.*?</style>\s*','\n',s,flags=re.S)
s=re.sub(r'\s*<div id="sevenAdminSidebar".*?</aside>\s*','\n',s,flags=re.S)
s=re.sub(r'\s*<section id="sevenLeadsScreen".*?</section>\s*','\n',s,flags=re.S)
s=re.sub(r'\s*<section id="sevenWalletScreen".*?</section>\s*','\n',s,flags=re.S)
s=re.sub(r'\s*<script id="sevenAdminMenuController">.*?</script>\s*','\n',s,flags=re.S)

style=r'''
<style id="sevenAdminMenuStyle">
:root{--seven-side:#07162f;--seven-side2:#0c2348;--seven-blue:#1976d2;--seven-line:#e6ebf1}
#sevenProtectedPanel.authorized{display:block!important;min-height:100vh;padding-left:250px;background:#eef1f5}
#sevenAdminSidebar{position:fixed;left:0;top:0;bottom:0;width:250px;background:linear-gradient(180deg,var(--seven-side),#0a1d3d);color:#fff;z-index:2400;display:flex;flex-direction:column;box-shadow:8px 0 30px #07162f1c}
.seven-side-brand{padding:25px 20px 20px;border-bottom:1px solid #ffffff14;display:flex;align-items:center;gap:12px;min-height:92px}.seven-side-brand img{width:74px;height:52px;object-fit:contain}.seven-side-brand strong{font-size:16px;line-height:1.2}.seven-side-brand small{display:block;color:#93a5c5;font-size:11px;margin-top:4px}
.seven-side-nav{padding:17px 12px;display:flex;flex-direction:column;gap:7px}.seven-side-item{width:100%;border:0;background:transparent;color:#b8c5da;display:flex;align-items:center;gap:13px;padding:13px 14px;border-radius:10px;font-weight:800;text-align:left;cursor:pointer;font-size:14px}.seven-side-item:hover{background:#ffffff0d;color:#fff}.seven-side-item.active{background:#1976d2;color:#fff;box-shadow:0 8px 20px #1976d233}.seven-side-icon{font-size:20px;width:25px;text-align:center}.seven-side-footer{margin-top:auto;padding:15px 12px 20px;border-top:1px solid #ffffff14}.seven-side-footer button{width:100%;border:1px solid #ffffff26;background:#ffffff0a;color:#fff;border-radius:10px;padding:11px;font-weight:800;cursor:pointer}
#sevenProtectedPanel>.seven-panel-securitybar{display:none!important}
#sevenProtectedPanel .container,#sevenProtectedPanel .agenda-container,#sevenProtectedPanel .resumo-container,#sevenLeadsScreen,#sevenWalletScreen{max-width:none;margin:0!important;border-radius:0;box-shadow:none;min-height:100vh;padding:28px 30px;background:#f5f7fa}
.seven-screen-header{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:22px}.seven-screen-title h1{font-size:24px;color:#0f294f;margin:0}.seven-screen-title p{margin:5px 0 0;color:#748096;font-size:13px}.seven-screen-card{background:#fff;border:1px solid var(--seven-line);border-radius:14px;padding:18px;box-shadow:0 4px 16px #0b173008}
#telaAgenda .agenda-head{margin-top:0}.agenda-container{display:none}.container{display:none}.resumo-container{display:none!important}
.seven-leads-toolbar{display:flex;gap:10px;margin-bottom:16px}.seven-leads-toolbar input{max-width:420px;background:#fff}.seven-leads-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.seven-lead-card{background:#fff;border:1px solid var(--seven-line);border-radius:14px;padding:17px}.seven-lead-top{display:flex;justify-content:space-between;gap:10px;border-bottom:1px solid #edf0f4;padding-bottom:11px;margin-bottom:11px}.seven-lead-name{font-size:17px;font-weight:900;color:#0f294f}.seven-lead-status{font-size:10px;font-weight:900;padding:5px 8px;border-radius:12px;background:#edf4ff;color:#1769aa;height:max-content}.seven-lead-data{display:grid;grid-template-columns:1fr 1fr;gap:9px 14px}.seven-lead-field{font-size:12px;line-height:1.35;overflow-wrap:anywhere}.seven-lead-field small{display:block;color:#8691a3;font-size:9px;font-weight:900;text-transform:uppercase;margin-bottom:2px}.seven-lead-field.full{grid-column:1/-1}.seven-lead-actions{display:flex;gap:8px;margin-top:13px}.seven-lead-actions button,.seven-lead-actions a{border:0;border-radius:8px;padding:8px 10px;font-weight:800;font-size:11px;text-decoration:none;cursor:pointer}.seven-lead-actions .open{background:#1976d2;color:#fff}.seven-lead-actions .wa{background:#25d366;color:#fff}
.seven-wallet-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:18px}.seven-wallet-kpi{background:#fff;border:1px solid var(--seven-line);border-radius:14px;padding:18px;border-left:5px solid #1976d2}.seven-wallet-kpi small{display:block;color:#7c8799;font-weight:800;font-size:11px}.seven-wallet-kpi strong{display:block;color:#0f294f;font-size:23px;margin-top:8px}.seven-wallet-kpi.paid{border-left-color:#20a45a}.seven-wallet-kpi.pending{border-left-color:#f59e0b}.seven-wallet-kpi.clients{border-left-color:#7c4dff}.seven-wallet-list{background:#fff;border:1px solid var(--seven-line);border-radius:14px;padding:18px}.seven-wallet-list h3{margin:0 0 14px;color:#0f294f}.seven-wallet-row{display:grid;grid-template-columns:1fr auto auto;gap:12px;padding:11px 0;border-bottom:1px solid #eef1f4;align-items:center;font-size:12px}.seven-wallet-row:last-child{border-bottom:0}.seven-wallet-row b{color:#0f294f}.seven-wallet-empty{color:#8691a3;text-align:center;padding:25px}
.seven-month-controls{display:flex;align-items:center;gap:8px}.seven-month-controls button{border:1px solid #d8e0e9;background:#fff;border-radius:8px;padding:8px 11px;font-weight:900;color:#0f4c81;cursor:pointer}.seven-month-label{font-weight:900;color:#0f294f;min-width:120px;text-align:center}
@media(max-width:1000px){.seven-leads-grid{grid-template-columns:1fr}.seven-wallet-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:800px){#sevenProtectedPanel.authorized{padding-left:76px}#sevenAdminSidebar{width:76px}.seven-side-brand{padding:14px 8px;justify-content:center;min-height:72px}.seven-side-brand img{width:54px}.seven-side-brand div{display:none}.seven-side-nav{padding:12px 8px}.seven-side-item{padding:12px 8px;justify-content:center}.seven-side-item span:not(.seven-side-icon){display:none}.seven-side-icon{font-size:22px}.seven-side-footer{padding:10px 7px}.seven-side-footer button span{display:none}#sevenProtectedPanel .container,#sevenProtectedPanel .agenda-container,#sevenProtectedPanel .resumo-container,#sevenLeadsScreen,#sevenWalletScreen{padding:18px 14px}.seven-screen-header{align-items:flex-start;flex-direction:column}}
@media(max-width:560px){.seven-wallet-grid{grid-template-columns:1fr}.seven-lead-data{grid-template-columns:1fr}.seven-lead-field.full{grid-column:auto}.seven-wallet-row{grid-template-columns:1fr}.seven-screen-title h1{font-size:21px}}
</style>
'''
s=s.replace('</head>',style+'\n</head>',1)

sidebar=r'''
<aside id="sevenAdminSidebar" aria-label="Menu administrativo">
  <div class="seven-side-brand"><img src="./seven-logo.png?v=4" alt="Seven Limpeza"><div><strong>Seven Limpeza</strong><small>Painel administrativo</small></div></div>
  <nav class="seven-side-nav">
    <button class="seven-side-item active" data-seven-screen="agenda"><span class="seven-side-icon">📅</span><span>Minha agenda</span></button>
    <button class="seven-side-item" data-seven-screen="novo"><span class="seven-side-icon">➕</span><span>Novo agendamento</span></button>
    <button class="seven-side-item" data-seven-screen="leads"><span class="seven-side-icon">👥</span><span>Meus leads</span></button>
    <button class="seven-side-item" data-seven-screen="carteira"><span class="seven-side-icon">💳</span><span>Carteira</span></button>
  </nav>
  <div class="seven-side-footer"><button id="sevenSideLogout" type="button">↪ <span>Sair</span></button></div>
</aside>
'''
needle='<div id="sevenProtectedPanel" class="seven-protected-panel">'
if needle not in s: raise SystemExit('sevenProtectedPanel não encontrado')
s=s.replace(needle,needle+sidebar,1)

# Adiciona telas novas antes do fechamento do painel protegido.
leads=r'''
<section id="sevenLeadsScreen" style="display:none">
  <div class="seven-screen-header"><div class="seven-screen-title"><h1>Meus leads</h1><p>Carteira completa dos clientes cadastrados na agenda.</p></div></div>
  <div class="seven-leads-toolbar"><input id="sevenLeadSearch" type="search" placeholder="Buscar por nome, telefone, endereço ou serviço"></div>
  <div id="sevenLeadsGrid" class="seven-leads-grid"></div>
</section>
<section id="sevenWalletScreen" style="display:none">
  <div class="seven-screen-header"><div class="seven-screen-title"><h1>Carteira</h1><p>Visão financeira dos atendimentos e recebimentos do mês.</p></div><div class="seven-month-controls"><button id="sevenWalletPrev">‹</button><div id="sevenWalletMonth" class="seven-month-label"></div><button id="sevenWalletNext">›</button></div></div>
  <div class="seven-wallet-grid"><div class="seven-wallet-kpi"><small>FATURAMENTO TOTAL</small><strong id="sevenWalletTotal">R$ 0,00</strong></div><div class="seven-wallet-kpi paid"><small>JÁ PAGO</small><strong id="sevenWalletPaid">R$ 0,00</strong></div><div class="seven-wallet-kpi pending"><small>PENDENTE</small><strong id="sevenWalletPending">R$ 0,00</strong></div><div class="seven-wallet-kpi clients"><small>CLIENTES NO MÊS</small><strong id="sevenWalletClients">0</strong></div></div>
  <div class="seven-wallet-list"><h3>Movimentação do mês</h3><div id="sevenWalletRows"></div></div>
</section>
'''
close='</div><!-- sevenProtectedPanel -->'
if close not in s: raise SystemExit('fechamento sevenProtectedPanel não encontrado')
s=s.replace(close,leads+'\n'+close,1)

controller=r'''
<script id="sevenAdminMenuController">
(function(){
 const $=id=>document.getElementById(id);let walletDate=new Date();walletDate.setDate(1);
 const money=v=>'R$ '+Number(v||0).toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2});
 const esc=v=>String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
 function list(){return Array.isArray(window.agendamentos)?window.agendamentos:[]}
 function setActive(name){document.querySelectorAll('.seven-side-item').forEach(b=>b.classList.toggle('active',b.dataset.sevenScreen===name))}
 function hideAll(){if($('telaAgenda'))$('telaAgenda').style.display='none';if($('telaRecibo'))$('telaRecibo').style.display='none';if($('telaResumo')){$('telaResumo').style.display='none';$('telaResumo').classList.remove('active')}if($('sevenLeadsScreen'))$('sevenLeadsScreen').style.display='none';if($('sevenWalletScreen'))$('sevenWalletScreen').style.display='none'}
 function screen(name){hideAll();setActive(name);if(name==='agenda'){if($('telaAgenda'))$('telaAgenda').style.display='block';try{window.renderCalendario?.()}catch(e){}}else if(name==='novo'){if($('telaRecibo'))$('telaRecibo').style.display='block'}else if(name==='leads'){if($('sevenLeadsScreen'))$('sevenLeadsScreen').style.display='block';renderLeads()}else if(name==='carteira'){if($('sevenWalletScreen'))$('sevenWalletScreen').style.display='block';renderWallet()}window.scrollTo({top:0,left:0,behavior:'auto'});try{sessionStorage.setItem('seven_admin_screen',name)}catch(e){}}
 window.sevenOpenScreen=screen;
 function renderLeads(){const box=$('sevenLeadsGrid');if(!box)return;const q=($('sevenLeadSearch')?.value||'').trim().toLowerCase();let rows=list().filter(a=>!q||[a.client_name,a.phone,a.client_address,a.description,a.notes,a.service_date,a.service_time,a.payment_status,a.service_status].some(v=>String(v||'').toLowerCase().includes(q)));rows.sort((a,b)=>String(b.service_date||'').localeCompare(String(a.service_date||'')));if(!rows.length){box.innerHTML='<div class="seven-screen-card">Nenhum cliente encontrado.</div>';return}box.innerHTML=rows.map(a=>{const phone=String(a.phone||'').replace(/\D/g,'');return '<article class="seven-lead-card"><div class="seven-lead-top"><div><div class="seven-lead-name">'+esc(a.client_name||'Sem nome')+'</div><div style="font-size:11px;color:#8691a3;margin-top:3px">Recibo '+esc(a.receipt_number||'—')+'</div></div><span class="seven-lead-status">'+esc(a.service_status||'Agendado')+'</span></div><div class="seven-lead-data"><div class="seven-lead-field"><small>Telefone</small>'+esc(a.phone||'—')+'</div><div class="seven-lead-field"><small>Data / horário</small>'+esc(a.service_date||'—')+' • '+esc(a.service_time||'—')+'</div><div class="seven-lead-field full"><small>Endereço</small>'+esc(a.client_address||'—')+'</div><div class="seven-lead-field full"><small>Serviço</small>'+esc(a.description||'—')+'</div><div class="seven-lead-field"><small>Valor</small>'+money(a.total)+'</div><div class="seven-lead-field"><small>Pagamento</small>'+esc(a.payment_method||'—')+' • '+esc(a.payment_status||'—')+'</div><div class="seven-lead-field"><small>Quantidade</small>'+esc(a.quantity??'—')+'</div><div class="seven-lead-field"><small>Valor unitário</small>'+money(a.unit_price)+'</div><div class="seven-lead-field full"><small>Observações</small>'+esc(a.notes||'—')+'</div><div class="seven-lead-field full"><small>Conversa registrada</small>'+esc(a.conversation||'—')+'</div></div><div class="seven-lead-actions"><button class="open" onclick="abrirDetalhes(\''+esc(a.id)+'\')">Ver ficha</button>'+(phone?'<a class="wa" target="_blank" href="https://wa.me/55'+phone+'">WhatsApp</a>':'')+'</div></article>'}).join('')}
 function renderWallet(){const y=walletDate.getFullYear(),m=walletDate.getMonth(),prefix=y+'-'+String(m+1).padStart(2,'0');const rows=list().filter(a=>String(a.service_date||'').startsWith(prefix));const paid=rows.filter(a=>a.payment_status!=='Pendente').reduce((s,a)=>s+Number(a.total||0),0);const pending=rows.filter(a=>a.payment_status==='Pendente').reduce((s,a)=>s+Number(a.total||0),0);$('sevenWalletTotal').textContent=money(paid+pending);$('sevenWalletPaid').textContent=money(paid);$('sevenWalletPending').textContent=money(pending);$('sevenWalletClients').textContent=rows.length;$('sevenWalletMonth').textContent=walletDate.toLocaleDateString('pt-BR',{month:'long',year:'numeric'});const box=$('sevenWalletRows');if(!rows.length){box.innerHTML='<div class="seven-wallet-empty">Nenhuma movimentação neste mês.</div>';return}rows.sort((a,b)=>String(b.service_date||'').localeCompare(String(a.service_date||'')));box.innerHTML=rows.map(a=>'<div class="seven-wallet-row"><div><b>'+esc(a.client_name||'Cliente')+'</b><div style="color:#8993a3;margin-top:3px">'+esc(a.service_date||'')+' • '+esc(a.description||'')+'</div></div><span>'+esc(a.payment_status||'—')+'</span><strong>'+money(a.total)+'</strong></div>').join('')}
 function start(){document.querySelectorAll('.seven-side-item').forEach(b=>b.addEventListener('click',()=>screen(b.dataset.sevenScreen)));$('sevenLeadSearch')?.addEventListener('input',renderLeads);$('sevenWalletPrev')?.addEventListener('click',()=>{walletDate.setMonth(walletDate.getMonth()-1);renderWallet()});$('sevenWalletNext')?.addEventListener('click',()=>{walletDate.setMonth(walletDate.getMonth()+1);renderWallet()});$('sevenSideLogout')?.addEventListener('click',()=>$('sevenLogoutBtn')?.click());
  const oldOpen=window.abrirResumo;window.abrirResumo=()=>screen('carteira');window.fecharResumo=()=>screen('agenda');
  const oldEdit=window.editarDetalhe;window.editarDetalhe=function(){if(window.detalheId&&window.carregarAgendamento?.(window.detalheId)){window.fecharDetalhes?.();screen('novo')}else if(typeof oldEdit==='function')oldEdit()};
  screen('agenda');
  const obs=new MutationObserver(()=>{const active=document.getElementById('sevenProtectedPanel')?.classList.contains('authorized');if(active&&!document.body.dataset.sevenMenuReady){document.body.dataset.sevenMenuReady='1';screen('agenda')}});const panel=$('sevenProtectedPanel');if(panel)obs.observe(panel,{attributes:true,attributeFilter:['class']});
  setInterval(()=>{const active=document.querySelector('.seven-side-item.active')?.dataset.sevenScreen;if(active==='leads')renderLeads();if(active==='carteira')renderWallet()},2500);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('body não encontrado')
s=s[:pos]+controller+'\n'+s[pos:]

for required in ['sevenAdminSidebar','data-seven-screen="agenda"','sevenLeadsScreen','sevenWalletScreen','sevenOpenScreen','FATURAMENTO TOTAL']:
    if required not in s: raise SystemExit('Menu administrativo incompleto: '+required)

p.write_text(s,encoding='utf-8')
print('Menu vertical Seven instalado: agenda, novo agendamento, leads e carteira')
