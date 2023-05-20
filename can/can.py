#!/usr/bin/env python
# -*- coding: utf-8 -*-

from machine import Pin,SPI,PWM,I2C
import ssd1306
import time
import array
import rp2

NUM_LEDS = 10
LED_PIN = 0

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():    
  T1 = 2
  T2 = 5
  T3 = 3
  wrap_target()
  label("bitloop")
  out(x, 1) .side(0) [T3 - 1]
  jmp(not_x, "do_zero") .side(1) [T1 - 1]
  jmp("bitloop") .side(1) [T2 - 1]
  label("do_zero")
  nop() .side(0) [T2 - 1]
  wrap()
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(LED_PIN))
sm.active(1)
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def drawpix(num, r, g, b):
  ar[num] = g << 16 | r << 8 | b

def fill(r, g, b):
  for i in range(NUM_LEDS):
    drawpix(i, r, g, b)

## Configuration Registers */
CANSTAT      = 0x0E
CANCTRL      = 0x0F
BFPCTRL      = 0x0C
TEC          = 0x1C
REC          = 0x1D
CNF3         = 0x28
CNF2         = 0x29
CNF1         = 0x2A
CANINTE      = 0x2B
CANINTF      = 0x2C
EFLG         = 0x2D
TXRTSCTRL    = 0x0D

##  Recieve Filters */
RXF0SIDH     = 0x00
RXF0SIDL     = 0x01
RXF0EID8     = 0x02
RXF0EID0     = 0x03
RXF1SIDH     = 0x04
RXF1SIDL     = 0x05
RXF1EID8     = 0x06
RXF1EID0     = 0x07
RXF2SIDH     = 0x08
RXF2SIDL     = 0x09
RXF2EID8     = 0x0A
RXF2EID0     = 0x0B
RXF3SIDH     = 0x10
RXF3SIDL     = 0x11
RXF3EID8     = 0x12
RXF3EID0     = 0x13
RXF4SIDH     = 0x14
RXF4SIDL     = 0x15
RXF4EID8     = 0x16
RXF4EID0     = 0x17
RXF5SIDH     = 0x18
RXF5SIDL     = 0x19
RXF5EID8     = 0x1A
RXF5EID0     = 0x1B

## Receive Masks */
RXM0SIDH     = 0x20
RXM0SIDL     = 0x21
RXM0EID8     = 0x22
RXM0EID0     = 0x23
RXM1SIDH     = 0x24
RXM1SIDL     = 0x25
RXM1EID8     = 0x26
RXM1EID0     = 0x27

## Tx Buffer 0 */
TXB0CTRL     = 0x30
TXB0SIDH     = 0x31
TXB0SIDL     = 0x32
TXB0EID8     = 0x33
TXB0EID0     = 0x34
TXB0DLC      = 0x35
TXB0D0       = 0x36
TXB0D1       = 0x37
TXB0D2       = 0x38
TXB0D3       = 0x39
TXB0D4       = 0x3A
TXB0D5       = 0x3B
TXB0D6       = 0x3C
TXB0D7       = 0x3D

## Tx Buffer 1 */
TXB1CTRL     = 0x40
TXB1SIDH     = 0x41
TXB1SIDL     = 0x42
TXB1EID8     = 0x43
TXB1EID0     = 0x44
TXB1DLC      = 0x45
TXB1D0       = 0x46
TXB1D1       = 0x47
TXB1D2       = 0x48
TXB1D3       = 0x49
TXB1D4       = 0x4A
TXB1D5       = 0x4B
TXB1D6       = 0x4C
TXB1D7       = 0x4D

## Tx Buffer 2 */
TXB2CTRL     = 0x50
TXB2SIDH     = 0x51
TXB2SIDL     = 0x52
TXB2EID8     = 0x53
TXB2EID0     = 0x54
TXB2DLC      = 0x55
TXB2D0       = 0x56
TXB2D1       = 0x57
TXB2D2       = 0x58
TXB2D3       = 0x59
TXB2D4       = 0x5A
TXB2D5       = 0x5B
TXB2D6       = 0x5C
TXB2D7       = 0x5D

