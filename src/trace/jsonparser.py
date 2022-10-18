import time
import json
  
f = open('data.json',)
data = json.load(f)
  
# Iterating through the json
for i in data['data']:
    output_list = [x['Time'] for x in data['data'] ]

for i in output_list:
    print('{:.4f}'.format(i/10))
    #print(time.strftime('%H:%M:%S', time.gmtime(i)))
  
f.close()
