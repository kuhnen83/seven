from pathlib import Path

p = Path('agendamento2.html')
s = p.read_text(encoding='utf-8')

old_import = "import{getAuth,signInWithEmailAndPassword,onAuthStateChanged}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';"
new_import = "import{getAuth,signInWithEmailAndPassword,onAuthStateChanged,setPersistence,browserSessionPersistence,signOut}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';"
if old_import in s:
    s = s.replace(old_import, new_import, 1)
elif new_import not in s:
    raise SystemExit('Import do Firebase Auth não encontrado')

old_auth = "const firebaseConfig={apiKey:'AIzaSyAN8PKdOni3mJC-DvAFfjHI1ohBpi7eb28',authDomain:'agendaseven-428ad.firebaseapp.com',projectId:'agendaseven-428ad',storageBucket:'agendaseven-428ad.firebasestorage.app',messagingSenderId:'908846325130',appId:'1:908846325130:web:e5badefe60a02740bc3c73',measurementId:'G-JRKKZWRFCN'};const app=initializeApp(firebaseConfig);const db=getFirestore(app);const auth=getAuth(app);window.sevenAuth=auth;window.sevenSignIn=signInWithEmailAndPassword;window.sevenAuthState=onAuthStateChanged;"
new_auth = "const firebaseConfig={apiKey:'AIzaSyAN8PKdOni3mJC-DvAFfjHI1ohBpi7eb28',authDomain:'agendaseven-428ad.firebaseapp.com',projectId:'agendaseven-428ad',storageBucket:'agendaseven-428ad.firebasestorage.app',messagingSenderId:'908846325130',appId:'1:908846325130:web:e5badefe60a02740bc3c73',measurementId:'G-JRKKZWRFCN'};const app=initializeApp(firebaseConfig);const db=getFirestore(app);const auth=getAuth(app);window.sevenAuth=auth;window.sevenSignIn=signInWithEmailAndPassword;window.sevenAuthState=onAuthStateChanged;window.sevenSetPersistence=setPersistence;window.sevenBrowserSessionPersistence=browserSessionPersistence;window.sevenSignOut=signOut;setPersistence(auth,browserSessionPersistence).catch(e=>console.error('Persistência da autenticação',e));"
if old_auth in s:
    s = s.replace(old_auth, new_auth, 1)
elif 'window.sevenBrowserSessionPersistence=browserSessionPersistence' not in s:
    raise SystemExit('Inicialização do Firebase Auth não encontrada')

old_login = "window.loginAdmin=async function(){const email=document.getElementById('adminEmail').value.trim(),pass=document.getElementById('adminPassword').value;if(!email||!pass){const m=document.getElementById('adminAuthMsg');m.textContent='Informe e-mail e senha.';m.classList.add('active');return}try{await window.sevenSignIn(window.sevenAuth,email,pass);window.fecharLoginAdmin()}catch(e){console.error(e);const m=document.getElementById('adminAuthMsg');m.textContent='Não foi possível entrar. Confira o e-mail e a senha.';m.classList.add('active')}};"
new_login = "window.loginAdmin=async function(){const email=document.getElementById('adminEmail').value.trim(),pass=document.getElementById('adminPassword').value;if(!email||!pass){const m=document.getElementById('adminAuthMsg');m.textContent='Informe e-mail e senha.';m.classList.add('active');return}try{await window.sevenSetPersistence(window.sevenAuth,window.sevenBrowserSessionPersistence);await window.sevenSignIn(window.sevenAuth,email,pass);window.sevenRegistrarAtividadeAdmin();window.fecharLoginAdmin()}catch(e){console.error(e);const m=document.getElementById('adminAuthMsg');m.textContent='Não foi possível entrar. Confira o e-mail e a senha.';m.classList.add('active')}};"
if old_login in s:
    s = s.replace(old_login, new_login, 1)
elif 'window.sevenRegistrarAtividadeAdmin' not in s:
    raise SystemExit('Função loginAdmin não encontrada')

security = r'''
<script id="sevenAdminSessionSecurity">
(function(){
  const TEMPO_INATIVIDADE=30*60*1000;
  const CHAVE='seven_admin_last_activity';
  let timer=null;
  let ultimoRegistro=0;

  function agora(){return Date.now()}
  function registrar(force=false){
    if(!window.sevenAuth||!window.sevenAuth.currentUser)return;
    const t=agora();
    if(!force&&t-ultimoRegistro<5000)return;
    ultimoRegistro=t;
    try{sessionStorage.setItem(CHAVE,String(t))}catch(e){}
  }
  window.sevenRegistrarAtividadeAdmin=()=>registrar(true);

  async function expirar(){
    if(!window.sevenAuth||!window.sevenAuth.currentUser)return;
    try{await window.sevenSignOut(window.sevenAuth)}catch(e){console.error('Logout automático',e)}
    try{sessionStorage.removeItem(CHAVE)}catch(e){}
    const m=document.getElementById('adminAuthMsg');
    if(m){m.textContent='Sua sessão administrativa expirou por segurança. Entre novamente.';m.classList.add('active')}
    const o=document.getElementById('adminAuthOverlay');
    if(o)o.classList.add('active');
  }

  function verificar(){
    if(!window.sevenAuth||!window.sevenAuth.currentUser)return;
    let last=0;
    try{last=Number(sessionStorage.getItem(CHAVE)||0)}catch(e){}
    if(!last){registrar(true);return}
    if(agora()-last>=TEMPO_INATIVIDADE)expirar();
  }

  function iniciar(){
    if(timer)clearInterval(timer);
    timer=setInterval(verificar,30000);
    ['pointerdown','keydown','touchstart','scroll'].forEach(ev=>document.addEventListener(ev,()=>registrar(false),{passive:true}));
    document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')verificar()});
    window.addEventListener('focus',verificar);
    if(window.sevenAuthState&&window.sevenAuth){
      window.sevenAuthState(window.sevenAuth,user=>{
        if(user){
          let last=0;
          try{last=Number(sessionStorage.getItem(CHAVE)||0)}catch(e){}
          if(last&&agora()-last>=TEMPO_INATIVIDADE){expirar();return}
          registrar(true);
        }else{
          try{sessionStorage.removeItem(CHAVE)}catch(e){}
        }
      });
    }
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',iniciar);else iniciar();
})();
</script>
'''

if 'id="sevenAdminSessionSecurity"' not in s:
    s = s.replace('</body>', security + '\n</body>', 1)

required = [
    'browserSessionPersistence','window.sevenSignOut=signOut','TEMPO_INATIVIDADE=30*60*1000',
    'seven_admin_last_activity','sevenAdminSessionSecurity','window.sevenRegistrarAtividadeAdmin'
]
for item in required:
    if item not in s:
        raise SystemExit('Proteção incompleta: '+item)

p.write_text(s,encoding='utf-8')
print('Proteção administrativa aplicada: sessão do navegador + 30 min de inatividade')
