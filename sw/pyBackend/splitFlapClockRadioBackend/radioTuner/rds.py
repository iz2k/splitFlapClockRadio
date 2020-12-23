from enum import Enum

class RDS:

    class GTYPES(Enum):
        STATION_NAME=0
        RADIO_TEXT=2

    class CHAR_ARRAY:
        def __init__(self, nchars):
            self.chars = [' '] * nchars
            self.string = ""

        def update_string(self):
            self.string = ''.join(self.chars)
            self.string = self.string.replace('  ', '').strip()

    def __init__(self):
            self.PS = self.CHAR_ARRAY(8)
            self.RadioTextA = self.CHAR_ARRAY(64)

    def reset(self):
            self.PS = self.CHAR_ARRAY(8)
            self.RadioTextA = self.CHAR_ARRAY(64)

    def process_rds_blocks(self, blockA, blockB, blockC, blockD):
        gtype=(blockB & 0xF000) >> 12
        b0=(blockB & 0x0800) >> 11
        tp=(blockB & 0x0400) >> 10
        pty=(blockB & 0x03E0) >> 5
        aux=(blockB & 0x001F)
        if gtype==self.GTYPES.STATION_NAME.value:
            ta=(aux & 0x10) >> 4
            ms=(aux & 0x08) >> 3
            di=(aux & 0x04) >> 2
            c=(aux & 0x03)
            self.PS.chars[2*c]=chr((blockD&0xFF00)>>8)
            self.PS.chars[2*c+1]=chr((blockD&0x00FF))
            self.PS.update_string()
        if gtype==self.GTYPES.RADIO_TEXT.value:
            ab=(aux & 0x10) >> 4
            c=(aux & 0x0F)
            self.RadioTextA.chars[4*c]=chr((blockC&0xFF00)>>8)
            self.RadioTextA.chars[4*c+1]=chr((blockC&0x00FF))
            self.RadioTextA.chars[4*c+2]=chr((blockD&0xFF00)>>8)
            self.RadioTextA.chars[4*c+3]=chr((blockD&0x00FF))
            self.RadioTextA.update_string()
        return gtype