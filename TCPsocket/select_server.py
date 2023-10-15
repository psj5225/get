import socket, select

sock_list = []
BUFFER = 1024
port = 2500
s_sock = socket.socket()
s_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s_sock.bind(('localhost',port))
s_sock.listen(5)
sock_list.append(s_sock) # 서버 소켓을 소켓 목록(sock_list)에 추가
print("Server waiting on port " + str(port))
while True:
    r_sock, w_sock, e_sock = select.select(sock_list, [],[]) # 읽기 이벤트 조사
    print(r_sock)
    for s in r_sock:
        if s == s_sock: # 서버에서 연결 이벤트 발생
            c_sock, addr = s_sock.accept()
            sock_list.append(c_sock) # 새로운 clinet 소켓 목록 추가
            print(" Client (%s, %s) connected" % addr)
        else: # 데이터 도착 이벤트
            try:
                data = s.recv(BUFFER) # client에서 읽기 이벤트
                print("Received: ",data.decode())
                if data:
                    s.send(data)
            except:
                print("Client (%s, %s) is offline" % addr)
                s.close()
                sock_list.remove(s) #연결 종료된 client 제거
        continue
s_sock.close()

