from termcolor import colored

def doMenu(menuItems):
    print(colored(menuItems['title'], 'yellow'))
    for option in menuItems['options']:
        print(colored(option + ' - ' + menuItems['options'][option]['descriptor'], 'cyan'))

    option = input()
    if option in menuItems['options']:
        return menuItems['options'][option]['function'](menuItems['title'])
    else:
        print('Invalid option')
        return True

def doReturn(preTitle):
    print(colored(preTitle + ' >> return', 'magenta'))
    return False


def getKeyFromDictionarySubitemName(myDict):
    print('Options:')
    for element in myDict:
        print(str(element) + ' - ' + myDict[element]['name'])
    print('Select:')
    key = input()
    if key not in myDict:
        print(colored('Invalid selection', 'red'))
        key = None
    return key

def getKeyFromDictionary(myDict):
    print('Options:')
    for element in myDict:
        print(element)
    print('Select:')
    key = input()
    if key not in myDict:
        print(colored('Invalid selection', 'red'))
        key = None
    return key


def select_value(element):
    if element['type'] == int:
        return getNewInt()
    if isinstance(element['type'],dict):
        return getContentFromDictionary(element['type'])
    if element['type'] == 'msp43xFwVersion':
        return getNewMsp43xFwVersion()

def getNewInt():
    print('Write new value:')
    try:
        return int(input())
    except:
        return None


def getContentFromDictionary(dictionary):
    print('Available options: ')
    for reg in dictionary:
        print(reg + " : " + dictionary[reg])

    print('Write new value:')
    key = input()
    if key not in dictionary:
        print(colored('Invalid selection', 'red'))
        key = None
    return key

def getNewMsp43xFwVersion():
    try:
        print('Write new major value:')
        major = int(input())
        print('Write new minor value:')
        minor = int(input())
        return ((major & 0xFF) << 8)  | (minor & 0xFF)
    except:
        print(colored('Invalid value', 'red'))
        return None


