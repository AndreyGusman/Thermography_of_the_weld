from pymodbus.client.sync import ModbusTcpClient
import random as rd
from src.config import Config
from src.data_format import DataFormat


class Profibus:

    def __init__(self):
        self.toPLC = None
        self.config = Config()
        self.read_data = None

    def read(self):
        lengthRead = 10
        client = ModbusTcpClient(self.config.PROFIBUS_HOST, self.config.PROFIBUS_PORT, auto_open=True,
                                 auto_close=True, timeout=10)
        while True:
            client.connect()
            # Start address to read from=0, length=64, Modbus slave ID
            rr = client.read_holding_registers(1000, lengthRead, unit=self.config.PROFIBUS_SLAVE)
            print(rr.registers)

    def write(self):

        client = ModbusTcpClient(host=self.config.PROFIBUS_HOST, port=self.config.PROFIBUS_PORT,
                                 unit_id=self.config.PROFIBUS_SLAVE, auto_open=True, auto_close=True, timeout=10)
        while True:
            client.connect()
            # Start address to read from=14, List of booleans to write, Modbus slave unit ID
            wr = client.write_registers(14, self.toPLC, unit=self.config.PROFIBUS_SLAVE)
            print(wr)

    # пока нет оборудования, функции имитации

    def get_random_plc_data(self):
        self.read_data = {'Live_Bit': True if rd.random() > 0.5 else False,
                          'Emergency_Stop': True if rd.random() > 0.5 else False,
                          'TestRelease': True if rd.random() > 0.5 else False,
                          'SeamSkip': True if rd.random() > 0.5 else False,
                          'NoJob': True if rd.random() > 0.5 else False,
                          'Stand_Perman_Perm': True if rd.random() > 0.5 else False, 'spare_01': None,
                          'spare_013': None,
                          'spare_02': None, 'spare_03': None,
                          'spare_04': None, 'spare_05': None, 'spare_06': None, 'spare_07': None, 'spare_08': None,
                          'spare_09': None,
                          'spare_091': None, 'spare_0911': None, 'spare_0912': None, 'Pos_UZK': rd.randint(1, 1000),
                          'RollersSpeedSet': rd.randint(1, 1000),
                          'RollersSpeedAkt': rd.randint(1, 1000), 'Diam': rd.randint(1, 1000),
                          'Part_Coil_UZK': rd.randint(1, 1000), 'Part_Coil_TOS': rd.randint(1, 1000),
                          'Count_Pipe': rd.randint(1, 1000),
                          'Num_Pipe': rd.randint(1, 1000), 'Length_Pipe': rd.randint(1, 1000),
                          'Pos_Begin_Cut': rd.randint(1, 1000), 'Num_Coil_UZK': rd.randint(1, 1000),
                          'Num_Coil_TOS': rd.randint(1, 1000),
                          'Reserve1': None, 'Reserve2': None, 'Reserve3': None, 'Reserve4': None, 'Reserve5': None,
                          'Reserve6': None}

    def get_profibus_status(self):
        return self.read_data.get('Live_Bit')

    def get_plc_data(self):
        self.get_random_plc_data()
        plc_var_name = DataFormat.using_plc_var_name.copy()
        return {var_name: self.read_data.get(var_name) for var_name in plc_var_name}


if __name__ == '__main__':
    Profibus().read()
    Profibus().write()
