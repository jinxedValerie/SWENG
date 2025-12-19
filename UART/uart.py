import machine
from machine import UART, Pin, idle
import micropython
from micropython import schedule
from time import ticks_ms, ticks_diff

micropython.alloc_emergency_exception_buf(100)

TX_PIN = Pin(16)
RX_PIN = Pin(17)

BTN = Pin(15, Pin.IN, Pin.PULL_DOWN)

CON = UART(0, baudrate=9600, bits=8, parity=None, stop=2, rx=RX_PIN, tx=TX_PIN)


# def read_transmission(rx: UART):
#     bytes = rx.read()

# def tx_detected():
#     schedule(handle_tx, None)

# con.irq(read_transmission, UART.IRQ_RXIDLE, False)

def send_message(_: None):
    MESSAGE = "HELLO WORLD"
    CON.write(MESSAGE)
    print(f"Sent message: {MESSAGE}")

DEBOUNCE_MARGIN = 100
last_button_press = ticks_ms()
def handle_button_press(pin: Pin):
    irq_state = machine.disable_irq()   # disable IRQs to prevent multiple repeated calls

    global last_button_press
    if (ticks_diff(ticks_ms(), last_button_press) > DEBOUNCE_MARGIN):
        last_button_press = ticks_ms()
        schedule(send_message, None)
        
    machine.enable_irq(irq_state)   # reenable IRQs

BTN.irq(handler=handle_button_press, trigger=Pin.IRQ_RISING, hard=False)

while True:
    if CON.any():
        bytes = CON.read()
        assert bytes is not None

        message = bytes.decode() 
        print(message)

    idle()