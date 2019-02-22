import os

timestamp_image = input('Enter the path for the adjustment file: ')
file_timestamp = os.path.getmtime(timestamp_image)

image_timestamps = input('Input the timestamp from the image: ')
image_timestamps = float(image_timestamps)

difference = file_timestamp - image_timestamps

print(difference)