# ## Rx Buffer 0 */
RXB0CTRL     = 0x60
RXB0SIDH     = 0x61
RXB0SIDL     = 0x62
RXB0EID8     = 0x63
RXB0EID0     = 0x64
RXB0DLC      = 0x65
RXB0D0       = 0x66
RXB0D1       = 0x67
RXB0D2       = 0x68
RXB0D3       = 0x69
RXB0D4       = 0x6A
RXB0D5       = 0x6B
RXB0D6       = 0x6C
RXB0D7       = 0x6D

# ## Rx Buffer 1 */
RXB1CTRL     = 0x70
RXB1SIDH     = 0x71
RXB1SIDL     = 0x72
RXB1EID8     = 0x73
RXB1EID0     = 0x74
RXB1DLC      = 0x75
RXB1D0       = 0x76
RXB1D1       = 0x77
RXB1D2       = 0x78
RXB1D3       = 0x79
RXB1D4       = 0x7A
RXB1D5       = 0x7B
RXB1D6       = 0x7C
RXB1D7       = 0x7D


# ##******************************************************************
 # *               Bit register masks                                *
 # *******************************************************************/

# ## TXBnCTRL */
TXREQ        = 0x08
TXP          = 0x03

# ## RXBnCTRL */
RXM          = 0x60
BUKT         = 0x04

# ## CANCTRL */
REQOP        = 0xE0
ABAT         = 0x10
#define OSM          = 0x08
CLKEN        = 0x04
CLKPRE       = 0x03

# ## CANSTAT */
REQOP        = 0xE0
ICOD         = 0x0E

## CANINTE */
RX0IE        = 0x01
RX1IE        = 0x02
TX0IE        = 0x04
TX1IE        = 0x80
TX2IE        = 0x10
ERRIE        = 0x20
WAKIE        = 0x40
MERRE        = 0x80

# ## CANINTF */
RX0IF        = 0x01
RX1IF        = 0x02
TX0IF        = 0x04
TX1IF        = 0x80
TX2IF        = 0x10
ERRIF        = 0x20
WAKIF        = 0x40
MERRF        = 0x80

# ## BFPCTRL */
B1BFS        = 0x20
B0BFS        = 0x10
B1BFE        = 0x08
B0BFE        = 0x04
B1BFM        = 0x02
B0BFM        = 0x01

# ## CNF1 Masks */
SJW          = 0xC0
BRP          = 0x3F

# ## CNF2 Masks */
BTLMODE      = 0x80
SAM          = 0x40
PHSEG1       = 0x38
PRSEG        = 0x07

# ## CNF3 Masks */
WAKFIL       = 0x40
PHSEG2       = 0x07

# ## TXRTSCTRL Masks */
TXB2RTS      = 0x04
TXB1RTS      = 0x02
TXB0RTS      = 0x01


# ##******************************************************************
 # *                    Bit Timing Configuration                     *
 # *******************************************************************/
 
# ## CNF1 */
SJW_1TQ      = 0x40
SJW_2TQ      = 0x80
SJW_3TQ      = 0x90
SJW_4TQ      = 0xC0

# ## CNF2 */
BTLMODE_CNF3 = 0x80
BTLMODE_PH1_IPT  = 0x00

SMPL_3X      = 0x40
SMPL_1X      = 0x00

PHSEG1_8TQ   = 0x38
PHSEG1_7TQ   = 0x30
PHSEG1_6TQ   = 0x28
PHSEG1_5TQ   = 0x20
PHSEG1_4TQ   = 0x18
PHSEG1_3TQ   = 0x10
PHSEG1_2TQ   = 0x08
PHSEG1_1TQ   = 0x00

PRSEG_8TQ    = 0x07
PRSEG_7TQ    = 0x06
PRSEG_6TQ    = 0x05
PRSEG_5TQ    = 0x04
PRSEG_4TQ    = 0x03
PRSEG_3TQ    = 0x02
PRSEG_2TQ    = 0x01
PRSEG_1TQ    = 0x00

# ## CNF3 */
PHSEG2_8TQ   = 0x07
PHSEG2_7TQ   = 0x06
PHSEG2_6TQ   = 0x05
PHSEG2_5TQ   = 0x04
PHSEG2_4TQ   = 0x03
PHSEG2_3TQ   = 0x02
PHSEG2_2TQ   = 0x01
PHSEG2_1TQ   = 0x00

