import discord
from discord.ext import commands

# Data soal dan flag dengan kategori dan detail tambahan
soal_ctf = {
    "soal1": {
        "description": "Deskripsi soal 1",
        "flag": "SIJACTF{contoh_flag1}",
        "category": "REVERSE",
        "title": "Broken",
        "author": "Dadan",
        "attachment": "http://example.com/download_soal1"
    },
    "soal2": {
        "description": "Deskripsi soal 2",
        "flag": "SIJACTF{contoh_flag2}",
        "category": "FORENS",
        "title": "Another Broken",
        "author": "Dadan",
        "attachment": "http://example.com/download_soal2"
    },
}

# Data pengguna yang sudah menyelesaikan soal
solved_by_user = {}

# Inisialisasi intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Aktifkan intents members jika diperlukan
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot berhasil login sebagai {bot.user}")

# Command untuk menampilkan soal
@bot.command()
async def soal(ctx, nomor):
    if nomor in soal_ctf:
        soal = soal_ctf[nomor]
        description = soal["description"]
        category = soal["category"]
        title = soal["title"]
        author = soal["author"]
        attachment = soal["attachment"]
        await ctx.send(
            f"Soal {nomor}: {description}\n"
            f"Title: {title}\n"
            f"Category: {category}\n"
            f"Author: {author}\n"
            f"Attachment: {attachment}"
        )
    else:
        await ctx.send("Soal tidak ditemukan.")

# Command untuk submit flag
@bot.command()
async def submit(ctx, nomor, flag):
    user_id = str(ctx.author.id)

    if nomor in soal_ctf:
        if flag == soal_ctf[nomor]["flag"]:
            if user_id not in solved_by_user:
                solved_by_user[user_id] = []

            if nomor in solved_by_user[user_id]:
                await ctx.send("Kamu sudah menyelesaikan soal ini sebelumnya.")
            else:
                solved_by_user[user_id].append(nomor)
                await ctx.send(f"Selamat {ctx.author.name}, flag benar! Soal {nomor} telah di-solve.")
        else:
            await ctx.send("Flag salah.")
    else:
        await ctx.send("Soal tidak ditemukan.")

# Command untuk menampilkan status soal yang sudah di-solve
@bot.command()
async def status(ctx):
    user_id = str(ctx.author.id)
    if user_id in solved_by_user and solved_by_user[user_id]:
        solved_list = ", ".join(solved_by_user[user_id])
        await ctx.send(f"Kamu telah menyelesaikan soal: {solved_list}")
    else:
        await ctx.send("Kamu belum menyelesaikan soal apapun.")

# Command untuk melihat daftar soal
@bot.command()
async def daftar_soal(ctx):
    if soal_ctf:
        soal_list = "\n".join(
            [f"{nomor}: {soal['title']} (Category: {soal['category']})" for nomor, soal in soal_ctf.items()]
        )
        await ctx.send(f"Daftar Soal:\n{soal_list}")
    else:
        await ctx.send("Tidak ada soal yang tersedia.")

# Command untuk melihat score pengguna
@bot.command()
async def score(ctx):
    if solved_by_user:
        score_list = "\n".join(
            [f"<@{user_id}>: {', '.join(soal_list)}" for user_id, soal_list in solved_by_user.items()]
        )
        await ctx.send(f"Skor Pengguna:\n{score_list}")
    else:
        await ctx.send("Belum ada pengguna yang menyelesaikan soal.")

# Jalankan bot menggunakan token
# Gantilah 'YOUR_BOT_TOKEN' dengan token bot Anda yang valid
bot.run('REDACTEDcle')