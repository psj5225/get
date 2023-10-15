import threading

import cv2
import socket
from ui import VideoChatUI
import tkinter as tk
from PIL import Image, ImageTk


class VideoChatServer:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 서버")
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # 소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("",2600))
        self.server_socket.listen(5)

        # 클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 웹캠 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()



        # 서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        for client in self.clients:
            client.send(message.encode())
        # 서버 UI에도 메시지 표시
        self.ui.receive_message("서버: " + message)

    def send_message_to_server(self, message):
        self.ui.receive_message(message) # 서버에서 받은 메시지를 UI에 표시
        self.send_message_to_clients(message) # 받은 메시지를 다른 클라이언트들에게 전송

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            _, encoded_frame = cv2.imencode('.jpg', frame,
[int(cv2.IMWRITE_JPEG_QUALITY),60])
            encoded_frame = encoded_frame.tobytes()
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
            # 서버 UI에도 비디오 화면 표시
            self.show_frame(frame)

    def receive_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.daemon = True
            client_handler.start()

    def handle_client(self, client_socket):
        self.clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                self.send_message_to_server(message)  # 클라이언트에서 받은 메시지를 서버로 전송
            except:
                pass

if __name__ == "__main__":
    server = VideoChatServer

# 화면 갱신 함수
def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)

# 메시지 보내기 함수
def send_message():
    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

# GUI 초기화
window = tk.Tk()
window.title("화상 채팅")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

# 라벨 위젯을 사용하여 영상 표시 (80%)
label = tk.Label(window)
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 입력 필드 (20%)
entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 보내기 버튼 (20%)
send_button = tk.Button(window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# 행 및 열 가중치 설정
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

# 갱신 함수 호출
update()

# GUI 시작
window.mainloop()

# 웹캠 해제
cap.release()

