from machine import UART, Pin
from time import sleep

uart1 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
message_out= ""
message_in= ""

#--------------check input--------------------
def type_input():
    type_input = input("what do you want to send?\n")
    return type_input


def key_input():
    key_input_str = input("what key do you want to use?\n")
    key_input = int(key_input_str)
    return key_input


#----------------Encoder-------------------------

def encode(message, key):
    new_word = ""
    for char in message.upper():
        if not (ord("A") <= ord(char) <= ord("Z")):    # ignore special characters
            new_word += char
            continue
        num_ascii = ord(char) - ord("A")
        new_num_ascii = (num_ascii + key) % 26
        new_char = chr(new_num_ascii + ord("A"))
        new_word += new_char
    return new_word



#-----------------Decoder---------------------

def decode(message, key):
    return encode(message, -key)


#------------------send message------------------

def send(key: int):
    payload = encode(type_input(), key)
    uart1.write(payload)
    print("sent data...")

#---------------recieve message--------------------
def recieve(key: int): 
    print("Waiting...")
    while not uart1.any():
        print("...")
        sleep(0.3)
    bytes = uart1.read()
    assert bytes is not None
    encrypted_message = bytes.decode() 
    decrypted_message = decode(encrypted_message, key)
    print(decrypted_message)

#---------------------main-----------------
def main():
        user_choice= input("Do you want to send or recieve a message? \n" \
        "[1] Send \n[2] Recieve\n")
        key = key_input()
        if user_choice == "1":
            send(key)
        elif user_choice == "2":
            recieve(key)
        else: 
            print("Not a valid choice!")    
        

if __name__== "__main__":
    main()



