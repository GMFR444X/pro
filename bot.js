const TelegramBot = require('node-telegram-bot-api');
const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const axios = require('axios');

// Ganti dengan token bot Telegram Anda
const token = '6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0';
const bot = new TelegramBot(token, { polling: true });

// Kode dari tictactoe.py
const {
    game_grid,
    empty_game_grid,
    unpacking_values,
    check_win,
    bot_ai,
} = require('./tictactoe');

// Penyimpanan status permainan Tic-Tac-Toe
const ticTacToeGames = new Map();

// Fungsi untuk menjalankan skrip Python
function runPythonScript(scriptName, args, chatId, resultFiles) {
    const pythonProcess = spawn('python3', [scriptName, ...args]);

    // Tampilkan pesan "Proses Cek Tunggu Dulu Bray"
    bot.sendMessage(chatId, 'Proses Cek Tunggu Dulu Bray...');

    pythonProcess.stdout.on('data', async (data) => {
        const message = data.toString('utf8').trim();
        bot.sendMessage(chatId, message);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        bot.sendMessage(chatId, 'Terjadi kesalahan dalam menjalankan skrip Python.');
    });

    pythonProcess.on('close', async (code) => {
        if (code === 0) {
            // Kirim file hasil jika ada
            for (const resultFile of resultFiles) {
                try {
                    const filePath = path.join(__dirname, resultFile);
                    const fileData = await fs.readFile(filePath, 'utf8');
                    bot.sendMessage(chatId, `Hasil ${resultFile}:\n${fileData}`);
                    await fs.unlink(filePath); // Hapus file setelah dikirim
                } catch (error) {
                    console.error('Error sending file:', error);
                }
            }
        } else {
            bot.sendMessage(chatId, 'Skrip Python tidak berhasil dijalankan.');
        }
    });
}

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
   • Menu Game
   - /tictactoe
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

// Menangani perintah /tictactoe
bot.onText(/\/tictactoe/, (msg) => {
    const chatId = msg.chat.id;
    const gameData = {
        values_dict: {
            '1': ' ', '2': ' ', '3': ' ',
            '4': ' ', '5': ' ', '6': ' ',
            '7': ' ', '8': ' ', '9': ' '
        },
        all_moves_set: new Set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    };
    ticTacToeGames.set(chatId, gameData);

    bot.sendMessage(chatId, 'Permainan Tic-Tac-Toe dimulai!', {
        reply_markup: game_grid(gameData.values_dict, gameData.all_moves_set)
    });
});

// Menangani callback dari game Tic-Tac-Toe
bot.on('callback_query', async (callbackQuery) => {
    const chatId = callbackQuery.message.chat.id;
    const gameId = chatId;
    const gameData = ticTacToeGames.get(gameId);

    if (!gameData) {
        bot.answerCallbackQuery(callbackQuery.id, { text: 'Permainan tidak ditemukan.' });
        return;
    }

    const { values_dict, all_moves_set } = gameData;
    const { data } = callbackQuery;

    if (data === 'none') {
        bot.answerCallbackQuery(callbackQuery.id, { text: 'Pilih kotak yang valid.' });
        return;
    }

    const [gameIdStr, move, gameValue] = data.split('-');

    if (gameIdStr !== '1') {
        bot.answerCallbackQuery(callbackQuery.id, { text: 'Pesan tidak valid.' });
        return;
    }

    values_dict[move] = '❌';
    all_moves_set.delete(move);

    const [isGameFinished, gameResult] = check_win(values_dict);

    if (isGameFinished) {
        await bot.editMessageText(`Permainan berakhir. ${gameResult}`, {
            chat_id: chatId,
            message_id: callbackQuery.message.message_id
        });
        ticTacToeGames.delete(gameId);
        return;
    }

    bot.editMessageReplyMarkup(game_grid(values_dict, all_moves_set), {
        chat_id: chatId,
        message_id: callbackQuery.message.message_id
    });

    setTimeout(async () => {
        const botMove = bot_ai(values_dict, all_moves_set);
        values_dict[botMove] = '⭕';
        all_moves_set.delete(botMove);

        const [isGameFinished, gameResult] = check_win(values_dict);

        if (isGameFinished) {
            await bot.editMessageText(`Permainan berakhir. ${gameResult}`, {
                chat_id: chatId,
                message_id: callbackQuery.message.message_id
            });
            ticTacToeGames.delete(gameId);
            return;
        }

        bot.editMessageReplyMarkup(game_grid(values_dict, all_moves_set), {
            chat_id: chatId,
            message_id: callbackQuery.message.message_id
        });

    }, 700);
});

// Menjalankan bot
console.log('Bot is running...');
