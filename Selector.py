import tkinter as tk
import discord
from discord.ext import commands
import threading
import keyboard
import asyncio
from pystray import Icon, Menu, MenuItem
from PIL import Image
import os


with open("resources\settings.txt", "r") as settings_file:
    settings = {}
    for line in settings_file:
        key, value = line.strip().split(":")
        settings[key.strip()] = value.strip()


bot_token = settings.get("bot_token", "YOUR_BOT_TOKEN")
channel_id = int(settings.get("channel_id", "YOU_CHANNEL_ID"))
hotkey = settings.get("key", "YOU_KEY")

intents = discord.Intents.default()
intents.messages = True  
bot = commands.Bot(command_prefix='!', intents=intents)


loop = None

def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    window.geometry(f"+{x}+{y}")

def show_commands_window():
    commands_window.deiconify()
    center_window(commands_window)

def hide_commands_window():
    commands_window.withdraw()

def on_f2_press(e):
    loop.call_soon_threadsafe(show_commands_window)

def on_f2_release(e):
    loop.call_soon_threadsafe(hide_commands_window)

def execute_command(command):
    if command == "stop_all":
        reset_button_colors()  
        
        print(f"Попытка поиска канала с ID {channel_id}")
        channel = bot.get_channel(channel_id)
        if channel:
            print(f"Канал найден: {channel.name}")
            try:
                asyncio.run_coroutine_threadsafe(channel.send(f"{command}"), loop)
                print(f"Сообщение успешно отправлено в канал {channel.name}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        else:
            print(f"Канал с ID {channel_id} не найден.")
    else:
       
        print(f"Попытка поиска канала с ID {channel_id}")
        channel = bot.get_channel(channel_id)
        if channel:
            print(f"Канал найден: {channel.name}")
            try:
                asyncio.run_coroutine_threadsafe(channel.send(f"{command}"), loop)
                print(f"Сообщение успешно отправлено в канал {channel.name}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        else:
            print(f"Канал с ID {channel_id} не найден.")


def bot_thread():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(bot.start(bot_token))
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(bot.logout())
        loop.close()


def on_exit(icon, item):
    icon.stop()
    os._exit(0)


def create_tray_icon():
    image = Image.open(r"resources\tornado.png")  
    menu = Menu(MenuItem('Завершить программу', on_exit))
    icon = Icon("DiscordSelector", image, "SelectorDiscord", menu)
    return icon


def run_tray_icon(icon):
    icon.run()



root = tk.Tk()
root.title("Main Window")

def update_commands_text():
    commands_text.delete(1.0, tk.END)
    commands_text.insert(tk.END, "Ваши команды здесь")

def reset_button_colors():
    for button in all_buttons:
        button.configure(bg="black")


def toggle_button_color(button):
    current_color = button.cget("bg")
    new_color = "green" if current_color == "black" else "black"
    button.configure(bg=new_color)


def create_buttons(parent_frame, command_list, row):
    buttons = []
    for command in command_list:
        button = tk.Button(parent_frame, text=command, command=lambda cmd=command: execute_command(cmd),
                           bg='black', fg='cyan', relief=tk.GROOVE, borderwidth=2, padx=10, pady=10, font=('Arial', 10),
                           bd=5, highlightthickness=0, activebackground='black', activeforeground='cyan')
        button.grid(row=row, column=command_list.index(command), sticky='nsew')
        button.bind("<Button-1>", lambda event, btn=button: toggle_button_color(btn))  # Привязываем функцию к событию нажатия кнопки
        buttons.append(button)
    return buttons


root.attributes('-alpha', 0.9)


def update_commands_text():
    commands_text.delete(1.0, tk.END)
    commands_text.insert(tk.END, "Ваши команды здесь")

commands_window = root
commands_window.title("Commands")
commands_window.protocol("WM_DELETE_WINDOW", lambda: None)
commands_window.withdraw()


commands_frame = tk.Frame(commands_window, bg='black')
commands_frame.pack()

acts_commands = ["mov", "vgaiky", "vportal", "tp", "inv", "blk" ]
maps_commands = ["stop_all", "start", "val", "fls", "getup", "aur"]
must_commands = ["hom", "esc", "ent", "tab", "rlg", "reset"]


acts_frame = tk.Frame(commands_frame, bg='black')
acts_frame.grid(row=0, column=0, pady=(0, 10))
acts_buttons = create_buttons(acts_frame, acts_commands, 0)

maps_frame = tk.Frame(commands_frame, bg='black')
maps_frame.grid(row=1, column=0, pady=(0, 10))
maps_buttons = create_buttons(maps_frame, maps_commands, 1)

must_frame = tk.Frame(commands_frame, bg='black')
must_frame.grid(row=2, column=0)
must_buttons = create_buttons(must_frame, must_commands, 2)


all_buttons = acts_buttons + maps_buttons + must_buttons

tray_icon_thread = threading.Thread(target=run_tray_icon, args=(create_tray_icon(),))
tray_icon_thread.start()


keyboard.on_press_key(hotkey, on_f2_press)
keyboard.on_release_key(hotkey, on_f2_release)

root.overrideredirect(True)
commands_window.overrideredirect(True)


bot_thread = threading.Thread(target=bot_thread)
bot_thread.start()


root.mainloop()