SOF_ENABLED  = 0x80
WAKFIL_ENABLED  =0x40
WAKFIL_DISABLED =0x00


# ##******************************************************************
 # *                  Control/Configuration Registers                *
 # *******************************************************************/

# ## CANINTE */
RX0IE_ENABLED= 0x01
RX0IE_DISABLED  =0x00
RX1IE_ENABLED =0x02
RX1IE_DISABLED  =0x00
G_RXIE_ENABLED  =0x03
G_RXIE_DISABLED =0x00

TX0IE_ENABLED= 0x04
TX0IE_DISABLED  =0x00
TX1IE_ENABLED =0x08
TX2IE_DISABLED  =0x00
TX2IE_ENABLED =0x10
TX2IE_DISABLED  =0x00
G_TXIE_ENABLED  =0x1C
G_TXIE_DISABLED =0x00

ERRIE_ENABLED= 0x20
ERRIE_DISABLED  =0x00
WAKIE_ENABLED= 0x40
WAKIE_DISABLED  =0x00
IVRE_ENABLED = 0x80
IVRE_DISABLED= 0x00

# ## CANINTF */
RX0IF_SET    = 0x01
RX0IF_RESET  = 0x00
RX1IF_SET    = 0x02
RX1IF_RESET  = 0x00
TX0IF_SET    = 0x04
TX0IF_RESET  = 0x00
TX1IF_SET    = 0x08
TX2IF_RESET  = 0x00
TX2IF_SET    = 0x10
TX2IF_RESET  = 0x00
ERRIF_SET    = 0x20
ERRIF_RESET  = 0x00
WAKIF_SET    = 0x40
WAKIF_RESET  = 0x00
IVRF_SET     = 0x80
IVRF_RESET   = 0x00

# ## CANCTRL */ 
REQOP_CONFIG = 0x80
REQOP_LISTEN = 0x60
REQOP_LOOPBACK  =0x40
REQOP_SLEEP  = 0x20
REQOP_NORMAL = 0x00

ABORT        = 0x10

OSM_ENABLED  = 0x08

CLKOUT_ENABLED  =0x04
CLKOUT_DISABLED =0x00
CLKOUT_PRE_8 = 0x03
CLKOUT_PRE_4 = 0x02
CLKOUT_PRE_2 = 0x01
CLKOUT_PRE_1 = 0x00

# ## CANSTAT */
OPMODE_CONFIG= 0x80
OPMODE_LISTEN= 0x60
OPMODE_LOOPBACK =0x40
OPMODE_SLEEP = 0x20
OPMODE_NORMAL= 0x00


# ## RXBnCTRL */
RXM_RCV_ALL  = 0x60
RXM_VALID_EXT= 0x40
RXM_VALID_STD= 0x20
RXM_VALID_ALL= 0x00

RXRTR_REMOTE = 0x08
RXRTR_NO_REMOTE =0x00

BUKT_ROLLOVER = 0x04
BUKT_NO_ROLLOVER =0x00

FILHIT0_FLTR_1  =0x01
FILHIT0_FLTR_0  =0x00

FILHIT1_FLTR_5  =0x05
FILHIT1_FLTR_4  =0x04
FILHIT1_FLTR_3  =0x03
FILHIT1_FLTR_2  =0x02
FILHIT1_FLTR_1  =0x01
FILHIT1_FLTR_0  =0x00


# ## TXBnCTRL */
TXREQ_SET    = 0x08
TXREQ_CLEAR  = 0x00

TXP_HIGHEST  = 0x03
TXP_INTER_HIGH  =0x02
TXP_INTER_LOW= 0x01
TXP_LOWEST   = 0x00
    

# ##******************************************************************
 # *                  Register Bit Masks                             *
 # *******************************************************************/
 
DLC_0       = 0x00
DLC_1       = 0x01
DLC_2       = 0x02
DLC_3       = 0x03
DLC_4       = 0x04
DLC_5       = 0x05
DLC_6       = 0x06
DLC_7       = 0x07    
DLC_8       = 0x08


