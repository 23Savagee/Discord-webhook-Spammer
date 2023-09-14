import os
import ctypes
import aiohttp
import asyncio
import sys
import time
import threading
import curses
import random
import re
from discord_webhook import DiscordWebhook
from colorama import Fore, init, Style
import msvcrt

ctypes.windll.kernel32.SetConsoleTitleW("23Savage WebHook Spammer Tool | discord.gg/nixakanazis")

init()

class WebhookSender:
    def __init__(self, webhook: str, msg: str, tasks: int):
        self.clear = lambda: os.system("cls; clear")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47"}
        self.webhook = webhook
        self.payload = {"content": msg}
        self.tasks = tasks
        self.sent_webhooks = 0

    async def webhook_sender(self, session, webhook, amount):
        while self.sent_webhooks < self.tasks:
            async with session.post(webhook, json=self.payload) as s:
                if s.status in (200, 201, 204):
                    self.sent_webhooks += 1
                    sys.stdout.write(f"{Fore.GREEN}[+] Enviado webhook al canal con {amount} tareas en su payload.\n\n")
                else:
                    json = await s.json()
                    sys.stdout.write(
                        f"{Fore.RED}[!] Error al enviar el webhook con {amount} tareas en su payload.\n[!] Mensaje: {json['message']}\n[!] Reintentar después: {json['retry_after']}\n\n")

    async def start(self):
        self.clear()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = []
            for amount in range(self.tasks):
                if self.sent_webhooks < self.tasks:
                    task = asyncio.create_task(self.webhook_sender(session, self.webhook, amount))
                    tasks.append(task)
            await asyncio.gather(*tasks)
            tasks.clear()

should_stop = False

def WebHookSpammer():
    global should_stop
    url = input("\nWebhook URL>> ")
    
    if not is_valid_webhook(url):
        print(f"{Fore.RED}[!] URL de webhook no válida. Ingresa una URL válida.")
        time.sleep(2)  
        os.system("cls" if os.name == "nt" else "clear")
        return  
    
    message = input("Mensaje>> ")
    os.system("cls" if os.name == "nt" else "clear")  

    def send_webhook():
        while not should_stop:
            try:
                webhook = DiscordWebhook(url=url, content=message)
                response = webhook.execute()
                print(f"{Fore.GREEN}[+] Mensaje enviado: {message}")
            except Exception as error:
                print(f"{Fore.RED}[!] Error al enviar el webhook: {error}")

    num_threads = 4  
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=send_webhook)
        threads.append(thread)
        thread.start()

    user_input_thread = threading.Thread(target=read_user_input)
    user_input_thread.start()

    for thread in threads:
        thread.join()
    user_input_thread.join()

def read_user_input():
    global should_stop
    print(f"{Fore.RED}\n[!] Si deseas detener el WebHookSpammer Presiona 'q'")
    while True:
        char = msvcrt.getch()
        if char == b'q':
            should_stop = True
            break

def curses_animation():
    screen = curses.initscr()
    width = screen.getmaxyx()[1]
    height = screen.getmaxyx()[0]
    size = width * height
    char = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
    b = []

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, 0, 0)
    curses.init_pair(2, 1, 0)
    curses.init_pair(3, 3, 0)
    curses.init_pair(4, 4, 0)
    screen.clear
    for i in range(size + width + 1):
        b.append(0)

    start_time = time.time() 
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= 4: 
            break

        for i in range(int(width / 9)):
            b[int((random.random() * width) + width * (height - 1))] = 65
        for i in range(size):
            b[i] = int((b[i] + b[i + 1] + b[i + width] + b[i + width + 1]) / 4)
            color = (4 if b[i] > 15 else (3 if b[i] > 9 else (2 if b[i] > 4 else 1)))
            if i < size - 1:
                screen.addstr(int(i / width), i % width, char[(9 if b[i] > 9 else b[i])],
                              curses.color_pair(color) | curses.A_BOLD)

        screen.refresh()
        screen.timeout(30)
        if screen.getch() != -1:
            break

    curses.endwin()

def countdown():
    for i in range(3, 0, -1):
        print(f"{Fore.YELLOW}Cerrando en {i}...")
        time.sleep(1)
    curses_animation()

def is_valid_webhook(url):
    webhook_pattern = r'https://discord\.com/api/webhooks/\d+/\S+'
    return re.match(webhook_pattern, url) is not None

while True:
    print(f"""
{Fore.RED}                                  _______________ 
{Fore.RED}                                 < Hello, World! >
{Fore.RED}                                  --------------- 
{Fore.RED}                                         \   ^__^
{Fore.RED}                                          \  (oo)\_______
{Fore.RED}                                             (__)\       )\/\\
{Fore.RED}                                                 ||----w |
{Fore.RED}                                                 ||     ||
      
{Fore.RED}                                          By 23Savage | ilvvvx

{Fore.RED}                                        [1] Discord WebHook Sender
{Fore.RED}                                        [2] WebHook Spammer
{Fore.RED}                                        [3] Exit
""")
    
    choice = input("\n23savage@lypse:~$ ")

    if choice == '1':
        try:
            tasks_to_send = int(input("\nNúmero de tareas?: "))
            webhook_url = input("Webhook URL?: ")

            if not is_valid_webhook(webhook_url):
                print(f"{Fore.RED}[!] La URL de la webhook no es válida. Ingresa una URL válida.")
                time.sleep(3) 
                os.system("cls" if os.name == "nt" else "clear")
                continue

            message = input("Mensaje a enviar?: ")
            os.system("cls" if os.name == "nt" else "clear")
            
            client = WebhookSender(
                webhook=webhook_url,
                msg=message,
                tasks=tasks_to_send
            )
            start_time = time.time()
            asyncio.get_event_loop().run_until_complete(client.start())
            finish_time = round((time.time() - start_time), 4)
            sys.stdout.write(f"{Fore.GREEN}[+] Terminado el envío de webhook.\n[+] Terminado en {finish_time}s.\n\n")
            input(Fore.MAGENTA + "\nPresiona Enter para volver al menú..." + Style.RESET_ALL)
            os.system("cls" if os.name == "nt" else "clear")
        except Exception as error:
            sys.stdout.write(
                f"{Fore.RED}[!] El bucle de eventos ha terminado o estás siendo rate-limited o se te han dado roles inválidos.\n[!] Excepción: {error}\n[!] Presiona Enter para volver al menú...\n")
            input("-> ")
            os.system("cls" if os.name == "nt" else "clear")
    elif choice == '2':
        WebHookSpammer()
        input(Fore.MAGENTA + "\nPresiona Enter para volver al menú..." + Style.RESET_ALL)
        os.system("cls" if os.name == "nt" else "clear")
    elif choice == '3':
        countdown()
        sys.exit()
    else:
        print(f"{Fore.RED}[!] Opción no válida. Ingresa una opción válida (1, 2 o 3).")
        time.sleep(3) 
        os.system("cls" if os.name == "nt" else "clear")
