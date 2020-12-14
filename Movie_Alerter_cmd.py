from lib.ImdbSearcherLib import ImdbSearcher, ImdbSearcherScheduler

"""
 1.search for box office movies on imdb
 2 check to see if their ratings & votes match our specifications
 3 report new movies that match our specifications
 4 eventually set them to auto download
 """


def main():
    """
    Commmand Line main fucnction
    """
    imdb_searcher = ImdbSearcher(2, '1', cat_blacklist=['Animation'], pushbullet_api_key='o.0nMJvY3uMwqnB89I4IQAkOcjPIzw2riZ')
    # imdb_searcher.get_rating('Onward', 'https://www.imdb.com/title/tt7146812/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f9f31d04-fc22-4d12-86b4-f46e25aa2f6f&pf_rd_r=5WGEFEMGTRFG9EVYFKBH&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=boxoffice&ref_=cht_bo_1', False)
    imdb_searcher.gather_new_box_office_hits()
    imdb_searcher.print_movie_matches()

def main_scheduler():
    imdb_scheduler = ImdbSearcherScheduler(2, '1', cat_blacklist=['Animation'], pushbullet_api_key='o.0nMJvY3uMwqnB89I4IQAkOcjPIzw2riZ')
    imdb_scheduler.start()

if __name__ == '__main__':
    #main()
    main_scheduler()
