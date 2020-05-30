import os
import select
from util import Util


class Stream:
    def __init__(self):
        self.stop_threads = False
        self.sampler = select.poll()

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

        except KeyboardInterrupt as kbd_ex:
            self.stop_threads = True
            print('Closing reader... ')

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
