import socket
import re
import logging
from typing import Tuple

class FTPClient:
    def __init__(self):
        self.control_sock = None
        self.data_sock = None
        self.logger = logging.getLogger(__name__)

    def connect(self, host: str, port: int = 21) -> bool:
        try:
            self.control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_sock.connect((host, port))
            response = self._receive_response()
            if not response.startswith('220'):
                raise Exception(f"Invalid welcome: {response}")
            return True
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            self.disconnect()
            return False

    def login(self, username: str, password: str) -> bool:
        try:
            self._send_command(f"USER {username}")
            user_response = self._receive_response()
            if "331" not in user_response:
                raise Exception(f"Username rejected: {user_response}")

            self._send_command(f"PASS {password}")
            pass_response = self._receive_response()
            if "230" not in pass_response:
                raise Exception(f"Password rejected: {pass_response}")

            # Set binary mode
            self._send_command("TYPE I")
            type_response = self._receive_response()
            if "200" not in type_response:
                raise Exception(f"Binary mode failed: {type_response}")

            return True
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False

    def _parse_pasv_response(self, response: str) -> Tuple[str, int]:
        match = re.search(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', response)
        if not match:
            raise Exception("Invalid PASV response format")
        
        ip = f"{match.group(1)}.{match.group(2)}.{match.group(3)}.{match.group(4)}"
        port = (int(match.group(5)) << 8 | int(match.group(6))
        return (ip, port)

    def download_file(self, remote_path: str, local_path: str) -> bool:
        try:
            # Enter passive mode
            self._send_command("PASV")
            pasv_response = self._receive_response()
            if "227" not in pasv_response:
                raise Exception(f"PASV failed: {pasv_response}")

            data_ip, data_port = self._parse_pasv_response(pasv_response)
            
            # Connect data channel
            self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_sock.connect((data_ip, data_port))

            # Send RETR command
            self._send_command(f"RETR {remote_path}")
            retr_response = self._receive_response()
            if "150" not in retr_response:
                raise Exception(f"RETR failed: {retr_response}")

            # Receive file data
            with open(local_path, 'wb') as f:
                while True:
                    data = self.data_sock.recv(4096)
                    if not data:
                        break
                    f.write(data)

            # Verify transfer complete
            transfer_response = self._receive_response()
            if "226" not in transfer_response:
                raise Exception(f"Transfer incomplete: {transfer_response}")

            return True
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            return False
        finally:
            if self.data_sock:
                self.data_sock.close()
                self.data_sock = None

    def list_files(self, path: str = "") -> list:
        try:
            # Enter passive mode
            self._send_command("PASV")
            pasv_response = self._receive_response()
            if "227" not in pasv_response:
                raise Exception(f"PASV failed: {pasv_response}")

            data_ip, data_port = self._parse_pasv_response(pasv_response)
            
            # Connect data channel
            self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_sock.connect((data_ip, data_port))

            # Send LIST command
            cmd = f"LIST {path}" if path else "LIST"
            self._send_command(cmd)
            list_response = self._receive_response()
            if "150" not in list_response:
                raise Exception(f"LIST failed: {list_response}")

            # Receive listing data
            listing = []
            while True:
                data = self.data_sock.recv(4096)
                if not data:
                    break
                listing.append(data.decode('utf-8'))

            # Verify transfer complete
            transfer_response = self._receive_response()
            if "226" not in transfer_response:
                raise Exception(f"Transfer incomplete: {transfer_response}")

            return ''.join(listing).splitlines()
        except Exception as e:
            self.logger.error(f"List failed: {e}")
            return []
        finally:
            if self.data_sock:
                self.data_sock.close()
                self.data_sock = None

    def disconnect(self):
        if self.control_sock:
            try:
                self._send_command("QUIT")
                self._receive_response()
            except:
                pass
            self.control_sock.close()
            self.control_sock = None

    def _send_command(self, command: str):
        self.control_sock.sendall(f"{command}\r\n".encode('utf-8'))

    def _receive_response(self) -> str:
        response = []
        while True:
            part = self.control_sock.recv(1024).decode('utf-8')
            response.append(part)
            if '\n' in part:
                break
        return ''.join(response)
