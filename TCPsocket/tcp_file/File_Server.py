import socket
import sys

# 포트 번호 설정
port = 2600
# 서버 소켓 생성
s_sock = socket.socket()
host = ''
s_sock.bind((host,port))
s_sock.listen(1)

print("Waiting for Connection")
# 클라이언트 연결을 대기
c_sock, addr = s_sock.accept()
print("connection from", addr)

# 클라이언트로부터 메세지 수신 및 출력
msg = c_sock.recv(1024)
print(msg.decode())

# 클라이언트로부터 파일 이름 입력 받기
filename = input("파일 이름")
# 클라이언트에 파일 이름 전송
c_sock.send(filename.encode())
# 파일 열어서 전송
with open("./dummy/" + filename, 'rb') as f:
    # 파일을 클라이언트에게 전송
    c_sock.sendfile(f,0)

print('Sending complete')
c_sock.close()