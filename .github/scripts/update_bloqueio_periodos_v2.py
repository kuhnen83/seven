from pathlib import Path
import re

# ============================================================
# PAINEL ADMINISTRATIVO
# ============================================================
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# CSS visual para dias bloqueados
s=re.sub(r'\s*<style id="sevenBlockedCalendarStyle">.*?</style>\s*','\n',s,flags=re.S)
admin_css=r'''
<style id="sevenBlockedCalendarStyle">
.cell.seven-blocked-day{position:relative!important;background:#f9e7e9!important;overflow:hidden!important;min-height:78px!important}
.cell.seven-blocked-day:after{content:"";position:absolute;left:-18%;top:50%;width:136%;height:3px;background:#b42332;transform:rotate(-24deg);opacity:.72;z-index:1;pointer-events:none}
.seven-blocked-label{position:relative;z-index:2;margin-top:10px;padding:4px 2px;text-align:center;font-size:9px;font-weight:900;color:#9d1d2d;background:#fff9;border-radius:4px;line-height:1.2}
.cell.seven-blocked-day .event{opacity:.38;filter:grayscale(.35)}
.seven-month-actions{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-top:8px}
.seven-month-actions button{font-size:11px!important;padding:8px 10px!important}
@media(max-width:600px){.seven-blocked-label{font-size:7px;margin-top:6px}.seven-month-actions{width:100%}.seven-month-actions button{flex:1;min-width:130px}}
</style>
'''
s=s.replace('</head>',admin_css+'\n</head>',1)

old_render="function renderCalendario(){let y=calMes.getFullYear(),m=calMes.getMonth(),hoje=new Date().toISOString().slice(0,10);$('calTitulo').textContent=MESES[m]+' '+y;let g=$('calGrid');g.innerHTML='';SEMANA.forEach(x=>{let e=document.createElement('div');e.className='weekday';e.textContent=x;g.appendChild(e)});let first=new Date(y,m,1).getDay(),days=new Date(y,m+1,0).getDate();for(let i=0;i<first;i++)g.appendChild(document.createElement('div'));for(let day=1;day<=days;day++){let ds=y+'-'+String(m+1).padStart(2,'0')+'-'+String(day).padStart(2,'0'),ev=agendamentos.filter(a=>a.service_date===ds);let c=document.createElement('div');c.className='cell'+(ds===hoje?' today-cell':'');let n=document.createElement('div');n.className='day';n.textContent=day;c.appendChild(n);ev.slice(0,3).forEach(a=>{let b=document.createElement('button');b.className='event '+classeEvento(a);b.textContent=(a.service_time?a.service_time+' ':'')+(a.client_name||'Cliente');b.title='Abrir cliente';b.onclick=()=>abrirDetalhes(a.id);c.appendChild(b)});if(ev.length>3){let more=document.createElement('div');more.className='more';more.textContent='+'+(ev.length-3)+' mais';c.appendChild(more)}g.appendChild(c)}}"
new_render="function renderCalendario(){let y=calMes.getFullYear(),m=calMes.getMonth(),hoje=new Date().toISOString().slice(0,10);$('calTitulo').textContent=MESES[m]+' '+y;let g=$('calGrid');g.innerHTML='';SEMANA.forEach(x=>{let e=document.createElement('div');e.className='weekday';e.textContent=x;g.appendChild(e)});let first=new Date(y,m,1).getDay(),days=new Date(y,m+1,0).getDate();for(let i=0;i<first;i++)g.appendChild(document.createElement('div'));for(let day=1;day<=days;day++){let ds=y+'-'+String(m+1).padStart(2,'0')+'-'+String(day).padStart(2,'0'),ev=agendamentos.filter(a=>a.service_date===ds),bloqueado=(window.agendaAberta===false)||(Array.isArray(window.diasFechados)&&window.diasFechados.includes(ds));let c=document.createElement('div');c.className='cell'+(ds===hoje?' today-cell':'')+(bloqueado?' seven-blocked-day':'');let n=document.createElement('div');n.className='day';n.textContent=day;c.appendChild(n);if(bloqueado){let lock=document.createElement('div');lock.className='seven-blocked-label';lock.textContent='🔒 SEM VAGA';c.appendChild(lock)}ev.slice(0,3).forEach(a=>{let b=document.createElement('button');b.className='event '+classeEvento(a);b.textContent=(a.service_time?a.service_time+' ':'')+(a.client_name||'Cliente');b.title='Abrir cliente';b.onclick=()=>abrirDetalhes(a.id);c.appendChild(b)});if(ev.length>3){let more=document.createElement('div');more.className='more';more.textContent='+'+(ev.length-3)+' mais';c.appendChild(more)}g.appendChild(c)}}"
if old_render not in s:
    raise SystemExit('ERRO: renderCalendario base não encontrado')
