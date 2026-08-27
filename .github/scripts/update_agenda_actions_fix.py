from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Preserva o ID do cliente aberto também em window para os módulos finais.
s=s.replace("detalheId=a.id;statusIndex=", "detalheId=a.id;window.detalheId=a.id;statusIndex=", 1)
s=s.replace("function fecharDetalhes(){$('detalheOverlay').classList.remove('active');detalheId=''}", "function fecharDetalhes(){$('detalheOverlay').classList.remove('active');detalheId='';window.detalheId=''}", 1)

# Adiciona botão de exclusão direto na ficha do cliente.
old_footer='<div class="detail-footer"><button class="btn orange" onclick="editarDetalhe()">✏️ EDITAR AGENDAMENTO</button></div>'
new_footer='<div class="detail-footer"><button class="btn orange" onclick="editarDetalhe()">✏️ EDITAR AGENDAMENTO</button><button id="btnExcluirDetalhe" class="btn red" type="button">🗑️ EXCLUIR</button></div>'
if old_footer in s:
    s=s.replace(old_footer,new_footer,1)
elif 'id="btnExcluirDetalhe"' not in s:
    raise SystemExit('Rodapé da ficha não encontrado')

# Remove versão anterior deste fix.
s=re.sub(r'\s*<script id="sevenAgendaActionsFix">.*?</script>\s*','\n',s,flags=re.S)

fix=r'''
<script id="sevenAgendaActionsFix">
(function(){
  const $=id=>document.getElementById(id);

  function autenticado(){return !!(window.sevenAuth&&window.sevenAuth.currentUser)}
  function exigirLogin(){if(autenticado())return true;alert('Sua sessão expirou. Entre novamente.');return false}

  async function excluirAtual(e){
    if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation()}
    if(!exigirLogin())return;
    const id=$('idEditando')?.value||window.detalheId||'';
    if(!id){alert('Nenhum agendamento selecionado para excluir.');return}
    if(!confirm('Deseja realmente excluir este agendamento?'))return;
    const btn=e?.target?.closest?.('button')||$('btnExcluirDetalhe')||$('btnExcluir');
    if(btn){btn.disabled=true;btn.dataset.oldText=btn.innerHTML;btn.textContent='⏳ Excluindo...'}
    try{
      if(typeof window.excluirAgendamentoCloud!=='function')throw new Error('Função de exclusão indisponível');
      const ok=await window.excluirAgendamentoCloud(id);
      if(!ok)return;
      try{window.agendamentos=(window.agendamentos||[]).filter(a=>String(a.id)!==String(id))}catch(x){}
      try{window.fecharDetalhes?.()}catch(x){}
      try{window.limparFormulario?.()}catch(x){}
      try{window.renderCalendario?.()}catch(x){}
      alert('Agendamento excluído com sucesso.');
    }catch(err){
      console.error('EXCLUSAO FINAL SEVEN:',err);
      alert('Não foi possível excluir o agendamento.\n\n'+(err?.message||err));
    }finally{
      if(btn){btn.disabled=false;btn.innerHTML=btn.dataset.oldText||'🗑️ EXCLUIR'}
    }
  }

  async function alternarAgendaFinal(e){
    if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation()}
    if(!exigirLogin())return;
    const atual=window.agendaAberta!==false;
    const novo=!atual;
    if(!novo&&!confirm('Fechar a agenda? Novos clientes não poderão realizar agendamentos pelo site até você abrir novamente.'))return;
    const btn=$('btnFecharAgenda');
    if(btn){btn.disabled=true;btn.dataset.oldText=btn.textContent;btn.textContent='⏳ Salvando...'}
    try{
      if(typeof window.salvarConfigAgenda!=='function')throw new Error('Função de configuração indisponível');
      await window.salvarConfigAgenda(novo,window.diasFechados||[]);
      window.aplicarStatusAgenda?.(novo);
    }catch(err){
      console.error('FECHAR AGENDA SEVEN:',err);
      alert('Não foi possível alterar o status da agenda.\n\n'+(err?.message||err));
    }finally{if(btn)btn.disabled=false}
  }

  async function fecharDiaFinal(e){
    if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation()}
    if(!exigirLogin())return;
    const input=$('dataFecharAgenda');
    const d=input?.value||'';
    if(!d){alert('Escolha uma data.');return}
    const atuais=Array.isArray(window.diasFechados)?window.diasFechados:[];
    if(atuais.includes(d)){alert('Esse dia já está fechado.');return}
    const btn=e?.target?.closest?.('button');
    if(btn){btn.disabled=true;btn.dataset.oldText=btn.innerHTML;btn.textContent='⏳ Salvando...'}
    const nova=[...new Set([...atuais,d])].sort();
    try{
      await window.salvarConfigAgenda(window.agendaAberta!==false,nova);
      window.diasFechados=nova;
      window.configAgenda=window.configAgenda||{};
      window.configAgenda.diasFechados=nova;
      window.renderDiasFechados?.();
      if(input)input.value='';
      alert('Dia '+d.split('-').reverse().join('/')+' fechado para novos agendamentos.');
    }catch(err){
      console.error('FECHAR DIA SEVEN:',err);
      alert('Não foi possível fechar este dia.\n\n'+(err?.message||err));
    }finally{if(btn){btn.disabled=false;btn.innerHTML=btn.dataset.oldText||'➕ Fechar este dia'}}
  }

  // Intercepta os cliques antes dos handlers antigos, evitando chamada dupla.
  document.addEventListener('click',function(e){
    const t=e.target;
    if(t.closest?.('#btnFecharAgenda'))return alternarAgendaFinal(e);
    if(t.closest?.('#btnExcluirDetalhe'))return excluirAtual(e);
    if(t.closest?.('#btnExcluir'))return excluirAtual(e);
    const fecharDia=t.closest?.('button[onclick*="adicionarDiaFechado"]');
    if(fecharDia)return fecharDiaFinal(e);
  },true);

  window.sevenExcluirAgendamentoFinal=excluirAtual;
  window.sevenAlternarAgendaFinal=alternarAgendaFinal;
  window.sevenFecharDiaFinal=fecharDiaFinal;
})();
</script>
'''

pos=s.rfind('</body>')
if pos<0:raise SystemExit('body não encontrado')
s=s[:pos]+fix+'\n'+s[pos:]

for x in ['sevenAgendaActionsFix','btnExcluirDetalhe','window.detalheId=a.id','sevenExcluirAgendamentoFinal','sevenAlternarAgendaFinal','sevenFecharDiaFinal']:
    if x not in s:raise SystemExit('Correção de ações incompleta: '+x)

p.write_text(s,encoding='utf-8')
print('Exclusão, fechar agenda e fechar dia corrigidos sem alterar o layout aprovado')
