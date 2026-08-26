from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Firebase Auth: sessão do navegador + logout.
old="import{getAuth,signInWithEmailAndPassword,onAuthStateChanged}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';"
new="import{getAuth,signInWithEmailAndPassword,onAuthStateChanged,setPersistence,browserSessionPersistence,signOut}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';"
if old in s:s=s.replace(old,new,1)
elif 'browserSessionPersistence' not in s:raise SystemExit('Import Firebase Auth não encontrado')

needle="window.sevenAuthState=onAuthStateChanged;"
if 'window.sevenSetPersistence=' not in s:
    if needle not in s:raise SystemExit('Inicialização Auth não encontrada')
    s=s.replace(needle,needle+"window.sevenSetPersistence=setPersistence;window.sevenBrowserSessionPersistence=browserSessionPersistence;window.sevenSignOut=signOut;setPersistence(auth,browserSessionPersistence).catch(console.error);",1)

# Remove overlay administrativo antigo: agora o login protege o painel inteiro.
s=re.sub(r'<div id="adminAuthOverlay" class="admin-auth-overlay">.*?</div></div>\s*','',s,count=1,flags=re.S)

# Tela de login Seven. Usa a logo existente no repositório.
login='''<div id="sevenLoginGate" class="seven-login-gate">
  <div class="seven-login-card">
    <img class="seven-login-logo" src="logo-seven.png" alt="Seven Limpeza" onerror="this.style.display='none';document.getElementById('sevenLogoFallback').style.display='block'">
    <div id="sevenLogoFallback" class="seven-logo-fallback">SEVEN</div>
    <h1>Painel Administrativo</h1>
    <p>Acesso restrito a usuários autorizados.</p>
    <label for="adminEmail">Usuário</label>
    <input id="adminEmail" type="email" placeholder="seuemail@gmail.com" autocomplete="username">
    <label for="adminPassword">Senha</label>
    <input id="adminPassword" type="password" placeholder="Digite sua senha" autocomplete="current-password">
    <button id="sevenLoginBtn" class="seven-login-btn" type="button">Entrar</button>
    <div id="adminAuthMsg" class="seven-login-msg"></div>
  </div>
</div>
<a class="seven-login-whatsapp" href="https://wa.me/5548996782471" target="_blank" rel="noopener" aria-label="Falar com a Seven pelo WhatsApp">WhatsApp</a>
<div id="sevenProtectedPanel" class="seven-protected-panel">'''
if 'id="sevenLoginGate"' not in s:
    s=s.replace('<body>', '<body>'+login,1)
    s=s.replace('</body>','</div></body>',1)

css='''
/* ===== Segurança do Painel Seven ===== */
body.seven-locked{overflow:hidden}.seven-protected-panel{display:none}.seven-protected-panel.authorized{display:block}.seven-login-gate{position:fixed;inset:0;z-index:10000;background:linear-gradient(145deg,#eef4fa,#dfeaf5);display:flex;align-items:center;justify-content:center;padding:20px}.seven-login-gate.hidden{display:none}.seven-login-card{width:100%;max-width:390px;background:#fff;border-radius:18px;padding:30px 26px;box-shadow:0 20px 60px #0f4c8126;border-top:5px solid var(--azul)}.seven-login-logo{display:block;max-width:145px;max-height:90px;object-fit:contain;margin:0 auto 12px}.seven-logo-fallback{display:none;text-align:center;font-size:34px;font-weight:900;letter-spacing:5px;color:var(--azul);margin-bottom:12px}.seven-login-card h1{text-align:center;color:var(--azul);font-size:21px;margin:5px 0 6px}.seven-login-card p{text-align:center;color:#68707a;font-size:13px;margin:0 0 22px}.seven-login-card label{display:block;margin:12px 0 6px}.seven-login-card input{background:#f7f9fb}.seven-login-btn{width:100%;margin-top:18px;border:0;border-radius:8px;padding:13px;background:var(--azul);color:#fff;font-weight:900;font-size:15px;cursor:pointer}.seven-login-msg{display:none;margin-top:12px;padding:10px;border-radius:8px;background:#fde8eb;color:#9d1d2d;font-size:12px}.seven-login-msg.active{display:block}.seven-login-whatsapp{position:fixed;right:18px;bottom:18px;z-index:10020;background:#25d366;color:#fff;text-decoration:none;font-weight:900;border-radius:28px;padding:13px 17px;box-shadow:0 6px 20px #0003}.seven-panel-securitybar{position:fixed;right:12px;top:12px;z-index:2500}.seven-logout-btn{border:0;border-radius:20px;background:#b42332;color:#fff;padding:9px 13px;font-weight:800;cursor:pointer}@media(max-width:600px){.seven-login-card{padding:25px 20px}.seven-login-whatsapp{right:12px;bottom:12px}}
'''
if '/* ===== Segurança do Painel Seven ===== */' not in s:s=s.replace('</style>',css+'</style>',1)

