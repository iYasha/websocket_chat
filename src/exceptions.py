"""
Ошибка для чата
"""


class AuthorizationError(Exception):
    """
    Ошибка валидации токена.
    Не удалось получить токен из функции is_authenticated.
    Токен пустой.
    """
    pass


class ChatNotExistsError(Exception):
    """
    Ошибка валидации чата.
    Чат не создан.
    У пользователя нет возможности читать/писать в чат.
    """
    pass
