import sys
import socket
import threading
from PyQt5 import QtWidgets, QtGui

class ChatClient(QtWidgets.QMainWindow):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 600, 400)

        self.chat_display = QtWidgets.QTextEdit(self)
        self.chat_display.setGeometry(20, 20, 560, 300)
        self.chat_display.setReadOnly(True)

        self.message_input = QtWidgets.QLineEdit(self)
        self.message_input.setGeometry(20, 330, 460, 40)
        self.message_input.setPlaceholderText("Type your message here...")

        self.send_button = QtWidgets.QPushButton("Send", self)
        self.send_button.setGeometry(490, 330, 90, 40)
        self.send_button.clicked.connect(self.send_message)

        self.show()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.close()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_display.append(message)
            except:
                print("Connection closed.")
                self.client_socket.close()
                break

    def send_message(self):
        message = self.message_input.text()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.message_input.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client = ChatClient('127.0.0.1', 12345)
    client.connect_to_server()
    sys.exit(app.exec_())