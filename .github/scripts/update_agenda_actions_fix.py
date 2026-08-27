from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

s=s.replace("detalheId=a.id;statusIndex=", "detalheId=a.id;window.detalheId=a.id;statusIndex=", 1)
s=s.replace("function fecharDetalhes(){$('detalheOverlay').classList.remove('active');detalheId=''}", "function fecharDetalhes(){$('detalheOverlay').classList.remove('active');detalheId='';window.detalheId=''}", 1)

old_footer='<div class="detail-footer"><button class="btn orange" onclick="editarDetalhe()">✏️ EDITAR AGENDAMENTO</button></div>'
new_footer='<div class="detail-footer"><button class="btn orange" onclick="editarDetalhe()">✏️ EDITAR AGENDAMENTO</button><button id="btnExcluirDetalhe" class="btn red" type="button">🗑️ EXCLUIR</button></div>'
if old_footer in s:s=s.replace(old_footer,new_footer,1)
elif 'id="btnExcluirDetalhe"' not in s:raise SystemExit('Rodapé da ficha não encontrado')

s=re.sub(r'\s*<script type="module" id="sevenAgendaConfigBridge">.*?</script>\s*','\n',s,flags=re.S)
s=re.sub(r'\s*<script id="sevenAgendaActionsFix">.*?</script>\s*','\n',s,flags=re.S)

bridge=r'''
<script type="module" id="sevenAgendaConfigBridge">
import { getApps,getApp,initializeApp } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';
import { getFirestore,doc,getDoc,setDoc } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';
const cfg={apiKey:'AIzaSyAN8PKdOni3mJC-DvAFfjHI1ohBpi7eb28',authDomain:'agendaseven-428ad.firebaseapp.com',projectId:'agendaseven-428ad',storageBucket:'agendaseven-428ad.firebasestorage.app',messagingSenderId:'908846325130',appId:'1:908846325130:web:e5badefe60a02740bc3c73',measurementId:'G-JRKKZWRFCN'};
const app=getApps().length?getApp():initializeApp(cfg);
const auth=getAuth(app),db=getFirestore(app);
window.sevenSalvarConfigAgenda=async function(aberta,dias){
 if(!auth.currentUser)throw new Error('Sessão expirada. Entre novamente.');
 await auth.currentUser.getIdToken(true);
 const ref=doc(db,'config','agenda');
 const snap=await getDoc(ref);const base=snap.exists()?snap.data():{};
 await setDoc(ref,{...base,aberta:aberta!==false,diasFechados:Array.isArray(dias)?dias:[],updated_at:Date.now(),updated_by:auth.currentUser.email||auth.currentUser.uid});
 return true;
};
</script>
'''

