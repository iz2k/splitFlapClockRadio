
from termcolor import colored

from splitFlapClockRadioBackend.clock.smbusMsp430 import smbusMsp430
from splitFlapClockRadioBackend.tools.menuTools import doMenu


def main():
    # Create instance of msp430smbus
    smbus430=smbusMsp430()

    menuItems = {
        'title' : '>> MAIN MENU',
        'options' : {
            '1' : {'descriptor' : 'MSP430 SMBUS', 'function' : smbus430.menu},
        }
    }

    # Loop on menu
    run=True
    while run:
        print(colored('____SPLIT-FLAP-CLOCK TESTING TOOL____', 'green'))
        run = doMenu(menuItems)



# If executed as main, call main
if __name__ == "__main__":
    main()

