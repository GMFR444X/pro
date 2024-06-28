const TelegramBot = require('node-telegram-bot-api');
const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const axios = require('axios');

// Replace YOUR_TELEGRAM_BOT_TOKEN with your bot's token
const token = '6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0';
const bot = new TelegramBot(token, { polling: true });

// Helper function to run a Python script and handle its output
const runPythonScript = (script, args, chatId, outputFiles) => {
  bot.sendMessage(chatId, '*Proses Cek Tunggu Dulu Bray*', { parse_mode: 'Markdown' }).then(async () => {
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
            // Delete the file after sending it
            await fs.unlink(filePath);
          }
        } catch (err) {
          // Ignore file not found or empty file errors
        }
      }

      if (!resultsSent) {
        bot.sendMessage(chatId, '*Ga ada Hasil Burik*', { parse_mode: 'Markdown' });
      }
    });
  });
};

// Handle /start command
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
  `;
  bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });
});

// Handle /wpcek command
bot.onText(/\/wpcek/, (msg) => {
  const chatId = msg.chat.id;

  bot.sendMessage(chatId, 'Please send me the file.');

  bot.once('document', async (msg) => {
    const fileId = msg.document.file_id;

    const filePath = await bot.downloadFile(fileId, './');
    runPythonScript('wpcek.py', [filePath, '20'], chatId, [
      'loginSuccess.txt', 'wpfilemanager.txt', 'wptheme.txt', 'page.txt', 'plugin-install.txt'
    ]); // Assuming thread_count is 10
  });
});

// Handle /cpcek command
bot.onText(/\/cpcek/, (msg) => {
  const chatId = msg.chat.id;

  bot.sendMessage(chatId, 'Please send me the file.');

  bot.once('document', async (msg) => {
    const fileId = msg.document.file_id;

    const filePath = await bot.downloadFile(fileId, './');
    runPythonScript('cp.py', [filePath, '20'], chatId, ['good.txt']); // Assuming thread_count is 10
  });
});

// Handle /shellcek command
bot.onText(/\/shellcek/, (msg) => {
  const chatId = msg.chat.id;

  bot.sendMessage(chatId, 'Please send me the file.');

  bot.once('document', async (msg) => {
    const fileId = msg.document.file_id;

    const filePath = await bot.downloadFile(fileId, './');
    runPythonScript('shell.py', [filePath, '20'], chatId, ['goodshell.txt']); // Assuming thread_count is 10
  });
});

// Handle /ai command
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

// Start the bot
console.log('Bot is running...');
