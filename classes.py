class loger(object):
    def __init__(self, path) -> None:
        self.file = open(path, 'wt')

    def write(self, msg: str) -> None:
        self.file.write(msg)
    
    def close(self) -> None:
        self.file.close()