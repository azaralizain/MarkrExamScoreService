# Markr Exam Score Service
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import xml.etree.ElementTree as ET
import numpy as np
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
        self.send_header("Content-type", "application/json")
        self.end_headers()
        split_url = self.path.split('/')
        test_id = split_url[2]
        print("test_id:" + test_id)
        sql_aggregate_Query = "select marks_obtained from db.StudentsMarks where test_id = '{}'".format(test_id)
        print("sql_aggregate_Query:" + sql_aggregate_Query)
        cursor.execute(sql_aggregate_Query)
        rv = cursor.fetchall()

        result_set = {"mean": np.mean(rv[0]), "count": len(rv),
                      "p25": np.percentile(rv[0], 25), "p50": np.percentile(rv[0], 50),
                      "p75": np.percentile(rv[0], 75)}

        # result_set = {"mean": np.mean(rv["marks_obtained"]), "count": rv.count(),
        #               "p25": np.percentile(rv["marks_obtained"], 25), "p50": np.percentile(rv["marks_obtained"], 50),
        #               "p75": np.percentile(rv["marks_obtained"], 75)}

        json_data = json.dumps(result_set)

        print("json: " + json_data)

        self.wfile.write(bytes(str(json.dumps(json_data)), "utf-8"))

        # self.wfile.write(bytes("<html><head><title>GET Method</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>in GET</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))

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
