import sys
from scapy.all import *

# 패킷 캡처를 시작합니다.
# 인터페이스 이름을 실제로 사용하는 네트워크 인터페이스 이름으로 변경하세요.
print(conf.ifaces)
while True:
    sniff(iface="Software Loopback Interface 1",prn = lambda x:x.show())