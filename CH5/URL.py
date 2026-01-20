import socket
import os

from Util import load

class URL:
    def __init__(self, url):
        # 로컬 파일 경로인지 확인
        if "://" not in url:
            self.is_file = True
            self.file_path = url
        else:
            self.is_file = False
            self.scheme, url = url.split("://", 1)
            assert self.scheme == "http"

            if "/" not in url:
                url = url + "/"

            self.host, url = url.split("/", 1)
            self.path = "/" + url
    
    def request(self):
        if self.is_file:
            # 로컬 파일 읽기
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            s = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP,
            )
            s.connect((self.host, 80))
            request = "GET {} HTTP/1.0\r\n".format(self.path)
            request += "Host: {}\r\n".format(self.host)
            request += "\r\n"
            s.send(request.encode("utf-8"))
            response = s.makefile("r", encoding="utf-8", newline="\r\n")
            statusline = response.readline()
            version, status, explanation = statusline.split(" ", 2)
            response_headers = {}
            while True:
                line = response.readline()
                if line == "\r\n": break
                header, value = line.split(":", 1)
                response_headers[header.casefold()] = value.strip()
            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers
            body = response.read()
            s.close()
            return body


if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))