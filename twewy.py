import os, sys, struct, re

'''
regex table
r'([0-9A-F]{2,4})=(.+)'
'''

def invertTable(table):
    return dict([[i,j] for j,i in table.items()])

table = {
             b'\x00\x00': ' ', b'\x01\x00': '!', b'\x02\x00': '"', b'\x03\x00': '#', b'\x04\x00': '$',
             b'\x05\x00': '%', b'\x06\x00': '&', b'\x07\x00': "'", b'\x08\x00': '(', b'\x09\x00': ')',
             b'\x0B\x00': '+', b'\x0C\x00': ',', b'\x0D\x00': '-', b'\x0E\x00': '.', b'\x10\x00': '0',
             b'\x11\x00': '1', b'\x12\x00': '2', b'\x13\x00': '3', b'\x14\x00': '4', b'\x15\x00': '5',
             b'\x16\x00': '6', b'\x17\x00': '7', b'\x18\x00': '8', b'\x19\x00': '9', b'\x1A\x00': ':',
             b'\x1B\x00': ';', b'\x1D\x00': '=', b'\x1F\x00': '?', b'\x3E\x00': '^', b'\x20\x00': '@',
             
             b'\x21\x00': 'A', b'\x22\x00': 'B', b'\x23\x00': 'C', b'\x24\x00': 'D', b'\x25\x00': 'E',
             b'\x26\x00': 'F', b'\x27\x00': 'G', b'\x28\x00': 'H', b'\x29\x00': 'I', b'\x2A\x00': 'J',
             b'\x2B\x00': 'K', b'\x2C\x00': 'L', b'\x2D\x00': 'M', b'\x2E\x00': 'N', b'\x2F\x00': 'O',
             b'\x30\x00': 'P', b'\x31\x00': 'Q', b'\x32\x00': 'R', b'\x33\x00': 'S', b'\x34\x00': 'T',
             b'\x35\x00': 'U', b'\x36\x00': 'V', b'\x37\x00': 'W', b'\x38\x00': 'X', b'\x39\x00': 'Y',
             b'\x3A\x00': 'Z', b'\x41\x00': 'a', b'\x42\x00': 'b', b'\x43\x00': 'c', b'\x44\x00': 'd',
             b'\x45\x00': 'e', b'\x46\x00': 'f', b'\x47\x00': 'g', b'\x48\x00': 'h', b'\x49\x00': 'i',
             b'\x4A\x00': 'j', b'\x4B\x00': 'k', b'\x4C\x00': 'l', b'\x4D\x00': 'm', b'\x4E\x00': 'n',
             b'\x4F\x00': 'o', b'\x50\x00': 'p', b'\x51\x00': 'q', b'\x52\x00': 'r', b'\x53\x00': 's',
             b'\x54\x00': 't', b'\x55\x00': 'u', b'\x56\x00': 'v', b'\x57\x00': 'w', b'\x58\x00': 'x',
             b'\x59\x00': 'y', b'\x5A\x00': 'z',

             b'\x8D\x01': 'à', b'\x8E\x01': 'á', b'\x8F\x01': 'â', b'\x90\x01': 'ã',
             b'\x94\x01': 'ç', b'\x96\x01': 'é', b'\x97\x01': 'ê', b'\x9A\x01': 'í',
             b'\x9E\x01': 'ñ', b'\xA0\x01': 'ó', b'\xA1\x01': 'ô', b'\xA2\x01': 'õ',
             b'\xA7\x01': 'ú',

             b'\x6F\x01': 'À', b'\x6F\x01': 'Á', b'\x70\x01': 'Â', b'\x71\x01': 'Ã',
             b'\x75\x01': 'Ç', b'\x77\x01': 'É', b'\x78\x01': 'Ê', b'\x7B\x01': 'Í',
             b'\x81\x01': 'Ó', b'\x82\x01': 'Ô', b'\x83\x01': 'Õ', b'\x88\x01': 'Ú',

             b'\xFE\xFF': '\n'
        }

tags = {
    b'\xB6\xFF': '<blue>', b'\xBA\xFF': '<green>', b'\xBC\xFF': '<red>',
    b'\xBE\xFF': '<black>', b'\x1C\x01': '<->', 
    }

