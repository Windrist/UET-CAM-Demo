from PyQt5.QtCore import QFileSelector
import snap7
import numpy as np

class PLC(object):

    def __init__(self):
        
        # Init Variables
        self.IP = '192.168.128.2'       # IP của PLC
        self.slot = 1                   # Lấy trong TIA Portal
        self.rack = 0                   # Lấy trong TIA Portal
        self.DBNumber = 1               # Data Block cần nhận dữ liệu (DB1, DB2,...)
        self.dataStart = 1              # Vị trí bit con trỏ nhận dữ liệu
        self.dataSize = 254             # Độ dài của data (1 byte, 4 bytes, 8 bytes,...)
        self.data = np.zeros(42)        # Biến truyền data cho PLC
    
    # Test Connection with PLC
    def testConnection(self):
        plc = snap7.client.Client()
        try:
            plc.connect(self.IP, self.rack, self.slot)
        except Exception as e:
            print("Connection Error!")
        finally:
            if plc.get_connected():
                plc.disconnect()
                print("Connection Success!")

    # Read Data Function
    def queryCommand(self):
        plc = snap7.client.Client()
        again = True
        while again:
            try:
                plc.connect(self.IP, self.rack, self.slot)
                data = plc.db_read(self.DBNumber, self.dataStart, self.dataSize)
                again = False
                return snap7.util.get_string(data, -1, 254)
            except Exception as e:
                print("Cannot Get Command! Error!")
            finally:
                if plc.get_connected():
                    plc.disconnect()

    def querySignal(self):
        plc = snap7.client.Client()
        again = True
        while again:
            try:
                plc.connect(self.IP, self.rack, self.slot)
                data = plc.db_read(self.DBNumber, 804, 1)
                again = False
                return snap7.util.get_bool(data, 0, 1)
            except Exception as e:
                print("Cannot Get Signal! Error!")
            finally:
                if plc.get_connected():
                    plc.disconnect()
    
    # Write Data Function
    def sendCommand(self, command):
        plc = snap7.client.Client()
        again = True
        while again:
            try:
                plc.connect(self.IP, self.rack, self.slot)
                data = plc.db_read(self.DBNumber, self.dataStart, self.dataSize)
                snap7.util.set_string(data, -1, command, self.dataSize)
                if not data.strip():
                    print("Command Corrupted!")
                    return
                plc.db_write(self.DBNumber, self.dataStart, data)
                # print("Command Write Successfully!")
                again = False
            except Exception as e:
                print("Cannot Send Command! Error!")
            finally:
                if plc.get_connected():
                    plc.disconnect()
    
    def sendData(self):
        plc = snap7.client.Client()
        again = True
        while again:
            try:
                plc.connect(self.IP, self.rack, self.slot)
                for i in range(42):
                    data = plc.db_read(self.DBNumber, 256+int(i/8), 1)
                    snap7.util.set_bool(data, 0, i%8, self.data[i])
                    plc.db_write(self.DBNumber, 256+int(i/8), data)
                # print("Data Write Successfully!")
                again = False
            except Exception as e:
                print("Cannot Send Data! Error!")
            finally:
                if plc.get_connected():
                    plc.disconnect()

    def sendTotal(self, total):
        plc = snap7.client.Client()
        again = True
        while again:
            try:
                plc.connect(self.IP, self.rack, self.slot)
                data = plc.db_read(self.DBNumber, 806, 1)
                snap7.util.set_int(data, 0, total)
                plc.db_write(self.DBNumber, 806, data)
                # print("Count Write Successfully!")
                again = False
            except Exception as e:
                print("Cannot Send Total! Error!")
            finally:
                if plc.get_connected():
                    plc.disconnect()
    
    def sendSignal(self, coord, signal):
        plc = snap7.client.Client()
        again = True
        while again:
            try:
                plc.connect(self.IP, self.rack, self.slot)
                data = plc.db_read(self.DBNumber, 804, 1)
                snap7.util.set_bool(data, 0, coord, signal)
                plc.db_write(self.DBNumber, 804, data)
                # print("Count Write Successfully!")
                again = False
            except Exception as e:
                print("Cannot Send Signal! Error!")
            finally:
                if plc.get_connected():
                    plc.disconnect()

if __name__ == "__main__":
    Controller = PLC()
    Controller.sendData()