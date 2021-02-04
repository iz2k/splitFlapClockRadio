
from termcolor import colored

from splitFlapClockRadioBackend.clock.smbus430.smbusMsp430 import smbusMsp430
from splitFlapClockRadioBackend.tools.menuTools import doMenu


def main():
    # Create instance of msp430smbus
    smbus430=smbusMsp430()
    hhFlaps = smbus430.getFlapStatus('hh')
    print(hhFlaps)
    smbus430.setFlapParameter('hh', 'DESIRED_DIGIT', int(hhFlaps['CURRENT_DIGIT'])+1)
    hhFlaps = smbus430.getFlapStatus('hh')
    print(hhFlaps)

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

