from urllib.parse import urlparse


class URLComparator:

    def compare(self, staging_urls, production_urls):

        staging_paths = {
            urlparse(url).path
            for url in staging_urls
        }

        production_paths = {
            urlparse(url).path
            for url in production_urls
        }

        common_paths = staging_paths & production_paths

        staging_only = staging_paths - production_paths

        production_only = production_paths - staging_paths

        return {
            "common": common_paths,
            "staging_only": staging_only,
            "production_only": production_only
        }