from pathlib import Path
import re

# ===== Página pública: consulta apenas agenda_publica e grava dados privados separadamente =====
p=Path('agendar4.html')
s=p.read_text(encoding='utf-8')

old_import="import{getFirestore,collection,query,where,getDocs,addDoc,doc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
new_import="import{getFirestore,collection,query,where,getDocs,addDoc,setDoc,doc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
if old_import in s:s=s.replace(old_import,new_import,1)
elif 'addDoc,setDoc,doc,getDoc' not in s:raise SystemExit('Import Firestore do agendar4 não encontrado')

s=s.replace("query(collection(db,'agendamentos'),where('service_date','==',data))","query(collection(db,'agenda_publica'),where('service_date','==',data))")
s=s.replace("query(collection(db,'agendamentos'),where('service_date','==',chosen.date))","query(collection(db,'agenda_publica'),where('service_date','==',chosen.date))")

old="await addDoc(collection(db,'agendamentos'),{receipt_number:'WEB-'+Date.now().toString().slice(-6),client_name:"
if old in s:
    s=s.replace(old,"const novoAgendamento=await addDoc(collection(db,'agendamentos'),{receipt_number:'WEB-'+Date.now().toString().slice(-6),client_name:",1)
    marker="created_at:new Date().toISOString()});const d=new Date(chosen.date+'T12:00:00');"
    repl="created_at:new Date().toISOString()});await setDoc(doc(db,'agenda_publica',novoAgendamento.id),{service_date:chosen.date,service_time:chosen.time,duration_minutes:i.dur,service_status:'Agendado'});const d=new Date(chosen.date+'T12:00:00');"
    if marker not in s:raise SystemExit('Final da criação pública não encontrado')
    s=s.replace(marker,repl,1)
elif "agenda_publica',novoAgendamento.id" not in s:
    raise SystemExit('Criação do agendamento público não encontrada')

for forbidden in ["collection(db,'agendamentos'),where('service_date'",]:
    if forbidden in s:raise SystemExit('Leitura pública de dados privados ainda presente')
for required in ["collection(db,'agenda_publica')","agenda_publica',novoAgendamento.id","addDoc,setDoc,doc,getDoc"]:
    if required not in s:raise SystemExit('Proteção pública incompleta: '+required)
p.write_text(s,encoding='utf-8')

# ===== Painel: mantém agenda_publica sincronizada ao criar/editar/excluir =====
p=Path('agendamento2.html')
s=p.read_text(encoding='utf-8')

old_import="import{getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
new_import="import{getFirestore,collection,addDoc,updateDoc,deleteDoc,doc,query,orderBy,onSnapshot,setDoc,getDoc}from'https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js';"
if old_import not in s:raise SystemExit('Import Firestore do painel não encontrado')

old_funcs="window.salvarAgendamentoCloud=async d=>{try{return(await addDoc(collection(db,'agendamentos'),d)).id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));return true}catch(e){console.error(e);return false}};"
new_funcs="window.sincronizarAgendaPublica=async(id,d)=>{const ref=doc(db,'agenda_publica',id);if(d&&d.service_date&&d.service_time&&d.service_status!=='Cancelado'){await setDoc(ref,{service_date:d.service_date,service_time:d.service_time,duration_minutes:Number(d.duration_minutes||60),service_status:d.service_status||'Agendado'})}else{try{await deleteDoc(ref)}catch(e){console.warn('Agenda pública',e)}}};window.salvarAgendamentoCloud=async d=>{try{const r=await addDoc(collection(db,'agendamentos'),d);await window.sincronizarAgendaPublica(r.id,d);return r.id}catch(e){console.error(e);return null}};window.atualizarAgendamentoCloud=async(id,d)=>{try{await updateDoc(doc(db,'agendamentos',id),d);const x=await getDoc(doc(db,'agendamentos',id));if(x.exists())await window.sincronizarAgendaPublica(id,x.data());return true}catch(e){console.error(e);return false}};window.excluirAgendamentoCloud=async id=>{try{await deleteDoc(doc(db,'agendamentos',id));try{await deleteDoc(doc(db,'agenda_publica',id))}catch(e){}return true}catch(e){console.error(e);return false}};"
if old_funcs in s:s=s.replace(old_funcs,new_funcs,1)
elif 'window.sincronizarAgendaPublica=' not in s:raise SystemExit('Funções cloud do painel não encontradas')

for required in ['window.sincronizarAgendaPublica=',"doc(db,'agenda_publica',id)"]:
    if required not in s:raise SystemExit('Sincronização do painel incompleta: '+required)
p.write_text(s,encoding='utf-8')
print('Privacidade Firestore aplicada às páginas Seven')
