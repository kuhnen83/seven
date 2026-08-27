from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Remove somente versões anteriores deste controlador final.
s=re.sub(r'\s*<script type="module" id="sevenSaveEditFinalFix">.*?</script>\s*','\n',s,flags=re.S)

script=r'''
<script type="module" id="sevenSaveEditFinalFix">
import { getApps,getApp,initializeApp } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js';
import { getFirestore,doc,updateDoc,setDoc,deleteDoc } from 'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';
const cfg={apiKey:'AIzaSyAN8PKdOni3mJC-DvAFfjHI1ohBpi7eb28',authDomain:'agendaseven-428ad.firebaseapp.com',projectId:'agendaseven-428ad',storageBucket:'agendaseven-428ad.firebasestorage.app',messagingSenderId:'908846325130',appId:'1:908846325130:web:e5badefe60a02740bc3c73',measurementId:'G-JRKKZWRFCN'};
const app=getApps().length?getApp():initializeApp(cfg);
const auth=getAuth(app),db=getFirestore(app);
const $=id=>document.getElementById(id);
const num=id=>Number(String($(id)?.value||'0').replace(',','.'))||0;
function dadosFormulario(){
 const q=num('quantidade')||1,u=num('valorUnitario'),desc=num('desconto');
 return {
  receipt_number:$('numRecibo')?.value?.trim()||'',
  client_name:$('nomeCliente')?.value?.trim()||'',
  client_address:$('enderecoCliente')?.value?.trim()||'',
  phone:$('telefoneCliente')?.value?.trim()||'',
  service_date:$('data')?.value||'',service_time:$('horario')?.value||'',
  description:$('descricao')?.value?.trim()||'',quantity:q,unit_price:u,discount:desc,
  payment_method:$('formaPagamento')?.value||'Pix',payment_status:$('statusPagamento')?.value||'Pago',
  service_status:$('statusAtendimento')?.value||'Agendado',notes:$('observacoes')?.value?.trim()||'',
  conversation:$('conversa')?.value?.trim()||'',total:Math.max(0,q*u-desc)
 };
}
async function salvar(e){
 if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation()}
 const id=$('idEditando')?.value||window.detalheId||'';
 if(!id)return alert('Nenhum agendamento selecionado.');
 if(!auth.currentUser)return alert('Sua sessão expirou. Saia e entre novamente.');
 const d=dadosFormulario();
 if(!d.client_name||!d.service_date)return alert('Preencha Nome e Data.');
 const btn=$('btnAtualizar'),old=btn?.innerHTML;
 if(btn){btn.disabled=true;btn.textContent='⏳ Salvando...'}
 try{
  await auth.currentUser.getIdToken(true);
  await updateDoc(doc(db,'agendamentos',String(id)),d);
  const existente=(window.agendamentos||[]).find(a=>String(a.id)===String(id));
  const dur=Number(existente?.duration_minutes||60);
  try{
   const pub=doc(db,'agenda_publica',String(id));
   if(d.service_status==='Cancelado'||!d.service_date||!d.service_time)await deleteDoc(pub);
   else await setDoc(pub,{service_date:d.service_date,service_time:d.service_time,duration_minutes:dur>0?dur:60,service_status:d.service_status});
  }catch(syncErr){console.warn('Registro salvo; falha somente na sincronização pública:',syncErr)}
  if(existente)Object.assign(existente,d);
  try{window.renderCalendario?.()}catch(err){console.warn(err)}
  try{if(document.getElementById('telaResumo')?.classList.contains('active'))window.renderResumo?.()}catch(err){console.warn(err)}
  try{window.limparFormulario?.()}catch(err){console.warn(err)}
  try{window.sevenOpenScreen?.('agenda')}catch(err){console.warn(err)}
  alert('Agendamento atualizado com sucesso!');
 }catch(err){
  console.error('SALVAR ALTERAÇÕES FINAL SEVEN:',err);
  alert('Não foi possível salvar as alterações.\n\nCódigo: '+(err?.code||'sem-codigo')+'\nDetalhe: '+(err?.message||String(err)));
 }finally{
  if(btn){btn.disabled=false;btn.innerHTML=old||'✏️ Salvar Alterações'}
 }
}
document.addEventListener('click',e=>{const b=e.target.closest?.('#btnAtualizar');if(b)salvar(e)},true);
window.sevenSalvarAlteracoesFinal=salvar;
</script>
'''

pos=s.rfind('</body>')
if pos<0: raise SystemExit('ERRO: </body> não encontrado')
s=s[:pos]+script+'\n'+s[pos:]

if s.count('id="sevenSaveEditFinalFix"') != 1:
 raise SystemExit('ERRO: controlador final duplicado')
for token in ['sevenSalvarAlteracoesFinal','SALVAR ALTERAÇÕES FINAL SEVEN',"updateDoc(doc(db,'agendamentos'",'payment_status']:
 if token not in s: raise SystemExit('ERRO: faltando '+token)
p.write_text(s,encoding='utf-8')
print('OK: controlador final de Salvar Alterações instalado')
