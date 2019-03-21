from pyModbusTCP.client import ModbusClient
import threading
import time
from configs.commandConfig import COMMAND


class ModbusClass():
    def __init__(self, host, port):
        self.c = ModbusClient(host=host, port=port)
        self.registers = {i: 0 for i in range(10)}
        self.connectLock = threading.Lock()
        self.regiLock = threading.Lock()
        # count = 5
        if self.c.open():
            print("connect success")
        else:
            print("connect failed")

        print("start reading threading")
        readThread = threading.Thread(target=self.readFromSlaveLoop)
        readThread.start()

    def connection(f):
        def checkConnection(self, *args, **kwargs):
            while not self.c.is_open():
                self.connectLock.acquire()
                self.c.open()
                print("reconnecting")
                self.connectLock.release()
                if self.c.is_open():
                    print("reconnected")
                    break
                time.sleep(2)

            f(self)
        return checkConnection

    def readFromSlaveLoop(self):
        while True:
            self.readFromSlave()

    @connection
    def readFromSlave(self):
        
        self.regiLock.acquire()
        self.connectLock.acquire()
        if self.c.is_open():
            # print("reading...")
            tempR = self.registers
            try:
                t = self.c.read_holding_registers(0, 10)
                self.registers = {i: t[i] for i in range(0, len(t))}
                print(self.registers)
            except:
                self.registers = tempR
            # print("end reading")
        self.regiLock.release()
        self.connectLock.release()
        
        time.sleep(1)

    def writeToSlave(self, writeDict):
        self.connectLock.acquire()
        if self.c.is_open():
            for k, v in writeDict.items():
                self.c.write_single_register(k, v)
            print("write success")
            return True
        self.connectLock.release()
        return False

    # def getGoodsFromAGV(self, orderId):
    #     self.writeToSlave(self.addSerialNum(orderId, COMMAND['TakeGoodsToAGV']))

    # def takeGoodsToAGV(self, orderId):
    #     self.writeToSlave(self.addSerialNum(orderId, COMMAND['GetGoodsFromAGV']))

    def getRegisters(self):
        self.regiLock.acquire()
        temp = self.registers
        self.regiLock.release()
        for k, v in temp.items():
            temp[k] = "%04d" % int(v)
        return temp

    def addSerialNum(self, work_order, wDict):
        wDict[0] = ord(work_order[0])*10 + int(work_order[1])
        wDict[1] = int(work_order[2])*1000 + int(work_order[3])*100 + int(work_order[4])*10 + int(work_order[5])*1
        return wDict

    def reconnect(self):
        self.c.open()