# ##******************************************************************
 # *                  CAN spi commands                               *
 # *******************************************************************/

CAN_RESET    = 0xC0
CAN_READ     = 0x03
CAN_WRITE    = 0x02
CAN_RTS      = 0x80
CAN_RTS_TXB0 = 0x81
CAN_RTS_TXB1 = 0x82
CAN_RTS_TXB2 = 0x84
CAN_RD_STATUS= 0xA0
CAN_BIT_MODIFY  =0x05  
CAN_RX_STATUS= 0xB0
CAN_RD_RX_BUFF  =0x90
CAN_LOAD_TX  = 0x40  


# ##******************************************************************
 # *                  Miscellaneous                                  *
 # *******************************************************************/

DUMMY_BYTE   = 0x00
TXB0         = 0x31
TXB1         = 0x41
TXB2         = 0x51
RXB0         = 0x61
RXB1         = 0x71
EXIDE_SET    = 0x08
EXIDE_RESET  = 0x00
# #CS   PORTAbits.RA2

CAN_RATE = {
  "5KBPS"   : [0xA7, 0XBF, 0x07],
  "10KBPS"  : [0x31, 0XA4, 0X04],
  "20KBPS"  : [0x18, 0XA4, 0x04],
  "50KBPS"  : [0x09, 0XA4, 0x04],
  "100KBPS" : [0x04, 0x9E, 0x03],
  "125KBPS" : [0x03, 0x9E, 0x03],
  "250KBPS" : [0x01, 0x1E, 0x03],
  "500KBPS" : [0x00, 0x9E, 0x03],
  "800KBPS" : [0x00, 0x92, 0x02],
  "1000KBPS": [0x00, 0x82, 0x02],
}

gRXFlag=0
sRXFlag=0
yRXFlag=0
Com_RecBuff = [0, 0, 0, 0, 0, 0, 0, 0] #8
# data = 0

SPI0_CS1 = 1
SPI0_CS0 = 5

