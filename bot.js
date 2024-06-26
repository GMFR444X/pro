const { Telegraf, Markup } = require('telegraf');
const { spawn } = require('child_process');

const bot = new Telegraf('6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0');

// Start command handler
bot.start((ctx) => {
    const username = ctx.from.username;
    const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });

    const welcomeMessage = `Halo selamat malam ${username}! 👋🏻\n\nSaya adalah bot yang dibuat oleh @cadelXploit.\n\nUntuk melihat menu lainnya, bisa pencet tombol di bawah ini.\n\n🗓 TANGGAL: ${currentDate}.`;

    const menuKeyboard = Markup.inlineKeyboard([
        Markup.button.url('Menu dan Command', 'https://yourwebsite.com/menu'),
        Markup.button.callback('Owner', 'owner_button')
    ]);

    ctx.reply(welcomeMessage, menuKeyboard);
});

// Command handlers
bot.command('ddos', async (ctx) => {
    const url = ctx.message.text.split(' ')[1];
    if (!url) {
        return ctx.reply('Please provide a URL after /ddos command.');
    }

    const process = spawn('python3', ['ddos.py', url]);
    process.stdout.on('data', (data) => {
        ctx.reply(data.toString());
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        ctx.reply(`Error: ${data}`);
    });
});

bot.command('subdomain', async (ctx) => {
    const url = ctx.message.text.split(' ')[1];
    if (!url) {
        return ctx.reply('Please provide a URL after /subdomain command.');
    }

    const process = spawn('python3', ['subdomain.py', url]);
    process.stdout.on('data', (data) => {
        ctx.reply(data.toString());
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        ctx.reply(`Error: ${data}`);
    });
});

bot.command('reverseip', async (ctx) => {
    const ip = ctx.message.text.split(' ')[1];
    if (!ip) {
        return ctx.reply('Please provide an IP after /reverseip command.');
    }

    const process = spawn('python3', ['reverseip.py', ip]);
    process.stdout.on('data', (data) => {
        ctx.reply(data.toString());
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        ctx.reply(`Error: ${data}`);
    });
});

bot.command('wpcek', async (ctx) => {
    const file = ctx.message.document;
    if (!file || !file.file_id) {
        return ctx.reply('Please upload a .txt file containing targets after /wpcek command.');
    }

    const process = spawn('python3', ['wpcek.py', file.file_id]);
    process.stdout.on('data', (data) => {
        ctx.reply(data.toString());
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        ctx.reply(`Error: ${data}`);
    });
});

bot.command('dapacek', async (ctx) => {
    const url = ctx.message.text.split(' ')[1];
    if (!url) {
        return ctx.reply('Please provide a URL after /dapacek command.');
    }

    const process = spawn('python3', ['dapacek.py', url]);
    process.stdout.on('data', (data) => {
        ctx.reply(data.toString());
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        ctx.reply(`Error: ${data}`);
    });
});

// Owner button callback handler
bot.action('owner_button', (ctx) => {
    ctx.reply('Jika Anda ingin menghubungi owner, silakan klik link ini: https://t.me/cadelXploit');
});

bot.launch();