"""
Класс пользователя чата
"""
import os

from SimpleWebSocketServer import WebSocket
from datetime import datetime
from src.types import *
from src.exceptions import *
import logging.config
import logging

logging.config.fileConfig('log.conf')
logger = logging.getLogger('main')
logger.setLevel(getattr(logging, os.getenv('LOG_MODE', 'DEBUG')))


class ClientInterface:
    """
    Контракт для ChatClient
    """
    def get_avatar(self, token: str) -> str:
        """
        Функция нужна для получения аватара и не является обязательна к выполнению
        :param token: Токен авторизации, клиент и сервер заранее обсуждают формат получения информации о пользователе (Token)
        :return: Возвращает ссылку на аватар пользователя, иначе None
        """
        pass

    def get_username(self, token: str) -> str:
        """
        Функция нужна для получения имени пользователя и его отображении на стороне клиента
        :param token: Токен авторизации, клиент и сервер заранее обсуждают формат получения информации о пользователе (Token)
        :return: Возвращает строку - имя пользователя которые будут отображаться на клиента
        """
        pass

    def is_authenticated(self, token: str) -> Optional[str]:
        """
        Функция нужна для получения ид клиента по токену, чтобы в дальнейшем заполнить параметр is_my, а так-же проверить авторизирован ли он
        :param token: Токен авторизации, клиент и сервер заранее обсуждают формат получения информации о пользователе (Token)
        :return: Возвращает строку - ид клиента если авторизация прошла успешно, иначе вернет None
        """
        pass

    def save_message(self, message: Message) -> Optional[str]:
        """
        Функция нужна для сохранения сообщения в БД, а так-же для присвоения ID сообщению.
        :param message: Получает сообщение которое необходимо сохранить
        :return: Если сохранения прошло успешно - возвращает ID сообщения, иначе None
        """
        pass

    def is_chat_exists(self, chat_id: str) -> bool:
        """
        Функция нужна для проверки чата на существование.
        Есть ли у пользователя возможность писать или видеть этот чат.
        :param chat_id: Принимает ID чата
        :return: Возвращает True если чат существует, иначе False
        """
        pass

    @property
    def get_clients(self) -> List['ChatClient']:
        """
        Функция нужна для получения всех клиентов чата
        :return: Возвращает массив клиентов (ChatClient)
        """
        pass

    def new_client(self, client: 'ChatClient') -> bool:
        """
        Функция нужна для добавления нового клиента в массив всех клиентов
        :param client: Клиент - обьект который является наследником ChatClient
        :return: Возвращает True если клиент успешно добавлен, иначе False
        """
        pass

    def send_notification(self, chat_id: str, message: Message, active_users: List[str]) -> bool:
        """
        Функция нужна для уведомления всех клиентов о новом сообщении
        :param active_users: ID пользователей которые находятся в чате (Их не нужно уведомлять)
        :param message: Сообщение о котором нужно уведомить
        :param chat_id: ID чата клиентов которого необходимо уведомить
        :return: Возвращает True если клиенты успешно уведомлены, иначе False
        """
        pass

    def remove_client(self, client: 'ChatClient') -> bool:
        """
        Функция нужна для удаления клиента из массива всех клиентов
        :param client: Клиент - обьект который является наследником ChatClient
        :return: Возвращает True если клиент успешно удален, иначе False
        """
        pass

    def get_messages(self, chat_id: str) -> List[Message]:
        """
        Функция нужна для получения всех сообщений из БД
        :param chat_id: ID чата сообщения которого необходимо получить
        :return: Возвращает массив обьектов Message, все поля модели являются обязательными
        """
        pass


class ChatClient(WebSocket, ClientInterface):
    user_id: Optional[str] = None
    """
    @TODO Проверить что выполнены все контракты
    """

    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)
        self.request = None

    def get_active_users(self, chat_id: str) -> List[str]:
        return [x.user_id for x in self.get_clients if x.request.chat_id == chat_id]

    def send_message(self):
        message = self.request.message
        message = message.to_dict()
        message['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message['username'] = self.get_username(self.request.token)
        message['avatar'] = self.get_avatar(self.request.token)
        message['chat_id'] = self.request.chat_id
        message['user_id'] = self.user_id
        message['id'] = self.save_message(message)
        print('test')
        for client in iter(filter(
                lambda x: x.request is not None and x.request.chat_id == self.request.chat_id, self.get_clients
        )):
            print('test1')
            message['is_my'] = False
            if client.user_id is not None and client.user_id == self.user_id:
                message['is_my'] = True
            print('test2')
            client.sendMessage(Response(type=ErrorType.SUCCESS, detail='Success',
                                        event_type=self.request.event_type,
                                        messages=[message]).to_json())
            print('test3')
            if os.getenv('USE_NOTIFICATION'):
                self.send_notification(self.request.chat_id, Message.from_dict(message),
                                       self.get_active_users(self.request.chat_id))

    def get_history(self):
        messages = [x.to_dict() for x in self.get_messages(self.request.chat_id)]
        for message in messages:
            message['is_my'] = False
            if message['user_id'] is not None and message['user_id'] == self.user_id:
                message['is_my'] = True
        messages = sorted(messages, key=lambda x: x['created_at'])
        self.sendMessage(Response(type=ErrorType.SUCCESS, detail='',
                                  event_type=self.request.event_type,
                                  messages=messages).to_json())

    def send_file(self):
        self.send_message()

    def handleMessage(self):
        try:
            logger.debug(f'Получено новое сообщение: {self.data}')
            self.request = Request.from_dict(json.loads(self.data))
            if not self.is_chat_exists(self.request.chat_id):
                raise ChatNotExistsError('Chat not exists or user dont have permissions to write/read this chat')
            if self.user_id is None:
                is_auth_success = self.is_authenticated(self.request.token)
                if is_auth_success is None:
                    raise AuthorizationError('Token validation error')
                self.user_id = is_auth_success
            getattr(self, self.request.event_type.value)()
        except AuthorizationError as e:
            logger.debug(e)
            self.sendMessage(Response(type=ErrorType.TOKEN_VALIDATION_ERROR, detail=str(e)
                                      , event_type=self.request.event_type).to_json())
        except ChatNotExistsError as e:
            logger.debug(e)
            self.sendMessage(Response(type=ErrorType.CHAT_NOT_EXISTS, detail=str(e)
                                      , event_type=self.request.event_type).to_json())
        except ValueError as e:
            logger.debug(e)
            self.sendMessage(Response(type=ErrorType.EVENT_NOT_FOUND, detail=str(e)
                                      , event_type=self.request.event_type).to_json())
        except Exception as e:
            logger.error(e)
            self.sendMessage(Response(type=ErrorType.SERVER_ERROR, detail=str(e)
                                      , event_type=self.request.event_type).to_json())

    def handleConnected(self):
        self.new_client(self)
        logger.debug(f'Подключен новый клиент: {self.request}')

    def handleClose(self):
        self.remove_client(self)
        logger.debug(f'Отключен клиент: {self.request}')
