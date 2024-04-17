#!/usr/Justin Pommell/Downloads/networkFileRW.py
#networkFileRW.py
#Justin Pommell
#4/4/2024
#Update routers and switches;
#read equipment from a file, write updates & errors to file

# Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Error: Could not import the JSON module.")

# Create file constants for the file names; file constants can be reused
# There are 2 files to read this program: equip_r.txt and equip_s.txt
# There are 2 files to write in this program: updated.txt and errors.txt
EQUIP_R_FILE = "equip_r.txt"
EQUIP_S_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERRORS_FILE = "errors.txt"

# prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

# function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        # prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")

# function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount

def main():
    # open files here
    try:
        with open(EQUIP_R_FILE, 'r') as file:
            routers = json.load(file)
    except FileNotFoundError:
        print(f"Error: {EQUIP_R_FILE} not found.")
        return
    try:
        with open(EQUIP_S_FILE, 'r') as file:
            switches = json.load(file)
    except FileNotFoundError:
        print(f"Error: {EQUIP_S_FILE} not found.")
        return
    try:
        updated_file = open(UPDATED_FILE, 'w')
        errors_file = open(ERRORS_FILE, 'w')
    except IOError as e:
        print("Error: Could not open files for writing.")
        print(e)
        return

    # the updated dictionary holds the device name and new ip address
    updated = {}

    # list of bad addresses entered by the user
    invalidIPAddresses = []

    # accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    # flags and sentinels
    quitNow = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        # function call to get valid device
        device = getValidDevice(routers, switches)
        if device == 'x':
            quitNow = True
            break
        
        # function call to get valid IP address
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

        # update device
        if 'r' in device:
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        # add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    # user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    # write the updated equipment dictionary to a file
    json.dump(updated, updated_file)

    print(f"Updated equipment written to file '{UPDATED_FILE}'")
    print()
    print("Number of invalid addresses attempted:", invalidIPCount)

    # write the list of invalid addresses to a file
    for address in invalidIPAddresses:
        errors_file.write(address + '\n')

    print(f"List of invalid addresses written to file '{ERRORS_FILE}'")

    # close files
    updated_file.close()
    errors_file.close()

# top-level scope check
if __name__ == "__main__":
    main()
