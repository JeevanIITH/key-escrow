import ssl
import http.server

CERTFILE = 'cert.pem'

class MyServerHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            with open('index.html','rb') as data:
                self.wfile.write(data.read())
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            with open('404.html','rb') as data:
                self.wfile.write(data.read())

def main():
    https_server(certfile=CERTFILE)

def https_server(certfile):
    print("https_server() starts...")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile)

    server_address = ('127.0.0.1', 4000)
    with http.server.HTTPServer(server_address, MyServerHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print_server_info(httpd)
        try:
            httpd.serve_forever()
        except Exception as e:
            httpd.server_close()
            raise e


def print_server_info(server):
    print(f"""Server info:\nname: {server.server_name} \naddress: {server.server_address}""")


if __name__ == "__main__":
    main()