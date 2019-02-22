import datetime

print('------ Photograph This timestamp ------')

while True:
    print(datetime.datetime.now().timestamp(), end='\r')