s=s.replace(old_render,new_render,1)

# Controlador isolado para fechar/reabrir o mês atualmente exibido
s=re.sub(r'\s*<script id="sevenMonthBlockingController">.*?</script>\s*','\n',s,flags=re.S)
admin_script=r'''
<script id="sevenMonthBlockingController">
(function(){
 const $=id=>document.getElementById(id);
 function datasMesAtual(){
   const titulo=($('calTitulo')?.textContent||'').trim();
   const meses=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];
   const partes=titulo.toLowerCase().split(/\s+/);const ano=Number(partes.at(-1));const mes=meses.indexOf(partes[0]);
   if(mes<0||!ano)return [];
   const qtd=new Date(ano,mes+1,0).getDate(),out=[];
   for(let d=1;d<=qtd;d++)out.push(ano+'-'+String(mes+1).padStart(2,'0')+'-'+String(d).padStart(2,'0'));
   return out;
 }
 async function salvar(dias){
   if(typeof window.sevenSalvarConfigAgenda!=='function')throw new Error('Configuração da agenda ainda não foi carregada.');
   await window.sevenSalvarConfigAgenda(window.agendaAberta!==false,dias);
   window.diasFechados=dias;window.configAgenda=window.configAgenda||{};window.configAgenda.diasFechados=dias;
   window.renderDiasFechados?.();window.renderCalendario?.();
 }
 window.sevenFecharMesAtual=async function(){
   const datas=datasMesAtual();if(!datas.length)return alert('Não foi possível identificar o mês exibido.');
   if(!confirm('Fechar '+($('calTitulo')?.textContent||'este mês')+' inteiro para novos agendamentos?'))return;
   try{await salvar([...new Set([...(window.diasFechados||[]),...datas])].sort());alert('Mês fechado para novos agendamentos.')}catch(e){console.error(e);alert('Não foi possível fechar o mês.\n\n'+(e?.message||e))}
 };
 window.sevenReabrirMesAtual=async function(){
   const datas=datasMesAtual();if(!datas.length)return alert('Não foi possível identificar o mês exibido.');
   if(!confirm('Reabrir '+($('calTitulo')?.textContent||'este mês')+'? Os dias serão liberados conforme os horários já ocupados.'))return;
   const set=new Set(datas);try{await salvar((window.diasFechados||[]).filter(d=>!set.has(d)));alert('Mês reaberto.')}catch(e){console.error(e);alert('Não foi possível reabrir o mês.\n\n'+(e?.message||e))}
 };
 function instalar(){
   const ctrl=document.querySelector('.agenda-control');if(!ctrl||document.getElementById('sevenMonthActions'))return;
   const box=document.createElement('div');box.id='sevenMonthActions';box.className='seven-month-actions';
   box.innerHTML='<button type="button" class="btn red" onclick="sevenFecharMesAtual()">🔒 Fechar mês</button><button type="button" class="btn green" onclick="sevenReabrirMesAtual()">🔓 Reabrir mês</button>';
   ctrl.appendChild(box);
 }
 document.addEventListener('DOMContentLoaded',instalar);setTimeout(instalar,500);
})();
</script>
'''
pos=s.rfind('</body>');s=s[:pos]+admin_script+'\n'+s[pos:]

for x in ['sevenBlockedCalendarStyle','seven-blocked-day','🔒 SEM VAGA','sevenMonthBlockingController','sevenFecharMesAtual','sevenReabrirMesAtual']:
    if x not in s:raise SystemExit('ERRO admin faltando '+x)
p.write_text(s,encoding='utf-8')

# ============================================================
# SITE PÚBLICO - DISPONIBILIDADE POR PERÍODO
# ============================================================
p=Path('agendar4.html')
s=p.read_text(encoding='utf-8')

