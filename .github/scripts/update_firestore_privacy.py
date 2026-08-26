from pathlib import Path
import re

# ===== Página pública: consulta apenas agenda_publica e grava dados privados separadamente =====
p=Path('agendar4.html')
s=p.read_text(encoding='utf-8')
old_import="import{getFirestore,collection,query,where,getDocs,addDoc,doc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
new_import="import{getFirestore,collection,query,where,getDocs,addDoc,setDoc,doc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
if old_import in s:s=s.replace(old_import,new_import,1)
elif 'addDoc,setDoc,doc,getDoc' not in s:raise SystemExit('Import Firestore do agendar4 não encontrado')
s=s.replace("query(collection(db,'agendamentos'),where('service_date','==',data))","query(collection(db,'agenda_publica'),where('service_date','==',data))")
s=s.replace("query(collection(db,'agendamentos'),where('service_date','==',chosen.date))","query(collection(db,'agenda_publica'),where('service_date','==',chosen.date))")
already_public="agenda_publica',novoAgendamento.id" in s
if not already_public:
    old="await addDoc(collection(db,'agendamentos'),{receipt_number:'WEB-'+Date.now().toString().slice(-6),client_name:"
    if old not in s:raise SystemExit('Criação pública do agendamento não encontrada')
    s=s.replace(old,"const novoAgendamento=await addDoc(collection(db,'agendamentos'),{receipt_number:'WEB-'+Date.now().toString().slice(-6),client_name:",1)
    marker="created_at:new Date().toISOString()});const d=new Date(chosen.date+'T12:00:00');"
    repl="created_at:new Date().toISOString()});await setDoc(doc(db,'agenda_publica',novoAgendamento.id),{service_date:chosen.date,service_time:chosen.time,duration_minutes:i.dur,service_status:'Agendado'});const d=new Date(chosen.date+'T12:00:00');"
    if marker not in s:raise SystemExit('Final da criação pública não encontrado')
    s=s.replace(marker,repl,1)
if "collection(db,'agendamentos'),where('service_date'" in s:raise SystemExit('Leitura pública de dados privados ainda presente')
p.write_text(s,encoding='utf-8')

# ===== Painel =====
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Evita que o navegador continue usando uma cópia antiga durante esta migração.
if 'http-equiv="Cache-Control"' not in s:
    s=s.replace('<meta name="viewport" content="width=device-width,initial-scale=1.0">','<meta name="viewport" content="width=device-width,initial-scale=1.0">\n<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n<meta http-equiv="Pragma" content="no-cache">\n<meta http-equiv="Expires" content="0">',1)

old_panel_import="getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc}"
new_panel_import="getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc,getDocs}"
if old_panel_import in s:s=s.replace(old_panel_import,new_panel_import,1)
elif 'getDoc,getDocs}' not in s:raise SystemExit('Import Firestore do painel não encontrado')

# Garante sincronização contínua.
old_funcs="window.salvarAgendamentoCloud=async d=>{try{return(await addDoc(collection(db,'agendamentos'),d)).id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));return true}catch(e){console.error(e);return false}};"
new_funcs="window.sincronizarAgendaPublica=async(id,d)=>{const ref=doc(db,'agenda_publica',id);if(d&&d.service_date&&d.service_time&&d.service_status!=='Cancelado'){await setDoc(ref,{service_date:String(d.service_date),service_time:String(d.service_time),duration_minutes:Number(d.duration_minutes||60),service_status:d.service_status||'Agendado'})}else{try{await deleteDoc(ref)}catch(e){}}};window.salvarAgendamentoCloud=async d=>{try{const r=await addDoc(collection(db,'agendamentos'),d);await window.sincronizarAgendaPublica(r.id,d);return r.id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);const x=await getDoc(doc(db,'agendamentos',id));if(x.exists())await window.sincronizarAgendaPublica(id,x.data());return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));try{await deleteDoc(doc(db,'agenda_publica',id))}catch(e){}return true}catch(e){console.error(e);return false}};"
if old_funcs in s:s=s.replace(old_funcs,new_funcs,1)
elif 'window.sincronizarAgendaPublica=' not in s:raise SystemExit('Funções cloud do painel não encontradas')

