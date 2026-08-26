from pathlib import Path
import re

# ===== Página pública: consulta apenas agenda_publica e grava dados privados separadamente =====
p=Path('agendar4.html')
s=p.read_text(encoding='utf-8')

old_import="import{getFirestore,collection,query,where,getDocs,addDoc,doc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
new_import="import{getFirestore,collection,query,where,getDocs,addDoc,setDoc,doc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
if old_import in s:
    s=s.replace(old_import,new_import,1)
elif 'addDoc,setDoc,doc,getDoc' not in s:
    raise SystemExit('Import Firestore do agendar4 não encontrado')

s=s.replace("query(collection(db,'agendamentos'),where('service_date','==',data))","query(collection(db,'agenda_publica'),where('service_date','==',data))")
s=s.replace("query(collection(db,'agendamentos'),where('service_date','==',chosen.date))","query(collection(db,'agenda_publica'),where('service_date','==',chosen.date))")

already_public = "agenda_publica',novoAgendamento.id" in s
if not already_public:
    old="await addDoc(collection(db,'agendamentos'),{receipt_number:'WEB-'+Date.now().toString().slice(-6),client_name:"
    if old not in s:
        raise SystemExit('Criação pública do agendamento não encontrada')
    s=s.replace(old,"const novoAgendamento=await addDoc(collection(db,'agendamentos'),{receipt_number:'WEB-'+Date.now().toString().slice(-6),client_name:",1)
    marker="created_at:new Date().toISOString()});const d=new Date(chosen.date+'T12:00:00');"
    repl="created_at:new Date().toISOString()});await setDoc(doc(db,'agenda_publica',novoAgendamento.id),{service_date:chosen.date,service_time:chosen.time,duration_minutes:i.dur,service_status:'Agendado'});const d=new Date(chosen.date+'T12:00:00');"
    if marker not in s:
        raise SystemExit('Final da criação pública não encontrado')
    s=s.replace(marker,repl,1)

if "collection(db,'agendamentos'),where('service_date'" in s:
    raise SystemExit('Leitura pública de dados privados ainda presente')
for required in ["collection(db,'agenda_publica')","agenda_publica',novoAgendamento.id","addDoc,setDoc,doc,getDoc"]:
    if required not in s:
        raise SystemExit('Proteção pública incompleta: '+required)
p.write_text(s,encoding='utf-8')

# ===== Painel: sincronização contínua + migração inicial =====
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

old_panel_import="getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc}"
new_panel_import="getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc,getDocs}"
if old_panel_import in s:
    s=s.replace(old_panel_import,new_panel_import,1)
elif 'getDoc,getDocs}' not in s:
    raise SystemExit('Import Firestore do painel não encontrado')

old_funcs="window.salvarAgendamentoCloud=async d=>{try{return(await addDoc(collection(db,'agendamentos'),d)).id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));return true}catch(e){console.error(e);return false}};"
new_funcs="window.sincronizarAgendaPublica=async(id,d)=>{const ref=doc(db,'agenda_publica',id);if(d&&d.service_date&&d.service_time&&d.service_status!=='Cancelado'){await setDoc(ref,{service_date:d.service_date,service_time:d.service_time,duration_minutes:Number(d.duration_minutes||60),service_status:d.service_status||'Agendado'})}else{try{await deleteDoc(ref)}catch(e){}}};window.salvarAgendamentoCloud=async d=>{try{const r=await addDoc(collection(db,'agendamentos'),d);await window.sincronizarAgendaPublica(r.id,d);return r.id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);const x=await getDoc(doc(db,'agendamentos',id));if(x.exists())await window.sincronizarAgendaPublica(id,x.data());return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));try{await deleteDoc(doc(db,'agenda_publica',id))}catch(e){}return true}catch(e){console.error(e);return false}};"
if old_funcs in s:
    s=s.replace(old_funcs,new_funcs,1)
elif 'window.sincronizarAgendaPublica=' not in s:
    raise SystemExit('Funções cloud do painel não encontradas')

