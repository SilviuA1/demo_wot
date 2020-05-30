from stream import Stream
from threading import Thread


if __name__ == '__main__':
    FIFO_NAME = "/tmp/comm"
    reader_endpoint = None
    thing_reader_stream = Stream()
    try:
        try:
            Stream.create_pipe(FIFO_NAME)
            reader_endpoint = Stream.connect_to_pipe(FIFO_NAME, True)

            try:
                thing_reader_stream.register_pipe_polling(reader_endpoint)
                while thing_reader_stream.get_threads_stop_flag() is False:
                    print("Starting the listening Thread !")
                    listening_thread = Thread(target=thing_reader_stream.listen_to_pipe_polling(reader_endpoint))
                    listening_thread.daemon = True
                    listening_thread.start()
                    listening_thread.join()

            except KeyboardInterrupt as kbd_ex:
                pass

            finally:
                thing_reader_stream.unregister_pipe_polling(reader_endpoint)
        finally:
            Stream.disconnect_pipe(reader_endpoint)
    finally:
        Stream.delete_pipe(FIFO_NAME)
