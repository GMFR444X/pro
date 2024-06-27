const TelegramBot = require('node-telegram-bot-api');
const { exec } = require('child_process');
const fs = require('fs');
const token = '6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0';
const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/wpcek/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, 'Please send the file with the list of WordPress sites.');

    bot.once('document', (msg) => {
        const fileId = msg.document.file_id;
        const filePath = `./${msg.document.file_name}`;
        const fileStream = bot.getFileStream(fileId);
        const writeStream = fs.createWriteStream(filePath);

        fileStream.pipe(writeStream).on('finish', () => {
            bot.sendMessage(chatId, 'File received. Starting the check...');

            exec(`python3 wpcek.py ${filePath}`, (error, stdout, stderr) => {
                if (error) {
                    bot.sendMessage(chatId, `Error: ${error.message}`);
                    return;
                }
                if (stderr) {
                    bot.sendMessage(chatId, `Stderr: ${stderr}`);
                    return;
                }

                const loginSuccessFile = './loginSuccess.txt';
                if (fs.existsSync(loginSuccessFile)) {
                    bot.sendDocument(chatId, loginSuccessFile).then(() => {
                        fs.unlinkSync(loginSuccessFile);
                    });
                } else {
                    bot.sendMessage(chatId, 'No successful logins found.');
                }
            });
        });
    });
});
