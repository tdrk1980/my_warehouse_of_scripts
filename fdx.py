# *-* encoding: utf-8 *-*
from ctypes import Structure, c_int8, c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_int64, c_uint64

class Fdx(Structure):
    _fields_ = [
        ("ihl", c_uint8),
        ("ui16", c_uint16)
    ]


a = Fdx()
a.ihl = 100
print(f"{a.ihl}")
print(f"{a.ui16}")

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