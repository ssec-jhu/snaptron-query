import httpx
import pandas as pd
from io import StringIO
from snaptron_query.app import exceptions


class SnaptronClientManager:
    def __init__(self, url):

        self.url = url
        # TODO: SnaptronClientManager: verify URL?
        # TODO: SnaptronClientManager: add a results>1 restriction to reduce the data returned... must test performance

    def run_query_sync(self):
        """
            Will run the url and return the response
            :return: the httpx response
        """
        if self.url:
            resp = httpx.get(self.url)
            if resp.status_code == 200:  # OK
                return resp
            else:  # 404?
                raise exceptions.BadURL

    def get_query_results_dataframe(self):
        """
            Will run the url and return the response
            :return: the result of the snaptron web interface converted into a dataframe
        """
        url_response = self.run_query_sync()
        data_bytes = url_response.read()
        if data_bytes:
            content_string = data_bytes.decode("utf-8")
            df = pd.read_csv(StringIO(content_string), sep='\t')
            return df
        else:
            raise exceptions.EmptyResponse
