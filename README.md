# **Arabic Tweets Scraper**
This project is a Python script that utilizes the `snscrape` library and `threading` to scrape  large number of Arabic tweets from Twitter. The use of multithreading improves the performance of the script and allows for the collection of a larger number of tweets. The script also uses file handling to store scraped tweets in a structured format, and includes additional functionality to track processed and unprocessed usernames.

<br>

---

<br>

## **Table of Contents**
- [**Overview**](#overview)
- [**Prerequisites**](#prerequisites)
- [**How to Use**](#how-to-use)
- [**Output**](#output)
- [**Issues**](#issues)
- [**Contribution Guide**](#contribution-guide)
- [**Scraped Data**](#scraped-data)

<br>

---

<br>

## **Overview**
This script is designed to efficiently scrape a large number of Arabic tweets from Twitter using the `snscrape` library. The use of multithreading improves the performance of the script and allows for the collection of a larger number of tweets.

The script works by starting with a list of usernames to process, contained in the file `to_process_usernames.txt`. As it scrapes tweets from each user, it also adds any mentioned usernames to a set for future processing.

To ensure that only Arabic tweets are collected, several steps are taken:
- Only tweets that contain at least one Arabic character are saved.
- If a tweet does not contain Arabic text, the mentioned usernames are not added to the set for future processing.
- If the script encounters 10 consecutive tweets without Arabic text while scraping a user, it will stop processing that user.

The script stores the scraped tweets for each user in a JSON file located in the `tweets/` directory, with the file name in the format of `username.json`. The tweets are stored in the following json format: `{"username": ["tweet1", "tweet2", "tweet3", ...]}`.

Additionally, the script includes a logging feature that records any exceptions and other important information in a separate log file for tracking and troubleshooting purposes.

<br>

---

<br>

## **Prerequisites**
In order to run this script, the following prerequisites are required:
- [Python 3](https://www.python.org/downloads/).
- `snscrape` library (can be installed using `pip install snscrape`).

<br>

---

<br>

## **How to Use**
1. Clone or download the repository to your local machine.
2. Ensure that you have all the [prerequisites](#prerequisites) installed.
3. Add the desired starting username(s) to the [to_process_usernames.txt](/usernames/to_process_usernames.txt) file.
4. Configure the `NUMBER_OF_THREADS` variable to your desired number of threads.
5. Execute the script by running the command `python scraper.py`.
6. The script will begin scraping tweets and saving them in the `tweets/` directory.

<br>

> Keep in mind that this script is specifically designed to scrape Arabic tweets. If you wish to use it for a different language, you will need to adjust the `contains_arabic` function to suit your needs. Alternatively, if you do not wish to filter tweets by language, you can make the function always return `True` or remove it altogether from the code.

<br>

---

<br>

## **Output**
The script generates several outputs, including:
1. Scraped tweets for each user, which are saved in a file `tweets/username.json`. The file contains the tweets in the following format: `{"username": ["tweet1", "tweet2", "tweet3", ...]}`.
2. A log file `log.txt` which records the progress of the scraping process and any exceptions that may have occurred.
3. The script modifies two files, `processed_usernames.txt` and `to_process_usernames.txt`, which contain sets of usernames. The first file contains the usernames that have been scraped, while the second file contains the usernames that have been mentioned by the scraped tweets and need to be processed.

<br>

> Keep in mind that the scraped tweets will be saved in multiple files, so it may be necessary to combine them into a single file before using them.

<br>

---

<br>

## **Issues**
- As using multithreading, the script can't terminate by key interrupt (`ctrl + c`), and it should be by force stop or close the terminal; this leads to not save the sets to the files.
- When using a large number of threads (I tried 30 and the problem occurred), an error thrown from the `snscrape` library (`4 requests to https://api.twitter.com/2/sea...`).

<br>

> If you are able to address these limitations, please open a pull request and include your code.

<br>

---

<br>

## **Contribution Guide**
1. Fork the repository on GitHub.
2. Clone the forked repository to your local machine.
3. Create a new branch for your changes.
4. Make the desired changes to the code, including tests and documentation.
5. Commit your changes and push them to your forked repository.
6. Open a pull request to the original repository.
7. The repository maintainers will review your changes and merge them if they are appropriate.

<br>

---

<br>

## **Scraped Data**
If you need a larger dataset for your research or project, please [reach out to me](https://www.linkedin.com/in/obada-tahayna/) as I have scraped over 90 million Arabic tweets and may be able to provide the data you need.
