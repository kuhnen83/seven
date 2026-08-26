from pathlib import Path
import re

# ===== Página pública =====
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
if 'http-equiv="Cache-Control"' not in s:
    s=s.replace('<meta name="viewport" content="width=device-width,initial-scale=1.0">','<meta name="viewport" content="width=device-width,initial-scale=1.0">\n<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n<meta http-equiv="Pragma" content="no-cache">\n<meta http-equiv="Expires" content="0">',1)

old_panel_import="getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc}"
new_panel_import="getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc,getDocs}"
if old_panel_import in s:s=s.replace(old_panel_import,new_panel_import,1)
elif 'getDoc,getDocs}' not in s:raise SystemExit('Import Firestore do painel não encontrado')

# Sincronização contínua dos novos/alterados/excluídos.
old_funcs="window.salvarAgendamentoCloud=async d=>{try{return(await addDoc(collection(db,'agendamentos'),d)).id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));return true}catch(e){console.error(e);return false}};"
new_funcs="window.sincronizarAgendaPublica=async(id,d)=>{const ref=doc(db,'agenda_publica',id);if(d&&d.service_date&&d.service_time&&d.service_status!=='Cancelado'){await setDoc(ref,{service_date:String(d.service_date),service_time:String(d.service_time),duration_minutes:Number(d.duration_minutes||60),service_status:d.service_status||'Agendado'})}else{try{await deleteDoc(ref)}catch(e){}}};window.salvarAgendamentoCloud=async d=>{try{const r=await addDoc(collection(db,'agendamentos'),d);await window.sincronizarAgendaPublica(r.id,d);return r.id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);const x=await getDoc(doc(db,'agendamentos',id));if(x.exists())await window.sincronizarAgendaPublica(id,x.data());return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));try{await deleteDoc(doc(db,'agenda_publica',id))}catch(e){}return true}catch(e){console.error(e);return false}};"
if old_funcs in s:s=s.replace(old_funcs,new_funcs,1)
elif 'window.sincronizarAgendaPublica=' not in s:raise SystemExit('Funções cloud do painel não encontradas')

# Migração robusta dos horários antigos.
block="""window.migrarAgendaPublica=async function(){
if(!auth.currentUser){const e=new Error('Usuário não autenticado no Firebase Authentication');e.code='auth-required';throw e}
await auth.currentUser.getIdToken(true);
let snap;try{snap=await getDocs(collection(db,'agendamentos'))}catch(e){const x=new Error('LEITURA de agendamentos falhou: '+(e.message||e.code||e));x.code=e.code||'read-failed';throw x}
let total=0,ignorados=0;
for(const d of snap.docs){const a=d.data();if(!a.service_date||!a.service_time||a.service_status==='Cancelado'){ignorados++;continue}try{await setDoc(doc(db,'agenda_publica',d.id),{service_date:String(a.service_date),service_time:String(a.service_time),duration_minutes:Number(a.duration_minutes||60),service_status:a.service_status||'Agendado'});total++}catch(e){const x=new Error('GRAVAÇÃO do documento '+d.id+' falhou: '+(e.message||e.code||e));x.code=e.code||'document-write-failed';throw x}}
return{total,ignorados}};
window.executarMigracaoAgendaPublica=async function(){
const b=document.getElementById('btnMigrarAgendaPublica'),st=document.getElementById('statusMigracaoAgendaPublica');if(!b||!st){alert('Erro interno: botão de sincronização não encontrado.');return}
if(!auth.currentUser){alert('Sua sessão não está autenticada no Firebase. Saia e entre novamente.');return}
b.disabled=true;b.textContent='⏳ Sincronizando...';st.style.whiteSpace='pre-wrap';st.textContent='Lendo agendamentos...';
try{const r=await window.migrarAgendaPublica();const ok='✅ Sincronização concluída: '+r.total+' horários copiados'+(r.ignorados?' • '+r.ignorados+' ignorados.':'.');st.textContent=ok;alert(ok)}catch(e){console.error('ERRO SINCRONIZAÇÃO:',e);const codigo=e?.code||'sem-codigo',mensagem=e?.message||String(e);st.textContent='❌ '+codigo+' — '+mensagem;alert('Falha na sincronização\n\nCódigo: '+codigo+'\n\nDetalhe: '+mensagem)}finally{b.disabled=false;b.textContent='🔄 Sincronizar horários v3'}};
"""
s=re.sub(r"window\.migrarAgendaPublica=async function\(\)\{.*?\};(?=window\.salvarConfigAgenda=async)",'',s,count=1,flags=re.S)
s=re.sub(r"window\.executarMigracaoAgendaPublica=async function\(\)\{.*?\};",'',s,flags=re.S)
pos=s.find('window.salvarConfigAgenda=async')
if pos<0:raise SystemExit('Ponto para inserir migração não encontrado')
s=s[:pos]+block+s[pos:]

