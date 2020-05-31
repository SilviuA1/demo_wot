import os
import select
from util import Util


class Stream:
    DEFAULT_FIFO_NAME = "/tmp/comm"
    TEMPORARY_RESPONSE_FIFO_NAME = "/tmp/comm_resp"

    def __init__(self):
        self.stop_threads = False
        self.sampler = select.poll()
        self.received_value = None
        self.endpoints = dict()

    def get_received_value(self):
        return self.received_value

    def register_pipe_polling(self, reader_endpoint):
        self.sampler.register(reader_endpoint, select.POLLIN)

    def unregister_pipe_polling(self, reader_endpoint):
        self.sampler.unregister(reader_endpoint)

    def listen_to_pipe_polling(self, reader_endpoint):
        try:
            while self.stop_threads is False:
                if (reader_endpoint, select.POLLIN) in self.sampler.poll(2000):
                    temp_value = Util.process_bytes(reader_endpoint)
                    print('Am primit: {0}'.format(temp_value))

                    self.received_value = temp_value
                    break

        except KeyboardInterrupt as kbd_ex:
            self.stop_threads = True
            print('Closing reader... ')

###################################################################
    def create_reader_pipe(self, pipe_name):
        Stream.create_pipe(pipe_name)
        reader_endpoint = Stream.connect_to_pipe(pipe_name, True)
        self.register_pipe_polling(reader_endpoint)
        if pipe_name not in self.endpoints.keys():
            self.endpoints[pipe_name] = dict()

        self.endpoints[pipe_name]['reader_endpoint'] = reader_endpoint
        return reader_endpoint

    def destroy_reader_pipe(self, pipe_name):
        if pipe_name in self.endpoints.keys():
            reader_endpoint = self.endpoints[pipe_name]['reader_endpoint']
            try:
                self.unregister_pipe_polling(reader_endpoint)
            finally:
                pass

            try:
                Stream.disconnect_pipe(reader_endpoint)
            finally:
                pass

            del self.endpoints[pipe_name]

        try:
            Stream.delete_pipe(pipe_name)
        finally:
            pass
###################################################################

    @staticmethod
    def create_pipe(pipe_name):
        os.mkfifo(path=pipe_name, mode=0o600)

    @staticmethod
    def connect_to_pipe(pipe_name, flag_read):
        if flag_read is True:
            reader_endpoint = os.open(pipe_name, os.O_RDONLY | os.O_NONBLOCK)
        else:
            reader_endpoint = os.open(pipe_name, os.O_WRONLY)

        return reader_endpoint

    @staticmethod
    def disconnect_pipe(reader_endpoint):
        os.close(reader_endpoint)

    @staticmethod
    def delete_pipe(pipe_name):
        os.remove(pipe_name)

    @staticmethod
    def write_to_pipe(fifo_writer, message):
        os.write(fifo_writer, message)

    def get_threads_stop_flag(self):
        return self.stop_threads

    def __del__(self):
        self.stop_threads = True
        self.sampler = None
