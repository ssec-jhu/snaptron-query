import collections

from snaptron_query.app import exceptions, utils
from snaptron_query.app import global_strings as gs
from snaptron_query.app import query_junction_inclusion as jiq


class GeneExpressionQueryManager:
    def __init__(self):
        self.rail_id_dictionary = collections.defaultdict(int)
        self.normalization_factor_table = collections.defaultdict(int)
        self.normalize_counts = False

    def setup_normalization_data_method(self, gene_id_norm, df_snaptron_results_norm, meta_data_dict):
        # extract the row with the normalization gene ID
        row_df = df_snaptron_results_norm.loc[df_snaptron_results_norm[gs.snpt_col_gene_id].str.contains(gene_id_norm)]

        if row_df.empty:
            raise exceptions.NormalizationGeneNotFound

        study_dictionary = collections.defaultdict(list)

        # if I convert it to a dictionary, instead of using a dataframe there is a big performance boost
        # meta_data_dict = meta_data_df['study'].to_dict()
        meta_data_dict = {
            key: inner_dict["study"] for key, inner_dict in meta_data_dict.items() if "study" in inner_dict
        }

        for sample_set in row_df[gs.snpt_col_samples]:  # list_of_sample_count_pairs
            # Samples are separated by commas, each sample is separated with a colon from its count as railID:count
            for rail_id_count_pair in sample_set.split(","):
                if rail_id_count_pair:
                    rail_id, count = jiq.split_and_cast(rail_id_count_pair)
                    study = meta_data_dict.get(rail_id)
                    if study:
                        study_dictionary[study].append((rail_id, count))

        for study_name, study_samples in study_dictionary.items():
            max_value = max(d[1] for d in study_samples)
            # Now divide each rail id's count by the max associated with its study to normalize the count per study max.
            for rail_id, raw_count in study_samples:
                factor = raw_count / max_value
                self.normalization_factor_table[rail_id] = factor

        self.normalize_counts = True
        return

    def run_gene_expression_query(self, gene_id_query, df_snaptron_results_query, meta_data_dict):
        gathered_rail_id_meta_data_and_counts = []

        # extract the row in the results that matches the query gene ID
        row_df = df_snaptron_results_query.loc[
            df_snaptron_results_query[gs.snpt_col_gene_id].str.contains(gene_id_query)
        ]

        if row_df.empty:
            raise exceptions.QueryGeneNotFound

        # extract the 'sample' column form the row this is where all the rail_id:count are
        for sample_set in row_df[gs.snpt_col_samples]:
            # samples are separated by commas then each sample is separated with a colon from its count as railID:count
            for rail_id_count_pair in sample_set.split(","):
                if rail_id_count_pair:
                    (rail_id, raw_count) = jiq.split_and_cast(rail_id_count_pair)
                    try:
                        # meta_data = collections.defaultdict(list)
                        meta_data = meta_data_dict[rail_id]
                        meta_data[gs.snpt_col_rail_id] = rail_id
                        meta_data[gs.table_geq_col_raw_count] = raw_count
                        meta_data[gs.table_geq_col_log_2_raw] = round(utils.log_2_plus(raw_count), 4)
                        if self.normalize_counts:
                            # if rail id is in the table then compute the normalized count
                            # if it's not in the factor table, then set it as -1
                            # using get method will return -1 if the rail_id is not found
                            factor = self.normalization_factor_table.get(rail_id, -1)
                            meta_data[gs.table_geq_col_factor] = factor
                            normalized_count = raw_count / factor if factor != -1 else -1
                            meta_data[gs.table_geq_col_norm_count] = normalized_count
                            meta_data[gs.table_geq_col_log_2_norm] = (
                                (round(utils.log_2_plus(normalized_count), 4)) if factor != -1 else -1
                            )

                        gathered_rail_id_meta_data_and_counts.append(meta_data)
                    except (KeyError, IndexError):
                        pass

        return gathered_rail_id_meta_data_and_counts