# Substitui sempre a função de migração para garantir diagnóstico detalhado.
migration="""window.migrarAgendaPublica=async function(){if(!window.sevenAuth?.currentUser){const e=new Error('Usuário não autenticado');e.code='auth-required';throw e}let snap;try{snap=await getDocs(collection(db,'agendamentos'))}catch(e){e.message='Falha ao LER agendamentos: '+(e.message||e.code||'erro desconhecido');throw e}let total=0,ignorados=0;for(const d of snap.docs){const a=d.data();if(!a.service_date||!a.service_time||a.service_status==='Cancelado'){ignorados++;continue}try{await setDoc(doc(db,'agenda_publica',d.id),{service_date:String(a.service_date),service_time:String(a.service_time),duration_minutes:Number(a.duration_minutes||60),service_status:a.service_status||'Agendado'});total++}catch(e){e.message='Falha ao GRAVAR agenda_publica no documento '+d.id+': '+(e.message||e.code||'erro desconhecido');throw e}}return{total,ignorados}};"""
if 'window.migrarAgendaPublica=' in s:
    s=re.sub(r"window\.migrarAgendaPublica=async function\(\)\{.*?\};(?=window\.salvarConfigAgenda=async)",migration,s,count=1,flags=re.S)
else:
    pos=s.find('window.salvarConfigAgenda=async')
    if pos<0:
        raise SystemExit('Ponto de migração não encontrado')
    s=s[:pos]+migration+s[pos:]

button='<button id="btnMigrarAgendaPublica" class="btn blue" type="button" onclick="executarMigracaoAgendaPublica()">🔄 Sincronizar horários</button><span id="statusMigracaoAgendaPublica" style="font-size:12px;color:#68707a"></span>'
if 'id="btnMigrarAgendaPublica"' not in s:
    target='<button id="btnFecharAgenda" class="btn red" onclick="alternarAgenda()">🔒 Fechar agenda</button>'
    if target not in s:
        raise SystemExit('Botão Fechar agenda não encontrado')
    s=s.replace(target,target+button,1)

helper="""window.executarMigracaoAgendaPublica=async function(){const b=document.getElementById('btnMigrarAgendaPublica'),st=document.getElementById('statusMigracaoAgendaPublica');if(!window.sevenAuth?.currentUser){alert('Faça login novamente.');return}b.disabled=true;st.textContent='Sincronizando...';try{await window.sevenAuth.currentUser.getIdToken(true);const r=await window.migrarAgendaPublica();st.textContent='✅ '+r.total+' horários sincronizados';alert('Sincronização concluída: '+r.total+' horários copiados'+(r.ignorados?' • '+r.ignorados+' ignorados sem horário ou cancelados.':'.'));}catch(e){console.error('ERRO SINCRONIZAÇÃO:',e);const codigo=e?.code||'sem-codigo';const mensagem=e?.message||String(e);st.textContent='❌ '+codigo;alert('Erro na sincronização\n\nCódigo: '+codigo+'\n\nDetalhe: '+mensagem+'\n\nCopie ou tire uma foto desta mensagem para fazermos a correção exata.');}finally{b.disabled=false}};"""
if 'window.executarMigracaoAgendaPublica=' in s:
    s=re.sub(r"window\.executarMigracaoAgendaPublica=async function\(\)\{.*?\};(?=</script>)",helper,s,count=1,flags=re.S)
else:
    pos=s.rfind('</script>')
    if pos<0:
        raise SystemExit('Script final do painel não encontrado')
    s=s[:pos]+helper+s[pos:]

for required in ['window.migrarAgendaPublica=','btnMigrarAgendaPublica','ERRO SINCRONIZAÇÃO:','Código: ','getIdToken(true)']:
    if required not in s:
        raise SystemExit('Diagnóstico incompleto: '+required)

p.write_text(s,encoding='utf-8')
print('Diagnóstico detalhado da sincronização aplicado')