# debug = False
debug = True
class MCP2515():
    def __init__(self):
      self.spi = SPI(1)
      self.spi = SPI(0,10000_000,polarity=0, phase=0,sck=Pin(6),mosi=Pin(7),miso=Pin(4))
      self.cs = Pin(SPI0_CS0,Pin.OUT)
        
    def ReadByte(self, addr):
      self.cs(0)
      self.spi.write(bytearray([CAN_READ]))
      self.spi.write(bytearray([addr]))
      res = self.spi.read(1)
      self.cs(1)
      return int.from_bytes(res,'big')
    def WriteByte(self, addr):
      self.cs(0)
      self.spi.write(bytearray([addr]))
      self.cs(1)
    def WriteBytes(self, addr, data):
      self.cs(0)
      self.spi.write(bytearray([CAN_WRITE]))
      self.spi.write(bytearray([addr]))
      self.spi.write(bytearray([data]))
      self.cs(1)
    def Reset(self):
      self.cs(0)
      self.spi.write(bytearray([CAN_RESET])) #Reset 0XC0
      self.cs(1)
    
    def Init(self, speed="500KBPS"):
      print("Reset")
      self.Reset()
      time.sleep(0.1)
      
      #set baud rate 125Kbps
      #<7:6>SJW=00(1TQ)
      #<5:0>BRP=0x03(TQ=[2*(BRP+1)]/Fsoc=2*4/8M=1us)
      #<5:0>BRP=0x03 (TQ=[2*(BRP+1)]/Fsoc=2*8/16M=1us)
      # self.WriteBytes(CNF1, 7)        
      # self.WriteBytes(CNF2,0x80|PHSEG1_3TQ|PRSEG_1TQ)     
      # self.WriteBytes(CNF3,PHSEG2_3TQ)
      self.WriteBytes(CNF1, CAN_RATE[speed][0])
      self.WriteBytes(CNF2, CAN_RATE[speed][1])
      self.WriteBytes(CNF3, CAN_RATE[speed][2])

      print(CAN_RATE[speed])

      #set TXB0,TXB1
      #<15:5> SID 11bit canid
      #<BIT3> exide,1:extended 0:standard
      self.WriteBytes(TXB0SIDH,0xFF)
      self.WriteBytes(TXB0SIDL,0xE0)
      self.WriteBytes(TXB0DLC,0x40|DLC_8)
      # self.WriteBytes(TXB1SIDH,0x50)
      # self.WriteBytes(TXB1SIDL,0x00)
      # self.WriteBytes(TXB1DLC,0x40 | DLC_8)    #Set DLC = 3 bytes and RTR bit*/

      #Set RX
      self.WriteBytes(RXB0SIDH,0x00)
      self.WriteBytes(RXB0SIDL,0x60)
      self.WriteBytes(RXB0CTRL,0x60)
      self.WriteBytes(RXB0DLC, DLC_8)

      self.WriteBytes(RXF0SIDH,0xFF)
      self.WriteBytes(RXF0SIDL,0xE0)
      self.WriteBytes(RXM0SIDH,0xFF)
      self.WriteBytes(RXM0SIDL,0xE0)

      #can int
      self.WriteBytes(CANINTF,0x00)#clean interrupt flag
      self.WriteBytes(CANINTE,0x01)#Receive Buffer 0 Full Interrupt Enable Bit

      self.WriteBytes(CANCTRL, REQOP_NORMAL|CLKOUT_ENABLED)#

      dummy=self.ReadByte(CANSTAT)
      if( OPMODE_NORMAL != (dummy and 0xE0)):
        self.WriteBytes(CANCTRL, REQOP_NORMAL|CLKOUT_ENABLED)#set normal mode

    def Send(self, CAN_ID, CAN_TX_Buf, length1):
      tempdata = self.ReadByte(CAN_RD_STATUS)
      self.WriteBytes(TXB0SIDH, (CAN_ID>>3)&0XFF)
      self.WriteBytes(TXB0SIDL, (CAN_ID&0x07)<<5)
    
      self.WriteBytes(TXB0EID8, 0)
      self.WriteBytes(TXB0EID0, 0)
      self.WriteBytes(TXB0DLC, length1)
      for j in range(0, length1): 
        self.WriteBytes(TXB0D0+j,CAN_TX_Buf[j])

      if(tempdata&0x04):# TXREQ
        time.sleep(0.01)
        self.WriteBytes(TXB0CTRL, 0)#clean flag
        while(1):#wite 
          if(self.ReadByte(CAN_RD_STATUS)&0x04 != 1):
            break
      self.WriteByte(CAN_RTS_TXB0)
    
    def LockBuffer0(self, CAN_ID):
      print("LOCK Buffer0: " + str(CAN_ID))
      self.WriteBytes(RXM0SIDH, 0xFF)
      self.WriteBytes(RXM0SIDL, 0xFF)
      self.WriteBytes(RXF0SIDH, (CAN_ID>>3)&0xFF)
      self.WriteBytes(RXF0SIDL, (CAN_ID&0x07)<<5)

    def LockBUffer1(sef, CAN_ID):
      print("LOCK Buffer1: " + str(CAN_ID))
      self.WriteBytes(RXM1SIDH, 0xFF)
      self.WriteBytes(RXM1SIDL, 0xFF)
      self.WriteBytes(RXF1SIDH, (CAN_ID>>3)&0xFF)
      self.WriteBytes(RXF1SIDL, (CAN_ID&0x07)<<5)
    
    def Receive(self, CAN_ID):
      self.WriteBytes(RXB0SIDH, (CAN_ID>>3)&0XFF)
      self.WriteBytes(RXB0SIDL, (CAN_ID&0x07)<<5)
      CAN_RX_Buf = []
      while(1):
        if(self.ReadByte(CANINTF) & 0x01):
          len = self.ReadByte(RXB0DLC)
          print(len)
          for i in range(0, len): 
            CAN_RX_Buf.append(hex(self.ReadByte(RXB0D0+i)))
            # print(self.ReadByte(RXB0D0+i))
          break

      self.WriteBytes(CANINTF, 0)
      self.WriteBytes(CANINTE,0x01)#enable
      self.WriteBytes(RXB0SIDH,0x00)#clean
      self.WriteBytes(RXB0SIDL,0x60)
      return CAN_RX_Buf

    def Receive2(self):
      CAN_RX_Buf = []
      while(1):
        if (self.ReadByte(CANINTF) & 0x01):
          id_h = self.ReadByte(RXB0SIDH)
          id_l = self.ReadByte(RXB0SIDL)
          id = ((id_h << 3) | (id_l >> 5)) & 0x7FF
          if (id == 0x201) or (id == 0x420):
            len = self.ReadByte(RXB0DLC)
            for i in range(0, len):
              CAN_RX_Buf.append(hex(self.ReadByte(RXB0D0+i)))
            break
          self.WriteBytes(CANINTF, 0)
          self.WriteBytes(CANINTE, 0x01)

      self.WriteBytes(CANINTF, 0)
      self.WriteBytes(CANINTE,0x01)#enable
      return id, CAN_RX_Buf

    def read_rx(self):
      while(1):
        if (self.ReadByte(CANINTF) & 0x01):
          cmd = bytearray([0x90])
          data = bytearray(13)
          self.cs.value(0)
          self.spi.write(cmd)
          data = self.spi.read(13)
          self.WriteBytes(CANINTF, 0)
          self.cs.value(1)
          break

      can_id = ((data[1] << 3) | (data[2] >> 5)) & 0x7FF
      dlc = data[5] & 0x0F
      return (can_id, dlc, data[6:12])
    
