class UserNotFoundException(Exception):
    detail = 'User not found'

class UserIncorrectPasswordException(Exception):
    detail = 'Incorrect password'