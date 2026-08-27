from pathlib import Path
import re

p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

# Remove versão anterior da correção final.
s=re.sub(r'\s*<script id="sevenLogoutFinalFix">.*?</script>\s*','\n',s,flags=re.S)

# Coloca chamada direta também no próprio botão, sem depender do controlador do menu.
s=s.replace('<button id="sevenSideLogout" type="button">↪ <span>Sair</span></button>',
            '<button id="sevenSideLogout" type="button" onclick="window.sevenDirectLogout&&window.sevenDirectLogout()">↪ <span>Sair</span></button>')

fix=r'''
<script id="sevenLogoutFinalFix">
(function(){
  async function sairSeven(e){
    if(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();}
    const btn=document.getElementById('sevenSideLogout');
    if(btn){btn.disabled=true;btn.textContent='Saindo...';}
    try{
      if(typeof window.sevenDirectLogout==='function'){
        await window.sevenDirectLogout('Você saiu do painel com segurança.');
      }else if(window.sevenAuth && typeof window.sevenSignOut==='function'){
        await window.sevenSignOut(window.sevenAuth);
        sessionStorage.clear();
        document.getElementById('sevenLoginGate')?.classList.remove('hidden');
        document.getElementById('sevenProtectedPanel')?.classList.remove('authorized');
        document.body.classList.add('seven-locked');
      }else{
        throw new Error('Função de logout não disponível');
      }
    }catch(err){
      console.error('LOGOUT FINAL SEVEN:',err);
      alert('Não foi possível sair. Recarregue a página e tente novamente.');
    }finally{
      if(btn){btn.disabled=false;btn.innerHTML='↪ <span>Sair</span>';}
    }
  }

  // Captura o clique ANTES do listener antigo do menu.
  document.addEventListener('click',function(e){
    const btn=e.target.closest?.('#sevenSideLogout');
    if(btn)sairSeven(e);
  },true);

  window.sevenLogoutFinal=sairSeven;
})();
</script>
'''

pos=s.rfind('</body>')
if pos<0: raise SystemExit('body não encontrado')
s=s[:pos]+fix+'\n'+s[pos:]

for x in ['sevenLogoutFinalFix','window.sevenLogoutFinal','stopImmediatePropagation','window.sevenDirectLogout']:
    if x not in s: raise SystemExit('Correção final de logout incompleta: '+x)

p.write_text(s,encoding='utf-8')
print('Botão Sair corrigido com interceptação direta e logout Firebase')
