class emptyUserException(Exception):
    def __init__(self, message="User not found in the database."):
        self.message = message
        super().__init__(self.message)

class invalidTimeException(Exception):
    def __init__(self, message="Invalid time format. Please provide time in the format 'YYYY-MM-DD HH:MM:SS'."):
        self.message = message
        super().__init__(self.message)

class emptyUrlException(Exception):
    def __init__(self, message="URL is empty. Please provide a valid URL."):
        self.message = message
        super().__init__(self.message)

class NullDataException(Exception):
    def __init__(self, message="Data is null. Please provide valid data."):
        self.message = message
        super().__init__(self.message)