fileNames = {
	1:  'week3_01.txt', 2: 'week3_02.txt', 3: 'week3_03.txt', 4: 'week3_04.txt',
        5:  'week3_05.txt', 6: 'week3_06.txt', 7: 'week3_07.txt', 8: 'week3_extra.txt',
        9:  'week1_01.txt', 10: 'week1_02.txt', 11: 'week1_03.txt', 12: 'week1_04.txt',
        13: 'week1_05.txt', 14: 'week1_06.txt', 15: 'week1_07.txt', 16: 'week1_extra.txt',
        17: 'system_01.txt', 18: 'system_02.txt', 19: 'system_03.txt', 20: 'system_04.txt',
        21: 'system_05.txt', 22: 'system_06.txt', 23: 'system_07.txt', 24: 'system_08.txt',
        25: 'system_09.txt', 26: 'system_10.txt', 27: 'system_11.txt', 28: 'system_12.txt',
        29: 'another_day_01.txt', 30: 'another_day_02.txt', 31: 'another_day_03.txt',
        32: 'another_day_04.txt', 33: 'credits.txt', 34: 'week2_01.txt',
        35: 'week2_02.txt', 36: 'week2_03.txt', 37: 'week2_04.txt',
        38: 'week2_05.txt', 39: 'week2_06.txt', 40: 'week2_07.txt', 41: 'week2_extra.txt',
        42: 'thoughts.txt', 43: 'reaper_creeper.txt', 44: 'info.txt', 45: 'pork_city.txt'
	    }
	
fileParts = {
	1:  467, 2: 364, 3: 615, 4: 592, 5: 376, 6: 233, 7: 740, 8: 529, 9: 241,
	10: 652, 11: 793, 12: 581, 13: 322, 14: 535, 15: 197, 16: 1099,
        17: 267, 18: 592, 19: 373, 20: 609, 21: 608, 22: 219, 23: 713, 24: 438,
        25: 196, 26: 735, 27: 716, 28: 604, 29: 714, 30: 560, 31: 560, 32: 613,
        33: 1083, 34: 240, 35: 752, 36: 1020, 37: 1076, 38: 515, 39: 382,
        40: 199, 41: 636, 42: 1256, 43: 599, 44: 77, 45: 545
	    }

def extractText():
    
    mf = open('script/mestxt.bin', 'rb')
    pf = open('script/mestable.bin', 'rb')
    
    try: os.mkdir('en/')
    except: pass

    pointers = []
    text_size = []

    sections = int(201864/8) # 25233
    files = len(fileNames) + 1
        
    pf.close()

    for i in range(1, files):
        output = open("en/%s" % fileNames[i], "w")
        parts = fileParts[i]
        p = 0
        while p < parts:
            byte = mf.read(2)
            if byte == b'\xFF\xFF':
                output.write('\n--------------------\n')
                p += 1
            elif byte in tags:
                output.write(tags[byte])
            elif byte in table:
                output.write(table[byte])
            else:
                output.write("{%04X}" % struct.unpack('<H', byte)[0])
        output.close()
        
    mf.close()

def insertText():

    he  = r'(\{[A-F0-9]{4}\})'
    col = r'(<.+?>)'

    mf = open('new_mestxt.bin', 'wb')
    pf = open('new_mestable.bin', 'wb')
    
    txts = []
    sizes = []
    tabela = invertTable(table)
    itags = invertTable(tags)
    txt = bytes()
    
    for i, name in enumerate(os.listdir("br")):
        f = open("br/%s" % fileNames[i+1], "r")
        for line in f:
            line = line.strip('\x0D\x0A')
            if line == '--------------------':
                txts.append(txt[:-2] + b'\xFF\xFF')
                sizes.append(len(txt))
                txt = bytes()
            else:
                s_hex = re.split(he, line)
                for s in s_hex:
                    if s:
                        if re.match(he, s):
                            txt += struct.pack("<H", int(s[1:5], 16))
                        else:
                            s_col = re.split(col, s)
                            for c in s_col:
                                if c:
                                    if re.match(col, c):
                                        txt += itags[c]
                                    else:
                                        for p in c:
                                            txt += tabela[p]
                txt += b'\xFE\xFF'
        f.close()

    for t in txts:
        mf.write(t)
    mf.close()

    p = 0
    sections = int(201864/8)

    for i in range(sections):
        pf.write(struct.pack("<L", p))
        pf.write(struct.pack("<L", sizes[i]))
        p += sizes[i]

    pf.close()

    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-e':
            extractText()
            print ('Texto extraido')
        elif sys.argv[1] == '-i':
            insertText()
            print ('Texto inserido.')
    else:
        print ('TWEWY dumper/inserter by alizor\nusage: twewy.py command\n\n-e\textrair\n-i\tinserir')
        sys.exit(1)
