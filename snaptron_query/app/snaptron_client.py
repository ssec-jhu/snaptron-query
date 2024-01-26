import httpx
import pandas as pd
from io import StringIO


class SnaptronClientManager:
    def __init__(self, url):

        self.url = url
        # TODO: SnaptronClientManager: verify URL?
        # TODO: SnaptronClientManager: remember to remove hardcoded URL
        # TODO: SnaptronClientManager: add a results>1 restriction to reduce the data returned... must test performance

    def get_url(self):
        return self.url

    # TODO: make get gene expression url

    def run_query_sync(self):
        url = self.get_url()
        # TODO: run_query_sync: if httpx.get fails we need to catch the error
        if url:
            resp = httpx.get(url)
            if resp.status_code == 200:  # OK
                return resp

    def get_query_results_dataframe(self):

        url_response = self.run_query_sync()

        # TODO: get_query_results_dataframe: multiple error checking is required
        data_bytes = url_response.read()
        if data_bytes:
            content_string = data_bytes.decode("utf-8")
            df = pd.read_csv(StringIO(content_string), sep='\t')
            return df

    # TODO: get_query_results_dataframe_json: test this function, is it faster? better?
    # def get_query_results_dataframe_json(self):
    #
    #     url_response = self.run_query_sync()
    #
    #     json_data = url_response.json()
    #     # Create a DataFrame from the JSON data
    #     df = pd.DataFrame(json_data)
    #     return df
