const { onDocumentCreated } = require('firebase-functions/v2/firestore');
const { defineSecret } = require('firebase-functions/params');
const logger = require('firebase-functions/logger');

const WHATSAPP_TOKEN = defineSecret('WHATSAPP_TOKEN');
const WHATSAPP_PHONE_NUMBER_ID = defineSecret('WHATSAPP_PHONE_NUMBER_ID');
const WHATSAPP_TO = '5548996782471';

function brl(value) {
  const n = Number(value || 0);
  return n.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function itemsText(items) {
  if (!Array.isArray(items) || !items.length) return 'Não informado';
  return items.map((item) => {
    const qty = Number(item.quantity || 1);
    const name = item.name || item.service_name || 'Serviço';
    const price = item.price ?? item.total ?? (Number(item.unit_price || 0) * qty);
    return `• ${name}${qty > 1 ? ` (${qty}x)` : ''} — ${brl(price)}`;
  }).join('\n');
}

function addressText(a) {
  const street = a.street || a.rua || a.address || '';
  const number = a.number || a.num || '';
  const neighborhood = a.neighborhood || a.bairro || '';
  const city = a.city || a.cidade || '';
  const reference = a.reference || a.ref || '';
  const cep = a.cep || '';
  return [
    street && `Rua: ${street}${number ? `, ${number}` : ''}`,
    neighborhood && `Bairro: ${neighborhood}`,
    city && `Cidade: ${city}`,
    cep && `CEP: ${cep}`,
    reference && `Referência: ${reference}`
  ].filter(Boolean).join('\n') || 'Não informado';
}

exports.notifyNewAppointment = onDocumentCreated({
  document: 'agendamentos/{appointmentId}',
  region: 'southamerica-east1',
  secrets: [WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID],
}, async (event) => {
  const data = event.data?.data();
  if (!data) return;

  const token = WHATSAPP_TOKEN.value();
  const phoneNumberId = WHATSAPP_PHONE_NUMBER_ID.value();

  if (!token || !phoneNumberId) {
    logger.error('WhatsApp não configurado. Defina WHATSAPP_TOKEN e WHATSAPP_PHONE_NUMBER_ID.');
    return;
  }

  const date = data.service_date || data.date || 'Não informado';
  const time = data.service_time || data.time || 'Não informado';
  const client = data.customer_name || data.nome || data.name || 'Não informado';
  const phone = data.customer_phone || data.tel || data.phone || 'Não informado';
  const total = data.total ?? data.total_price ?? 0;
  const observation = data.observation || data.obs || '';

  const message = [
    '🔔 *NOVO AGENDAMENTO — SEVEN*',
    '',
    `👤 *Cliente:* ${client}`,
    `📱 *WhatsApp:* ${phone}`,
    '',
    '🧼 *Serviços:*',
    itemsText(data.items || data.services),
    '',
    `💰 *Total:* ${brl(total)}`,
    `📅 *Data:* ${date}`,
    `⏰ *Horário:* ${time}`,
    '',
    '📍 *Endereço:*',
    addressText(data),
    observation && `\n📝 *Observação:* ${observation}`,
    '',
    `🆔 Agendamento: ${event.params.appointmentId}`
  ].filter(Boolean).join('\n');

  const url = `https://graph.facebook.com/v23.0/${phoneNumberId}/messages`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      messaging_product: 'whatsapp',
      recipient_type: 'individual',
      to: WHATSAPP_TO,
      type: 'text',
      text: { preview_url: false, body: message },
    }),
  });

  const result = await response.json().catch(() => ({}));
  if (!response.ok) {
    logger.error('Falha ao enviar notificação WhatsApp', { status: response.status, result });
    throw new Error(`WhatsApp API retornou HTTP ${response.status}`);
  }

  logger.info('Notificação de novo agendamento enviada', {
    appointmentId: event.params.appointmentId,
    to: WHATSAPP_TO,
    messageId: result?.messages?.[0]?.id || null,
  });
});
