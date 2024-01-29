import decimal
import numpy as np
import pandas as pd
import global_strings
# TODO: rail id dictionary should become a member of the class

# 1: normal way
# 2: using low memory flag,
# 3: using required columns only
readingCSV = 3
# setting this to 1 is definitely faster
indexing = 1

# 1: normal for loop,
# 2: lookup via keys
lookupInDictionary = 1

# 1 ND 3 SEEM SIMILAR? THE DATAFRAME CREATION STEP IS INSIGNIFICANT
workingList = 1

log_time = 0


def read_meta_data_file(compilation):
    # TODO: this function should be called upon app init put it there
    # TODO: verify that the file path is correct and that the file exists, if not throw an exception
    # TODO: file path must not be static
    # TODO: add the other compilations meta data files into folder
    # TODO: probably all meta data files should be read once upon app fireup, put this in global space
    file = f'data/samples_{compilation}.tsv'

    if readingCSV == 1:
        df = pd.read_csv('data/samples_SRAV3H.tsv', sep='\t')
    elif readingCSV == 2:  # this made it slower
        df = pd.read_csv('data/samples_SRAV3H.tsv', sep='\t', low_memory=False)  # will remove the complaints

    elif readingCSV == 3:  # winner
        req_cols = global_strings.meta_data_required_list
        df = pd.read_csv('data/samples_SRAV3H.tsv', sep='\t', usecols=req_cols)

    elif readingCSV == 4:  # this actually made it slower!
        req_cols = global_strings.meta_data_required_list
        df = pd.read_csv('data/samples_SRAV3H.tsv', sep='\t', usecols=req_cols,
                         dtype={'rail_id': 'int64',
                                'external_id': 'string',
                                'study': 'string',
                                'study_title': 'string',
                                'library_layout': 'string'
                                })

    # ----------------------
    # resetting the index
    # ---------------------
    if indexing:
        df = df.set_index(global_strings.snaptron_col_rail_id)
        # print(df_samples.loc[135471]) # rail ID is an integer if it was a string you needed quotes
        # for railID in rail_id_dictionary:
        #    meta_data = df_samples.loc[int(railID)] # must cast to an int here because the data is not a string
        #    print('Lookup RailID: {}'.format(railID))
        #    print(meta_data['study_title'])
        #    #hmmm, cannot do meta_data['rail_id'] because the frame was indexed by this....what to do?

    return df


"""
    Module that processes the junction inclusion query given the dataframe output from snaptron
"""


