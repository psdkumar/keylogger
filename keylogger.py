#!/usr/bin/python

import re
import threading
import time
import glob
import os

from Xlib import X, XK, display, error
from Xlib.ext import record
from Xlib.protocol import rq
from datetime import datetime


#######################################################################
########################START CLASS DEF################################
#######################################################################

class HookManager(threading.Thread):
    """This is the main class. Instantiate it, and you can hand it KeyDown and KeyUp (functions in your own code) which execute to parse the pyxhookkeyevent class that is returned.

    This simply takes these two values for now:
    KeyDown = The function to execute when a key is pressed, if it returns anything. It hands the function an argument that is the pyxhookkeyevent class.
    KeyUp = The function to execute when a key is released, if it returns anything. It hands the function an argument that is the pyxhookkeyevent class.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.finished = threading.Event()

        # Give these some initial values
        self.mouse_position_x = 0
        self.mouse_position_y = 0
        self.ison = {"shift":False, "caps":False}

        # Compile our regex statements.
        self.isshift = re.compile('^Shift')
        self.iscaps = re.compile('^Caps_Lock')
        self.shiftablechar = re.compile('^[a-z0-9]$|^minus$|^equal$|^bracketleft$|^bracketright$|^semicolon$|^backslash$|^apostrophe$|^comma$|^period$|^slash$|^grave$')
        self.logrelease = re.compile('.*')
        self.isspace = re.compile('^space$')

        # Assign default function actions (do nothing).
        self.KeyDown = lambda x: True
        self.KeyUp = lambda x: True

        self.contextEventMask = [X.KeyPress,X.MotionNotify]

        # Hook to our display.
        self.local_dpy = display.Display()
        self.record_dpy = display.Display()

        #initializing a dictionary for pressed keys
        self.Keys_down = {}
        self.Keys_down['Return'] = datetime.now()

        #last pressed and released buttons
        self.Last_pressed = ['Return' , datetime.now()]
        self.Last_released = ['' , datetime.now()]

        #boolean to know if its testing
        self.is_testing = False

    def run(self):
        # Check if the extension is present
        if not self.record_dpy.has_extension("RECORD"):
            #print "RECORD extension not found"
            sys.exit(1)
        r = self.record_dpy.record_get_version(0, 0)
        #print "RECORD extension version %d.%d" % (r.major_version, r.minor_version)

        # Create a recording context; we only want key and mouse events
        self.ctx = self.record_dpy.record_create_context(
                0,
                [record.AllClients],
                [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        'device_events': tuple(self.contextEventMask), #(X.KeyPress, X.ButtonPress),
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                }])

        # Enable the context; this only returns after a call to record_disable_context,
        # while calling the callback function in the meantime
        self.record_dpy.record_enable_context(self.ctx, self.processevents)
        # Finally free the context
        self.record_dpy.record_free_context(self.ctx)

    def cancel(self):
        self.finished.set()
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()

    def printevent(self, event):
        print event

    def HookKeyboard(self):
        pass
        # We don't need to do anything here anymore, since the default mask
        # is now set to contain X.KeyPress
        #self.contextEventMask[0] = X.KeyPress

    def processevents(self, reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print "* received swapped protocol data, cowardly ignored"
            return
        if not len(reply.data) or ord(reply.data[0]) < 2:
            # not an event
            return
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)
            if event.type == X.KeyPress:
                hookevent = self.keypressevent(event)
                self.KeyDown(hookevent)
            elif event.type == X.KeyRelease:
                hookevent = self.keyreleaseevent(event)
                self.KeyUp(hookevent)

    def keypressevent(self, event):
        matchto = self.lookup_keysym(self.local_dpy.keycode_to_keysym(event.detail, 0))
        if self.shiftablechar.match(self.lookup_keysym(self.local_dpy.keycode_to_keysym(event.detail, 0))): ## This is a character that can be typed.
            if self.ison["shift"] == False:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
                return self.makekeyhookevent(keysym, event)
            else:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 1)
                return self.makekeyhookevent(keysym, event)
        else: ## Not a typable character.
            keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
            if self.isshift.match(matchto):
                self.ison["shift"] = self.ison["shift"] + 1
            elif self.iscaps.match(matchto):
                if self.ison["caps"] == False:
                    self.ison["shift"] = self.ison["shift"] + 1
                    self.ison["caps"] = True
                if self.ison["caps"] == True:
                    self.ison["shift"] = self.ison["shift"] - 1
                    self.ison["caps"] = False
            return self.makekeyhookevent(keysym, event)

    def keyreleaseevent(self, event):
        if self.shiftablechar.match(self.lookup_keysym(self.local_dpy.keycode_to_keysym(event.detail, 0))):
            if self.ison["shift"] == False:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
            else:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 1)
        else:
            keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
        matchto = self.lookup_keysym(keysym)
        if self.isshift.match(matchto):
            self.ison["shift"] = self.ison["shift"] - 1
        return self.makekeyhookevent(keysym, event)

    # need the following because XK.keysym_to_string() only does printable chars
    # rather than being the correct inverse of XK.string_to_keysym()
    def lookup_keysym(self, keysym):
        for name in dir(XK):
            if name.startswith("XK_") and getattr(XK, name) == keysym:
                return name.lstrip("XK_")
        return "[%d]" % keysym

    def asciivalue(self, keysym):
        asciinum = XK.string_to_keysym(self.lookup_keysym(keysym))
        if asciinum < 256:
            return asciinum
        else:
            return 0

    def makekeyhookevent(self, keysym, event):
        timediff = None
        down_pair = []
        up_pair = []
        up_down_pair = []
        curr_time = datetime.now()
        key = str( self.lookup_keysym(keysym) )
        if event.type == X.KeyPress:
            MessageName = "key_down"
            if self.Last_pressed[0] != '' and (curr_time - self.Last_pressed[1]).total_seconds() < 3.5 :
                down_pair.append(self.Last_pressed[0] + '-' + key)
                down_pair.append( (curr_time - self.Last_pressed[1]).total_seconds() )
            if self.Last_released[0] != '' and (curr_time - self.Last_released[1]).total_seconds() < 2.5 :
                up_down_pair.append(self.Last_released[0] + '-' + key)
                up_down_pair.append( (curr_time - self.Last_released[1]).total_seconds() )
            self.Last_pressed[0] = key
            self.Last_pressed[1] = curr_time
            if key not in self.Keys_down :
                self.Keys_down[key] = curr_time

        elif event.type == X.KeyRelease:
            MessageName = "key_up"
            if self.Last_released[0] != '' and (curr_time - self.Last_released[1]).total_seconds() < 3.5 :
                up_pair.append(self.Last_released[0] + '-' + key)
                up_pair.append( (curr_time - self.Last_released[1]).total_seconds() )
            self.Last_released[0] = key
            self.Last_released[1] = curr_time
            if key in self.Keys_down :
                timediff = (curr_time - self.Keys_down[key]).total_seconds()
                del self.Keys_down[key]

        return pyxhookkeyevent(self.lookup_keysym(keysym), self.asciivalue(keysym), MessageName, timediff, down_pair, up_pair, up_down_pair, self.is_testing)

class pyxhookkeyevent:
    """This is the class that is returned with each key event.f
    It simply creates the variables below in the class.

    Window = The handle of the window.
    WindowName = The name of the window.
    WindowProcName = The backend process for the window.
    Key = The key pressed, shifted to the correct caps value.
    Ascii = An ascii representation of the key. It returns 0 if the ascii value is not between 31 and 256.
    KeyID = This is just False for now. Under windows, it is the Virtual Key Code, but that's a windows-only thing.
    ScanCode = Please don't use this. It differs for pretty much every type of keyboard. X11 abstracts this information anyway.
    MessageName = "key down", "key up".
    """

    def __init__(self, Key, Ascii, MessageName, Timediff, Down_pair, Up_pair ,Up_Down_pair, Is_testing):
        self.Key = Key
        self.Ascii = Ascii
        self.MessageName = MessageName
        self.Timediff = Timediff
        self.Down_pair = Down_pair
        self.Up_pair = Up_pair
        self.Up_Down_pair = Up_Down_pair
        self.Is_testing = Is_testing
    def __str__(self):
        curr_time = datetime.now()
        self.log = str(curr_time) + "\t" + str(self.Ascii) + "\t" + str(self.Key) + "\t" + str(self.MessageName) + "\n"
        if self.Is_testing == True :
            head = "Testing/"
        else :
            head = ""
        self.write_data(head)
        return self.log
    def write_data(self, head) :
        with open(head+"Logs.txt", "a") as myfile:
            myfile.write(self.log)
        if self.Timediff is not None:
            with open(head+"Primary_features/"+str(self.Key)+".txt", "a") as myfile:
                myfile.write(str(self.Timediff)+ "\n" )
        if self.Down_pair != [] :
            with open(head+"Secondary_features_down/"+str(self.Down_pair[0])+".txt", "a") as myfile:
                myfile.write(str(self.Down_pair[1])+ "\n" )
        if self.Up_pair != [] :
            with open(head+"Secondary_features_up/"+str(self.Up_pair[0])+".txt", "a") as myfile:
                myfile.write(str(self.Up_pair[1])+ "\n" )
        if self.Up_Down_pair != [] :
            with open(head+"Teritiary_features/"+str(self.Up_Down_pair[0])+".txt", "a") as myfile:
                myfile.write(str(self.Up_Down_pair[1])+ "\n" )

class pyxhookmouseevent:
    """This is the class that is returned with each key event.f
    It simply creates the variables below in the class.

    Window = The handle of the window.
    WindowName = The name of the window.
    WindowProcName = The backend process for the window.
    Position = 2-tuple (x,y) coordinates of the mouse click
    MessageName = "mouse left|right|middle down", "mouse left|right|middle up".
    """

    def __init__(self, Window, WindowName, WindowProcName, Position, MessageName):
        self.Window = Window
        self.WindowName = WindowName
        self.WindowProcName = WindowProcName
        self.Position = Position
        self.MessageName = MessageName

    def __str__(self):
        return "Window Handle: " + str(self.Window) + "\nWindow Name: " + str(self.WindowName) + "\nWindow's Process Name: " + str(self.WindowProcName) + "\nPosition: " + str(self.Position) + "\nMessageName: " + str(self.MessageName) + "\n"

#######################################################################
#########################END CLASS DEF#################################
#######################################################################

def clear_testing_content() :
    base_directory = os.getcwd()+"/"
    folder_name = "Testing/"
    directories = ["Primary_features/", "Secondary_features_down/", "Secondary_features_up/", "Teritiary_features/"]
    for directory in directories :
        os.chdir(base_directory+folder_name+directory)
        filelist = glob.glob("*.txt")
        for f in filelist:
            os.remove(f)
    os.chdir(base_directory)

def start_keylogger(seconds) :
    hm = HookManager()
    if seconds != -1 :
        hm.is_testing = True
        clear_testing_content()
    hm.HookKeyboard()
    hm.KeyDown = hm.printevent
    hm.KeyUp = hm.printevent
    hm.start()
    if seconds != -1 :
        time.sleep(seconds)
        hm.cancel()

if __name__ == '__main__':
    start_keylogger(-1)
