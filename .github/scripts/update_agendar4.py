from pathlib import Path
import re

p = Path('agendar4.html')
s = p.read_text(encoding='utf-8')

# ===== 1. CSS do aviso do carpete =====
css_carpete = '''
.carpete-box{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:12px!important}
.carpete-fields{display:flex;align-items:center;justify-content:space-between;gap:12px}
.carpete-fields label{margin:0;font-size:13px}
.carpete-fields input{width:90px;text-align:center}
.carpete-info{display:flex;flex-direction:column;gap:5px;background:#fff7e6;border:1px solid #f2c76d;border-radius:10px;padding:11px 12px;color:#5f4a17;font-size:12px;line-height:1.45}
.carpete-info strong{color:#8a5a00;font-size:12px}
@media(max-width:420px){.carpete-fields{align-items:flex-start;flex-direction:column}.carpete-fields input{width:100%}}
'''
if '.carpete-info{' not in s:
    s = s.replace('</style>', css_carpete + '</style>', 1)

# ===== 2. Cards adicionais =====
if 'id="carro"' not in s:
    old = '''<div class="service service-card"><label><input type="checkbox" id="cad"><span class="service-icon">🪑</span><span class="service-name">Cadeiras</span><span class="service-count">Por quantidade</span></label><div id="cadq" class="qty"><label for="qcad">Quantidade (R$ 24,00 cada)</label><input id="qcad" type="number" min="1" max="50" value="1" inputmode="numeric"></div></div></div>
<div class="total"><strong>Total</strong><strong id="total">R$ 0,00</strong></div>'''
    new = '''<div class="service service-card"><label><input type="checkbox" id="cad"><span class="service-icon">🪑</span><span class="service-name">Cadeiras</span><span class="service-count">Por quantidade</span></label><div id="cadq" class="qty"><label for="qcad">Quantidade (R$ 24,00 cada)</label><input id="qcad" type="number" min="1" max="50" value="1" inputmode="numeric"></div></div>
<div class="service service-card"><label><input type="checkbox" id="carro"><span class="service-icon">🚗</span><span class="service-name">Carro</span><span class="service-count">4 opções</span></label><div id="carrov" class="variants"><label class="variant"><span><input type="radio" name="carv" value="209" data-name="Hatch - bancos e carpete" data-dur="120"> Hatch - bancos e carpete</span><b>R$ 209,00</b></label><label class="variant"><span><input type="radio" name="carv" value="249" data-name="Sedan - bancos e carpete" data-dur="120"> Sedan - bancos e carpete</span><b>R$ 249,00</b></label><label class="variant"><span><input type="radio" name="carv" value="289" data-name="SUV - bancos e carpete" data-dur="120"> SUV - bancos e carpete</span><b>R$ 289,00</b></label><label class="variant"><span><input type="radio" name="carv" value="289" data-name="Caminhonete - bancos e carpete" data-dur="120"> Caminhonete - bancos e carpete</span><b>R$ 289,00</b></label></div></div>
<div class="service service-card"><label><input type="checkbox" id="carpete"><span class="service-icon">🧹</span><span class="service-name">Carpete</span><span class="service-count">R$ 49/m²</span></label><div id="carpeteq" class="qty carpete-box"><div class="carpete-fields"><label for="qcarpete">Quantidade em m² (R$ 49,00/m²)</label><input id="qcarpete" type="number" min="1" max="100" step="0.5" value="1" inputmode="decimal"></div><div class="carpete-info"><strong>⚠️ Informação importante</strong><span>O carpete será higienizado no local, com processo de higienização a seco. O tempo de secagem pode ser de até 8 horas.</span></div></div></div>
<div class="service service-card"><label><input type="checkbox" id="cab"><span class="service-icon">🛏️</span><span class="service-name">Cabeceira</span><span class="service-count">4 opções</span></label><div id="cabv" class="variants"><label class="variant"><span><input type="radio" name="cabv" value="109" data-name="Cabeceira solteiro" data-dur="60"> Cabeceira solteiro</span><b>R$ 109,00</b></label><label class="variant"><span><input type="radio" name="cabv" value="139" data-name="Cabeceira casal" data-dur="60"> Cabeceira casal</span><b>R$ 139,00</b></label><label class="variant"><span><input type="radio" name="cabv" value="149" data-name="Cabeceira Queen" data-dur="60"> Cabeceira Queen</span><b>R$ 149,00</b></label><label class="variant"><span><input type="radio" name="cabv" value="169" data-name="Cabeceira King" data-dur="60"> Cabeceira King</span><b>R$ 169,00</b></label></div></div></div>
<div class="total"><strong>Total</strong><strong id="total">R$ 0,00</strong></div>'''
    if old not in s:
        raise SystemExit('ERRO: bloco Cadeiras/Total não encontrado')
    s = s.replace(old, new, 1)

