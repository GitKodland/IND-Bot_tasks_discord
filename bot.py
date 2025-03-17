import discord
from discord.ext import commands
from config import TOKEN

# Membuat objek intents untuk bot agar bot dapat menerima pesan
intents = discord.Intents.default()
intents.messages = True

# Membuat objek bot dengan prefix '!' untuk perintah
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary untuk menyimpan tugas pengguna. Kunci - ID pengguna, nilai - daftar tugas
tasks = {}

# Event yang terpicu ketika bot berhasil dijalankan
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Perintah untuk mengelola tugas
@bot.command()
async def task(ctx, action=None, *, content=None):
    # Mendapatkan ID pengguna yang memanggil perintah
    user_id = ctx.author.id
    # Jika pengguna belum memiliki tugas, buat daftar tugas kosong untuknya
    if user_id not in tasks:
        tasks[user_id] = []

    # Memproses perintah untuk menambahkan tugas
    if action == 'add':
        task_id = len(tasks[user_id]) + 1  # Menghasilkan ID tugas
        tasks[user_id].append({'id': task_id, 'content': content})  # Menambahkan tugas ke daftar pengguna
        await ctx.send(f'Tugas ditambahkan: {content} (ID: {task_id})')  # Mengirim konfirmasi

    # Memproses perintah untuk menghapus tugas
    elif action == 'remove':
        if content and content.isdigit():  # Memeriksa apakah ID tugas yang diberikan valid
            task_id = int(content)  # Mengubah ID tugas menjadi angka
            task_list = tasks[user_id]  # Mendapatkan daftar tugas pengguna
            # Mencari tugas berdasarkan ID
            task_to_remove = next((task for task in task_list if task['id'] == task_id), None)
            if task_to_remove:
                task_list.remove(task_to_remove)  # Menghapus tugas dari daftar
                await ctx.send(f'Tugas dengan ID {task_id} telah dihapus.')  # Mengirim konfirmasi
            else:
                await ctx.send(f'Tugas dengan ID {task_id} tidak ditemukan.')  # Memberi tahu jika tugas tidak ditemukan
        else:
            await ctx.send('Harap tentukan ID tugas yang valid untuk dihapus.')  # Memberi tahu tentang kesalahan

    # Memproses perintah untuk menampilkan daftar tugas
    elif action == 'list':
        task_list = tasks[user_id]  # Mendapatkan daftar tugas pengguna
        if task_list:
            # Membuat respons dengan daftar tugas
            response = "Tugas Anda saat ini:\n"
            response += "\n".join([f"ID: {task['id']}, Deskripsi: {task['content']}" for task in task_list])
        else:
            response = "Anda tidak memiliki tugas saat ini."  # Memberi tahu jika tidak ada tugas
        await ctx.send(response)  # Mengirim daftar tugas

    # Memproses perintah yang tidak dikenal
    else:
        await ctx.send('Tindakan tidak dikenal. Silakan gunakan add, remove, atau list.')

# Perintah terpisah untuk menampilkan informasi bantuan
@bot.command()
async def info(ctx):
    response = (
        "Perintah yang tersedia:\n"
        "!task add [deskripsi tugas] - menambahkan tugas baru.\n"
        "!task remove [ID tugas] - menghapus tugas berdasarkan ID.\n"
        "!task list - menampilkan daftar tugas saat ini.\n"
        "!info - menampilkan informasi bantuan ini."
    )
    await ctx.send(response)  # Mengirim informasi bantuan

# Menjalankan bot dengan token Anda
bot.run(TOKEN)
