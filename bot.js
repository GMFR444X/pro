const TelegramBot = require('node-telegram-bot-api');
const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const axios = require('axios');

// Replace YOUR_TELEGRAM_BOT_TOKEN with your bot's token
const token = '6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0';
const bot = new TelegramBot(token, { polling: true });

// Helper function to run a Python script and handle its output
const runPythonScript = async (script, args, chatId, outputFiles) => {
    let message = await bot.sendMessage(chatId, '𝗣𝗿𝗼𝘀𝗲𝘀 𝗖𝗲𝗸 𝗧𝘂𝗻𝗴𝗴𝘂 𝗗𝘂𝗹𝘂 𝗕𝗿𝗮𝘆...');
    let count = 0;
    const animations = ['.', '..', '...', ''];

    const intervalId = setInterval(async () => {
        const animation = animations[count % animations.length];
        count++;
        await bot.editMessageText(`𝗣𝗿𝗼𝘀𝗲𝘀 𝗖𝗲𝗸 𝗧𝘂𝗻𝗴𝗴𝘂 𝗗𝘂𝗹𝘂 𝗕𝗿𝗮𝘆${animation}`, {
            chat_id: chatId,
            message_id: message.message_id
        });
    }, 500);

    const pythonProcess = spawn('python3', [script, ...args]);

    pythonProcess.on('close', async (code) => {
        clearInterval(intervalId);
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
            bot.sendMessage(chatId, '*𝗚𝗮 𝗔𝗱𝗮 𝗛𝗮𝘀𝗶𝗹 𝗕𝗮𝗻𝗴 𝗕𝘂𝗿𝗶𝗸*', { parse_mode: 'Markdown' });
        }
    });
};

// Handle /start command
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const message = `
𝗣𝗜𝗟𝗜𝗛 𝗠𝗘𝗡𝗨 𝗖𝗨𝗬
• 𝗠𝗘𝗡𝗨 𝗘𝗫𝗣𝗟𝗢𝗜𝗧
- /wpcek
𝗪𝗼𝗿𝗱𝗽𝗿𝗲𝘀𝘀 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 
- /cpcek
𝗖𝗽𝗮𝗻𝗲𝗹 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 
- /shellcek
𝗦𝗵𝗲𝗹𝗹 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 
- /kcfinderscan
𝗞𝗰𝗳𝗶𝗻𝗱𝗲𝗿 𝗦𝗰𝗮𝗻𝗻𝗲𝗿

• 𝗠𝗘𝗡𝗨 𝗟𝗔𝗜𝗡𝗡𝗬𝗔
- /ai <pesan
𝗖𝗛𝗔𝗧𝗚𝗣𝗧 𝗔𝗜
- /simi <pesan
𝗦𝗜𝗠𝗜 𝗔𝗡𝗝
  `;
    bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });
});

// Handle /wpcek command
bot.onText(/\/wpcek/, (msg) => {
    const chatId = msg.chat.id;

    bot.sendMessage(chatId, '𝗦𝗲𝗻𝗱 𝗟𝗶𝘀𝘁 𝗪𝗼𝗿𝗱𝗽𝗿𝗲𝘀𝘀.');

    bot.once('document', async (msg) => {
        const fileId = msg.document.file_id;

        const filePath = await bot.downloadFile(fileId, './');
        runPythonScript('wpcek.py', [filePath, '10'], chatId, [
            'loginSuccess.txt', 'wpfilemanager.txt', 'wptheme.txt', 'page.txt', 'plugin-install.txt'
        ]);
    });
});

// Handle /cpcek command
bot.onText(/\/cpcek/, (msg) => {
    const chatId = msg.chat.id;

    bot.sendMessage(chatId, '𝗦𝗲𝗻𝗱 𝗟𝗶𝘀𝘁 𝗖𝗽𝗮𝗻𝗲𝗹.');

    bot.once('document', async (msg) => {
        const fileId = msg.document.file_id;

        const filePath = await bot.downloadFile(fileId, './');
        runPythonScript('cp.py', [filePath, '10'], chatId, ['good.txt']);
    });
});

// Handle /shellcek command
bot.onText(/\/shellcek/, (msg) => {
    const chatId = msg.chat.id;

    bot.sendMessage(chatId, '𝗦𝗲𝗻𝗱 𝗟𝗶𝘀𝘁 𝗦𝗵𝗲𝗹𝗹.');

    bot.once('document', async (msg) => {
        const fileId = msg.document.file_id;

        const filePath = await bot.downloadFile(fileId, './');
        runPythonScript('shell.py', [filePath, '10'], chatId, ['goodshell.txt']);
    });
});

// Handle /kcfinderscan command
bot.onText(/\/kcfinderscan/, (msg) => {
    const chatId = msg.chat.id;

    bot.sendMessage(chatId, '𝗦𝗲𝗻𝗱 𝗟𝗶𝘀𝘁 𝗨𝗿𝗹.');

    bot.once('document', async (msg) => {
        const fileId = msg.document.file_id;

        const filePath = await bot.downloadFile(fileId, './');
        runPythonScript('kcfinder.py', [filePath, '10'], chatId, ['result_kcfinder.txt']);
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

// Handle /simi command
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

// Start the bot
console.log('Bot is running...');