fix=r'''
<script id="sevenAgendaActionsFix">
(function(){
 const $=id=>document.getElementById(id);
 const autenticado=()=>!!(window.sevenAuth&&window.sevenAuth.currentUser);
 const exigirLogin=()=>{if(autenticado())return true;alert('Sua sessão expirou. Entre novamente.');return false};
 async function salvarConfig(aberta,dias){
   if(typeof window.sevenSalvarConfigAgenda==='function')return window.sevenSalvarConfigAgenda(aberta,dias);
   if(typeof window.salvarConfigAgenda==='function')return window.salvarConfigAgenda(aberta,dias);
   throw new Error('Função de configuração ainda não foi carregada. Recarregue a página.');
 }
 async function excluirAtual(e){
   if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation()}if(!exigirLogin())return;
   const id=$('idEditando')?.value||window.detalheId||'';if(!id)return alert('Nenhum agendamento selecionado para excluir.');
   if(!confirm('Deseja realmente excluir este agendamento?'))return;
   const btn=e?.target?.closest?.('button')||$('btnExcluirDetalhe')||$('btnExcluir');if(btn){btn.disabled=true;btn.dataset.oldText=btn.innerHTML;btn.textContent='⏳ Excluindo...'}
   try{const ok=await window.excluirAgendamentoCloud(id);if(!ok)return;window.agendamentos=(window.agendamentos||[]).filter(a=>String(a.id)!==String(id));window.fecharDetalhes?.();window.limparFormulario?.();window.renderCalendario?.();alert('Agendamento excluído com sucesso.')}catch(err){console.error(err);alert('Não foi possível excluir o agendamento.\n\n'+(err?.message||err))}finally{if(btn){btn.disabled=false;btn.innerHTML=btn.dataset.oldText||'🗑️ EXCLUIR'}}
 }
 async function alternarAgendaFinal(e){
   if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation()}if(!exigirLogin())return;
   const atual=window.agendaAberta!==false,novo=!atual;if(!novo&&!confirm('Fechar a agenda? Novos clientes não poderão realizar agendamentos pelo site até você abrir novamente.'))return;
   const btn=$('btnFecharAgenda');if(btn){btn.disabled=true;btn.textContent='⏳ Salvando...'}
   try{await salvarConfig(novo,window.diasFechados||[]);window.aplicarStatusAgenda?.(novo);window.configAgenda=window.configAgenda||{};window.configAgenda.aberta=novo;}
   catch(err){console.error('FECHAR AGENDA SEVEN:',err);alert('Não foi possível alterar o status da agenda.\n\n'+(err?.message||err))}
   finally{if(btn)btn.disabled=false}
 }
 async function fecharDiaFinal(e){
   if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation()}if(!exigirLogin())return;
   const input=$('dataFecharAgenda'),d=input?.value||'';if(!d)return alert('Escolha uma data.');const atuais=Array.isArray(window.diasFechados)?window.diasFechados:[];if(atuais.includes(d))return alert('Esse dia já está fechado.');
   const btn=e?.target?.closest?.('button');if(btn){btn.disabled=true;btn.dataset.oldText=btn.innerHTML;btn.textContent='⏳ Salvando...'}const nova=[...new Set([...atuais,d])].sort();
   try{await salvarConfig(window.agendaAberta!==false,nova);window.diasFechados=nova;window.configAgenda=window.configAgenda||{};window.configAgenda.diasFechados=nova;window.renderDiasFechados?.();if(input)input.value='';alert('Dia '+d.split('-').reverse().join('/')+' fechado para novos agendamentos.');}
   catch(err){console.error('FECHAR DIA SEVEN:',err);alert('Não foi possível fechar este dia.\n\n'+(err?.message||err))}
   finally{if(btn){btn.disabled=false;btn.innerHTML=btn.dataset.oldText||'➕ Fechar este dia'}}
 }
 document.addEventListener('click',e=>{const t=e.target;if(t.closest?.('#btnFecharAgenda'))return alternarAgendaFinal(e);if(t.closest?.('#btnExcluirDetalhe')||t.closest?.('#btnExcluir'))return excluirAtual(e);if(t.closest?.('button[onclick*="adicionarDiaFechado"]'))return fecharDiaFinal(e)},true);
 window.sevenExcluirAgendamentoFinal=excluirAtual;window.sevenAlternarAgendaFinal=alternarAgendaFinal;window.sevenFecharDiaFinal=fecharDiaFinal;
})();
</script>
'''

pos=s.rfind('</body>')
if pos<0:raise SystemExit('body não encontrado')
s=s[:pos]+bridge+'\n'+fix+'\n'+s[pos:]
for x in ['sevenAgendaConfigBridge','window.sevenSalvarConfigAgenda','sevenAgendaActionsFix','btnExcluirDetalhe','sevenAlternarAgendaFinal','sevenFecharDiaFinal']:
 if x not in s:raise SystemExit('Correção incompleta: '+x)
p.write_text(s,encoding='utf-8')
print('Persistência de fechar agenda e fechar dia corrigida com bridge Firestore independente')
