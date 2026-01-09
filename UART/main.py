from machine import UART, Pin
from time import sleep

uart1 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
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
    key_input_raw = int(key_input_str)
    key_input= key_input_raw % 26
    return key_input



#--------------calc new letter------------------
def find_new_letter(letter, case_offset, key):                       #97 lower, 65 upper 
    letter_num = ord(letter) - case_offset
    new_num = ((letter_num + key) % 26) +case_offset
    new_letter = chr(new_num)
    return new_letter


#----------------Encoder-------------------------

def encoder(message, key):
    new_word = ""
    for letter in message:
        if ord(letter)==32:             #Leerzeichen
             new_letter = " "
        elif letter.islower():
             new_letter= find_new_letter(letter, 97, key)
        else:
             new_letter= find_new_letter(letter,65, key)
        new_word += new_letter
    return new_word



#-----------------Decoder---------------------

def decoder(message, key):
    return encoder(message, key *-1)


#------------------send message------------------

def send():
    key = key_input()
    message_text = encoder(type_input(), key)
    payload = f"{message_text};{key}\n"
    uart1.write(payload.encode('utf-8'))
    print("sending data...")

#---------------recieve message--------------------
def recieve(): 
    print("Waiting...")
    while not uart1.any():
        print("...")
        sleep(0.3)
    raw_data = uart1.readline()
    if raw_data:
        formatted = raw_data.decode('utf-8').strip()
        message_parts = formatted.split(";")
        if len(message_parts) == 2:
            text = message_parts[0]
            key = int(message_parts[1])
            print("Message:", decoder(text, key))
        else:
            print("Received eroor data:", formatted)
    



#---------------------main-----------------
def main():
        print("Do you want to send or recieve a message? \n" \
        "[1] Send \n[2] Recieve")
        user_choice= input()
        if user_choice == "1":
            send()
        elif user_choice == "2":
            recieve()
        else: print("Not a valid choice!")    
        


if __name__== "__main__":
    main()



