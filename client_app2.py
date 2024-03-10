import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
import socket
import sys

# Client setup
HOST = '127.0.0.1'
PORT = 12345
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Setting up the GUI for the chat
class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatApp")

        self.chat_log = scrolledtext.ScrolledText(master, state='disabled')
        self.chat_log.grid(row=0, column=0, columnspan=3)

        # Print escape option at the beginning
        self.chat_log.insert(tk.END, "Press 'esc' to exit.\n\n")
        self.chat_log.yview(tk.END)

        self.msg_entry = tk.Entry(master)
        self.msg_entry.grid(row=1, column=0)

        self.send_button = tk.Button(master, text="Send", command=self.send_msg)
        self.send_button.grid(row=1, column=1)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_text)
        self.clear_button.grid(row=1, column=2)

        self.exit_button = tk.Button(master, text="Exit", command=self.show_exit_confirmation)
        self.exit_button.grid(row=1, column=3)

        self.receive_thread = Thread(target=self.receive_msg)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # Bind the escape key to exit the application
        self.master.bind('<Escape>', self.show_exit_confirmation)

    def send_msg(self):
        message = self.msg_entry.get()
        client.send(message.encode('utf-8'))
        self.msg_entry.delete(0, tk.END)

    def receive_msg(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    client.send(nickname.encode('utf-8'))
                else:
                    self.chat_log.config(state='normal')
                    self.chat_log.insert(tk.END, message + "\n")
                    self.chat_log.yview(tk.END)
                    self.chat_log.config(state='disabled')
            except:
                print("An error occurred!")
                client.close()
                break

    def show_exit_confirmation(self, event=None):
        # Show a messagebox to confirm exiting the application
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            client.close()
            sys.exit()

    def clear_text(self):
        # Clear the chat log
        self.chat_log.config(state='normal')
        self.chat_log.delete(1.0, tk.END)
        self.chat_log.config(state='disabled')

# Ask for the client's nickname
nickname = input("Choose your nickname: ")

root = tk.Tk()
gui = ClientGUI(root)
root.mainloop()


