class Command:
    def __init__(self, command, start, end):
        self.command = command
        self.start = start
        self.end = end

    def to_string(self):
        return "{:20} from {:.2f} sec to {:.2f} sec".format(
            self.command, self.start, self.end)



