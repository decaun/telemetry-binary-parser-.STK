import struct,sys,csv
import numpy as np
import pandas as pd

TMP_LIST_CSV=r'C:\\temp\TLM_LIST.csv'
TELEMETRY=r'C:\temp\telemetry.bin'
OUTPUT=r'C:\\temp\STK.csv'

def parser(file,position,type):
    if type=='uint8':
        return np.uint8(struct.unpack('<I',file[int(position):int(position)+4]))[0]
    elif type=='uint16':
        return np.uint16(struct.unpack('<I',file[int(position):int(position)+4]))[0]
    elif type=='uint32':
        return np.uint32(struct.unpack('<I',file[int(position):int(position)+4]))[0]
    elif type=='int8':
        return np.int8(struct.unpack('<I',file[int(position):int(position)+4]))[0]
    elif type=='int16':
        return np.int16(struct.unpack('<I',file[int(position):int(position)+4]))[0]
    elif type=='int32':
        return np.int32(struct.unpack('<I',file[int(position):int(position)+4]))[0]
    else:
        return np.nan

if __name__=='__main__':
    df = pd.read_csv(TMP_LIST_CSV, delimiter=',')
    file = open(TELEMETRY, "rb")
    all = file.read()

    print("Total chunks of data: {}".format(len(all)/2068))
    
    for chunk in range(0,int((len(all)/2068))):
        current_chunk=all[0+int(chunk)*2068:2068+int(chunk)*2068]
        parsed_data=[]
        print("Parsing data chunk: {}".format(chunk))

        for byte,type in zip(df.Byte.values, df['Tlm Type'].values):
            try:
                parsed_data.append(parser(current_chunk,byte,type))
            except:
                parsed_data.append(np.nan)
        df['Data Chunk '+str(chunk)]=parsed_data

    print("Saving to Output file...")
    df.to_csv(OUTPUT, sep=',')