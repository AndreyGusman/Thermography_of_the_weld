from pymodbus.client.sync import ModbusTcpClient
import random as rd
from src.config import Config
from src.data_format import DataFormat


class SettingCamera:

    def __init__(self):
        self.send = None
        self.config = Config()
        self.read_data = None

        self.transfocator_status = False

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

    def get_random_transfocator_data(self):
        self.read_data = {'ReqActualZoom+': rd.randint(1, 1000), 'ReqActualZoom-': rd.randint(1, 1000),
                          'ReqActualFocus+': rd.randint(1, 1000), 'ReqActualFocus-': rd.randint(1, 1000)}

    def get_transfocator_data(self):
        self.get_random_transfocator_data()
        transfocator_var_name = DataFormat.using_transfocator_var_name.copy()
        return {var_name: self.read_data.get(var_name) for var_name in transfocator_var_name}

    def get_transfocator_status(self):
        if rd.random() > 0.5:
            self.transfocator_status = not self.transfocator_status


if __name__ == '__main__':
    test = SettingCamera().read(), SettingCamera().write()