# CSS de períodos
s=re.sub(r'\s*<style id="sevenPeriodAvailabilityStyle">.*?</style>\s*','\n',s,flags=re.S)
public_css=r'''
<style id="sevenPeriodAvailabilityStyle">
.period-slots{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:10px}
.period-slot{background:#fff;border:1px solid #bfd0df;color:#0f4c81;border-radius:10px;padding:11px 7px;font-weight:800;line-height:1.25;min-height:62px}
.period-slot small{display:block;font-size:10px;font-weight:600;margin-top:4px;color:#68707a}
.period-slot.sel{background:#1976d2;color:#fff;border-color:#1976d2}.period-slot.sel small{color:#fff}
.period-slot.off{opacity:.42;text-decoration:line-through;background:#eceff2;cursor:not-allowed}
.period-slot.off small{color:#666}
.day.no-vacancy{background:#f8e8ea;border-color:#e0adb3}.day.no-vacancy>b{color:#9d1d2d}.seven-no-vacancy{margin-top:8px;color:#9d1d2d;font-weight:900;text-align:center;padding:8px;border-radius:7px;background:#fff8}
@media(max-width:600px){.period-slots{grid-template-columns:1fr}.period-slot{min-height:54px}}
</style>
'''
s=s.replace('</head>',public_css+'\n</head>',1)

old_helpers="function mins(h){const[a,b]=h.split(':').map(Number);return a*60+b}function hh(m){return String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0')}function iso(d){return d.toISOString().slice(0,10)}function clash(start,dur,a){const x=mins(a.service_time),y=x+Number(a.duration_minutes||60);return start<y&&start+dur>x}async function agendamentos(data){const s=await getDocs(query(collection(db,'agenda_publica'),where('service_date','==',data)));return s.docs.map(x=>x.data()).filter(a=>a.service_status!=='Cancelado'&&a.service_time)}"
new_helpers="function mins(h){const[a,b]=h.split(':').map(Number);return a*60+b}function hh(m){return String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0')}function iso(d){return d.toISOString().slice(0,10)}function clash(start,dur,a){const x=mins(a.service_time),y=x+Number(a.duration_minutes||60);return start<y&&start+dur>x}const PERIODOS=[{id:'manha',nome:'☀️ Manhã',ini:480,fim:720,rotulo:'08h às 12h'},{id:'tarde',nome:'🌤️ Tarde',ini:780,fim:1020,rotulo:'13h às 17h'},{id:'noite',nome:'🌙 Noite',ini:1080,fim:1260,rotulo:'18h às 21h'}];function periodoOcupado(p,ags){return ags.some(a=>{const x=mins(a.service_time),y=x+Number(a.duration_minutes||60);return x<p.fim&&y>p.ini})}function periodoDoHorario(h){const m=mins(h);return PERIODOS.find(p=>m>=p.ini&&m<p.fim)||null}async function agendamentos(data){const s=await getDocs(query(collection(db,'agenda_publica'),where('service_date','==',data)));return s.docs.map(x=>x.data()).filter(a=>a.service_status!=='Cancelado'&&a.service_time)}"
if old_helpers not in s:raise SystemExit('ERRO: helpers públicos não encontrados')
s=s.replace(old_helpers,new_helpers,1)

