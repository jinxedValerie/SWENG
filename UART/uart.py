from machine import UART, Pin, idle
import micropython

micropython.alloc_emergency_exception_buf(100)

TX_PIN = Pin(16)
RX_PIN = Pin(17)

BTN = Pin(15, Pin.IN, Pin.PULL_UP)

CON = UART(0, baudrate=9600, bits=8, parity=None, stop=2, rx=RX_PIN, tx=TX_PIN)


def caesar_cipher(input: str, shift: int) -> str:
    message = ""
    for c in input.upper():
        if not (ord("A") <= ord(c) <= ord("Z")):    # ignore special characters
            message += c
            continue
        message += chr(((ord(c) - ord("A") + shift) % 26) + ord("A"))
    return message

def send_message(_: Pin) -> None:
    MESSAGE = "HELLO WORLD!"
    sent_bytes = CON.write(MESSAGE)
    print(f"Sent message: {MESSAGE} ({sent_bytes})")

BTN.irq(handler=send_message, trigger=Pin.IRQ_FALLING, hard=False)

print("RUNNING")

while True:
    if CON.any():
        bytes = CON.read()
        assert bytes is not None

        message = bytes.decode() 
        print(message)

    idle()