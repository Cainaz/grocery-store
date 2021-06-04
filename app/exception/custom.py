class CustomException(Exception):
    def __init__(self, code: int, desc: str, excep_type: str):
        self.code = code
        self.desc = desc
        self.type = excep_type