# CORREÇÃO PRINCIPAL: clientes só são lidos DEPOIS que o Firebase confirma o login.
old_listener=re.compile(r"window\.addEventListener\('DOMContentLoaded',async\(\)=>\{window\.configAgenda=.*?onSnapshot\(q,s=>\{agendamentos=s\.docs\.map\(x=>\(\{id:x\.id,\.\.\.x\.data\(\)\}\)\);gerarProximoNumeroRecibo\(\);renderCalendario\(\);if\(document\.getElementById\('telaResumo'\)\.classList\.contains\('active'\)\)renderResumo\(\)\},e=>console\.error\('Firestore',e\)\)\}\);",re.S)
listener="""let sevenAgendaUnsub=null;
function iniciarLeituraPrivada(){if(sevenAgendaUnsub){sevenAgendaUnsub();sevenAgendaUnsub=null}if(!auth.currentUser){agendamentos=[];renderCalendario();return}const q=query(collection(db,'agendamentos'),orderBy('service_date'));sevenAgendaUnsub=onSnapshot(q,snap=>{agendamentos=snap.docs.map(x=>({id:x.id,...x.data()}));gerarProximoNumeroRecibo();renderCalendario();if(document.getElementById('telaResumo').classList.contains('active'))renderResumo();const st=document.getElementById('statusMigracaoAgendaPublica');if(st&&st.textContent.includes('Carregando'))st.textContent='✅ '+agendamentos.length+' clientes carregados';},e=>{console.error('Firestore privado',e);const st=document.getElementById('statusMigracaoAgendaPublica');if(st)st.textContent='❌ Erro ao carregar clientes: '+(e.code||e.message);});}
window.addEventListener('DOMContentLoaded',async()=>{window.configAgenda=await window.carregarConfigAgenda();window.diasFechados=window.configAgenda.diasFechados||[];window.aplicarStatusAgenda(window.configAgenda.aberta);window.renderDiasFechados();const st=document.getElementById('statusMigracaoAgendaPublica');if(st)st.textContent='Carregando clientes...';onAuthStateChanged(auth,user=>{if(user){iniciarLeituraPrivada()}else{if(sevenAgendaUnsub){sevenAgendaUnsub();sevenAgendaUnsub=null}agendamentos=[];renderCalendario()}});});"""
if old_listener.search(s):s=old_listener.sub(listener,s,count=1)
elif 'function iniciarLeituraPrivada()' not in s:raise SystemExit('Listener antigo de agendamentos não encontrado')

# Botão V3 e listener direto, além do onclick.
s=s.replace('onclick="executarMigracaoAgendaPublica()"','onclick="window.executarMigracaoAgendaPublica()"')
s=s.replace('onclick="window.executarMigracaoAgendaPublica()">🔄 Sincronizar horários v2</button>','onclick="window.executarMigracaoAgendaPublica()">🔄 Sincronizar horários v3</button>')
s=s.replace('>🔄 Sincronizar horários v2</button>','>🔄 Sincronizar horários v3</button>')

# Adiciona ligação adicional após DOM carregado para evitar qualquer problema de onclick inline.
extra="""window.addEventListener('DOMContentLoaded',()=>{const b=document.getElementById('btnMigrarAgendaPublica');if(b){b.onclick=null;b.addEventListener('click',()=>window.executarMigracaoAgendaPublica())}});"""
if extra not in s:
    pos=s.find('window.salvarConfigAgenda=async')
    s=s[:pos]+extra+s[pos:]

for required in ['function iniciarLeituraPrivada()','onAuthStateChanged(auth,user=>','Sincronizar horários v3','addEventListener(\'click\'','window.executarMigracaoAgendaPublica=async function']:
    if required not in s:raise SystemExit('Correção incompleta: '+required)
p.write_text(s,encoding='utf-8')
print('Clientes restaurados após autenticação e sincronização V3 corrigida')
