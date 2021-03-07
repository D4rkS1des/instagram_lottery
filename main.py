import os
import time
import random

from instagram_private_api import Client


class Lottery:
    """
    This class implements instagram api object and methods for making lottery.
    This class contains 3 methods:
    :method get_threads: it is useful for taking all threads from direct
    :method get_users_who_participant: it is useful for taking all people who participant in lottery
    :method get_followers: it is useful for taking all people who follow your account in instagram
    """
    def __init__(self, user_name, password):
        """
        api is a instagram lib api object
        :param user_name: sting with username to instagram account
        :param password: sting with password to instagram account
        """
        self.api = Client(user_name, password)

    def get_threads(self, followers):
        """
        This method taking all threads from direct.
        :param followers: list with users who following your account
        :return all_threads: list with all threads from direct
        """
        all_threads = []
        cursor = None
        while cursor != 'end':
            messages = self.api.direct_v2_inbox(cursor)
            for thread in messages['inbox']['threads']:
                if thread['users'][0]['username'] in followers:
                    all_threads.append({'username': thread['users'][0]['username'], 'thread_id': thread['thread_id']})
            try:
                cursor = messages['inbox']['oldest_cursor']
            except KeyError:
                cursor = 'end'
        return all_threads

    def get_users_who_participant(self, all_threads):
        """
        This method take all_threads list and get all messages from those threads,
        then it try to find your messages that startswith a text: 'Ваш номер в розыгрыше',
        when it find it write username to users_who_accepted list.
        :param all_threads: list with all threads from direct
        :return users_who_accepted: list with users who accepted in lottery
        """
        users_who_accepted = []
        for thread in all_threads:
            current_user_messages = self.api.direct_v2_threads(thread['thread_id'])['thread']
            message_list = current_user_messages['items']
            while len(current_user_messages['items']) != 0:
                current_user_messages = self.api.direct_v2_threads(
                    thread['thread_id'],
                    current_user_messages['oldest_cursor']
                )['thread']
                message_list += current_user_messages['items']
            for message in message_list:
                try:
                    if message['user_id'] == self.api.authenticated_user_id and message['text'].startswith('Ваш номер в розыгрыше'):
                        users_who_accepted.append(thread['username'])
                        break
                except Exception as err:
                    continue
        return users_who_accepted

    def get_followers(self):
        followers = self.api.user_followers(self.api.authenticated_user_id, self.api.generate_uuid())
        users_who_following = []
        for follower in followers['users']:
            users_who_following.append(follower['username'])
        return users_who_following


def get_winners(users_who_following, users_who_accepted):
    """
    This function takes two list and grep overlapping values in both to possible_winners list,
    then randomly choice 3 winners from possible_winners list and write to winners list.
    :param users_who_following: list with users who following your account
    :param users_who_accepted: list with users who accepted in lottery
    :return winners: list with winners
    :return possible_winners: list with users who participants in lottery and do all that need
    """
    possible_winners = list(set(users_who_following) & set(users_who_accepted))
    winners = []
    while len(winners) != 3:
        winner = random.choice(possible_winners)
        if winner not in winners:
            winners.append(winner)
    return winners, possible_winners


def piu(user_name, password):
    insta_api = Lottery(user_name, password)
    followers = insta_api.get_followers()
    threads = insta_api.get_threads(followers)
    users_who_accepted = insta_api.get_users_who_participant(threads)
    winners, possible_winners = get_winners(users_who_accepted, followers)
    print('Всего человек участвовало: ' + str(len(possible_winners)))
    print('Все аккаунты участвовавшие в конкурсе:')
    print(possible_winners)
    time.sleep(5)
    print('--------------------5-----------------------')
    time.sleep(1)
    print('--------------------4-----------------------')
    time.sleep(1)
    print('--------------------3-----------------------')
    time.sleep(1)
    print('--------------------2-----------------------')
    time.sleep(1)
    print('--------------------1-----------------------')
    print('Победители:')
    i = 1
    for winner in winners:
        print('{} место: {} поздравляем!'.format(str(i), winner))
        i += 1
    print('Удача на вашей стороне!')
    print('--------------------------------------------')


if __name__ == '__main__':
    username = os.environ['username']
    password = os.environ['password_inst']
    piu(username, password)

