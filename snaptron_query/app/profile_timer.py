from timeit import default_timer as timer


# from dash import callback_context as ctx #use in conjunction with dash context


class Timer:
    def __init__(self, function_name=None):
        self.enabled = False  # Set to True to turn on the timers
        self.start_time = None
        self.split_start_time = None
        self.function_name = function_name
        self.start()

    def turn_on(self):
        self.enabled = True

    def turn_off(self):
        self.enabled = False

    def start(self):
        """
        starts the timer
        """
        if self.enabled:
            self.start_time = timer()
            print(f"Start: {self.function_name}")

    def stop(self, msg=None):
        """
        stop the timer completely
        :param msg: provide function name as strings
        """
        if self.enabled and self.start_time is not None:
            # stop the time
            end_time = timer()

            # if there was a split before it calculate the splits
            if self.split_start_time:
                elapsed = end_time - self.split_start_time
                print(f"\t{msg}: {elapsed:.6f} seconds")
                # ctx.record_timing(msg, elapsed)

            total = end_time - self.start_time
            print(f"End: {self.function_name}\tTotal time: {total:.6f} seconds")
            # ctx.record_timing(self.function_name, total)

            self.turn_off()

    def split(self, msg=None):
        """
        Use this function to create time splits in the main function.
        The previous split timer will stop and a new split timer will start
        :param msg: provide function name as strings
        """
        if self.enabled:
            if self.start_time is not None:
                current_time = timer()
                if self.split_start_time is None:
                    # first split
                    split_time = current_time - self.start_time
                else:
                    split_time = current_time - self.split_start_time

                print(f"\t{msg}: {split_time:.6f} seconds")
                # ctx.record_timing(msg, split_time)
                # start the timer for the next split
                self.split_start_time = current_time
