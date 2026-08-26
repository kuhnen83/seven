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

# Corrige o módulo principal, se existir.
s=s.replace("import{initializeApp}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js';import{getFirestore,", "import{initializeApp,getApps,getApp}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js';import{getFirestore,")
s=s.replace("const app=initializeApp(firebaseConfig);const db=getFirestore(app);const auth=getAuth(app);", "const app=getApps().length?getApp():initializeApp(firebaseConfig);const db=getFirestore(app);const auth=getAuth(app);")

# Mantém botão visível e renomeia para V5 para confirmar publicação.
s=re.sub(r'>🔄 Sincronizar horários v\d+</button>','>🔄 Sincronizar horários v5</button>',s)
s=s.replace('>🔄 Sincronizar horários</button>','>🔄 Sincronizar horários v5</button>')

# Remove recuperação anterior, se houver.
s=re.sub(r'<script type="module" id="sevenAgendaRecovery">.*?</script>','',s,flags=re.S)

# Módulo independente: não depende do módulo principal da agenda.
recovery=r'''
<script type="module" id="sevenAgendaRecovery">
import { getApps, getApp, initializeApp } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js';
import { getAuth, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';
import { getFirestore, collection, query, orderBy, onSnapshot, getDocs, doc, setDoc } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';

const cfg={apiKey:'AIzaSyAN8PKdOni3mJC-DvAFfjHI1ohBpi7eb28',authDomain:'agendaseven-428ad.firebaseapp.com',projectId:'agendaseven-428ad',storageBucket:'agendaseven-428ad.firebasestorage.app',messagingSenderId:'908846325130',appId:'1:908846325130:web:e5badefe60a02740bc3c73',measurementId:'G-JRKKZWRFCN'};
const app=getApps().length?getApp():initializeApp(cfg);
const auth=getAuth(app);
const db=getFirestore(app);
let unsub=null;

function status(txt){const st=document.getElementById('statusMigracaoAgendaPublica');if(st)st.textContent=txt}
function renderClientes(lista){
  window.agendamentos=lista;
  try{if(typeof window.gerarProximoNumeroRecibo==='function')window.gerarProximoNumeroRecibo()}catch(e){console.warn(e)}
  try{if(typeof window.renderCalendario==='function')window.renderCalendario()}catch(e){console.warn(e)}
  try{const r=document.getElementById('telaResumo');if(r?.classList.contains('active')&&typeof window.renderResumo==='function')window.renderResumo()}catch(e){console.warn(e)}
}
function iniciar(){
  if(unsub){unsub();unsub=null}
  if(!auth.currentUser){renderClientes([]);status('Aguardando login...');return}
  status('Carregando clientes...');
  const q=query(collection(db,'agendamentos'),orderBy('service_date'));
  unsub=onSnapshot(q,snap=>{
    const lista=snap.docs.map(x=>({id:x.id,...x.data()}));
    renderClientes(lista);
    status('✅ '+lista.length+' clientes carregados');
  },e=>{
    console.error('SEVEN RECOVERY - clientes:',e);
    status('❌ Erro ao carregar clientes: '+(e.code||e.message||e));
  });
}

window.executarMigracaoAgendaPublica=async function(){
  const b=document.getElementById('btnMigrarAgendaPublica');
  if(!auth.currentUser){alert('Faça login novamente.');return}
  if(b){b.disabled=true;b.textContent='⏳ Sincronizando...'}
  status('Lendo agendamentos...');
  try{
    await auth.currentUser.getIdToken(true);
    const snap=await getDocs(collection(db,'agendamentos'));
    let total=0,ignorados=0;
    for(const d of snap.docs){
      const a=d.data();
      if(!a.service_date||!a.service_time||a.service_status==='Cancelado'){ignorados++;continue}
      await setDoc(doc(db,'agenda_publica',d.id),{
        service_date:String(a.service_date),
        service_time:String(a.service_time),
        duration_minutes:Number(a.duration_minutes||60),
        service_status:a.service_status||'Agendado'
      });
      total++;
    }
    const m='✅ Sincronização concluída: '+total+' horários copiados'+(ignorados?' • '+ignorados+' ignorados.':'.');
    status(m);alert(m);
  }catch(e){
    console.error('SEVEN RECOVERY - sincronização:',e);
    const codigo=e?.code||'sem-codigo';const detalhe=e?.message||String(e);
    status('❌ '+codigo+' — '+detalhe);
    alert('Falha na sincronização\n\nCódigo: '+codigo+'\n\nDetalhe: '+detalhe);
  }finally{
    if(b){b.disabled=false;b.textContent='🔄 Sincronizar horários v5'}
  }
};

document.addEventListener('DOMContentLoaded',()=>{
  const b=document.getElementById('btnMigrarAgendaPublica');
  if(b){b.onclick=null;b.addEventListener('click',window.executarMigracaoAgendaPublica)}
});
onAuthStateChanged(auth,user=>{if(user)iniciar();else{if(unsub){unsub();unsub=null}renderClientes([]);status('Aguardando login...')}});
</script>
'''

pos=s.rfind('</body>')
if pos<0:raise SystemExit('body não encontrado')
s=s[:pos]+recovery+'\n'+s[pos:]

for required in ['sevenAgendaRecovery','✅ "+lista.length+" clientes carregados' if False else 'clientes carregados','Sincronizar horários v5','onSnapshot(q,snap=>']:
    if required not in s:raise SystemExit('Recuperação incompleta: '+required)

p.write_text(s,encoding='utf-8')
print('Módulo independente de recuperação da agenda instalado')
