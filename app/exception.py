class UserNotFoundException(Exception):
    detail = 'User not found'


class UserIncorrectPasswordException(Exception):
    detail = 'Incorrect password'


class TokenExpiredException(Exception):
    detail = 'Token expired'


class TokenNotCorrectException(Exception):
    detail = 'Token not correct'

class TaskNotFoundException(Exception):
    detail = 'Task not found'