# Substitui o carregamento de horários de 30min por Manhã/Tarde/Noite
start=s.find("$('load').onclick=async()=>{")
end=s.find("function esc(v)",start)
if start<0 or end<0:raise SystemExit('ERRO: handler load não encontrado')
old_load=s[start:end]
new_load=r'''$('load').onclick=async()=>{clearError();await window.agendaConfigReady;if(!window.agendaAberta){return}if(!(await consultarCEP()))return;if(!$('num').value.trim()||!$('rua').value.trim()||!$('bairro').value.trim()||!$('cidade').value.trim()){error('Preencha o endereço completo.');return}show(3);$('days').textContent='Consultando agenda...';$('cont').disabled=true;chosen=null;const i=info(),today=new Date();today.setHours(0,0,0,0);$('days').innerHTML='';for(let n=0;n<14;n++){const d=new Date(today);d.setDate(today.getDate()+n);if(d.getDay()===0)continue;const data=iso(d),card=document.createElement('div');card.className='day';card.innerHTML='<b>'+d.toLocaleDateString('pt-BR',{weekday:'long',day:'2-digit',month:'2-digit'})+'</b>';if(window.diasFechados.includes(data)){card.classList.add('no-vacancy');card.innerHTML+='<div class="seven-no-vacancy">🔒 SEM VAGA — Data bloqueada</div>';$('days').appendChild(card);continue}const ags=await agendamentos(data);const grid=document.createElement('div');grid.className='period-slots';let livres=0;PERIODOS.forEach(p=>{const b=document.createElement('button');b.className='period-slot';b.type='button';b.innerHTML=p.nome+'<small>'+p.rotulo+'</small>';const durPeriodo=p.fim-p.ini;const ocupado=periodoOcupado(p,ags)||i.dur>durPeriodo;if(ocupado){b.classList.add('off');b.disabled=true;b.title=i.dur>durPeriodo?'O serviço ultrapassa a duração deste período':'Já existe atendimento neste período'}else{livres++;b.onclick=()=>{document.querySelectorAll('.period-slot').forEach(x=>x.classList.remove('sel'));b.classList.add('sel');chosen={date:data,time:hh(p.ini),dur:i.dur,period:p.id,periodName:p.nome,periodLabel:p.rotulo};$('cont').disabled=false}}grid.appendChild(b)});if(!livres){card.classList.add('no-vacancy');card.innerHTML+='<div class="seven-no-vacancy">🔒 SEM VAGA — Todos os períodos ocupados</div>'}card.appendChild(grid);$('days').appendChild(card)}};
'''
s=s[:start]+new_load+s[end:]

# Resumo mostra o período e horário inicial
old_summary="+'<br><b>Data:</b> '+d.toLocaleDateString('pt-BR')+' às '+chosen.time+'<br><br><strong"
new_summary="+'<br><b>Data:</b> '+d.toLocaleDateString('pt-BR')+' — '+(chosen.periodName||'Período')+' ('+(chosen.periodLabel||chosen.time)+')<br><br><strong"
if old_summary in s:s=s.replace(old_summary,new_summary,1)
else:raise SystemExit('ERRO: resumo público não encontrado')

# Validação final por período imediatamente antes de gravar
old_check="if(s.docs.some(x=>{const a=x.data();return a.service_status!=='Cancelado'&&a.service_time&&clash(mins(chosen.time),i.dur,a)})){error('Esse horário acabou de ser ocupado. Escolha outro.');$('send').disabled=false;show(3);return}"
new_check="const periodoAtual=PERIODOS.find(p=>p.id===chosen.period)||periodoDoHorario(chosen.time);if(!periodoAtual){error('Período inválido. Escolha novamente.');$('send').disabled=false;show(3);return}const agsAtuais=s.docs.map(x=>x.data()).filter(a=>a.service_status!=='Cancelado'&&a.service_time);if(periodoOcupado(periodoAtual,agsAtuais)){error('Esse período acabou de ser ocupado. Escolha outro período.');$('send').disabled=false;show(3);return}"
if old_check not in s:raise SystemExit('ERRO: validação final pública não encontrada')
s=s.replace(old_check,new_check,1)

# Grava o período também no registro privado (agenda_publica continua com schema atual)
s=s.replace("service_date:chosen.date,service_time:chosen.time,description:","service_date:chosen.date,service_time:chosen.time,service_period:chosen.period||'',description:",1)

# Mensagem final
s=s.replace("'Seu atendimento foi reservado para '+d.toLocaleDateString('pt-BR')+' às '+chosen.time+'. Valor total:","'Seu atendimento foi reservado para '+d.toLocaleDateString('pt-BR')+' no período '+(chosen.periodName||'selecionado')+' ('+(chosen.periodLabel||chosen.time)+'). Valor total:",1)

for x in ['sevenPeriodAvailabilityStyle','PERIODOS=[','periodoOcupado','period-slots','Todos os períodos ocupados','Esse período acabou de ser ocupado','service_period:chosen.period']:
    if x not in s:raise SystemExit('ERRO público faltando '+x)
p.write_text(s,encoding='utf-8')

print('OK: bloqueio visual, fechar mês e disponibilidade por períodos aplicados na branch de teste')
