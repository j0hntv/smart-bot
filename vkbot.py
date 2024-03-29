import os
from dotenv import load_dotenv
import dialogflow_api
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import logging
import config

logger = logging.getLogger('VK-bot')


def reply(event, vk_api):
    answer = dialogflow_api.get_answer(GOOGLE_PROJECT_ID, event.user_id, event.text, 'ru')
    if answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1,1000)
        )
        logger.info(f'Message <{answer}> sent to ID <{event.user_id}>')


if __name__ == "__main__":
    load_dotenv()
    VK_TOKEN = os.getenv('VK_TOKEN')
    GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')

    config.setup_logger(logger)
    logger.info('Бот заработал.')

    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.info(f'Message <{event.text}> received from ID <{event.user_id}>')
            reply(event, vk_api)
    