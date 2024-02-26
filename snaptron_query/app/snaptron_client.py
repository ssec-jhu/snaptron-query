import httpx
import pandas as pd
from io import BytesIO
from snaptron_query.app import exceptions
import re


class SnaptronClientManager:
    def __init__(self):
        self._host = 'https://snaptron.cs.jhu.edu'
        self._url = ''

    def get_url(self):
        return self._url

    @staticmethod
    def verify_coordinates(coordinates):
        # TODO: this is a first step. More will be added as I get more info from PI
        pattern = r'chr\d{0,2}:\d{0,9}-\d{0,9}$'
        if not re.match(pattern, (str(coordinates))):
            return False

        return True

    def create_junction_inclusion_url(self, compilation, junction_coordinates):
        """create the junction inclusion query"""

        self._url = f'{self._host}/{str(compilation).lower()}/snaptron?regions={str(junction_coordinates)}'
        # temp_url = 'https://snaptron.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'

    def create_gene_expression_url(self, compilation, junction_coordinates):
        """create the gene expression query"""

        self._url = f'{self._host}/{str(compilation).lower()}/genes?regions={junction_coordinates}'
        # temp_url = 'https://snaptron.cs.jhu.edu/srav3h/genes?regions=chr1:11013716-11024183'

    def get_query_results_dataframe(self):
        """Will run the url and return the response
        :return: the result of the snaptron web interface converted into a dataframe
        """
        if self._url:
            resp = httpx.get(self._url)
            if resp.status_code == 200:  # OK
                data_bytes = resp.read()
                if data_bytes:
                    df = pd.read_csv(BytesIO(data_bytes), sep='\t')
                    return df
                else:
                    raise exceptions.EmptyResponse
            else:  # 404?
                raise exceptions.BadURL
