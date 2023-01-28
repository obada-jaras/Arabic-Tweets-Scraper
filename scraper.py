from threading import Thread, Lock, current_thread
import snscrape.modules.twitter as sntwitter
import time
from datetime import datetime
import random
import traceback
import json


TO_PROCESS_USERNAMES__FILE = 'usernames/to_process_usernames.txt'
PROCESSED_USERNAMES__FILE = 'usernames/processed_usernames.txt'
LOGS__FILE = 'logs.txt'
TWEETS__PATH = 'tweets/'

TO_PROCESS_USERNAMES__SET = set()
PROCESSED_USERNAMES__SET = set()

NUMBER_OF_THREADS = 10


def main():
    log("Starting...")
    read_processed_usernames(PROCESSED_USERNAMES__FILE)
    read_to_process_usernames(TO_PROCESS_USERNAMES__FILE)

    threads = []
    lock = Lock()
    for _ in range(NUMBER_OF_THREADS):
        thread = Thread(target=scrap_twitter_with_exception_handling, args=(lock,))
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    save_processed_usernames(PROCESSED_USERNAMES__FILE)
    save_usernames(TO_PROCESS_USERNAMES__FILE)
    log("Finished")



def read_processed_usernames(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            username = line.strip()
            PROCESSED_USERNAMES__SET.add(username)

def save_processed_usernames(filename):
    save_set_to_file(filename, PROCESSED_USERNAMES__SET)

def read_to_process_usernames(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            username = line.strip()
            TO_PROCESS_USERNAMES__SET.add(username)

def save_usernames(filename):
    save_set_to_file(filename, TO_PROCESS_USERNAMES__SET)

def save_set_to_file(filename, set):
    with open(filename, 'w', encoding="utf-8") as f:
        for username in set:
            f.write(username + "\n")



def scrap_twitter_with_exception_handling(lock):
    print(f"Thread {current_thread().name} started...")

    attempts = 0
    max_attempts = random.randint(5, 10)

    while True:
        try:
            scrap_twitter(lock)
            break

        except Exception:
            traceback_error = traceback.format_exc()
            random_sleep = random.uniform(0, 10)

            log(f"Attempt: {attempts}\t retry in: {random_sleep}\n{traceback_error}")
            attempts += 1

            if attempts == max_attempts:
                log(f"Attempt: {attempts}\nMax attempts reached, exiting...")
                raise

            time.sleep(random_sleep)

def scrap_twitter(lock):
    while TO_PROCESS_USERNAMES__SET:
        with lock:
            username = TO_PROCESS_USERNAMES__SET.pop()
        print(f"thread: {current_thread().name}\nScraping user: {username}\n\n")

        if username not in PROCESSED_USERNAMES__SET:
            with lock:
                PROCESSED_USERNAMES__SET.add(username)

            get_user_tweets(username, lock)

def get_user_tweets(username, lock):
    file_name = f'{TWEETS__PATH}{username}.json'

    non_arabic_count = 0
    mentions_set = set()

    with open(file_name, 'a', encoding="utf-8") as file:
        file.write("{\"" + username + "\":[")
        first_tweet = True

        for tweet in sntwitter.TwitterSearchScraper(f'from:{username}').get_items():
            if contains_arabic(tweet.content):
                non_arabic_count = 0
                save_mentioned_users(tweet.mentionedUsers, mentions_set)
                tweet_content = tweet.content.replace("\n", "\\n")

                if first_tweet:
                    file.write("\"" + tweet_content + "\"")
                    first_tweet = False
                
                else:
                    file.write(",\"" + tweet_content + "\"")

            else:
                non_arabic_count += 1

            if non_arabic_count == 10:
                break

        file.write("]}")

    with lock:
        TO_PROCESS_USERNAMES__SET.update(mentions_set)



def save_mentioned_users(list_of_users, user_mentions):
    if list_of_users:
        for user in list_of_users:
            username = user.username
            if username not in PROCESSED_USERNAMES__SET:
                user_mentions.add(username)



def contains_arabic(text):
    return any('\u0600' <= character <= '\u06FF' for character in text)

def log(log):
    log = (f"thread: {current_thread().name} \t\
            at: {str(datetime.now())} \n\
            {log}\
            \n\n####################\n\n")
    print(log)

    with open(LOGS__FILE, 'a', encoding="utf-8") as file:
        file.write(log)


if __name__ == "__main__":
    try:
        main()

    except Exception:
        log("Saving usernames and processed users...")
        save_usernames(TO_PROCESS_USERNAMES__FILE)
        save_processed_usernames(PROCESSED_USERNAMES__FILE)
        exit(1)
