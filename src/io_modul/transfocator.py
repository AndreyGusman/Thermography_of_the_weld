from pymodbus.client.sync import ModbusTcpClient
import time
from src.config import Config

toTransfocator = {'Zoom+': None, 'Zoom-': None, 'SetZoom': None, 'Focus+': None, 'Focus-': None, 'SetFocus': None,
                  'DiagOFF': None, 'DiagON': None}

fromTransfocator = {'ReqActualZoom+': None, 'ReqActualZoom-': None, 'ReqActualFocus+': None, 'ReqActualFocus-': None}


class TransfocatorCamera:

    def __init__(self):
        self.config = Config()

    def read(self):
        length_read = 10
        client = ModbusTcpClient(host=self.config.TRANSFOCATOR_HOST, port=self.config.TRANSFOCATOR_PORT,
                                 unit_id=self.config.TRANSFOCATOR_SLAVE, auto_open=True, auto_close=True, timeout=10)

        while True:
            client.connect()
            rr = client.read_holding_registers(1000, length_read, unit=self.config.TRANSFOCATOR_SLAVE)
            # FUNCTIE 03 - Read register (Start address to read from=0, length=64, Modbus slave ID)
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
            wr = client.write_registers(14, list, unit=self.config.TRANSFOCATOR_SLAVE)
            # FUNCTIE 10 - (Write register) (Start address to read from=14, List of booleans to write,
            # Modbus slave unit ID)
            # write to multiple registers using list of data
            # wr = client.write_registers(1000,list,unit=1)
            print(wr)



if __name__ == '__main__':
    test = TransfocatorCamera().read(), TransfocatorCamera().write(toTransfocator)
