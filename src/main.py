from flask import Flask
from flask import abort, request
import datetime

import glob
import os
from threading import Thread

from stream import Stream
from util import Util

app = Flask(__name__)
application_stream = Stream()


def get_files_from_dir():
    files = glob.glob("./test_dir/*")
    response = []
    for file in files:
        response.append(os.path.basename(file))
    return response


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/api/directory/<fileName>', methods=['GET'])
def get_file_contents(fileName):
    response = get_files_from_dir()

    print(fileName)
    if fileName in response:
        file_to_read = open(glob.glob("./test_dir/" + fileName)[0])
        response = file_to_read.read()
        file_to_read.close()
    else:
        abort(404)
    print(response)
    return response


@app.route('/api/directory/<fileName>', methods=['PUT'])
def create_or_replace(fileName):
    files = get_files_from_dir()
    filename_path = ''

    if fileName in files:
        return "NOK", 204
    else:
        filename_path = './test_dir/' + fileName
        os.mknod(filename_path)

    return "File " + filename_path + " created", 201


@app.route('/api/directory/<fileName>', methods=['DELETE'])
def delete_file(fileName):
    files = get_files_from_dir()
    if fileName in files:
        file_with_path = './test_dir/' + fileName
        os.remove(file_with_path)
        return "OK", 200
    else:
        abort(404)


@app.route('/api/directory', methods=['POST'])
def post_data_to_dir():
    uniq_filename = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    file = './test_dir/' + uniq_filename
    print(file)
    data = request.get_data()
    print (data)

    if not data or len(data) == 0:
        return "No content", 204

    os.mknod(file)
    file = open(file, 'w+')
    file.write(data.decode('ascii'))
    file.close()
    return "OK"


@app.route('/api/directory', methods=['GET'])
def display_files():
    response = 'empty'
    try:
        reader_endpoint = application_stream.create_reader_pipe(Stream.TEMPORARY_RESPONSE_FIFO_NAME)

        listening_thread = Thread(target=application_stream.listen_to_pipe_polling, args=(reader_endpoint,))

        print("get thread started")

        listening_thread.daemon = True
        listening_thread.start()
        message = Util.create_get_msg(b"GET")
        writer_endpoint = application_stream.connect_to_pipe(Stream.DEFAULT_FIFO_NAME, False)
        Stream.write_to_pipe(writer_endpoint, message)

        listening_thread.join()
        response = application_stream.get_received_value()
        response = Util.decode_value(response)
    finally:
        application_stream.destroy_reader_pipe(Stream.TEMPORARY_RESPONSE_FIFO_NAME)

    return str(response)


if __name__ == "__main__":
    app.run()
