import logging
from simple_slack_bot import SimpleSlackBot


class KarmaBot(SimpleSlackBot):
    def parse_mentioned_user_ids(self, text):
        '''
        Parses the mentioned ids in text
        '''

        user_ids = []
        tokens = text.split()

        for token in tokens:
            if token.startswith("<@"):
                user_ids.append(token[2:-1])

        self._logger.info("user_ids {}".format(user_ids))

        return user_ids


    def parse_mentioned_user_names(self, text):
        '''
        Parses the mentioned names in text
        '''

        user_names = []

        for user_id in self.parse_mentioned_user_ids(text):
            user_names.append(self.user_id_to_user_name(user_id))

        self._logger.info("user_names {}".format(user_names))

        return user_names


    def hello(self, dictionary):
        return "hello"


    def mentions(self, dictionary):
        ret = ""
        MENTIONED_USER_IDS = self.parse_mentioned_user_ids(dictionary["text"])
        MENTIONED_USER_NAMES = self.parse_mentioned_user_names(dictionary["text"])

        for user_id, user_name in zip(MENTIONED_USER_IDS, MENTIONED_USER_NAMES):
            ret += "user_id {} user_name {}\n".format(user_id, user_name)

        return ret
