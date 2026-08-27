from pathlib import Path
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')
old="window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);const x=await getDoc(doc(db,'agendamentos',id));if(x.exists())await window.sincronizarAgendaPublica(id,x.data());return true}catch(e){console.error(e);return false}};"
new="window.atualizarAgendamentoCloud=async(id,d)=>{try{if(!window.sevenAuth?.currentUser)throw new Error('Usuário não autenticado. Faça login novamente.');await window.sevenAuth.currentUser.getIdToken(true);await updateDoc(doc(db,'agendamentos',id),d);try{const x=await getDoc(doc(db,'agendamentos',id));if(x.exists())await window.sincronizarAgendaPublica(id,x.data())}catch(syncErr){console.warn('Agendamento privado atualizado; falha apenas ao sincronizar agenda pública:',syncErr)}return true}catch(e){console.error('Erro ao atualizar agendamento:',e);window.sevenLastUpdateError=e;return false}};"
if old not in s:
    if new in s:
        print('Correção já aplicada')
    else:
        raise SystemExit('Trecho atualizarAgendamentoCloud não encontrado')
else:
    s=s.replace(old,new,1)
old2="async function atualizarAgenda(){let id=$('idEditando').value;if(!id){alert('Nenhum agendamento selecionado.');return}let d=capturar();if(!d.client_name||!d.service_date){alert('Preencha Nome e Data.');return}let ok=await window.atualizarAgendamentoCloud(id,d);if(ok){fecharDetalhes();limparFormulario();alert('Agendamento atualizado com sucesso!')}else alert('Erro ao atualizar.')}"
new2="async function atualizarAgenda(){let id=$('idEditando').value;if(!id){alert('Nenhum agendamento selecionado.');return}let d=capturar();if(!d.client_name||!d.service_date){alert('Preencha Nome e Data.');return}const btn=$('btnAtualizar');btn?.classList.add('loading');if(btn)btn.disabled=true;try{let ok=await window.atualizarAgendamentoCloud(id,d);if(ok){let a=agendamentos.find(x=>String(x.id)===String(id));if(a)Object.assign(a,d);renderCalendario();if($('telaResumo')?.classList.contains('active'))renderResumo();fecharDetalhes();limparFormulario();alert('Agendamento atualizado com sucesso!')}else{const e=window.sevenLastUpdateError;alert('Erro ao atualizar.'+(e?.message?'\\n\\n'+e.message:''))}}finally{btn?.classList.remove('loading');if(btn)btn.disabled=false}}"
if old2 not in s:
    if new2 in s:
        print('Handler já corrigido')
    else:
        raise SystemExit('Função atualizarAgenda não encontrada')
else:
    s=s.replace(old2,new2,1)
if 'window.sevenLastUpdateError=e' not in s or "getIdToken(true)" not in s:
    raise SystemExit('Validação da correção falhou')
p.write_text(s,encoding='utf-8')
print('OK: salvamento de alterações corrigido')
