class InputError(Exception):
    def __init__(self, message="Input must be 1 upto 6"):
        self.message = message
        super().__init__(self.message)


