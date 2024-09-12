import discord
import os
from discord.ext import commands
from datetime import datetime
from soal_ctf import soal_ctf  

# Data pengguna yang sudah menyelesaikan soal dan total poin mereka
solved_by_user = {}

# Inisialisasi intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Aktifkan intents members jika diperlukan
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot berhasil login sebagai {bot.user}")

# Command untuk menyapa atau memanggil bot dengan gaya Neofetch
@bot.command()
async def sapa(ctx):
    # Ambil informasi tentang bot dan waktu sekarang
    bot_name = bot.user.name
    bot_id = bot.user.id
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guild_count = len(bot.guilds)
    user_count = sum(guild.member_count for guild in bot.guilds)

    # ASCII art Neofetch-style untuk bot
    ascii_art = """
     ____                _ _                ___             
    |  _ \ _ __ ___   __| (_) __ _ _   _   / _ \ _ __   ___ 
    | |_) | '__/ _ \ / _` | |/ _` | | | | | | | | '_ \ / _ \
    |  __/| | | (_) | (_| | | (_| | |_| | | |_| | | | |  __/
    |_|   |_|  \___/ \__,_|_|\__, |\__, |  \___/|_| |_|\___|
                             |___/ |___/                    
    """

    # Embed dengan gaya Neofetch, menggunakan warna dan teks dengan format
    embed = discord.Embed(
        title="💻 Neofetch Bot Info",
        description=f"```fix\n{ascii_art}```",
        color=0x7289DA  # Warna biru muda khas Discord
    )

    embed.add_field(name="🤖 Bot Name", value=f"{bot_name}", inline=False)
    embed.add_field(name="🆔 Bot ID", value=f"{bot_id}", inline=False)
    embed.add_field(name="⏰ Current Time", value=f"{current_time}", inline=False)
    embed.add_field(name="🌐 Server Count", value=f"{guild_count}", inline=False)
    embed.add_field(name="👥 User Count", value=f"{user_count}", inline=False)

    embed.set_footer(text="Powered by Neofetch Inspired Bot", icon_url=bot.user.display_avatar.url)

    # Kirimkan embed
    await ctx.send(embed=embed)

# Command untuk menampilkan soal
@bot.command()
async def soal(ctx, nomor):
    if nomor in soal_ctf:
        soal = soal_ctf[nomor]
        embed = discord.Embed(
            title=f"📝 Soal {nomor}: {soal['title']}",
            description=f"*Deskripsi:* {soal['description']}\n"
                        f"*Category:* {soal['category']}\n"
                        f"*Author:* {soal['author']}\n"
                        f"*Points:* {soal['points']} 🏅\n"
                        f"[Attachment]({soal['attachment']})",
            color=0x00FF00  # Warna hijau
        )
        embed.set_footer(text="Semoga berhasil!")
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Soal tidak ditemukan.")

# Command untuk submit flag
@bot.command()
async def submit(ctx, nomor, flag):
    user_id = str(ctx.author.id)

    if nomor in soal_ctf:
        if flag == soal_ctf[nomor]["flag"]:
            if user_id not in solved_by_user:
                solved_by_user[user_id] = {"soal": [], "total_points": 0}

            if nomor in solved_by_user[user_id]["soal"]:
                await ctx.send("⚠️ Kamu sudah menyelesaikan soal ini sebelumnya.")
            else:
                solved_by_user[user_id]["soal"].append(nomor)
                soal_points = soal_ctf[nomor]["points"]
                solved_by_user[user_id]["total_points"] += soal_points
                await ctx.send(f"✅ Selamat {ctx.author.name}, flag benar! Kamu mendapatkan {soal_points} poin untuk soal {nomor}. 🎉")
        else:
            await ctx.send("❌ Flag salah.")
    else:
        await ctx.send("❌ Soal tidak ditemukan.")

# Command untuk menampilkan status soal yang sudah di-solve
@bot.command()
async def status(ctx):
    user_id = str(ctx.author.id)
    if user_id in solved_by_user and solved_by_user[user_id]["soal"]:
        solved_list = "\n".join(f"📝 {nomor}" for nomor in solved_by_user[user_id]["soal"])
        total_points = solved_by_user[user_id]["total_points"]

        embed = discord.Embed(
            title=f"Status Soal {ctx.author.name}",
            description=f"Kamu telah menyelesaikan soal-soal berikut:\n{solved_list}\n\n"
                        f"*Total Poin:* {total_points} 🏅",
            color=0x00A1D9  # Warna biru
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("⚠️ Kamu belum menyelesaikan soal apapun.")

# Command untuk melihat daftar soal, dikelompokkan berdasarkan kategori
@bot.command()
async def daftar_soal(ctx):
    if soal_ctf:
        categories = {}
        for nomor, soal in soal_ctf.items():
            category = soal["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(f"{nomor}: {soal['title']} (Points: {soal['points']} 🏅)")

        embed = discord.Embed(
            title="📜 Daftar Soal",
            description="Soal dikelompokkan berdasarkan kategori.",
            color=0x00FF00  # Warna hijau
        )

        for category, soal_list in categories.items():
            embed.add_field(
                name=f"🔖 {category}",
                value="\n".join(soal_list),
                inline=False
            )

        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Tidak ada soal yang tersedia.")

# Command untuk melihat scoreboard (ranking berdasarkan total poin)
@bot.command()
async def scoreboard(ctx):
    if solved_by_user:
        # Urutkan pengguna berdasarkan total poin
        ranked_users = sorted(solved_by_user.items(), key=lambda x: x[1]["total_points"], reverse=True)
        embed = discord.Embed(
            title="🏆 Scoreboard Pengguna",
            color=0xFFD700  # Warna emas untuk scoreboard
        )

        for rank, (user_id, data) in enumerate(ranked_users, 1):
            username = await bot.fetch_user(int(user_id))  # Ambil username berdasarkan user_id
            total_points = data["total_points"]

            # Tambahkan emoji khusus untuk 1st, 2nd, dan 3rd
            if rank == 1:
                rank_emoji = "🥇"
            elif rank == 2:
                rank_emoji = "🥈"
            elif rank == 3:
                rank_emoji = "🥉"
            else:
                rank_emoji = f"{rank}."

            embed.add_field(
                name=f"{rank_emoji} {username}",
                value=f"Total Points: {total_points} 🏅",
                inline=False
            )

        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Belum ada pengguna yang menyelesaikan soal.")


# Jalankan bot menggunakan token
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)