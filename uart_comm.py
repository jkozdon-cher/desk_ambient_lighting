import serial
import serial.tools.list_ports


class ComPort:
    @staticmethod
    def find_com_port(board_name='Urządzenie szeregowe USB'):
        # Arduino nano every board_name='CH340'
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if board_name in port[1]:
                return port[0]
            else:
                return None


class ArduinoSerial:
    @staticmethod
    def set_serial():
        com_port = ComPort.find_com_port()
        if com_port:
            return serial.Serial(com_port, 9600, timeout=0.01)

# arduino = ArduinoSerial.set_serial()