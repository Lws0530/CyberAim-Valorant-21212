import time
import numpy as np
import socket
import threading


class Mouse:
    def __init__(self, config):
        self.com_type = config.com_type
        self.click_thread = threading.Thread(target=self.send_click)
        self.last_click_time = time.time()
        self.target_cps = 10
        self.lock = threading.Lock()

        self.symbols = '-,0123456789'
        self.code = 'cyberaim'
        self.encrypt = config.encrypt

        self.ip = config.ip
        self.port = config.port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.com_port = config.com_port
        self.board = None

        match self.com_type:
            case 'socket':
                print(f'Connecting to {self.ip}:{self.port}...')
                try:
                    self.client.connect((self.ip, self.port))
                    print('Socket connected')
                except Exception as e:
                    print(f'ERROR: Could not connect (Socket). {e}')
                    self.close_connection()

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        if self.com_type == 'socket':
            if self.client is not None:
                self.client.close()
        elif self.com_type == 'serial':
            if self.board is not None:
                self.board.close()

    def encrypt_command(self, command):
        if self.encrypt:
            encrypted_command = ""
            for char in command:
                if char in self.symbols:
                    index = self.symbols.index(char)
                    encrypted_command += self.code[index]
                else:
                    encrypted_command += char  # Keep non-symbol characters unchanged
            return encrypted_command
        else:
            return command

    def move(self, x, y):
        x = int(np.floor(x + 0.5))
        y = int(np.floor(y + 0.5))

        if x != 0 or y != 0:
            match self.com_type:
                case 'socket' | 'serial':
                    self.send_command(f'M{x},{y}\r')

    def click(self, delay_before_click=0):
        if (
                not self.click_thread.is_alive() and
                time.time() - self.last_click_time >= 1 / self.target_cps
        ):
            self.click_thread = threading.Thread(target=self.send_click, args=(delay_before_click,))
            self.click_thread.start()

    def send_click(self, delay_before_click=0):
        time.sleep(delay_before_click)
        self.last_click_time = time.time()
        match self.com_type:
            case 'socket' | 'serial':
                self.send_command('C\r')
        time.sleep((np.random.randint(10) + 25) / 1000)  # Sleep to avoid sending another click instantly after mouseup

    def send_command(self, command):
        command = self.encrypt_command(command)
        with self.lock:
            match self.com_type:
                case 'socket':
                    self.client.sendall(command.encode())
            print(f'Sent: {command}')
            print(f'Response from {self.com_type}: {self.get_response()}')

    def get_response(self):  # Waits for a response before sending a new instruction
        match self.com_type:
            case 'socket':
                return self.client.recv(4).decode()

