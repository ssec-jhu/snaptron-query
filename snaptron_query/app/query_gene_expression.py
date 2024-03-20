import collections

from snaptron_query.app import exceptions, global_strings as gs, query_junction_inclusion as jiq


class GeneExpressionQueryManager:
    """Module that processes the junction inclusion query given the dataframe output from snaptron"""

    def __init__(self, gene_id):
        self._gene_id = gene_id
        self.rail_id_dictionary = collections.defaultdict(int)
        self.normalization_factor_table = collections.defaultdict(int)
        self.gathered_rail_id_meta_data_and_counts = []
        self.normalize_counts = False

    def setup_normalization_data(self, normalization_gene_id, df_normalization):
        row_df = df_normalization.loc[df_normalization[gs.snaptron_col_gene_id].str.contains(normalization_gene_id)]

        if row_df.empty:
            raise exceptions.GeneNotFound

        # extract the 'sample' column form the row this is where all the samples and their count is
        samples = (row_df['samples']).tolist()
        norm_gene_counts = collections.defaultdict(int)
        for gene_samples in samples:
            # samples are separated by commas then each sample is separated with a colon from its count as railID:count
            for each_sample in gene_samples.split(','):
                if each_sample:
                    (rail_id, count) = jiq.split_and_cast(each_sample)
                    norm_gene_counts[rail_id] = count

        max_count = max(norm_gene_counts.values())
        self.normalization_factor_table = {key: value / max_count for key, value in norm_gene_counts.items()}
        self.normalize_counts = True
        return

    def _gather_samples_rail_id_and_counts(self, samples):
        for gene_samples in samples:
            # samples are separated by commas then each sample is separated with a colon from its count as railID:count
            for each_sample in gene_samples.split(','):
                if each_sample:
                    (rail_id, count) = jiq.split_and_cast(each_sample)

                    # keep the item in a defaultdict(int)
                    self.rail_id_dictionary[rail_id] = count

    def _gather_rail_id_meta_data(self, rail_id, df_meta_data):
        """Given the metadata for the compilation and the rail ids,function extracts the related metadata for
        rail ids
        """
        # look up the rail id and extract the information
        try:
            # gather the metadata associated with this rail id
            meta_data = (df_meta_data.loc[rail_id]).to_dict()

            # add counts data
            raw_count = self.rail_id_dictionary[rail_id]
            meta_data[gs.table_geq_col_raw_count] = raw_count
            if self.normalize_counts:
                if rail_id in self.normalization_factor_table:
                    factor = self.normalization_factor_table[rail_id]
                    meta_data['factor'] = factor
                    meta_data['normalized_count'] = raw_count / factor

            # add the rail id information
            meta_data[gs.snaptron_col_rail_id] = rail_id

            # append to the rest of the data
            self.gathered_rail_id_meta_data_and_counts.append(meta_data)

        except (KeyError, IndexError):
            # TODO: look into the rail ids that are not found in the meta data file.
            # TODO: IT MUST BE IN THE META FILE, is this a snaptron error? discuss with PI
            # print(f"{rail_id} not in meta data file.  Moving on to the next iteration.")
            # code must continue and not stop
            pass

    def run_gene_expression_query(self, df, df_meta_data):
        row_df = df.loc[df[gs.snaptron_col_gene_id].str.contains(self._gene_id)]

        if row_df.empty:
            raise exceptions.GeneNotFound

        # extract the 'sample' column form the row this is where all the samples and their count is
        samples = (row_df['samples']).tolist()
        self._gather_samples_rail_id_and_counts(samples)

        for rail_id in self.rail_id_dictionary:
            self._gather_rail_id_meta_data(rail_id, df_meta_data)

        return self.gathered_rail_id_meta_data_and_counts
