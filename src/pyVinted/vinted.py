from pyVinted.scraper import Scraper
from pyVinted.requester import requester

class Vinted:
    """
    This class is built to connect with the pyVinted API.

    It's main goal is to be able to retrieve items from a given url search.\n

    """

    def __init__(self, locale="fr", proxy=None):
        """
        Args:
            proxy : proxy to be used to bypass vinted's limit rate
        """

        if proxy is not None:
            requester.session.proxies.update(proxy)

        self.scraper = Scraper(locale=locale)
