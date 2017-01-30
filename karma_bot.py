import logging, redis
from simple_slack_bot import SimpleSlackBot


class KarmaBot(SimpleSlackBot):
    def __init__(self):
        super().__init__()
        self._redis = redis.StrictRedis(host='localhost', port=6379, db=0)


    def increment_user_id(self, user_id):
        '''
        Increases this user id's karma by one
        '''

        CURRENT_SCORE =  self._redis.get(user_id)
        if CURRENT_SCORE is None:
            CURRENT_SCORE = 0
        NEW_SCORE = int(CURRENT_SCORE) + 1
        self._redis.set(user_id, NEW_SCORE)

        return NEW_SCORE


    def decrement_user_id(self, user_id):
        '''
        Decrease this user id's karma by one
        '''

        CURRENT_SCORE =  self._redis.get(user_id)
        if CURRENT_SCORE is None:
            CURRENT_SCORE = 0
        NEW_SCORE = int(CURRENT_SCORE) - 1
        self._redis.set(user_id, NEW_SCORE)

        return NEW_SCORE

    def parse_mentioned_user_ids(self, text):
        '''
        Parses the mentioned ids in text by positive and negative
        '''

        positive_user_ids = []
        negative_user_ids = []
        tokens = text.split()

        for token in tokens:
            if token.startswith("<@") and token.endswith(">++"):
                positive_user_ids.append(token[2:-3])
            if token.startswith("<@") and token.endswith(">--"):
                negative_user_ids.append(token[2:-3])

        self._logger.info("positive user_ids {}".format(positive_user_ids))
        self._logger.info("negative user_ids {}".format(negative_user_ids))

        return positive_user_ids, negative_user_ids


    def hello(self, dictionary):
        return "hello"


    def mentions(self, dictionary):
        ret = ""
        POSITIVE_USER_IDS, NEGATIVE_USER_IDS = self.parse_mentioned_user_ids(dictionary["text"])
        MENTIONED_USER_NAMES = []

        for positive_user_id in POSITIVE_USER_IDS:
            USER_NAME = self.user_id_to_user_name(positive_user_id)
            MENTIONED_USER_NAMES.append(USER_NAME)
            NEW_SCORE = self.increment_user_id(positive_user_id)
            ret += USER_NAME + ":" + str(NEW_SCORE)

        for negative_user_id in NEGATIVE_USER_IDS:
            USER_NAME = self.user_id_to_user_name(negative_user_id)
            MENTIONED_USER_NAMES.append(USER_NAME)
            NEW_SCORE = self.decrement_user_id(negative_user_id)
            ret += USER_NAME + ":" + str(NEW_SCORE)

        return ret
