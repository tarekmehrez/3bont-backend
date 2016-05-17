"""
Contains the InstagramCrawler class as part of the crawler package.
"""
from instagram.client import InstagramAPI
from talata_bont_backend.util import log


log.init_logger()
logger = log.get_logger()


class InstagramCrawler(object):

    """
    Crawl data in mentioned instagram accounts.
    """

    def __init__(self, access_token, client_secret):
        """
        Init instagram crawler, and the api object.

        Args:
            access_token (str): instagram api access token
            client_secret (str): instagram api secret client
        """
        self._api = InstagramAPI(
            access_token=access_token,
            client_secret=client_secret)

    def fetch_ids(self, accounts):
        """
        Given instagram accounts, get their ids.

        accounts (list): instagram usernames
        """
        logger.info('fetching instagram IDs')

        users = {}

        accounts = list(set(accounts))

        for account in accounts:
            logger.debug('fetching id for %s', account)
            user_list = self._api.user_search(account)

            for user in user_list:
                if user.username == account:
                    users[account] = {}
                    users[account]['id'] = user.id
                    users[account]['image'] = user.profile_picture

        return users

    def run(self, users):
        """
        Get all fetched images.

        Args:
            users (dict): instagram user dicts in the following format:
            {
            username:
                {
                id:
                image
                }
            }
        Returns:
            list: fetched images
        """
        self._user_dicts = users
        fetched_images = []

        for user in self._user_dicts:
            fetched_for_user = self._fetch_for_user(user)
            fetched_images.append(fetched_for_user)

    def _fetch_for_user(self, username):
        """
        Given a user, get recent data on his profile.

        Args:
            username (str)

        Returns:
            list: fetched images
        """
        logger.debug('retrieving data for %s', str(username))

        recent_media, next_ = self._api.user_recent_media(
            user_id=self._user_dicts[username]['id'])

        fetched_images = []
        for media_item in recent_media:
            parsed_item = self._parse_media_item(media_item, username)

            fetched_images.append(parsed_item)

        return fetched_images

    def _parse_media_item(self, media_item, username):
        """
        Parse media object.

        Args:
            media_item (obj): instagram media object
            username (str)

        Returns:
            dict: parsed media_item item
        """
        parsed_media_item = {}

        parsed_media_item['account'] = username
        parsed_media_item['account_image'] = self._user_dicts[
            username]['image']

        if media_item.caption:
            parsed_media_item['caption'] = media_item.caption.text

        parsed_media_item['lang'] = 'en'
        parsed_media_item['date'] = media_item.created_time
        parsed_media_item['src'] = 'instagram'

        parsed_media_item['tags'] = []
        for tag in media_item.tags:
            parsed_media_item['tags'].append(str(tag).split(' ')[1])

        parsed_media_item['url'] = media_item.link
        parsed_media_item['type'] = media_item.type

        if media_item.type == 'image':
            parsed_media_item['img_vid_src'] = media_item.images[
                'standard_resolution'].url
        else:
            parsed_media_item['img_vid_src'] = media_item.videos[
                'standard_resolution'].url

        parsed_media_item['likes'] = media_item.like_count
        parsed_media_item['media_id'] = media_item.id

        return parsed_media_item
