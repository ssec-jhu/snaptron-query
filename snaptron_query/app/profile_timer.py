import time


class Timer:
    def __init__(self, function_name=None):
        self.enabled = True  # Set to True to turn on the timers
        self.start_time = None
        self.split_start_time = None
        self.function_name = function_name
        self.start()

    def start(self):
        """
        starts the timer
        """
        if self.enabled:
            self.start_time = time.time()
            print(f"Start: {self.function_name}")

    def stop(self, msg=None):
        """
        stop the timer completely
        :param msg: provide function name as strings
        """
        if self.enabled and self.start_time is not None:
            # stop the time
            end_time = time.time()

            # if there was a split before it calculate the splits
            if self.split_start_time:
                elapsed = end_time - self.split_start_time
                print(f"\t{msg}: {elapsed:.4f} seconds")

            print(f"End: {self.function_name}\tTotal time: {end_time - self.start_time:.4f} seconds")

    def split(self, msg=None):
        """
        Use this function to create time splits in the main function.
        The previous split timer will stop and a new split timer will start
        :param msg: provide function name as strings
        """
        if self.enabled:
            if self.start_time is not None:
                if self.split_start_time is None:
                    self.split_start_time = time.time()
                else:
                    # print the elapsed time
                    print(f"\t{msg}: {time.time() - self.split_start_time:.4f} seconds")
                    # start the timer for the next split
                    self.split_start_time = time.time()
