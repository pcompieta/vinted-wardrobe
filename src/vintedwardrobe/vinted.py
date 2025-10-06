from vintedwardrobe.wardrobe import Wardrobe
from vintedwardrobe.requester import requester

class Vinted:
    """
    Access point to the 'vintedwardrobe' package.
    """

    def __init__(self, locale="fr", proxy=None):
        """
        Args:
            proxy : proxy to be used to bypass vinted's limit rate
        """

        if proxy is not None:
            requester.session.proxies.update(proxy)

        self.wardrobe = Wardrobe(locale=locale)