# Migração com teste explícito de permissão e diagnóstico por etapa.
migration="""window.migrarAgendaPublica=async function(){
if(!window.sevenAuth?.currentUser){const e=new Error('Usuário não autenticado no Firebase Authentication');e.code='auth-required';throw e}
await window.sevenAuth.currentUser.getIdToken(true);
const testeId='__teste_migracao__';
try{await setDoc(doc(db,'agenda_publica',testeId),{service_date:'2099-01-01',service_time:'00:00',duration_minutes:1,service_status:'Agendado'});await deleteDoc(doc(db,'agenda_publica',testeId))}catch(e){const x=new Error('TESTE DE ESCRITA em agenda_publica falhou: '+(e.message||e.code||e));x.code=e.code||'write-test-failed';throw x}
let snap;
try{snap=await getDocs(collection(db,'agendamentos'))}catch(e){const x=new Error('LEITURA de agendamentos falhou: '+(e.message||e.code||e));x.code=e.code||'read-failed';throw x}
let total=0,ignorados=0;
for(const d of snap.docs){const a=d.data();if(!a.service_date||!a.service_time||a.service_status==='Cancelado'){ignorados++;continue}try{await setDoc(doc(db,'agenda_publica',d.id),{service_date:String(a.service_date),service_time:String(a.service_time),duration_minutes:Number(a.duration_minutes||60),service_status:a.service_status||'Agendado'});total++}catch(e){const x=new Error('GRAVAÇÃO do documento '+d.id+' falhou: '+(e.message||e.code||e));x.code=e.code||'document-write-failed';throw x}}
return{total,ignorados}};"""
if 'window.migrarAgendaPublica=' in s:
    s=re.sub(r"window\.migrarAgendaPublica=async function\(\)\{.*?\};(?=window\.salvarConfigAgenda=async)",migration,s,count=1,flags=re.S)
else:
    pos=s.find('window.salvarConfigAgenda=async')
    if pos<0:raise SystemExit('Ponto de migração não encontrado')
    s=s[:pos]+migration+s[pos:]

# Botão com versão visível para confirmar que o navegador carregou o arquivo correto.
s=s.replace('>🔄 Sincronizar horários</button>','>🔄 Sincronizar horários v2</button>')
if 'id="btnMigrarAgendaPublica"' not in s:
    target='<button id="btnFecharAgenda" class="btn red" onclick="alternarAgenda()">🔒 Fechar agenda</button>'
    button='<button id="btnMigrarAgendaPublica" class="btn blue" type="button" onclick="executarMigracaoAgendaPublica()">🔄 Sincronizar horários v2</button><span id="statusMigracaoAgendaPublica" style="font-size:12px;color:#68707a"></span>'
    if target not in s:raise SystemExit('Botão Fechar agenda não encontrado')
    s=s.replace(target,target+button,1)

helper="""window.executarMigracaoAgendaPublica=async function(){const b=document.getElementById('btnMigrarAgendaPublica'),st=document.getElementById('statusMigracaoAgendaPublica');if(!window.sevenAuth?.currentUser){alert('Faça login novamente.');return}b.disabled=true;st.style.whiteSpace='pre-wrap';st.textContent='Sincronizando...';try{const r=await window.migrarAgendaPublica();const ok='✅ Sincronização concluída: '+r.total+' horários copiados'+(r.ignorados?' • '+r.ignorados+' ignorados.':'.');st.textContent=ok;alert(ok)}catch(e){console.error('ERRO SINCRONIZAÇÃO V2:',e);const codigo=e&&e.code?e.code:'sem-codigo';const mensagem=e&&e.message?e.message:String(e);const txt='❌ ERRO '+codigo+' — '+mensagem;st.textContent=txt;alert('SINCRONIZAÇÃO V2 FALHOU\n\nCódigo: '+codigo+'\n\nDetalhe: '+mensagem)}finally{b.disabled=false}};"""
if 'window.executarMigracaoAgendaPublica=' in s:
    s=re.sub(r"window\.executarMigracaoAgendaPublica=async function\(\)\{.*?\};(?=</script>)",helper,s,count=1,flags=re.S)
else:
    pos=s.rfind('</script>');
    if pos<0:raise SystemExit('Script final do painel não encontrado')
    s=s[:pos]+helper+s[pos:]

for required in ['Sincronizar horários v2','SINCRONIZAÇÃO V2 FALHOU','__teste_migracao__','Cache-Control','window.migrarAgendaPublica=']:
    if required not in s:raise SystemExit('Diagnóstico V2 incompleto: '+required)
p.write_text(s,encoding='utf-8')
print('Sincronização V2 aplicada com teste de permissão, diagnóstico e anti-cache')
