
from pymodbus.client.sync import ModbusTcpClient

from src.config import Config

toCamera = {'Zoom+': None, 'Zoom-': None, 'SetZoom': None, 'Focus+': None, 'Focus-': None, 'SetFocus': None,
            'DiagOFF': None, 'DiagON': None}

fromCamera = {'ReqActualZoom+': None, 'ReqActualZoom-': None, 'ReqActualFocus+': None, 'ReqActualFocus-': None}


class SettingCamera:

    def __init__(self):
        self.send = None
        self.config = Config()

    def read(self):
        length_read = 10
        client = ModbusTcpClient(host=self.config.TRANSFOCATOR_HOST, port=self.config.TRANSFOCATOR_PORT,
                                 unit_id=self.config.TRANSFOCATOR_SLAVE, auto_open=True, auto_close=True, timeout=10)

        while True:
            client.connect()

            # Start address to read from=0, length=64, Modbus slave ID
            response = client.read_holding_registers(1000, length_read, unit=self.config.TRANSFOCATOR_SLAVE)
            print(response.registers)
            return response.registers


    def write(self):

        client = ModbusTcpClient(host=self.config.TRANSFOCATOR_HOST, port=self.config.TRANSFOCATOR_PORT,
                                 unit_id=self.config.TRANSFOCATOR_SLAVE, auto_open=True, auto_close=True, timeout=10)
        while True:
            client.connect()

            # Start address to read from=14, List of booleans to write,Modbus slave unit ID
            request = client.write_registers(14, list, unit=self.config.TRANSFOCATOR_SLAVE)
            print(request)


if __name__ == '__main__':
    test = SettingCamera().read(), SettingCamera().write()

