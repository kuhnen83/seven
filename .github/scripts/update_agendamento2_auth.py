from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Remove versões anteriores da proteção para recriar de forma limpa.
s=re.sub(r'<script id="sevenStandaloneLogin".*?</script>','',s,flags=re.S)
s=re.sub(r'<script id="sevenFullPanelSecurity">.*?</script>','',s,flags=re.S)

# Garante atributos do botão de login.
s=s.replace('<button id="sevenLoginBtn" class="seven-login-btn" type="button">Entrar</button>',
            '<button id="sevenLoginBtn" class="seven-login-btn" type="button" onclick="window.sevenDirectLogin&&window.sevenDirectLogin()">Entrar</button>')

# Corrige o wrapper protegido caso tenha sido fechado imediatamente após o botão Sair.
s=s.replace('<div id="sevenProtectedPanel" class="seven-protected-panel"><div class="seven-panel-securitybar"><button id="sevenLogoutBtn" class="seven-logout-btn" type="button">Sair</button></div></div>\n<div class="container" id="telaRecibo">',
            '<div id="sevenProtectedPanel" class="seven-protected-panel"><div class="seven-panel-securitybar"><button id="sevenLogoutBtn" class="seven-logout-btn" type="button">Sair</button></div>\n<div class="container" id="telaRecibo">')

if '<div id="sevenProtectedPanel"' in s and '</div><!-- sevenProtectedPanel -->' not in s:
    pos=s.rfind('</body>')
    if pos<0: raise SystemExit('body não encontrado')
    s=s[:pos]+'\n</div><!-- sevenProtectedPanel -->\n'+s[pos:]

standalone=r'''
<script type="module" id="sevenStandaloneLogin">
import { initializeApp, getApps, getApp } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js';
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged, setPersistence, browserSessionPersistence, signOut } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';

const cfg={apiKey:'AIzaSyAN8PKdOni3mJC-DvAFfjHI1ohBpi7eb28',authDomain:'agendaseven-428ad.firebaseapp.com',projectId:'agendaseven-428ad',storageBucket:'agendaseven-428ad.firebasestorage.app',messagingSenderId:'908846325130',appId:'1:908846325130:web:e5badefe60a02740bc3c73',measurementId:'G-JRKKZWRFCN'};
const app=getApps().length?getApp():initializeApp(cfg);
const auth=getAuth(app);
const IDLE=30*60*1000, KEY='seven_admin_last_activity';
let timer=null,lastWrite=0;
const el=id=>document.getElementById(id);
const domainOK=email=>/^[^\s@]+@(?:gmail\.com|icloud\.com|me\.com|mac\.com)$/i.test((email||'').trim());

window.sevenAuth=auth;
window.sevenSignIn=signInWithEmailAndPassword;
window.sevenAuthState=onAuthStateChanged;
window.sevenSetPersistence=setPersistence;
window.sevenBrowserSessionPersistence=browserSessionPersistence;
window.sevenSignOut=signOut;

function msg(t){const m=el('adminAuthMsg');if(!m)return;m.textContent=t||'';m.classList.toggle('active',!!t)}
function showLogin(t=''){el('sevenLoginGate')?.classList.remove('hidden');el('sevenProtectedPanel')?.classList.remove('authorized');document.body.classList.add('seven-locked');msg(t)}
function showPanel(){el('sevenLoginGate')?.classList.add('hidden');el('sevenProtectedPanel')?.classList.add('authorized');document.body.classList.remove('seven-locked');msg('')}
function activity(force=false){if(!auth.currentUser)return;const n=Date.now();if(!force&&n-lastWrite<5000)return;lastWrite=n;sessionStorage.setItem(KEY,String(n))}
async function logout(t='Você saiu do painel com segurança.'){
 try{await signOut(auth)}catch(e){console.error('LOGOUT SEVEN:',e)}
 sessionStorage.removeItem(KEY);
 try{sessionStorage.removeItem('seven_admin_screen')}catch(e){}
 showLogin(t);
}
window.sevenDirectLogout=logout;

function check(){if(!auth.currentUser)return;const last=Number(sessionStorage.getItem(KEY)||0);if(last&&Date.now()-last>=IDLE)logout('Sua sessão expirou após 30 minutos de inatividade. Entre novamente.');else if(!last)activity(true)}

window.sevenDirectLogin=async function(){
 const email=el('adminEmail')?.value.trim()||'';
 const pass=el('adminPassword')?.value||'';
 const btn=el('sevenLoginBtn');
 msg('');
 if(!domainOK(email)){msg('Use um e-mail autorizado do Gmail ou uma conta Apple (iCloud).');return}
 if(!pass){msg('Digite sua senha.');return}
 if(btn){btn.disabled=true;btn.textContent='Entrando...'}
 try{await setPersistence(auth,browserSessionPersistence);await signInWithEmailAndPassword(auth,email,pass);activity(true)}
 catch(e){console.error('LOGIN SEVEN:',e);msg('Não foi possível entrar. Confira o e-mail, a senha e se a conta está cadastrada no Firebase Authentication.')}
 finally{if(btn){btn.disabled=false;btn.textContent='Entrar'}}
};

function bindLogoutButtons(){
 const old=el('sevenLogoutBtn');
 if(old){old.onclick=null;old.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();window.sevenDirectLogout()})}
 const side=el('sevenSideLogout');
 if(side){side.onclick=null;side.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();window.sevenDirectLogout()})}
}

el('adminPassword')?.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();window.sevenDirectLogin()}});
document.addEventListener('DOMContentLoaded',bindLogoutButtons);
setTimeout(bindLogoutButtons,300);
['pointerdown','keydown','touchstart','scroll'].forEach(ev=>document.addEventListener(ev,()=>activity(false),{passive:true}));
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')check()});
window.addEventListener('focus',check);
timer=setInterval(check,30000);

onAuthStateChanged(auth,user=>{
 if(!user){showLogin();return}
 if(!domainOK(user.email||'')){logout('Esta conta não está autorizada para o painel.');return}
 const last=Number(sessionStorage.getItem(KEY)||0);
 if(last&&Date.now()-last>=IDLE){logout('Sua sessão expirou. Entre novamente.');return}
 activity(true);showPanel();bindLogoutButtons();
});
</script>
'''

pos=s.find('<script type="module">')
if pos<0: raise SystemExit('script principal não encontrado')
s=s[:pos]+standalone+'\n'+s[pos:]
s=s.replace('window.sevenRegistrarAtividadeAdmin();','')

required=['sevenStandaloneLogin','window.sevenDirectLogin','window.sevenDirectLogout=logout','sevenSideLogout','browserSessionPersistence']
for x in required:
    if x not in s: raise SystemExit('Login/logout incompleto: '+x)

p.write_text(s,encoding='utf-8')
print('Login e logout administrativo corrigidos')
