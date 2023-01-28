from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent
from time import sleep
from gpiozero import LED

CENTER_TOLERANCE = 350
STICK_MAX = 65536
led = LED(12) # GPIO 12

#On raspberrypi connected to xbox controller: list_devices()[0] = /dev/input/event8
xboxcontrol = InputDevice( list_devices()[0] )

axis = {
    ecodes.ABS_X: 'ls_x', # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt', # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x', # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

center = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

last = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

#evdev polls the xbox controller in a loop
for event in xboxcontrol.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == "BTN_A":
                print("Button A Pressed")
                led.on()
            elif keyevent.keycode[0] == "BTN_B":
                print("Button B Pressed")
                led.on()
            elif keyevent.keycode[0] == "BTN_WEST":
                print("Button Y Pressed")
                led.on()
                #calibrate zero on Y button
                center['ls_x'] = last['ls_x']
                center['ls_y'] = last['ls_y']
                center['rs_x'] = last['rs_x']
                center['rs_y'] = last['rs_y']
                print( 'calibrated' )
            elif keyevent.keycode[0] == "BTN_NORTH":
                print("Button X Pressed")
                led.on()
        if keyevent.keystate == KeyEvent.key_up:
            if keyevent.keycode[0] == "BTN_A":
                print("Button A Released")
                led.off()
            elif keyevent.keycode[0] == "BTN_B":
                print("Button B Released")
                led.off()
            elif keyevent.keycode[0] == "BTN_WEST":
                print("Button Y Released")
                led.off()
            elif keyevent.keycode[0] == "BTN_NORTH":
                print("Button X Released")
                led.off()
    elif event.type == ecodes.EV_ABS:
        if axis[ event.code ] in [ 'ls_x', 'ls_y', 'rs_x', 'rs_y' ]:
            last[ axis[ event.code ] ] = event.value

            value = event.value - center[ axis[ event.code ] ]

            if abs( value ) <= CENTER_TOLERANCE:
                value = 0

            if axis[ event.code ] == 'rs_x':
                if value < 0:
                    print('Stick Left')
                else:
                    print('Stick Right')
                print( value )

            elif axis[ event.code ] == 'ls_y':
                if value < 0:
                    print('Stick Forward')
                else:
                    print('Stick Backward')
                print( value )