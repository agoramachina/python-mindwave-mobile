import time
import bluetooth
from mindwavemobile.MindwaveDataPoints import RawDataPoint
from mindwavemobile.MindwaveDataPoints import EEGPowersDataPoint
from mindwavemobile.MindwaveDataPoints import PoorSignalLevelDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import textwrap
import datetime
import time
import re
import csv

if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    if (mindwaveDataPointReader.isConnected()):    
	current_datetime = datetime.datetime.now().__str__()
	time_init = time.time()	
	data_row = []
	fields = ['Time', 'Poor Signal Level', 'Attention', 'Meditation', 'Delta', 'Theta', 'Low Alpha', 'High Alpha', 'Low Beta', 'High Beta', 'Low Gamma', 'Mid Gamma']
	with open("EEG_output.csv", "a") as f:
		writer = csv.writer(f)
		writer.writerow([current_datetime])
		writer.writerow(fields)
	i = 0
	
        while(True):
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (not dataPoint.__class__ is RawDataPoint):
		if (i is 1):
			if (dataPoint.__class__ is PoorSignalLevelDataPoint):
				data_row = []
				data_row.append("{0:.3f}".format(time.time() - time_init))

			data_cleaned = re.sub(r'[^\d\n]+', "", str(dataPoint))
			data_row.extend(data_cleaned.split())
			#data_cleaned = re.sub(r'[\n]+', ", ", data_cleaned)
		    	#print data_cleaned

		if (dataPoint.__class__ is EEGPowersDataPoint): 
			#print time.time() - time_init
			if (i is 1):			
				print data_row
				with open("EEG_output.csv", "a") as f:
					writer = csv.writer(f)
					writer.writerow(data_row)
			i = 1
    else:
        print(textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " "))
        
