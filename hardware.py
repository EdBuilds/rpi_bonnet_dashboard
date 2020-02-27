import board
from digitalio import DigitalInOut, Direction, Pull
import RPi.GPIO as GPIO

class buttons:

    def __init__(self):
        self.buttonpins = {
            "a": board.D5,
            "b": board.D6,
            "left": board.D27,
            "right": board.D23,
            "up": board.D17,
            "down": board.D22,
            "c": board.D4
        }
        self.buttons = {}
        for pin_key, pin_value in self.buttonpins.items():
            self.buttons[pin_key] = DigitalInOut(pin_value)
            self.buttons[pin_key].direction = Direction.INPUT
            self.buttons[pin_key].pull = Pull.UP

    def register_callback(self, button_name, callback_func):
        GPIO.add_event_detect(self.buttonpins[button_name].id, GPIO.FALLING,
                              callback=callback_func, bouncetime=300)
