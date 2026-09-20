class CredentialsError(Exception):
    """Неверные учётные данные."""


class InvalidTokenError(Exception):
    """Невалидный или истёкший токен."""
