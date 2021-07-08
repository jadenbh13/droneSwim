import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def setLed(R, G, B):
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Set virtual mem effect effect
        cf.param.set_value('ring.effect', '13')

        # Get LED memory and write to it
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
        if len(mem) > 0:
            mem[0].leds[0].set(r=R,   g=G, b=B)
            mem[0].leds[1].set(r=R,   g=G, b=B)
            mem[0].leds[2].set(r=R,   g=G, b=B)
            mem[0].leds[3].set(r=R,   g=G, b=B)
            mem[0].leds[4].set(r=R,   g=G, b=B)
            mem[0].leds[5].set(r=R,   g=G, b=B)
            mem[0].leds[6].set(r=R,   g=G, b=B)
            mem[0].leds[7].set(r=R,   g=G, b=B)
            mem[0].leds[8].set(r=R,   g=G, b=B)
            mem[0].leds[9].set(r=R,   g=G, b=B)
            mem[0].write_data(None)