# ===== 3. Cálculo =====
if "$('carro').checked" not in s:
    old = "if($('cad').checked){const q=qty('qcad',1,50);a.push({name:'Cadeira',price:24*q,dur:60*q,quantity:q,unit_price:24})}return a}"
    new = "if($('cad').checked){const q=qty('qcad',1,50);a.push({name:'Cadeira',price:24*q,dur:60*q,quantity:q,unit_price:24})}if($('carro').checked){const x=document.querySelector('input[name=carv]:checked');if(!x)return null;a.push({name:x.dataset.name,price:+x.value,dur:+x.dataset.dur,quantity:1,unit_price:+x.value})}if($('carpete').checked){const q=Math.max(1,Math.min(100,parseFloat($('qcarpete').value)||1));$('qcarpete').value=q;a.push({name:'Carpete '+q.toLocaleString('pt-BR')+' m²',price:49*q,dur:Math.max(30,Math.ceil(q*30)),quantity:q,unit_price:49})}if($('cab').checked){const x=document.querySelector('input[name=cabv]:checked');if(!x)return null;a.push({name:x.dataset.name,price:+x.value,dur:+x.dataset.dur,quantity:1,unit_price:+x.value})}return a}"
    if old not in s:
        raise SystemExit('ERRO: função items() não encontrada')
    s = s.replace(old, new, 1)

# ===== 4. Inicialização =====
if "$('carrov').style.display='none'" not in s:
    old = "$('polq').style.display='none';$('cadq').style.display='none';"
    new = "$('polq').style.display='none';$('cadq').style.display='none';$('carrov').style.display='none';$('carpeteq').style.display='none';$('cabv').style.display='none';"
    if old not in s:
        raise SystemExit('ERRO: inicialização não encontrada')
    s = s.replace(old, new, 1)

# ===== 5. Eventos =====
if "$('carro').onchange=" not in s:
    marker = "$('sofa').onchange=()=>{"
    events = "$('carro').onchange=()=>{$('carrov').style.display=$('carro').checked?'block':'none';if(!$('carro').checked)document.querySelectorAll('input[name=carv]').forEach(x=>x.checked=false);calc()};$('carpete').onchange=()=>{$('carpeteq').style.display=$('carpete').checked?'flex':'none';calc()};$('cab').onchange=()=>{$('cabv').style.display=$('cab').checked?'block':'none';if(!$('cab').checked)document.querySelectorAll('input[name=cabv]').forEach(x=>x.checked=false);calc()};$('qcarpete').oninput=calc;"
    if marker not in s:
        raise SystemExit('ERRO: eventos atuais não encontrados')
    s = s.replace(marker, events + marker, 1)

# ===== 6. Validação =====
oldv = "if(($('sofa').checked&&!document.querySelector('input[name=sv]:checked'))||($('col').checked&&!document.querySelector('input[name=cv]:checked'))){error('Selecione o tamanho do sofá ou colchão.');return}"
newv = "if(($('sofa').checked&&!document.querySelector('input[name=sv]:checked'))||($('col').checked&&!document.querySelector('input[name=cv]:checked'))||($('carro').checked&&!document.querySelector('input[name=carv]:checked'))||($('cab').checked&&!document.querySelector('input[name=cabv]:checked'))){error('Selecione a opção do serviço escolhido.');return}"
if oldv in s:
    s = s.replace(oldv, newv, 1)

