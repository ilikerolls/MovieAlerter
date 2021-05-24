import urllib.request
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import re
from pathlib import Path
from pushbullet import Pushbullet
# ImdbSearcherScheduler imports
from apscheduler.schedulers.background import BackgroundScheduler


class ImdbSearcher:
    """
    1.search for box office movies on imdb
    2. check to see if their ratings & votes match given specifications
    3. report new movies that match given specifications
    4. eventually set them to auto download
    """

    def __init__(self, lowest_rating, lowest_votes, cat_blacklist=None, db_file=None, pushbullet_api_key=None,
                 url_box_office_link=r'https://www.imdb.com/chart/boxoffice?ref_=nv_ch_cht_2'):
        """Initialize attributes to be used, so such lowest votes & Lower rating

        :param lowest_rating: Lowest rating to accept 1-10. Anything lower will be ignored
        :param lowest_votes: Lowest amount of votes movie must have
        :param cat_blacklist: Optional param. List of categories not to allow. ex: ['Animation', 'Adventure']
        :param db_file: Optional: Specify your own database file to store movies already processed
        :param url_box_office_link: url_box_office_link: link to where Box imdb page is. Will use default if none
        specified
        """
        self.matched_count = 0
        self.too_low_count = 0
        if cat_blacklist is None:
            cat_blacklist = []
        self.lowest_rating = lowest_rating
        self.lowest_votes = lowest_votes
        self._top_box_office_dict = {}
        self.cat_blacklist = cat_blacklist
        self.db_file = db_file or 'ImdbSearcher.db'
        self._seen_movies = self.load_movie_data()
        self.url_box_office_link = url_box_office_link
        self.notify_msg = None
        self.pushbullet_api_key = pushbullet_api_key

    def gather_new_box_office_hits(self):
        """
        Gather Box office links, web links, and ratings of each movie

        :return: Dictionary of Movie Name => imdb web links
        """
        url_content = urllib.request.urlopen(self.url_box_office_link).read()
        soup = BeautifulSoup(url_content, 'html.parser')

        title_elements = soup.select('td.titleColumn')

        if not len(title_elements) > 0:
            print('ERROR: We found no movies on webpage %s. You may need update this link!' % self.url_box_office_link)
            exit(1)

        for elem in title_elements:
            movie_name = elem.a.get_text()
            # Check if we already processed this movie in previous run
            if movie_name not in self._seen_movies.keys():
                self.add_movie_data(movie_name, {'url': 'https://www.imdb.com/%s' % elem.a.get('href')})

        # Gather movie ratings
        self._get_ratings()

        return self._top_box_office_dict

    def _get_ratings(self):
        """
        Gather votes and ratings for each movie given by gather_new_box_office_hits

        :return: Dictionary of 'Movie Name' => 'url' = imdb web links
                                            => 'rating' = rating number 1-10
                                            => 'votes' = votes for movie
        """

        top_box_office_list_copy = self._top_box_office_dict.copy()

        for movie_name, url_dict in top_box_office_list_copy.items():
            self.get_rating(movie_name, url_dict['url'])

        return self._top_box_office_dict

    def get_rating(self, movie_name, url, add_to_db=True):
        """
        Gather votes, ratings, and categories for a single movie given and add to db with the exception of ones on
        the category blacklist

        :param movie_name: Name of movie
        :param url: imdb url of movie
        :param add_to_db: True = add to database, False = don't add to db(mostly for debugging)
        """
        url_content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(url_content, 'html.parser')

        movie_rating = soup.find(itemprop="ratingValue").get_text()
        movie_votes = soup.find(itemprop="ratingCount").get_text()

        cat_dev_subtext = soup.select('div.subtext')
        cat_movie_links = cat_dev_subtext[0].find_all('a', {'href': re.compile(r"/search/title\?genres")})

        movie_categories = []
        for cat_link in cat_movie_links:
            movie_categories.append(cat_link.get_text())

        if add_to_db:
            cat_blacklisted = set(self.cat_blacklist).intersection(movie_categories)
            # If category is not in the blacklist, then process add it. Otherwise remove it
            if not cat_blacklisted:
                self.add_movie_data(movie_name,
                                    {'rating': movie_rating, 'votes': movie_votes, 'categories': movie_categories})
            else:
                print("Ignoring movie: %s. It's categories: %s are on the blacklist." % (movie_name, cat_blacklisted))
                del self._top_box_office_dict[movie_name]

    def add_movie_data(self, movie_name, movie_data=None):
        """
        Adds data to Movie dictionary structure such as url, rating, votes, etc...

        :param movie_name: Name of movie used as main key for dictionary
        :param movie_data: A dictionary to add under ex:  'Movie Name' => 'url' = imdb web links
                                                                 => 'rating' = rating number 1-10
                                                                 => 'votes' = votes for movie
        :return: Movie dictionary of movies to be checked
        """

        if movie_data is None:
            movie_data = {}
        for m_key, m_value in movie_data.items():
            # Check if movie already in movie dictionary
            if movie_name in self._top_box_office_dict.keys():
                # If movie already exists update movie data
                self._top_box_office_dict[movie_name][m_key] = m_value
            else:
                # If movie not exists, then add it
                self._top_box_office_dict[movie_name] = movie_data

        return self._top_box_office_dict

    def print_movie_matches(self):
        """ Print Movies that made our vote / rating cut and the ones that did not """
        print('\n*****Movies higher than %s Rating and higher than %s Votes*****' % (
            self.lowest_rating, self.lowest_votes))
        (movies_matched, movies_too_low) = self.get_matched_movies()

        for movie_name, m_data in movies_matched.items():
            print('Movie: %s, Rating: %s, Votes: %s' % (movie_name, m_data['rating'], m_data['votes']))
            self.set_movie_notified([movie_name])

        print('\n\n*****Movies with not enough votes or high enough ratings*****')
        for movie_name, m_data in movies_too_low.items():
            print('Movie: %s, Rating: %s, Votes: %s' % (movie_name, m_data['rating'], m_data['votes']))

    @staticmethod
    def get_float_int(number):
        """
        Remove commas, $, or anything none numeric, so that it can be converted to an int or float

        :param number: Number that contains
        :return: Integer or float representation of the number given in the parameter
        """
        real_number = ''.join(c for c in str(number) if c.isnumeric() or c == '.')
        if '.' in real_number:
            return float(real_number)
        else:
            return int(real_number)

    def set_movie_notified(self, movie_names=None):
        """ Saves movies to a sqlite database file set by self.db_file

        :param movie_names: Movie names to add to previously notified database
        """

        if movie_names is None:
            movie_names = []
        for movie_name in movie_names:
            conn = None
            try:
                conn = sqlite3.connect(self.db_file)
                c = conn.cursor()
                c.execute(
                    '''CREATE TABLE IF NOT EXISTS log (id integer PRIMARY KEY, movie_name text NOT NULL, created_at 
                    timestamp);''')
                c.execute('SELECT * FROM log WHERE movie_name=?', (movie_name,))
                movie_row = c.fetchone()

                # If movie_name doesn't exist in log table
                if movie_row is None:
                    c.execute("INSERT INTO log(movie_name, created_at) VALUES(?, ?)", (movie_name, datetime.now(),))

                conn.commit()
            except (sqlite3.Error, sqlite3.IntegrityError) as e:
                print(e)
            finally:
                if conn:
                    conn.close()

    def load_movie_data(self):
        """
        Loads movies from database file self.db_file into self.seen_movies

        :return: Dictionary of movies processed in previous run set to True
        """
        seen_movies = {}
        conn = None
        # Only try to load db if the file is there
        if Path(self.db_file).exists():
            try:
                conn = sqlite3.connect(self.db_file)
                c = conn.cursor()
                c.execute('SELECT movie_name FROM log')
                rows = c.fetchall()
                for row in rows:
                    seen_movies[row[0]] = True
            except sqlite3.OperationalError as e:
                print("ERROR: Table or Database probably doesn't exist Error: ", e)
            finally:
                if conn:
                    conn.close()

        return seen_movies

    def get_matched_movies(self):
        """
        Create 2 dictionaries. 1 of movies that meet our required rating and 1 of movies that don't meet our
        requirements. Also get matched and too low count

        :return: dictionary of matched movies and dictionary with ratings/votes of too low movies
        """
        movies_too_low = {}
        movies_matched = {}
        self.matched_count = 0
        self.too_low_count = 0

        for movie_name, m_data in self._top_box_office_dict.items():
            if self.get_float_int(m_data['rating']) >= self.get_float_int(
                    self.lowest_rating) and self.get_float_int(
                m_data['votes']) >= self.get_float_int(self.lowest_votes):
                self.matched_count += 1
                movies_matched[movie_name] = m_data
            else:
                self.too_low_count += 1
                movies_too_low[movie_name] = m_data

        return movies_matched, movies_too_low

    def gen_notification_msg(self):
        """
        Generate the message to send for notification method

        :rtype: int
        :return: Number of movie matches with enough votes & ratings
        """
        matched_count = 0
        if self.notify_msg is None:
            msg = '\n*****Movies higher than %s Rating and higher than %s Votes*****\n\n' % (
                self.lowest_rating, self.lowest_votes)

            (movies_matched, movies_too_low) = self.get_matched_movies()

            matched_count = 0
            for movie_name, m_data in movies_matched.items():
                matched_count += 1
                msg += '%i. %s, Rating: %s, Votes: %s\n' % (
                    matched_count, movie_name, m_data['rating'], m_data['votes'])
                self.set_movie_notified([movie_name])

            self.notify_msg = msg

        return matched_count

    def notify_pushbullet(self, device='all'):
        """
        Notify a pushbullet device of movies that exceed imdb ratings/votes

        :param device: Pushbullet device to send to ex: chrome. Default is to send to all devices
        """

        matched_count = self.gen_notification_msg()

        # Only notify if we have matches
        if matched_count > 0:
            pb = Pushbullet(self.pushbullet_api_key)
            if device.lower() == 'all':
                pb.push_note('Top Box Office Movie Alert', body=self.notify_msg)
            else:
                pb.push_note(title='Top Box Office Movie Alert', body=self.notify_msg, device=device)


class ImdbSearcherScheduler(ImdbSearcher):
    """
    Runs ImdbSearcher ever X amount of hours
    """

    def __init__(self, lowest_rating, lowest_votes, cat_blacklist=None, db_file=None, pushbullet_api_key=None,
                 url_box_office_link=r'https://www.imdb.com/chart/boxoffice?ref_=nv_ch_cht_2', hours=24):
        super().__init__(lowest_rating, lowest_votes, cat_blacklist, db_file, pushbullet_api_key=pushbullet_api_key,
                         url_box_office_link=url_box_office_link)
        self.scheduler = BackgroundScheduler()
        self.job_id = self.scheduler.add_job(self.job, 'interval', hours=hours)

    def start(self):
        """
        Start Scheduler to run task ever self.hours hours
        """
        self.job()
        self.scheduler.start()

    def stop(self):
        """
        Stop the scheduled task
        """
        self.scheduler.shutdown(wait=False)

    def job(self):
        """
        Job to run for Scheduler
        """
        self.gather_new_box_office_hits()
        self.get_matched_movies()
        if self.matched_count > 0:
            if self.pushbullet_api_key is not None:
                self.notify_pushbullet()
