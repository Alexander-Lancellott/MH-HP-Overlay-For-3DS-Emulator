import struct
import random
import enum
import socket
import time
import psutil

# RPC protocol version spoken by this client. It is NOT fixed: negotiate_version() /
# connect_rpc() try the newest version first and keep the one that works for the session.
#   2 -> Azahar 2126.2 and newer (strict: any other version gets an empty reply)
#   1 -> older Azahar versions and Citra
CURRENT_REQUEST_VERSION = 2
SUPPORTED_REQUEST_VERSIONS = (2, 1)  # order matters: newest first
MAX_REQUEST_DATA_SIZE = 1024
MAX_PACKET_SIZE = 1024 + 0x10

PROBE_ADDRESS = 0x100000  # start of the game's code, readable as soon as a game is loaded
PROBE_TIMEOUT = 0.5  # seconds to wait for each version before trying the next one


class RequestType(enum.IntEnum):
    ReadMemory = 1,
    WriteMemory = 2,
    ProcessList = 3,
    SetGetProcess = 4,


CITRA_PORT = 45987


class Citra:
    def __init__(self, address="127.0.0.1", port=CITRA_PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address

    @staticmethod
    def is_connected():
        return any(conn.laddr.port == CITRA_PORT for conn in psutil.net_connections())

    @staticmethod
    def _generate_header(request_type, data_size):
        request_id = random.getrandbits(32)
        return (struct.pack("IIII", CURRENT_REQUEST_VERSION, request_id, request_type, data_size), request_id)

    @staticmethod
    def _read_and_validate_header(raw_reply, expected_id, expected_type):
        reply_version, reply_id, reply_type, reply_data_size = struct.unpack("IIII", raw_reply[:4*4])
        if (CURRENT_REQUEST_VERSION == reply_version and
            expected_id == reply_id and
            expected_type == reply_type and
            reply_data_size == len(raw_reply[4*4:])):
            return raw_reply[4*4:]
        return None

    def _probe_version(self, version):
        """
        Reads 4 bytes of game memory using the given protocol version.
        True only if the emulator answers with a valid reply carrying the data.
        """
        request_data = struct.pack("II", PROBE_ADDRESS, 4)
        request_id = random.getrandbits(32)
        request = struct.pack("IIII", version, request_id, RequestType.ReadMemory, len(request_data))
        request += request_data
        self.socket.sendto(request, (self.address, CITRA_PORT))

        deadline = time.monotonic() + PROBE_TIMEOUT
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False  # no answer (old emulators ignore unknown versions)
            self.socket.settimeout(remaining)
            try:
                raw_reply = self.socket.recv(MAX_PACKET_SIZE)
            except OSError:  # timeout, or "connection reset" when nothing listens on the port
                return False
            if len(raw_reply) < 4*4:
                continue
            reply_version, reply_id, reply_type, reply_data_size = struct.unpack("IIII", raw_reply[:4*4])
            if reply_id != request_id:
                continue  # late reply to an earlier probe, ignore it
            return (reply_version == version and
                    reply_type == RequestType.ReadMemory and
                    reply_data_size == 4 and
                    len(raw_reply) == 4*4 + 4)

    def negotiate_version(self):
        """
        Finds out which RPC protocol version the emulator understands.
        Version 2 is tried first, then version 1. The first one that works is kept
        (CURRENT_REQUEST_VERSION) and used for every later request in this session.
        Returns the version in use, or None if the emulator answers to none of them.
        """
        global CURRENT_REQUEST_VERSION
        previous_timeout = self.socket.gettimeout()
        try:
            for version in SUPPORTED_REQUEST_VERSIONS:
                if self._probe_version(version):
                    CURRENT_REQUEST_VERSION = version
                    return version
        finally:
            self.socket.settimeout(previous_timeout)
        CURRENT_REQUEST_VERSION = SUPPORTED_REQUEST_VERSIONS[0]
        return None

    def process_list(self):
        processes = {}
        read_processes = 0
        while True:
            request_data = struct.pack("II", read_processes, 0x7FFFFFFF)
            request, request_id = self._generate_header(RequestType.ProcessList, len(request_data))
            request += request_data
            self.socket.sendto(request, (self.address, CITRA_PORT))

            raw_reply = self.socket.recv(MAX_PACKET_SIZE)
            reply_data = self._read_and_validate_header(raw_reply, request_id, RequestType.ProcessList)

            if reply_data:
                read_count = struct.unpack("I", reply_data[0:4])[0]
                reply_data = reply_data[4:]
                if read_count == 0:
                    break
                read_processes += read_count
                for i in range(read_count):
                    proc_data = reply_data[i * 0x14: (i + 1) * 0x14]
                    proc_id, title_id, proc_name = struct.unpack("<IQ8s", proc_data)
                    proc_name = proc_name.rstrip(b"\x00").decode("ascii")
                    processes[proc_id] = (title_id, proc_name)
            else:
                break
        return processes

    def get_process(self):
        request_data = struct.pack("II", 0, 0)
        request, request_id = self._generate_header(RequestType.SetGetProcess, len(request_data))
        request += request_data
        self.socket.sendto(request, (self.address, CITRA_PORT))

        raw_reply = self.socket.recv(MAX_PACKET_SIZE)
        reply_data = self._read_and_validate_header(raw_reply, request_id, RequestType.SetGetProcess)

        if reply_data:
            return struct.unpack("I", reply_data)[0]
        else:
            return None

    def set_process(self, process_id):
        request_data = struct.pack("II", 1, process_id)
        request, request_id = self._generate_header(RequestType.SetGetProcess, len(request_data))
        request += request_data
        self.socket.sendto(request, (self.address, CITRA_PORT))

        self.socket.recv(MAX_PACKET_SIZE)

    def read_memory(self, read_address, read_size):
        result = bytes()
        while read_size > 0:
            temp_read_size = min(read_size, MAX_REQUEST_DATA_SIZE)
            request_data = struct.pack("II", read_address, temp_read_size)
            request, request_id = self._generate_header(RequestType.ReadMemory, len(request_data))
            request += request_data
            self.socket.sendto(request, (self.address, CITRA_PORT))

            raw_reply = self.socket.recv(MAX_PACKET_SIZE)
            reply_data = self._read_and_validate_header(raw_reply, request_id, RequestType.ReadMemory)

            if reply_data:
                result += reply_data
                read_size -= len(reply_data)
                read_address += len(reply_data)
            else:
                return None

        return result

    def write_memory(self, write_address, write_contents):
        """
        >>> c.write_memory(0x100000, b"\\xff\\xff\\xff\\xff")
        True
        >>> c.read_memory(0x100000, 4)
        b'\\xff\\xff\\xff\\xff'
        >>> c.write_memory(0x100000, b"\\x07\\x00\\x00\\xeb")
        True
        >>> c.read_memory(0x100000, 4)
        b'\\x07\\x00\\x00\\xeb'
        """
        write_size = len(write_contents)
        while write_size > 0:
            temp_write_size = min(write_size, MAX_REQUEST_DATA_SIZE - 8)
            request_data = struct.pack("II", write_address, temp_write_size)
            request_data += write_contents[:temp_write_size]
            request, request_id = self._generate_header(RequestType.WriteMemory, len(request_data))
            request += request_data
            self.socket.sendto(request, (self.address, CITRA_PORT))

            raw_reply = self.socket.recv(MAX_PACKET_SIZE)
            reply_data = self._read_and_validate_header(raw_reply, request_id, RequestType.WriteMemory)

            if None != reply_data:
                write_address += temp_write_size
                write_size -= temp_write_size
                write_contents = write_contents[temp_write_size:]
            else:
                return False
        return True


def connect_rpc():
    """
    Connects to the emulator's RPC server and picks the protocol version (2 first, then 1).
    Uses a throwaway socket, so the sockets used to read memory are not touched.
    Returns the version in use (2 or 1), or None if the server does not answer to either.
    """
    probe = Citra()
    try:
        return probe.negotiate_version()
    finally:
        probe.socket.close()


if "__main__" == __name__:
    import doctest
    doctest.testmod(extraglobs={'c': Citra()})
