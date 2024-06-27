const TelegramBot = require('node-telegram-bot-api');
const { exec } = require('child_process');
const fs = require('fs');
const token = '6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0';
const bot = new TelegramBot(token, { polling: true });

function sendProgressUpdate(chatId, messageId) {
    const progressFile = 'progress.txt';
    if (fs.existsSync(progressFile)) {
        fs.readFile(progressFile, 'utf8', (err, data) => {
            if (err) {
                console.error(`Error reading progress file: ${err}`);
            } else {
                const progress = data.trim();
                if (progress) {
                    bot.editMessageText(`File received. Starting the check... ${progress}%`, {
                        chat_id: chatId,
                        message_id: messageId,
                        reply_markup: {
                            inline_keyboard: [[{ text: `Progress: ${progress}%`, callback_data: 'progress' }]]
                        }
                    });
                }
            }
        });
    }
}

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const username = msg.from.username;
    const currentDate = new Date().toDateString();

    bot.sendMessage(chatId, `Halo selamat malam ${username}! 👋🏻\n\nSaya adalah bot yang dibuat oleh @cadelXploit.\n\nUntuk melihat menu lainnya, bisa pencet tombol di bawah ini.\n\n🗓 TANGGAL: ${currentDate}`, {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: 'Wordpress Checker', callback_data: 'wpcek' },
                ],
                [
                    { text: 'Owner', url: 'https://t.me/cadelXploit' }
                ]
            ]
        }
    });
});

bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;
    const { data } = query;

    switch (data) {
        case 'wpcek':
            bot.sendMessage(chatId, `WordPress Checker\n\nCommand: /wpcek\n\nDescription: Use this command to check WordPress sites for login success and specific features like WP File Manager, Plugin Install, Theme Editor, Add Page, and Add Article.\n\nPlease send the file with the list of WordPress sites.`);
            break;
        default:
            break;
    }

    bot.answerCallbackQuery(query.id); // Close the button spinner
});

bot.onText(/\/wpcek/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, 'Please send the file with the list of WordPress sites.');

    bot.once('document', (msg) => {
        const fileId = msg.document.file_id;
        const filePath = `./${msg.document.file_name}`;
        const fileStream = bot.getFileStream(fileId);
        const writeStream = fs.createWriteStream(filePath);

        fileStream.pipe(writeStream).on('finish', () => {
            bot.sendMessage(chatId, 'File received. Starting the check...', {
                reply_markup: {
                    inline_keyboard: [[{ text: 'Progress: 0%', callback_data: 'progress' }]]
                }
            }).then(sentMessage => {
                const messageId = sentMessage.message_id;
                
                const intervalId = setInterval(() => {
                    sendProgressUpdate(chatId, messageId);
                }, 5000); // Check progress every 5 seconds

                exec(`python3 wpcek.py ${filePath} 10`, (error, stdout, stderr) => {
                    clearInterval(intervalId); // Stop checking progress
                    if (error) {
                        bot.sendMessage(chatId, `Error: ${error.message}`);
                        console.error(`Error: ${error.message}`);
                        return;
                    }
                    if (stderr) {
                        bot.sendMessage(chatId, `Stderr: ${stderr}`);
                        console.error(`Stderr: ${stderr}`);
                        return;
                    }

                    console.log(`Stdout: ${stdout}`);
                    bot.sendMessage(chatId, stdout); // Sending stdout to the user for debugging

                    const filesToSend = [
                        { path: './loginSuccess.txt', name: 'Login Success' },
                        { path: './wpfilemanager.txt', name: 'WP File Manager' },
                        { path: './plugin-install.txt', name: 'Plugin Install' },
                        { path: './wptheme.txt', name: 'Theme Editor' },
                        { path: './page.txt', name: 'Add Page' },
                    ];

                    let sentAnyFile = false;
                    filesToSend.forEach(file => {
                        if (fs.existsSync(file.path)) {
                            bot.sendDocument(chatId, file.path, { caption: `Results for ${file.name}` }).then(() => {
                                fs.unlinkSync(file.path);
                            });
                            sentAnyFile = true;
                        }
                    });

                    if (!sentAnyFile) {
                        bot.sendMessage(chatId, 'No successful logins or specific features found.');
                    }
                });
            });
        });

        writeStream.on('error', (error) => {
            bot.sendMessage(chatId, `Failed to write file: ${error.message}`);
            console.error(`Failed to write file: ${error.message}`);
        });
    });
});

bot.on('polling_error', (error) => console.log(`Polling Error: ${error.message}`));
