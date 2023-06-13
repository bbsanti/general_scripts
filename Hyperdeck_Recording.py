import telnetlib
import time
import datetime
#import keyboard

# define your host and port
HOST = input("Hyperdeck IP Address: ")
PORT = input("Hyperdeck Port: ")


while True:
    try:
        fileName = str(input("What would you like the file to be called (Date and Time are automatically added): "))
        interval = int(input('How many minutes to make each clip: '))
        mins = int(input('How many minutes would you like to record for: '))

    except ValueError:
        print('Please enter a number')
        continue
    break

print("\nto stop recording press ctrl+c\n")
# define your command and interval (in seconds)
# START_COMMAND = f"record: name: {filename_date_time}\n"
# STOP_COMMAND = "stop"
INTERVAL = int(interval)*60  # in seconds

class RecordingStoppedException(Exception):
    pass

# create a function that will connect to the telnet server and execute the command
def telnet_connect(host, port):

    # connect to the host
    try:
        tn = telnetlib.Telnet(host, port)
        tn.set_debuglevel(1)
        
        startTime = datetime.datetime.now()
        endTime = startTime + datetime.timedelta(minutes=mins)
        
        startTimeStr = startTime.strftime("%d.%m.%y_%H_%M_%S")
        endTimeStr = endTime.strftime("%d.%m.%y_%H_%M_%S")


        print("Time now: " + startTimeStr + "\nRecording will end at: " + endTimeStr)

        # set up a hotkey for 'ctrl + q' to raise an exception
        #keyboard.add_hotkey('ctrl + q', lambda: raise_exception())

        # send the command and print the result


        while datetime.datetime.now() <= endTime:
            now = datetime.datetime.now()
            filename_date_time = fileName +"_"+ now.strftime("%d.%m.%y_%H_%M_%S")
            start_command = f"record: name: {filename_date_time}\n"
            stop_command = "stop\n"

            deviceInfo = "device info\n"

           # tn.write(deviceInfo.encode('ascii'))

            tn.write(start_command.encode('ascii'))
            print("Connected successfully")
            print(f"Recording: {filename_date_time}")

            print("\nAfter start command: ")
            # Read and print Telnet output
            response = tn.read_very_eager().decode('ascii')
            print(response)

            time.sleep(INTERVAL)
            tn.write(stop_command.encode('ascii'))

            print("\nAfter stop command: ")
            # Read and print Telnet output
            response = tn.read_very_eager().decode('ascii')
            print(response)

        raise RecordingStoppedException("Recording time has exceeded the specified end time.")

    except (KeyboardInterrupt, RecordingStoppedException):
        tn.write(stop_command.encode('ascii'))
        tn.close()
        print(f"recording stopped")

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    # finally:
    #     tn.write(stop_command.encode('ascii'))
    #     tn.close()

# def raise_exception():
#     raise Exception('bye')


# call the function
telnet_connect(HOST, PORT)


#   pause for recording issues
#   when it asks how many hours