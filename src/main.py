from flask import Flask
from flask import abort, request
from flask import jsonify

from flask_restful import Api
import resources

import glob
import os
from threading import Thread

from stream import Stream
from util import Util

app = Flask(__name__)
api = Api(app)

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


@app.route('/api/directory/<fileName>', methods=['DELETE'])
def delete_file(fileName):
    files = get_files_from_dir()
    if fileName in files:
        file_with_path = './test_dir/' + fileName
        os.remove(file_with_path)
        return "OK", 200
    else:
        abort(404)


@app.route('/api/directory/<sensorName>', methods=['PUT'])
def create_or_replace(sensorName):
    uniq_filename = sensorName+"_config"
    file = './test_dir/' + uniq_filename
    data = request.get_json()
    print(data)

    if not data or len(data) == 0:
        return "No content", 204

    if not os.path.exists(file):
        return "File does not exists", 400
    else:
        file = open(file, 'w')
        file.write(data['resolution'])
        file.close()

    return "OK"


@app.route('/api/directory/<sensorName>', methods=['POST'])
def post_data_to_dir(sensorName):
    uniq_filename = sensorName+"_config"
    file = './test_dir/' + uniq_filename
    data = request.get_json()
    print(data)

    if not data or len(data) == 0:
        return "No content", 204

    if os.path.exists(file):
        return "File already exists", 400
    else:
        os.mknod(file)
        file = open(file, 'w')
        file.write(data['resolution'])
        file.close()

    return_message = jsonify({'message': 'OK'})
    return return_message


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
