from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events  # , EventData, EventMetrics
from linkedin_jobs_scraper.query import Query  # , QueryOptions, QueryFilters
# from linkedin_jobs_scraper.filters import (
#     RelevanceFilters,
#     TimeFilters,
#     TypeFilters,
#     ExperienceLevelFilters,
#     OnSiteOrRemoteFilters
# )

from skillixir.logging import get_logger


__all__ = ['Scraper']

logger = get_logger(__name__)


class Scraper:
	def __init__(
		self,
		sleep_time: float = 1.0,
		page_load_timeout: int = 60,
		on_data_callback: callable = None,
		on_error_callback: callable = None,
		on_end_callback: callable = None,
	):
		self.fp = open('/var/tmp/skillixir_data.json', 'w')
		self.scraper = LinkedinScraper(
			chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
			chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
			chrome_options=None,  # Custom Chrome options here
			headless=True,  # Overrides headless mode only if chrome_options is None
			max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
			slow_mo=sleep_time,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
			page_load_timeout=page_load_timeout,  # Page load timeout (in seconds)
		)

		self.scraper.on(Events.DATA, on_data_callback or self.__default_data_callback)
		self.scraper.on(Events.ERROR, on_error_callback or self.__default_error_callback)
		self.scraper.on(Events.END, on_end_callback or self.__default_end_callback)

	def __del__(self):
		self.fp.close()

	def __default_data_callback(self, data):
		logger.info(
			f'Scraped {data.title} {data.company} {data.company_link} {data.date} {data.link} {data.insights} {len(data.description)}'
		)
		data_dict = data._asdict()
		self.fp.write(f'{data_dict}\n')

	def __default_error_callback(self, error):
		logger.error(f'{error}')

	def __default_end_callback(self):
		logger.info('Scraper finished')

	def run(self, query: Query):
		self.scraper.run(queries=[query])
