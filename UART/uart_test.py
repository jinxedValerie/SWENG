'''# Bibliotheken laden
from machine import UART, Pin
from time import sleep

# UART0 initialisieren
uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
print('UART0:', uart0)
print()

# UART1 initialisieren
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), bits=8, parity=None, stop=1)
print('UART1:', uart1)
print()

# Daten zum Senden
txData = 'Hallo Welt'
print('Daten senden:', txData)

# Daten senden
uart0.write(txData)
sleep(1)

# Daten empfangen und ausgeben
rxData = uart1.readline()
print('Daten empfangen:', rxData.decode('utf-8'))
'''





from machine import UART, Pin
from time import sleep

uart1 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
uart2 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), bits=8, parity=None, stop=1)
message_out= ""
message_in= ""

#--------------check input--------------------
def type_input():
    print("what do you want to send? (No special Characters!)")
    type_input = input()
    return type_input


def key_input():
    print("what key do you want to use?")
    key_input_str = input()
    key_input = int(key_input_str)
    return key_input



#--------------calc new letter------------------
def new_letter_fn(letter, case_offset, key):                       #97 lower, 65 upper 
    letter_num = ord(letter) - case_offset
    new_num = ((letter_num + key) % 26) +case_offset
    new_letter = chr(new_num)
    return new_letter


#----------------Encoder-------------------------

def encoder(message_in, key):
    message = message_in
    new_word = ""
    for letter in message:
        if ord(letter)==32:             #Leerzeichen
             new_letter = " "
        elif letter.islower():
             new_letter= new_letter_fn(letter, 97, key)
        else:
             new_letter= new_letter_fn(letter,65, key)
        new_word += new_letter
    return new_word



#-----------------Decoder---------------------

def decoder(message_in, key):
    message = message_in
    new_word = ""
    key_rev= -1 * key
    for letter in message:
        if ord(letter)==32:             #Leerzeichen
             new_letter = " "
        elif letter.islower():
             new_letter= new_letter_fn(letter, 97, key_rev)
        else:
             new_letter= new_letter_fn(letter,65, key_rev)
        new_word += new_letter
    return new_word


#---------------send message---------------------

def send():
    key = key_input()
    message_text = encoder(type_input(), key)
    payload = f"{message_text};{key}\n"
    uart1.write(payload.encode('utf-8'))
    print("sending data...")
    

#---------------recieve message--------------------

def recieve():
    if uart2.any(): 
        raw_data = uart2.readline()
        if raw_data:
            decoded = raw_data.decode('utf-8').strip()
            message_parts = decoded.split(";")
            if len(message_parts) == 2:
                text = message_parts[0]
                key = int(message_parts[1])
                print("Message:", decoder(text, key))
            else:
                print("Received eroor data:", decoded)
    else:
        print("No data recieved.")

#------------main----------------

def main():
    send()
    sleep(1)
    recieve()

if __name__== "__main__":
    main()