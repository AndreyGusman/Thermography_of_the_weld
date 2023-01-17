from pymodbus.client.sync import ModbusTcpClient
from src.config import Config

sendPLC = {'W_Live_Bit': None, 'W_Emergency_Stop': None, 'W_Defect_bool': None, 'W_spare_04': None, 'W_spare_05': None,
           'W_spare_06': None, 'W_spare_07': None, 'W_spare_08': None, 'W_spare_09': None, 'W_spare_10': None,
           'W_spare_11': None, 'W_spare_12': None, 'W_spare_13': None, 'W_spare_14': None, 'W_spare_15': None,
           'W_spare_16': None, 'W_spare_17': None, 'W_spare_091': None, 'W_spare_0911': None, 'W_spare_0912': None,
           'W_Defect_dint': None, 'W_Temperature': None, 'W_Reserve1': None, 'W_Reserve22': None, 'W_Reserve3': None,
           'W_Reserve4': None, 'W_Reserve5': None, 'W_Reserve6': None}

fromPLC = {'Live_Bit': None, 'Emergency_Stop': None, 'TestRelease': None, 'SeamSkip': None, 'NoJob': None,
           'Stand_Perman_Perm': None, 'spare_01': None, 'spare_013': None, 'spare_02': None, 'spare_03': None,
           'spare_04': None, 'spare_05': None, 'spare_06': None, 'spare_07': None, 'spare_08': None, 'spare_09': None,
           'spare_091': None, 'spare_0911': None, 'spare_0912': None, 'Pos_UZK': None, 'RollersSpeedSet': None,
           'RollersSpeedAkt': None, 'Diam': None, 'Part_Coil_UZK': None, 'Part_Coil_TOS': None, 'Count_Pipe': None,
           'Num_Pipe': None, 'Length_Pipe': None, 'Pos_Begin_Cut': None, 'Num_Coil_UZK': None, 'Num_Coil_TOS': None,
           'Reserve1': None, 'Reserve2': None, 'Reserve3': None, 'Reserve4': None, 'Reserve5': None, 'Reserve6': None}


class Profibus:

    def __init__(self):
        self.toPLC = None
        self.config = Config()

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


if __name__ == '__main__':
    Profibus().read()
    Profibus().write()
