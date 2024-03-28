import collections

from snaptron_query.app import exceptions, global_strings as gs, query_junction_inclusion as jiq


class GeneExpressionQueryManager:
    def __init__(self):
        self.rail_id_dictionary = collections.defaultdict(int)
        self.normalization_factor_table = collections.defaultdict(int)
        self.gathered_rail_id_meta_data_and_counts = []
        self.normalize_counts = False

    def setup_normalization_data(self, gene_id_norm, df_snaptron_results_norm):
        row_df = df_snaptron_results_norm.loc[
            df_snaptron_results_norm[gs.snpt_col_gene_id].str.contains(gene_id_norm)]

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

    def setup_normalization_data_method_2(self, gene_id_norm, df_snaptron_results_norm, df_meta_data):

        # extract the row with the normalization gene ID
        row_df = df_snaptron_results_norm.loc[
            df_snaptron_results_norm[gs.snpt_col_gene_id].str.contains(gene_id_norm)]

        if row_df.empty:
            raise exceptions.GeneNotFound

        study_dictionary = collections.defaultdict(list)
        # extract the 'sample' column form the row this is where all the samples and their count is
        gene_samples = (row_df['samples']).tolist()
        for sample in gene_samples:
            # samples are separated by commas then each sample is separated with a colon from its count as railID:count
            for each_sample in sample.split(','):
                if each_sample:
                    (rail_id, count) = jiq.split_and_cast(each_sample)
                    try:  # you need the try because railID may not be in the metadata
                        # get the study title for this rail id
                        study = (df_meta_data.loc[rail_id])['study']
                        t = (rail_id, count)
                        study_dictionary[study].append(t)
                    except KeyError:
                        # TODO: look into the rail ids that are not found in the meta data file.
                        pass

        study_max_count_dict = collections.defaultdict(int)
        for study in study_dictionary.keys():
            # calculate the max count for each list
            max_value = max(d[1] for d in study_dictionary[study])
            study_max_count_dict[study] = max_value

        # Now divide each rail id's count by the max associated with its study to normalize the count per study max.
        for study in study_dictionary.keys():
            max_value = study_max_count_dict[study]
            for item in study_dictionary[study]:
                rail_id = item[0]
                raw_count = item[1]
                factor = raw_count / max_value
                if rail_id not in self.normalization_factor_table:
                    self.normalization_factor_table[rail_id] = factor
                else:
                    print("ERROR: why are we here, can a similar rail id come from different samples???")
                    pass

        self.normalize_counts = True
        return

    def setup_normalization_data_method_2_opt(self, gene_id_norm, df_snaptron_results_norm, df_meta_data):

        # extract the row with the normalization gene ID
        row_df = df_snaptron_results_norm.loc[
            df_snaptron_results_norm[gs.snpt_col_gene_id].str.contains(gene_id_norm)]

        if row_df.empty:
            raise exceptions.GeneNotFound

        study_dictionary = collections.defaultdict(list)
        # Extract the 'sample' column from the DataFrame
        gene_samples = row_df['samples'].tolist()

        # if I convert it to a dictionary, instead of using a dataframe there is a big performance boost
        meta_data_dict = df_meta_data['study'].to_dict()

        for sample in gene_samples:
            # Samples are separated by commas, each sample is separated with a colon from its count as railID:count
            for each_sample in sample.split(','):
                if each_sample:
                    rail_id, count = jiq.split_and_cast(each_sample)
                    study = meta_data_dict.get(rail_id)
                    if study:
                        study_dictionary[study].append((rail_id, count))

        for study in study_dictionary:
            # calculate the max count for each list
            max_value = max(d[1] for d in study_dictionary[study])
            # Now divide each rail id's count by the max associated with its study to normalize the count per study max.
            for rail_id, raw_count in study_dictionary[study]:
                factor = raw_count / max_value
                # self.normalization_factor_table.setdefault(rail_id, factor)
                self.normalization_factor_table[rail_id] = factor

        self.normalize_counts = True
        return

    def _gather_samples_rail_id_and_counts(self, samples):
        for gene_samples in samples:
            # samples are separated by commas then each sample is separated with a colon from its count as railID:count
            for each_sample in gene_samples.split(','):
                if each_sample:
                    (rail_id, raw_count) = jiq.split_and_cast(each_sample)
                    # keep the item in a defaultdict(int)
                    self.rail_id_dictionary[rail_id] = raw_count

    def _gather_rail_id_meta_data(self, rail_id, df_meta_data):
        """Given the metadata for the compilation and the rail ids,function extracts the related metadata for
        rail ids and any other quantities calculated
        """
        # look up the rail id and extract the information
        try:
            # gather the metadata associated with this rail id
            meta_data = (df_meta_data.loc[rail_id]).to_dict()

            # add the raw count data
            raw_count = self.rail_id_dictionary[rail_id]
            meta_data[gs.table_geq_col_raw_count] = raw_count

            # add the normalized count if needed
            if self.normalize_counts:
                # if rail id is in the table then compute the normalized count
                # if it's not in the factor table, then set it as -1
                # using get method will return -1 if the rail_id is not found
                factor = self.normalization_factor_table.get(rail_id, -1)
                meta_data[gs.table_geq_col_factor] = factor
                meta_data['normalized_count'] = raw_count / factor if factor != -1 else -1

            # add the rail id information
            meta_data[gs.snpt_col_rail_id] = rail_id

            # append to the rest of the gathered data
            self.gathered_rail_id_meta_data_and_counts.append(meta_data)

        except (KeyError, IndexError):
            # TODO: look into the rail ids that are not found in the meta data file.
            # TODO: IT MUST BE IN THE META FILE, is this a snaptron error? discuss with PI
            # print(f"{rail_id} not in meta data file.  Moving on to the next iteration.")
            # code must continue and not stop
            pass

    def run_gene_expression_query(self, gene_id_query, df_snaptron_results_query, df_meta_data):
        # extract the row in the results that matches the query gene ID
        row_df = df_snaptron_results_query.loc[
            df_snaptron_results_query[gs.snpt_col_gene_id].str.contains(gene_id_query)]

        if row_df.empty:
            raise exceptions.GeneNotFound

        # extract the 'sample' column form the row this is where all the rail_id:count are
        samples = (row_df['samples']).tolist()
        self._gather_samples_rail_id_and_counts(samples)

        for rail_id in self.rail_id_dictionary:
            self._gather_rail_id_meta_data(rail_id, df_meta_data)

        return self.gathered_rail_id_meta_data_and_counts
