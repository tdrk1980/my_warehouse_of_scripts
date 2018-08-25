# *-* encoding: utf-8 *-*
from ctypes import Structure, LittleEndianStructure, BigEndianStructure, c_int8, c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_int64, c_uint64, c_float, c_double

# CANoe_FDX_Protocol_EN.pdf
# Manual CANoe FDX Protocol Version 2.0 English 
# 2.2.1  Datagram Header

# 43414e6f65464458020002000000000006000600010010000500020008000000000000000000
#   ↓
# 43414e6f65464458 0200 0200 00000000 0600060001001000 0500020008000000000000000000
s = "43414e6f65464458020002000000000006000600010010000500020008000000000000000000"
# 43414e6f65464458
# 02
# 00
# 0200
# 0000
# 00
# 00

# 0600
# 0600
# 0100
# 1000

# 0500020008000000000000000000

class DatagramHeader(LittleEndianStructure):
    _fields_ = [
        ("fdxSignature",     c_uint8 * 8),
        ("fdxMajorVersion",  c_uint8),
        ("fdxMinorVersion",  c_uint8),
        ("numberOfCommands", c_uint16),
        ("seqNrOrDgramLen",  c_uint16),
        ("fdxProtocolFlags", c_uint8),
        ("reserved",         c_uint8),
    ]

    def __new__(self, buf=None):
        if buf:
            return self.from_buffer_copy(buf)
        else:
            return super().__new__(self)

    def __init__(self, buf=None):
        if buf == None:
            self.fdxSignature     = (c_uint8 * 8)(0x43, 0x41, 0x4E, 0x6F, 0x65, 0x46, 0x44, 0x58) # b'CANoeFDX'
            self.fdxMajorVersion  = 2
            self.fdxMinorVersion  = 0
            self.numberOfCommands = 0
            self.seqNrOrDgramLen  = 0
            self.fdxProtocolFlags = 0x0 # b0:Byte Order, Little Endian (0)
            self.reserved         = 0
    
    def tobytes(self):
        return bytes(self)

class CommandHeader(LittleEndianStructure):
    _fields_ = [
        ("commandSize", c_uint16),
        ("commandCode", c_uint16),
    ]

    def __new__(self, buf=None):
        if buf:
            return self.from_buffer_copy(buf)
        else:
            return super().__new__(self)

    def __init__(self, buf=None):
        pass

    def tobytes(self):
        return bytes(self)

class CommandCode:
    Start               = 0x0001
    Stop                = 0x0002
    Key                 = 0x0003
    Status              = 0x004
    DataExchange        = 0x0005
    DataRequest         = 0x0006
    DataError           = 0x0007
    FreeRunningRequest  = 0x0008
    FreeRunningCancel   = 0x0009
    StatusRequest       = 0x000A
    SequenceNumberError = 0x000B
    HardwareChanged     = 0x0010
    IncrementTime       = 0x0011
    Custom              = 0x8000
    RT2RT_COM           = 0x8001

class Start(CommandHeader):
     def __init__(self, buf=None):
        if buf == None:
            self.commandSize = 4
            self.commandCode = CommandCode.Start

class Stop(CommandHeader):
     def __init__(self, buf=None):
        if buf == None:
            self.commandSize = 4
            self.commandCode = CommandCode.Stop

class Key(CommandHeader):
    _fields_ = [
        ("canoeKeyCode", c_uint32),
    ]

    def __init__(self, buf=None):
        if buf == None:
            self.commandSize = 8
            self.commandCode = CommandCode.Key
            self.canoeKeyCode = 0

class DataRequest(CommandHeader):
    _fields_ = [
        ("groupID", c_uint16),
    ]

    def __init__(self, buf=None):
        if buf == None:
            self.commandSize = 6
            self.commandCode = CommandCode.DataRequest
            self.groupID = 0

class DataExchange(CommandHeader):
    _fields_ = [
        ("groupID", c_uint16),
        ("dataSize", c_uint16),
        ("dataBytes", c_uint8),
    ]

    def __init__(self, buf=None):
        if buf == None:
            self.commandSize = 4
            self.commandCode = CommandCode.DataRequest
            self.groupID = 0

if __name__ == "__main__":
    a = DatagramHeader()
    print(f"{a.tobytes()}")

    a2 = DatagramHeader(b'MYOWNDAT\x02\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b')
    print(f"{a2.tobytes()}")

    b = CommandHeader()
    b.commandCode = CommandCode.RT2RT_COM
    print(f"{b.tobytes()}")

    b2 = CommandHeader(b'\xde\xad\xbe\xef')
    print(f"{b2.tobytes()}")
    print(f"{b2.commandCode:04x}")

    print(f"{a.tobytes() + b.tobytes()}")

    print(f"Start       : {Start().tobytes()}")
    print(f"Stop        : {Stop().tobytes()}")
    print(f"Key         : {Key().tobytes()}")
    print(f"DataRequest : {DataRequest().tobytes()}")

# さくっとbytearrayにいれてしまう。
# ↓ではmemoryview(a).tobytes()を使っている。
# https://qiita.com/pashango2/items/5075cb2d9248c7d3b5d4#memoryview%E3%81%A7bytes%E3%81%AB%E5%A4%89%E6%8F%9B


# C:\Users\Public\Documents\Vector\CANoe\Sample Configurations 11.0.42\IO_HIL\FDX
# C:\Users\Public\Documents\Vector\CANoe\Sample Configurations 11.0.42\IO_HIL\FDX\EasyClient

# >  int8   (1 Byte signed integer) 
# >  uint8   (1 Byte unsigned integer) 
# >  int16  (2 Byte signed integer) 
# >  uint16  (2 Byte unsigned integer) 
# >  int32  (4 Byte signed integer) 
# >  uint32  (4 Byte unsigned integer) 
# >  int64  (8 Byte signed integer) 
# >  uint64  (8 Byte unsigned integer) 
# >  float:   (4 Byte floating point) 
# >  double  (8 Byte floating point) 
# >  string:   (null terminated ASCII character string)
# >  bytearray   (sequence of individual data bytes) 
# >  floatarray   (sequence of 4 byte floating point numbers) 
# >  doublearray  (sequence of 8 byte floating point numbers) 
# >  int32array   (sequence of 4 byte signed integer numbers)