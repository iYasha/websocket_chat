"""
Создание обьекта server и запуск сокета
"""
from SimpleWebSocketServer import SimpleWebSocketServer
from src.chat_client import ChatClient
from src.types import *
from src.utility import *
import os
import logging.config
import logging

clients = []
logging.config.fileConfig('log.conf')
logger = logging.getLogger('main')
logger.setLevel(getattr(logging, os.getenv('LOG_MODE', 'DEBUG')))
logger.info(f'Подключение к БД, Хост: {os.getenv("DATABASE_HOST")}, Порт: {os.getenv("DATABASE_PORT")}, БД: {os.getenv("DATABASE_NAME")}')
connection = get_connection()
cursor = connection.cursor()
logger.info('БД успешно подключена')


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class User:
    id: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
    avatar: Optional[str] = None


class Client(ChatClient):
    """
    Клиент чата, который наследуется от ChatClient и выполняет контракт ClientInterface
    """

    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)
        self.user_profile = None

    def get_user_profile(self, token) -> Optional[User]:
        global connection, cursor
        try:
            logger.debug('Начала работать функция get_user_profile')
            if self.user_profile is None:
                cursor.execute(f"SELECT user_id FROM authtoken_token WHERE key = '{token}'")
                result = cursor.fetchone()
                if result is None:
                    return None
                user_id = result[0]
                cursor.execute(f'SELECT * from slm_user WHERE id = {user_id}')
                user_keys = [desc[0] for desc in cursor.description]
                result = cursor.fetchone()
                if result is None:
                    return None
                self.user_profile = User.from_dict({x: result[idx] for idx, x in enumerate(user_keys)})
            logger.debug('Закончила работать функция get_user_profile')
            return self.user_profile
        except Exception as e:
            logger.error(e)
            connection = get_connection()
            cursor = connection.cursor()

    def get_avatar(self, token: str) -> str:
        return self.get_user_profile(token).avatar

    def get_username(self, token: str) -> str:
        user = self.get_user_profile(token)
        return user.first_name + ' ' + user.last_name

    def is_authenticated(self, token: str) -> Optional[str]:
        logger.debug('Начала работать функция is_authenticated')
        user = self.get_user_profile(token)
        logger.debug('Закончила работать функция is_authenticated')
        if user is not None:
            return user.id
        return None

    def save_message(self, message: Message) -> Optional[str]:
        global connection, cursor
        if 'id' in message:
            message.pop('id')
        keys = ', '.join(message.keys())
        values = ', '.join(["'" + str(x) + "'" for x in message.values()])
        cursor.execute(f'INSERT INTO task_chatmessage({keys}) VALUES ({values})')
        connection.commit()
        cursor.execute('SELECT LASTVAL()')
        return cursor.fetchone()[0]

    def get_messages(self, chat_id: str) -> List[Message]:
        cursor.execute(f'SELECT * FROM task_chatmessage WHERE chat_id = {chat_id}')
        result = cursor.fetchall()
        messages = [Message.from_dict(x) for x in result]
        return messages

    def is_chat_exists(self, chat_id: str) -> bool:
        cursor.execute(f'SELECT * FROM task_task WHERE id = {chat_id}')
        task = cursor.fetchone()
        if task is None:
            return False
        return True

    @property
    def get_clients(self) -> List['ChatClient']:
        return clients

    def new_client(self, client: 'ChatClient') -> bool:
        try:
            clients.append(client)
            return True
        except Exception:
            return False

    def send_notification(self, chat_id: str, message: Message, active_users: List[str]) -> bool:
        pass

    def remove_client(self, client: 'ChatClient') -> bool:
        try:
            clients.remove(client)
            return True
        except Exception:
            return False


if __name__ == '__main__':
    logger.info(f'Запуск веб-сокета, Хост: {os.getenv("HOST")}, Порт: {os.getenv("PORT")}')
    server = SimpleWebSocketServer(os.getenv('HOST', ''), os.getenv('PORT'), Client)
    logger.info('Сокет запустился')
    server.serveforever()
    logger.info('Соединение закрыто')
