import socket
import threading
import queue

class ErrorLogger:
    _log_queue = queue.Queue()
    _server_address = "localhost"
    _port = 5000

    def __init__(self):
        threading.Thread(target=self._process_log_queue, daemon=True).start()

    def _process_log_queue(self):
        while True:
            log_message = self._log_queue.get()
            if log_message is None:
                break
            try:
                with socket.create_connection((self._server_address, self._port), timeout=5) as client:
                    client.sendall(log_message.encode('utf-8'))
            except (ConnectionRefusedError, socket.timeout) as ex:
                # Handle the case where the TCP receiver is offline
                print(f"Logging failed (TCP server offline): {ex}")
            except Exception as ex:
                print(f"Logging failed: {ex}")

    @staticmethod
    def send_error(error, script, context):
        message = f"\nError: {error}\nScript: {script}\nContext: {context}"
        ErrorLogger._log_queue.put(message)

    @staticmethod
    def send_debug(error, script, context):
        message = f"\nDebug: {error}\nScript: {script}\nContext: {context}"
        ErrorLogger._log_queue.put(message)