class JunctionInclusionQueryManager:
    def __init__(self,
                 exclusion_start: int,
                 exclusion_end: int,
                 inclusion_start: int,
                 inclusion_end: int) -> None:

        self.exclusion_start = exclusion_start
        self.exclusion_end = exclusion_end
        self.inclusion_start = inclusion_start
        self.inclusion_end = inclusion_end
        self.rail_id_dictionary = dict()
        return

    def gather_rail_id_and_counts(self, samples, mark_in_or_ex):
        """
            Given the samples extracted for the junction,
            extract the rail id and count info from the data.
            If the sample is from an inclusion junction, mark it.
        """
        # samples  usually has 1 row, but just in case
        # I am putting it in a for loop
        for junction_samples in samples:
            # samples are separated by commas
            # then each sample is separated with a colon b=from its count
            js = junction_samples.split(',')
            for eachSample in js:
                # each sample in snaptron is set as railID:count
                if eachSample:
                    rail_id_count = eachSample.split(':')  # (railId, count)
                    rail_id = rail_id_count[0]
                    count = rail_id_count[1]
                    dict_value = {'count': count,
                                  'inc': mark_in_or_ex}

                    # keep the item in a  dictionary
                    if rail_id in self.rail_id_dictionary:
                        self.rail_id_dictionary[rail_id].append(dict_value)
                    else:
                        self.rail_id_dictionary[rail_id] = [dict_value]

    def __gather_rail_id_meta_data(self, df_meta_data, rail_id_meta_data_list, rail_id):
        """
            Given the metadata for the compilation and the rail ids,
            function extracts the related metadata for rail ids
        """
        # look up the rail id and extract the information
        try:
            # meta_data_series = get_meta_data_for_railID(df_samples, railID)
            if indexing:
                # with indexing, it will return a SERIES
                meta_data_series = df_meta_data.loc[int(rail_id)]  # NEED to cast to int or it won't work!
            else:
                # without indexing this returns a data FRAME
                df_data = df_meta_data.loc[df_meta_data['rail_id'] == int(rail_id)]
                meta_data_series = df_data.iloc[0]  # extract the only row, 0

            # TODO: move forward only if the rail id was found, throw exception otherwise,
            #  need to figure out how to catch the excpetions in the main layout in dash

            # TODO: this data will be different for different compilations
            # external_id, study, study_title = lookup_meta_data(meta_data_series)
            external_id = meta_data_series['external_id']
            study = meta_data_series['study']
            study_title = meta_data_series['study_title']

            counts = self.rail_id_dictionary[rail_id]
            inclusion_count = 0
            exclusion_count = 0
            psi = 0.0
            for c in counts:
                if c['inc'] == 'True':
                    inclusion_count = int(c['count'])
                if c['inc'] == 'False':
                    exclusion_count = int(c['count'])
            total_count = inclusion_count + exclusion_count

            # TODO: PSI calculation tolerance of 15? original code had this, ut now with ag grid it can be removed
            if total_count > 0:
                # calculate the percent spliced in
                psi = (100 * decimal.Decimal(inclusion_count)) / decimal.Decimal(total_count)
                psi = round(psi, 2)

                # TODO: finalize workingList after timing
                # TODO: append study_title as well, some bug here
                # TODO: maybe this setup should be a dictionary, will it be faster?
                # see: https://stackoverflow.com/questions/1316887/what-is-the-most-efficient-string-concatenation-method-in-python/24718551#24718551
                if workingList == 1:
                    data = f'{rail_id},{external_id},{study},{inclusion_count},{exclusion_count},{total_count},{psi}'
                    rail_id_meta_data_list.append(data)
                elif workingList == 2:
                    data = [f'{rail_id},{study},{inclusion_count}']
                    rail_id_meta_data_list.append(data)
                elif workingList == 3:
                    r = f'{rail_id}'
                    s = f'{study}'
                    # st = f'{study_title}'
                    i = f'{inclusion_count}'
                    rail_id_meta_data_list.append(r)
                    rail_id_meta_data_list.append(s)
                    # myList.append(st)
                    rail_id_meta_data_list.append(i)
        except (KeyError, IndexError):
            # TODO: look into the rail ids that are not found in the meta data file.
            print(f"{rail_id} not in meta data file.  Moving on to the next iteration.")

        return rail_id_meta_data_list

    def run_junction_inclusion_query(self, df):
        """
            Given the snaptron interface results, this function calculates the Percent Spliced In  (PSI)
            given the inclusion junction and the exclusion junction
        """
        # TODO: GLOBAL: move all strings into a strings file
        exc_junctions_df = df.loc[(df['start'] == self.exclusion_start) & (df['end'] == self.exclusion_end)]
        inc_junctions_df = df.loc[(df['start'] == self.inclusion_start) & (df['end'] == self.inclusion_end)]

        # TODO: do I need to check for df size?

        # extract the 'sample' column form the row
        # this is where all the samples and their count is
        exclusion_junction_samples = (exc_junctions_df['samples']).tolist()
        inclusion_junction_samples = (inc_junctions_df['samples']).tolist()

        # Gather results in a dictionary. Samples that were extracted
        # as part of an inclusion junction are marked as 'true'
        # rail_id_dictionary = {}
        # rail_id_dictionary = self.gather_rail_id_and_counts(exclusion_junction_samples, 'False', rail_id_dictionary)
        # rail_id_dictionary = self.gather_rail_id_and_counts(inclusion_junction_samples, 'True', rail_id_dictionary)
        self.gather_rail_id_and_counts(exclusion_junction_samples, 'False')
        self.gather_rail_id_and_counts(inclusion_junction_samples, 'True')

        # TODO: GLOBAL: this function should be called in global space
        #  and its data frame passed in based on compilation. String should also be global
        df_meta_data = read_meta_data_file('srav3h')

        # this list will gather all the rail ids and their meta data
        rail_id_data_list = []
        if lookupInDictionary == 1:
            for rail_id in self.rail_id_dictionary:
                rail_id_data_list = self.__gather_rail_id_meta_data(df_meta_data, rail_id_data_list, rail_id)
        elif lookupInDictionary == 2:
            for rail_id in self.rail_id_dictionary.keys():
                rail_id_data_list = self.__gather_rail_id_meta_data(df_meta_data, rail_id_data_list, rail_id)
        elif lookupInDictionary == 3:
            keyList = list(self.rail_id_dictionary.keys())
            for rail_id in keyList:
                rail_id_data_list = self.__gather_rail_id_meta_data(df_meta_data, rail_id_data_list, rail_id)

        # create a dataframe form the list
        # TODO: column here will be different based on compilation -> maybe make that  function,
        # also used in gathering meta data
        try:
            if workingList == 1:
                split_data = [item.split(',') for item in rail_id_data_list]
                df_final = pd.DataFrame(split_data,
                                        columns=[global_strings.snaptron_col_rail_id, 'external_id', 'study', 'inc', 'exc', 'total', 'psi'])
                # df = pd.DataFrame(split_data)
            elif workingList == 2:
                split_data = [item[0].split(',') for item in rail_id_data_list]
                df_final = pd.DataFrame(split_data,
                                        columns=[global_strings.snaptron_col_rail_id, 'external_id', 'study', 'inc', 'exc', 'total', 'psi'])
            elif workingList == 3:
                reshaped_data3 = np.array(rail_id_data_list).reshape(-1, 3)  # 3 because there are 3 columns right now
                df_final = pd.DataFrame(reshaped_data3,
                                        columns=[global_strings.snaptron_col_rail_id, 'external_id', 'study', 'inc', 'exc', 'total', 'psi'])

            # TODO: column names will change based on compilation here too
            # convert the datatypes here so it's easy later
            df_final['psi'] = df_final['psi'].astype('float')
            df_final[global_strings.snaptron_col_rail_id] = df_final[global_strings.snaptron_col_rail_id].astype('int')
            df_final['inc'] = df_final['inc'].astype('int')
            df_final['exc'] = df_final['exc'].astype('int')
            df_final['total'] = df_final['total'].astype('int')

        except ValueError:
            stop = 1
            # TODO: do something if this is thrown

        return df_final
