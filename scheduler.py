import schedule
import scraper


def run_jobs():
    # On scheduler start, update all collections
    scraper.get_records()
    scraper.get_results()
    scraper.get_athletes()
    scraper.get_contests()

    # Update at 11:59 everyday
    schedule.every().day.at("23:59").do(scraper.get_records)
    schedule.every().day.at("23:59").do(scraper.get_results)
    schedule.every().day.at("23:59").do(scraper.get_athletes)
    schedule.every().day.at("23:59").do(scraper.get_contests)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    run_jobs()
