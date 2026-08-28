from pathlib import Path

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

old="window.salvarAgendamentoCloud=async d=>{try{const r=await addDoc(collection(db,'agendamentos'),d);await window.sincronizarAgendaPublica(r.id,d);return r.id}catch(e){console.error(e);return null}};"
new="window.salvarAgendamentoCloud=async d=>{try{if(!window.sevenAuth?.currentUser)throw new Error('Usuário não autenticado. Faça login novamente.');await window.sevenAuth.currentUser.getIdToken(true);const r=await addDoc(collection(db,'agendamentos'),d);try{await window.sincronizarAgendaPublica(r.id,d)}catch(syncErr){console.warn('Novo cliente salvo; falha apenas ao sincronizar agenda pública:',syncErr)}window.sevenLastCreateError=null;return r.id}catch(e){console.error('Erro ao salvar novo cliente:',e);window.sevenLastCreateError=e;return null}};"
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('ERRO: função salvarAgendamentoCloud não encontrada')

old2="async function salvarNaAgenda(){let d=capturar();if(!d.client_name||!d.service_date){alert('Preencha Nome e Data.');return}if(agendamentos.some(a=>a.receipt_number===d.receipt_number)){alert('Este número de recibo já existe.');return}$('btnSalvar').classList.add('loading');let id=await window.salvarAgendamentoCloud(d);$('btnSalvar').classList.remove('loading');if(id){limparFormulario();alert('Agendamento salvo!')}else alert('Não foi possível salvar.')}"
new2="async function salvarNaAgenda(){let d=capturar();if(!d.client_name||!d.service_date){alert('Preencha Nome e Data.');return}if(agendamentos.some(a=>a.receipt_number===d.receipt_number)){alert('Este número de recibo já existe.');return}const btn=$('btnSalvar');btn.classList.add('loading');btn.disabled=true;const texto=btn.innerHTML;btn.textContent='⏳ Salvando...';try{let id=await window.salvarAgendamentoCloud(d);if(id){limparFormulario();renderCalendario();alert('Agendamento salvo!')}else{const e=window.sevenLastCreateError;alert('Não foi possível salvar.'+(e?.message?'\\n\\n'+e.message:''))}}finally{btn.classList.remove('loading');btn.disabled=false;btn.innerHTML=texto}}"
if old2 in s:
    s=s.replace(old2,new2,1)
elif new2 not in s:
    raise SystemExit('ERRO: função salvarNaAgenda não encontrada')

for token in ["window.sevenLastCreateError=e","getIdToken(true)","Novo cliente salvo; falha apenas ao sincronizar agenda pública","⏳ Salvando..."]:
    if token not in s:
        raise SystemExit('ERRO: validação falhou: '+token)

p.write_text(s,encoding='utf-8')
print('OK: novo cliente agora salva com autenticação renovada e sincronização pública separada')
