import time
import numpy as np

from mouse import Mouse
from utils import Utils


def main():

    # Program loop
    while True:
        # Track delta time
        start_time = time.time()

        utils = Utils()
        config = utils.config
        # cheats = Cheats(config)
        mouse = Mouse(config)
        # screen = Screen(config)

        print('Unibot ON')

        # Cheat loop
        while True:
            delta_time = time.time() - start_time
            start_time = time.time()

            mouse.move(10, 10)
            time.sleep(1)
            # mouse.move(-10, -10)

            # Do not loop above the set refresh rate
            # time_spent = (time.time() - start_time) * 1000
            # if time_spent < screen.fps:
            #     time.sleep((screen.fps - time_spent) / 1000)

        del utils
        # del cheats
        del mouse
        # del screen
        print('Reloading')
        break


if __name__ == "__main__":
    main()