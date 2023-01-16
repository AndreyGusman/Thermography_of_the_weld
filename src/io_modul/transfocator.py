from pymodbus.client.sync import ModbusTcpClient
# import time
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
            rr = client.read_holding_registers(0, length_read, unit=self.config.TRANSFOCATOR_SLAVE)
            # Start address to read from=0, length=64, Modbus slave ID
            print(rr.registers)
            return rr.registers

    def write(self, send):
        self.send = send

        client = ModbusTcpClient(host=self.config.TRANSFOCATOR_HOST, port=self.config.TRANSFOCATOR_PORT,
                                 unit_id=self.config.TRANSFOCATOR_SLAVE, auto_open=True, auto_close=True, timeout=10)
        while True:
            client.connect()
            # To Write values to multiple registers
            #     list = []
            #     for i in range(10):
            #         data = random.randint(25,35)
            #         list.append(data)
            wr = client.write_registers(14, dict, unit=self.config.TRANSFOCATOR_SLAVE)
            # Start address to read from=14, dict to write, Modbus slave unit ID

            print(wr)


if __name__ == '__main__':
    test = SettingCamera().read()