# ===== 7. Chamada comercial antes dos cards =====
old_intro = '<h1>Monte seu atendimento</h1><p>Escolha um ou mais serviços. O total será calculado automaticamente.</p>'
new_intro = '''<h1>Monte seu atendimento</h1><div class="service-intro"><p class="service-intro-main">Escolha o item abaixo, veja o preço e agende em 2 minutos.</p><div class="service-benefits"><span>🕒 Pague só no dia</span><span class="benefit-separator">•</span><span>✨ Seguro para pets e crianças</span></div></div>'''
if 'service-intro-main' not in s:
    if old_intro not in s:
        raise SystemExit('ERRO: texto introdutório atual não encontrado')
    s = s.replace(old_intro, new_intro, 1)

# ===== 8. CSS compacto definitivo =====
compact_css = '''
/* ===== Cards compactos Seven ===== */
.service-intro{margin:0 0 13px}.service-intro-main{margin:0 0 8px;font-size:15px;line-height:1.4;color:#202124}.service-benefits{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:13px;font-weight:800;color:#0f4c81}.benefit-separator{color:#9aa8b8}.service-mobile-grid{gap:8px!important;margin:12px 0 14px!important}.service-mobile-grid .service-card{border-radius:12px!important;box-shadow:0 4px 12px #0b17300b!important}.service-mobile-grid .service-card>label{min-height:96px!important;padding:9px 10px!important}.service-icon{width:34px!important;height:34px!important;border-radius:9px!important;font-size:19px!important;margin-bottom:6px!important}.service-name{font-size:15px!important;line-height:1!important}.service-count{font-size:10.5px!important;padding-top:5px!important}.service-card:has(input:checked)>label{padding:9px 10px!important;grid-template-columns:42px 1fr!important}.service-card:has(input:checked) .service-icon{width:34px!important;height:34px!important}.service-card:has(input:checked) .service-name{font-size:15px!important}.service-card:has(input:checked) .service-count{font-size:10.5px!important}.service-mobile-grid .variants,.service-mobile-grid .qty{margin:0 8px 8px!important}.service-mobile-grid .variant{padding:7px!important;margin:5px 0!important}@media(min-width:701px){.service-mobile-grid{grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:10px!important}.service-mobile-grid .service-card>label{min-height:102px!important}}@media(max-width:700px){.service-intro-main{font-size:14px}.service-benefits{font-size:12px;gap:7px}.service-mobile-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important}.service-mobile-grid .service-card>label{min-height:92px!important;padding:8px 9px!important}.service-icon{width:32px!important;height:32px!important;font-size:18px!important;margin-bottom:5px!important}.service-name{font-size:14px!important}.service-count{font-size:10px!important;padding-top:4px!important}}@media(max-width:380px){.service-benefits{gap:5px;font-size:11px}.service-mobile-grid{gap:7px!important}.service-mobile-grid .service-card>label{min-height:88px!important;padding:7px 8px!important}.service-icon{width:30px!important;height:30px!important;font-size:17px!important}.service-name{font-size:13.5px!important}.service-count{font-size:9.5px!important}}
'''
marker = '/* ===== Cards compactos Seven ===== */'
if marker not in s:
    s = s.replace('</style>', compact_css + '</style>', 1)
else:
    s = re.sub(r'/\* ===== Cards compactos Seven ===== \*/.*?(?=</style>)', compact_css.strip()+'\n', s, flags=re.S)

# ===== 9. Validação final =====
required = ['id="carro"','id="carpete"','id="cab"','Hatch - bancos e carpete','Sedan - bancos e carpete','SUV - bancos e carpete','Caminhonete - bancos e carpete','Cabeceira solteiro','Cabeceira casal','Cabeceira Queen','Cabeceira King','⚠️ Informação importante','até 8 horas',"$('carro').onchange=", "$('carpete').onchange=", "$('cab').onchange=",'Escolha o item abaixo, veja o preço e agende em 2 minutos.','Pague só no dia','Seguro para pets e crianças','Cards compactos Seven']
for item in required:
    if item not in s:
        raise SystemExit('ERRO: faltando '+item)

p.write_text(s, encoding='utf-8')
print('agendar4.html atualizado com sucesso')