i2c = I2C(0, sda=Pin(16), scl=Pin(17))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

def state0():
  fill(0, 0, 0)

def state1():
  state0()
  drawpix(0, 0, 200, 0)
  drawpix(9, 0, 200, 0)

def state2():
  state1()
  drawpix(1, 50, 200, 0)
  drawpix(8, 50, 200, 0)

def state3():
  state2()
  drawpix(2, 100, 200, 0)
  drawpix(7, 100, 200, 0)

def state4():
  state3()
  drawpix(3, 150, 200, 0)
  drawpix(6, 150, 200, 0)

def state5():
  state4()
  drawpix(4, 200, 200, 0)
  drawpix(5, 200, 200, 0)

def showState0():
  state0()
  sm.put(ar, 8)

def showState1():
  state1()
  sm.put(ar, 8)

def showState2():
  state2()
  sm.put(ar, 8)

def showState3():
  state3()
  sm.put(ar, 8)

def showState4():
  state4()
  sm.put(ar, 8)

def showState5():
  state5()
  sm.put(ar, 8)

def showState6():
  fill(200, 0, 0)
  sm.put(ar, 8)

def opening():
  interval = 0.1
  showState0()

  showState1()
  time.sleep(interval)

  showState2()
  time.sleep(interval)

  showState3()
  time.sleep(interval)

  showState4()
  time.sleep(interval)

  showState5()
  time.sleep(interval)

  showState4()
  time.sleep(interval)

  showState3()
  time.sleep(interval)

  showState2()
  time.sleep(interval)

  showState1()
  time.sleep(interval)

  showState0()

if __name__ == '__main__':
  print("--------------------------------------------------------")
  can = MCP2515()
  print("init...")
  can.Init()
  # id = 0x201 #max 7ff

  readbuf = []
  display.fill(0)
  display.text("CAN Monitor", 17, 2, True)
  display.text("RPM   : 0", 17, 17, True)
  display.text("W Temp: 0", 17, 34, True)
  display.show()

  # Opening
  time.sleep(1)
  opening()
  time.sleep(0.1)
  opening()

  can.Lock(513)

  temp = 0
  rpm = 0
  
  while(1):
    id, readbuf = can.Receive2()
    display.fill(0)
    if (id == 0x201):
      rpm = (int(readbuf[0]) * 256 + int(readbuf[1])) / 4
      print(rpm)
      if (rpm > 8800):
        showState6()
      elif (rpm > 8600):
        showState5()
      elif (rpm > 8400):
        showState4()
      elif (rpm > 8200):
        showState3()
      elif (rpm > 8000):
        showState2()
      elif (rpm > 7800):
        showState1()
      else:
        showState0()
    elif (id == 0x420):
      temp = int(readbuf[0]) - 40

    display.text("RPM   : " + str(rpm), 17, 17, True)
    display.text("W Temp: " + str(temp), 17, 34, True)

    display.show()

  print("--------------------------------------------------------")
