from pynput.mouse import Button, Controller
mouse = Controller()
# read pointer position
print('the current pointer position is {0}'.format(mouse.position))

#set pointer position
mouse.position = (10,20)
print('Now we have moved it to {0}'.format(mouse.position))

#move pointer relative to current position'
mouse.move(5,-5)

#press and release
mouse.press(Button.left)
mouse.press(Button.left)

#double click this is different from pressing and releasing twice on macos
mouse.click(Button.left, 2)

#scroll two steps down
mouse.scroll(0,2)



from pynput import mouse
def on_move(x,y):
    print('Pointer moved to {0}'.format(
    (x,y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x,y)))
    if not pressed:
        #stop listener
    return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x,y)))
 
#collect events until Released
with mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll) as listener:
    listener.join()

#...or, in a non-blocking function
listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()

