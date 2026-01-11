from machine import UART, Pin
from time import sleep

uart_connection = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1) # Initialize UART connection

#--------------check input--------------------

def message_input():
    """Prompts user for the message to encrypt"""

    type_input = input("what do you want to send?\n")
    return type_input


def key_input():
    """Prompts user for the shift key"""

    key_input_str = input("what key do you want to use?\n")
    key_input = int(key_input_str)
    return key_input


#----------------Ceasar Cipher-------------------------
def ceasar_cipher(message: str, key: int):
    """Encrypt message using a key with the ceasar cipher algorithm"""
    new_word = ""
    for char in message.upper():                        # shift one character at a time
        if not (ord("A") <= ord(char) <= ord("Z")):     # ignore special characters
            new_word += char
            continue
        num_ascii = ord(char) - ord("A")                # convert to alphabet index space
        new_num_ascii = (num_ascii + key) % 26          # shift and wrap around to stay within the normal alphabet
        new_char = chr(new_num_ascii + ord("A"))        # convert back to character from alphabet index space
        new_word += new_char
    return new_word


#----------------Ceasar Cipher Aliases-------------------------
def encrypt(message, key):
    return ceasar_cipher(message, key)

def decrypt(message, key):
    return ceasar_cipher(message, -key)     # Decrypting is just encrypting with the negative key


#------------------send message------------------

def send(key: int):
    """Gets input, encrypts it, and then send via UART"""

    payload = encrypt(message_input(), key)
    uart_connection.write(payload)
    print("sent data...")

#---------------recieve message--------------------
def recieve(key: int): 
    """Waits until a message gets recieved and then returns it"""

    print("Waiting...")
    while not uart_connection.any():    # Check if there is data in the buffer
        print("...")
        sleep(0.3)

    bytes = uart_connection.read()                          # Read the incoming data bytes
    assert bytes is not None                                # Appease the type-checker (and sanity check)
    encrypted_message = bytes.decode()                      # Decode bytes to a string (UTF-8 by default)
    decrypted_message = decrypt(encrypted_message, key)     # Decrypt the received string using the key

    return decrypted_message

#---------------------main-----------------
def main():
        user_choice= input("Do you want to send or recieve a message? \n" \
        "[1] Send \n[2] Recieve\n")     # Ask user for mode
        key = key_input()               # Get the secret key (must match on both devices)

        if user_choice == "1":
            send(key)
        elif user_choice == "2":
            recieved_message = recieve(key)
            print(recieved_message)

        else: 
            print("Not a valid choice!")    
        

if __name__== "__main__":
    main()      # could optionally also be wrapped in a while True loop to keep sending or recieving



