from asyncio.proactor_events import _ProactorDuplexPipeTransport
import pyxdf
#from psychopy import core, visual, event
#import matplotlib.pyplot as plt
import numpy as np
from pylsl import StreamInfo, StreamOutlet
#from psychopy import prefs, visual, core, event, monitors, tools, logging
import numpy as np
import tobii_research as tr
import time
import random
import os
import pylsl as lsl
import sys

found_eyetrackers = tr.find_all_eyetrackers()
mt = found_eyetrackers[0]
print("Address: " + mt.address)
print("Model: " + mt.model)
print("Name (It's OK if this is empty): " + mt.device_name)
print("Serial number: " + mt.serial_number)

# # Preface here
# #
# # from psychopy import prefs, visual, core, event, monitors, tools, logging
# import numpy as np
# import tobii_research as tr
# import time
# import random
# import os
# import pylsl as lsl
# import sys

# # Find Eye Tracker and Apply License (edit to suit actual tracker serial no)
# ft = tr.find_all_eyetrackers()
# if len(ft) == 0:
#     print ("No Eye Trackers found!?")
#     exit(1)

# # Pick first tracker
# mt = ft[0]
# print ("Found Tobii Tracker at '%s'" % (mt.address))


channels = 31 # count of the below channels, incl. those that are 3 or 2 long
gaze_stuff = [
    ('device_time_stamp', 1), # 0

    ('left_gaze_origin_validity',  1),  #1
    ('right_gaze_origin_validity',  1), #2

    ('left_gaze_origin_in_user_coordinate_system',  3), #3-5
    ('right_gaze_origin_in_user_coordinate_system',  3), #6-8

    ('left_gaze_origin_in_trackbox_coordinate_system',  3), #9-11
    ('right_gaze_origin_in_trackbox_coordinate_system',  3), #12-14

    ('left_gaze_point_validity',  1), #15
    ('right_gaze_point_validity',  1), #16

    ('left_gaze_point_in_user_coordinate_system',  3), #17-19
    ('right_gaze_point_in_user_coordinate_system',  3),#20-22

    ('left_gaze_point_on_display_area',  2), #23-24
    ('right_gaze_point_on_display_area',  2), #25-26

    ('left_pupil_validity',  1), #27
    ('right_pupil_validity',  1), #28

    ('left_pupil_diameter',  1), #29
    ('right_pupil_diameter',  1) #30
]
    

def unpack_gaze_data(gaze_data):
    x = []
    for s in gaze_stuff:
        d = gaze_data[s[0]]
        if isinstance(d, tuple):
            x = x + list(d)
        else:
            x.append(d)
    return x

last_report = 0
N = 0


def gaze_data_callback(gaze_data):
    '''send gaze data'''

    '''
    This is what we get from the tracker:

    device_time_stamp

    left_gaze_origin_in_trackbox_coordinate_system (3)
    left_gaze_origin_in_user_coordinate_system (3)
    left_gaze_origin_validity
    left_gaze_point_in_user_coordinate_system (3)
    left_gaze_point_on_display_area (2)
    left_gaze_point_validity
    left_pupil_diameter
    left_pupil_validity

    right_gaze_origin_in_trackbox_coordinate_system (3)
    right_gaze_origin_in_user_coordinate_system (3)
    right_gaze_origin_validity
    right_gaze_point_in_user_coordinate_system (3)
    right_gaze_point_on_display_area (2)
    right_gaze_point_validity
    right_pupil_diameter
    right_pupil_validity

    system_time_stamp
    '''


    # for k in sorted(gaze_data.keys()):
    #     print ' ' + k + ': ' +  str(gaze_data[k])

    try:
        global last_report
        global outlet
        global N
        global halted

        sts = gaze_data['system_time_stamp'] / 1000000.

        outlet.push_sample(unpack_gaze_data(gaze_data), sts)
        
        if sts > last_report + 5:
            sys.stdout.write("%14.3f: %10d packets\r" % (sts, N))
            last_report = sts
        N += 1
     
        #print(unpack_gaze_data(gaze_data))
    except:
        print("Error in callback: ")
        print(sys.exc_info())

        halted = True


def start_gaze_tracking():
    mt.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    return True

def end_gaze_tracking():
    mt.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    return True

halted = False


# Set up lsl stream
def setup_lsl():
    global channels
    global gaze_stuff

    info = lsl.StreamInfo('Tobii', 'ET', channels, 90, 'float32', mt.address)
    info.desc().append_child_value("manufacturer", "Tobii")
    channels = info.desc().append_child("channels")
    cnt = 0
    for s in gaze_stuff:
        if s[1]==1:
            cnt += 1
            channels.append_child("channel") \
                    .append_child_value("label", s[0]) \
                    .append_child_value("unit", "device") \
                    .append_child_value("type", 'ET')
        else:
            for i in range(s[1]):
                cnt += 1
                channels.append_child("channel") \
                        .append_child_value("label", "%s_%d" % (s[0], i)) \
                        .append_child_value("unit", "device") \
                        .append_child_value("type", 'ET')

    outlet = lsl.StreamOutlet(info)

    return outlet

outlet = setup_lsl()

# Main loop; run until escape is pressed
print ("%14.3f: LSL Running; press CTRL-C repeatedly to stop" % lsl.local_clock())
start_gaze_tracking()
try:
    while not halted:
        time.sleep(1)
        keys = ()  # event.getKeys()
        if len(keys) != 0:
            if keys[0]=='escape':
                halted = True

        if halted:
            break

        # print lsl.local_clock()

except:
    print ("Halting...")

print ("terminating tracking now")
end_gaze_tracking()
