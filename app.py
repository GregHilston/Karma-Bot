from simple_slack_bot import SimpleSlackBot
from karma_bot import KarmaBot


def main():
    karma_bot = KarmaBot()
    karma_bot.register_mentions(karma_bot.mentions)
    karma_bot.start()


if __name__ == "__main__":
    main()
