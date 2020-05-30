from stream import Stream
from threading import Thread


if __name__ == '__main__':
    FIFO_NAME = "/tmp/comm"
    reader_endpoint = None
    thing_reader_stream = Stream()
    try:
        reader_endpoint = thing_reader_stream.create_reader_pipe(FIFO_NAME)

        try:
            while thing_reader_stream.get_threads_stop_flag() is False:
                print("Starting the listening Thread !")
                listening_thread = Thread(target=thing_reader_stream.listen_to_pipe_polling(reader_endpoint))
                listening_thread.daemon = True
                listening_thread.start()
                listening_thread.join()

        except KeyboardInterrupt as kbd_ex:
            pass

        finally:
            pass
    finally:
        thing_reader_stream.destroy_reader_pipe(FIFO_NAME)
