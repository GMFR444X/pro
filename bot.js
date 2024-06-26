const { Telegraf, Markup } = require('telegraf');
const { spawn } = require('child_process');

const bot = new Telegraf('6674838409:AAHLkaUy93k648M8FlvlhBddJLD0NgfzYd0');

// Start command handler
bot.start((ctx) => {
    const username = ctx.from.username;
    const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });

    const welcomeMessage = `Halo selamat malam ${username}! 👋🏻\n\nSaya adalah bot yang dibuat oleh @cadelXploit.\n\nUntuk melihat menu lainnya, bisa pencet tombol di bawah ini.\n\n🗓 TANGGAL: ${currentDate}.`;

    const menuKeyboard = Markup.inlineKeyboard([
        Markup.button.callback('Menu dan Command', 'menu_button'),
        Markup.button.url('Owner', 'https://t.me/cadelXploit')
    ]);

    ctx.replyWithHTML(welcomeMessage, menuKeyboard);
});

// Command handlers
bot.command('ddos', async (ctx) => {
    const url = ctx.message.text.split(' ')[1];
    if (!url) {
        return ctx.reply('Please provide a URL after /ddos command.');
    }

    const process = spawn('python3', ['ddos.py', url]);
    let output = '';

    process.stdout.on('data', (data) => {
        output += data.toString();
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        output += data.toString();
    });

    process.on('close', () => {
        ctx.reply(output.trim() || 'No response from DDoS script.');
    });
});

bot.command('subdomain', async (ctx) => {
    const url = ctx.message.text.split(' ')[1];
    if (!url) {
        return ctx.reply('Please provide a URL after /subdomain command.');
    }

    const process = spawn('python3', ['subdomain.py', url]);
    let output = '';

    process.stdout.on('data', (data) => {
        output += data.toString();
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        output += data.toString();
    });

    process.on('close', () => {
        ctx.reply(output.trim() || 'No response from subdomain script.');
    });
});

bot.command('reverseip', async (ctx) => {
    const ip = ctx.message.text.split(' ')[1];
    if (!ip) {
        return ctx.reply('Please provide an IP after /reverseip command.');
    }

    const process = spawn('python3', ['reverseip.py', ip]);
    let output = '';

    process.stdout.on('data', (data) => {
        output += data.toString();
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        output += data.toString();
    });

    process.on('close', () => {
        ctx.reply(output.trim() || 'No response from reverse IP script.');
    });
});

bot.command('wpcek', async (ctx) => {
    const file = ctx.message.document;
    if (!file || !file.file_id) {
        return ctx.reply('Please upload a .txt file containing targets after /wpcek command.');
    }

    const fileId = file.file_id;
    const fileLink = await ctx.telegram.getFileLink(fileId);

    ctx.reply('Memulai proses checker WordPress, harap tunggu sebentar...');

    // Mock progress, replace with actual logic
    let progress = 0;
    const interval = setInterval(() => {
        progress += 20;
        if (progress <= 100) {
            ctx.reply(`Proses ${progress}%`);
        } else {
            clearInterval(interval);
        }
    }, 1000);

    const process = spawn('python3', ['wpcek.py', fileId]);
    let output = '';

    process.stdout.on('data', (data) => {
        output += data.toString();
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        output += data.toString();
    });

    process.on('close', () => {
        clearInterval(interval);
        ctx.reply(output.trim() || 'No response from WordPress checker script.');
    });
});

bot.command('dapacek', async (ctx) => {
    const url = ctx.message.text.split(' ')[1];
    if (!url) {
        return ctx.reply('Please provide a URL after /dapacek command.');
    }

    const process = spawn('python3', ['dapacek.py', url]);
    let output = '';

    process.stdout.on('data', (data) => {
        output += data.toString();
    });

    process.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        output += data.toString();
    });

    process.on('close', () => {
        ctx.reply(output.trim() || 'No response from DA PA checker script.');
    });
});

// Menu button callback handler
bot.action('menu_button', (ctx) => {
    const menuMessage = `
📋 Menu dan Command:

1. <b>DDoS</b>: /ddos <i>&lt;url&gt;</i> - Melakukan serangan DDoS terhadap URL yang diberikan.
2. <b>Subdomain Search</b>: /subdomain <i>&lt;url&gt;</i> - Mencari subdomain dari URL yang diberikan.
3. <b>Reverse IP Lookup</b>: /reverseip <i>&lt;ip&gt;</i> - Mencari domain berdasarkan IP yang diberikan.
4. <b>WordPress Checker</b>: /wpcek - Memeriksa login WordPress dari file .txt yang diunggah.
5. <b>DA PA Checker</b>: /dapacek <i>&lt;url&gt;</i> - Memeriksa Domain Authority (DA) dan Page Authority (PA) dari URL yang diberikan.
`;

    ctx.replyWithHTML(menuMessage);
});

bot.launch();