# Botão Sair dentro do painel.
if 'id="sevenLogoutBtn"' not in s:
    s=s.replace('<div id="sevenProtectedPanel" class="seven-protected-panel">','<div id="sevenProtectedPanel" class="seven-protected-panel"><div class="seven-panel-securitybar"><button id="sevenLogoutBtn" class="seven-logout-btn" type="button">Sair</button></div>',1)

# Script de controle integral do painel.
security=r'''
<script id="sevenFullPanelSecurity">
(function(){
 const IDLE=30*60*1000,KEY='seven_admin_last_activity';let timer,lastWrite=0;
 const $=id=>document.getElementById(id);
 function domainOK(email){email=(email||'').trim().toLowerCase();return /^[^\s@]+@(?:gmail\.com|icloud\.com|me\.com|mac\.com)$/.test(email)}
 function showLogin(msg=''){$('sevenProtectedPanel')?.classList.remove('authorized');$('sevenLoginGate')?.classList.remove('hidden');document.body.classList.add('seven-locked');if(msg){$('adminAuthMsg').textContent=msg;$('adminAuthMsg').classList.add('active')}}
 function showPanel(){$('sevenLoginGate')?.classList.add('hidden');$('sevenProtectedPanel')?.classList.add('authorized');document.body.classList.remove('seven-locked');$('adminAuthMsg')?.classList.remove('active')}
 function activity(force=false){if(!window.sevenAuth?.currentUser)return;const n=Date.now();if(!force&&n-lastWrite<5000)return;lastWrite=n;sessionStorage.setItem(KEY,String(n))}
 async function logout(msg='Sessão encerrada. Entre novamente.'){try{if(window.sevenAuth?.currentUser)await window.sevenSignOut(window.sevenAuth)}catch(e){console.error(e)}sessionStorage.removeItem(KEY);showLogin(msg)}
 function check(){if(!window.sevenAuth?.currentUser)return;const last=Number(sessionStorage.getItem(KEY)||0);if(last&&Date.now()-last>=IDLE)logout('Sua sessão expirou após 30 minutos de inatividade. Entre novamente.');else if(!last)activity(true)}
 async function login(){const email=$('adminEmail').value.trim(),pass=$('adminPassword').value,msg=$('adminAuthMsg');msg.classList.remove('active');if(!domainOK(email)){msg.textContent='Use um e-mail autorizado do Gmail ou uma conta Apple (iCloud).';msg.classList.add('active');return}if(!pass){msg.textContent='Digite sua senha.';msg.classList.add('active');return}try{await window.sevenSetPersistence(window.sevenAuth,window.sevenBrowserSessionPersistence);await window.sevenSignIn(window.sevenAuth,email,pass);activity(true)}catch(e){console.error(e);msg.textContent='Acesso não autorizado. Confira o e-mail e a senha.';msg.classList.add('active')}}
 function start(){showLogin();$('sevenLoginBtn').onclick=login;$('adminPassword').addEventListener('keydown',e=>{if(e.key==='Enter')login()});$('sevenLogoutBtn').onclick=()=>logout('Você saiu do painel com segurança.');['pointerdown','keydown','touchstart','scroll'].forEach(ev=>document.addEventListener(ev,()=>activity(),{passive:true}));document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')check()});window.addEventListener('focus',check);timer=setInterval(check,30000);window.sevenAuthState(window.sevenAuth,user=>{if(user){const email=(user.email||'').toLowerCase();if(!domainOK(email)){logout('Esta conta não está autorizada para o painel.');return}const last=Number(sessionStorage.getItem(KEY)||0);if(last&&Date.now()-last>=IDLE){logout('Sua sessão expirou. Entre novamente.');return}activity(true);showPanel()}else showLogin()})}
 const wait=setInterval(()=>{if(window.sevenAuth&&window.sevenAuthState&&window.sevenSignIn&&window.sevenSignOut&&window.sevenSetPersistence){clearInterval(wait);start()}},50);
})();
</script>
'''
# Remove proteção de sessão antiga para não duplicar listeners/overlays.
s=re.sub(r'<script id="sevenAdminSessionSecurity">.*?</script>','',s,flags=re.S)
if 'id="sevenFullPanelSecurity"' not in s:s=s.replace('</body>',security+'\n</body>',1)

# Compatibilidade: funções administrativas antigas passam a usar o mesmo login global.
compat="window.loginAdmin=function(){document.getElementById('sevenLoginBtn')?.click()};window.fecharLoginAdmin=function(){};"
if 'window.loginAdmin=async function' in s:
    s=re.sub(r"window\.loginAdmin=async function\(\)\{.*?\};window\.fecharLoginAdmin=function\(\)\{.*?\};",compat,s,count=1,flags=re.S)

required=['sevenLoginGate','sevenProtectedPanel','sevenFullPanelSecurity','browserSessionPersistence','sevenLogoutBtn','gmail\\.com|icloud\\.com|me\\.com|mac\\.com','IDLE=30*60*1000']
for x in required:
    if x not in s:raise SystemExit('Proteção incompleta: '+x)
p.write_text(s,encoding='utf-8')
print('Painel Seven protegido integralmente por Firebase Authentication')
