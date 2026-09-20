class UserNotFoundError(Exception):
    """Пользователь не найден"""

class UserAlreadyExistsError(Exception):
    """Пользователь уже существует."""
