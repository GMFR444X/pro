const TelegramBot = require('node-telegram-bot-api');
const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const axios = require('axios');

// Ganti dengan token bot Telegram Anda
const token = '6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0';
const bot = new TelegramBot(token, { polling: true });

// Fungsi untuk menjalankan skrip Python dan menangani outputnya
const runPythonScript = (script, args, chatId, outputFiles) => {
  bot.sendMessage(chatId, '*Proses Cek Tunggu Dulu Bray*', { parse_mode: 'Markdown' });

  const pythonProcess = spawn('python3', [script, ...args]);

  pythonProcess.on('close', async (code) => {
    let resultsSent = false;

    for (const file of outputFiles) {
      try {
        const filePath = path.resolve(file);
        const stats = await fs.stat(filePath);

        if (stats.size > 0) {
          await bot.sendDocument(chatId, filePath);
          resultsSent = true;
          // Hapus file setelah mengirim
          await fs.unlink(filePath);
        }
      } catch (err) {
        // Abaikan jika file tidak ditemukan atau kosong
      }
    }

    if (!resultsSent) {
      bot.sendMessage(chatId, '*Ga ada Hasil Burik*', { parse_mode: 'Markdown' });
    }
  });
};

// Menangani perintah /start
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  const message = `
Pilih menu:

   • Menu Exploit
   - /wpcek
   - /cpcek
   - /shellcek
   • Menu Lainnya
   - /ai <pesan>
   - /simi <pesan>
  `;
  bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });
});

// Menangani perintah /wpcek
bot.onText(/\/wpcek/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Please send me the file.');

  bot.once('document', async (msg) => {
    const fileId = msg.document.file_id;
    const filePath = await bot.downloadFile(fileId, './');
    runPythonScript('wpcek.py', [filePath, '10'], chatId, [
      'loginSuccess.txt', 'wpfilemanager.txt', 'wptheme.txt', 'page.txt', 'plugin-install.txt'
    ]);
  });
});

// Menangani perintah /cpcek
bot.onText(/\/cpcek/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Please send me the file.');

  bot.once('document', async (msg) => {
    const fileId = msg.document.file_id;
    const filePath = await bot.downloadFile(fileId, './');
    runPythonScript('cp.py', [filePath, '10'], chatId, ['good.txt']);
  });
});

// Menangani perintah /shellcek
bot.onText(/\/shellcek/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Please send me the file.');

  bot.once('document', async (msg) => {
    const fileId = msg.document.file_id;
    const filePath = await bot.downloadFile(fileId, './');
    runPythonScript('shell.py', [filePath, '10'], chatId, ['goodshell.txt']);
  });
});

// Menangani perintah /ai
bot.onText(/\/ai (.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const pesan = match[1];

  try {
    bot.sendChatAction(chatId, 'typing');
    const response = await axios.get(`https://chatgpt.apinepdev.workers.dev/?question=${encodeURIComponent(pesan)}`);
    const jawaban = response.data.answer;
    bot.sendMessage(chatId, jawaban, { parse_mode: 'Markdown', reply_to_message_id: msg.message_id });
  } catch (error) {
    console.error('Error:', error);
    bot.sendMessage(chatId, 'Maaf, terjadi kesalahan.');
  }
});

// Menangani perintah /simi
bot.onText(/\/simi (.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const pesan = match[1];

  try {
    bot.sendChatAction(chatId, 'typing');
    const response = await axios.get(`https://simsimi.site/api/v2/?mode=talk&lang=en&message=${encodeURIComponent(pesan)}&filter=true`);
    const jawaban = response.data.success ? response.data.success : "Maaf, terjadi kesalahan.";
    bot.sendMessage(chatId, jawaban, { parse_mode: 'Markdown', reply_to_message_id: msg.message_id });
  } catch (error) {
    console.error('Error:', error);
    bot.sendMessage(chatId, 'Maaf, terjadi kesalahan.');
  }
});

// Menjalankan bot
console.log('Bot is running...');
