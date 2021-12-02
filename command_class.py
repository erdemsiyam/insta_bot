from instabot import Bot
import instabot

class Command:
    def __init__():
        pass

    def run(bot:instabot.Bot):

        while True:

            cmd = input().split(' ')

            if len(cmd) < 2:
                continue

            try:
                if cmd[0] == 'get_user_id_from_username':
                    print(bot.get_user_id_from_username(cmd[1]))
                elif cmd[0] == 'get_total_followers_or_followings':
                    print(bot.get_total_followers_or_followings(cmd[1]))
                elif cmd[0] == 'get_user_id_from_username':
                    print(bot.get_user_id_from_username(cmd[1]))
                elif cmd[0] == 'get_username_from_user_id':
                    print(bot.get_username_from_user_id(cmd[1]))
                elif cmd[0] == 'get_user_info':
                    print(bot.get_user_info(cmd[1]))
                elif cmd[0] == 'get_user_followers':
                    print(bot.get_user_followers(cmd[1]))
                elif cmd[0] == 'get_user_following':
                    print(bot.get_user_following(cmd[1]))
                elif cmd[0] == 'follow':
                    print(bot.follow(cmd[1]))
                elif cmd[0] == 'unfollow':
                    print(bot.unfollow(cmd[1]))
            except Exception as e:
                bot.logger.error(e)