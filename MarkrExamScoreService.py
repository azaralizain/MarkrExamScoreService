# Markr Exam Score Service

from http.server import BaseHTTPRequestHandler, HTTPServer

import xml.etree.ElementTree as ET

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         database='db',
                                         user='user',
                                         password='password',
                                         port='3306')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL:", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

add_record = ("INSERT INTO StudentsMarks "
              "(student_number, test_id, marks_obtained, marks_total) "
              "VALUES (%s, %s, %s, %s)")


hostName = "localhost"
serverPort = 5000


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # sql_mean_Query = "select avg(marks_obtained) from StudentsMarks where test_id ="

        # records = cursor.fetchall()

        self.wfile.write(bytes("<html><head><title>GET Method</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>in GET</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        content = self.rfile.read(int(self.headers.get('content-length')))
        self.wfile.write(bytes("<HTML>POST OK.<BR>", "utf-8"))
        self.log_message('POST data: %s' % content)
        tree = ET.ElementTree(ET.fromstring(content))
        print(tree.findall("mcq-test-result"))
        for elem in tree.findall("mcq-test-result"):

            data_record = (elem.find("student-number").text, elem.find("test-id").text, elem.find("summary-marks").attrib["obtained"], elem.find("summary-marks").attrib["available"])
            print(data_record)

            cursor.execute(add_record, data_record)

        connection.commit()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
