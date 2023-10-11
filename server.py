from http.server import BaseHTTPRequestHandler, HTTPServer
import serial

ser = serial.Serial('COM5',9600)

host_name = '127.0.0.1'  # IP Address of Raspberry Pi
host_port = 8000

class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <form action="/" method="POST">
               Move Robot :
               <input type="submit" name="submit" value="1">
               <input type="submit" name="submit" value="2">
                <input type="submit" name="submit" value="3">
               <input type="submit" name="submit" value="4">
           </form>
           </body>
           </html>
        '''
        self.do_HEAD()
        self.wfile.write(html.encode())

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]

        # print("Chair is moving {}".format(post_data))
        ser.write(post_data.encode())
        self._redirect('/')  # Redirect back to the root url

    # def connect():
    #     http_server = HTTPServer((host_name, host_port), MyServer)
    #     print("Server Starts - %s:%s" % (host_name, host_port))

    #     try:
    #         http_server.serve_forever()
    #     except KeyboardInterrupt:
    #         http_server.server_close()

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()