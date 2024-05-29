import pandas as pd
from snaptron_query.app import utils, paths, global_strings as gs


def extract_meta_data_from_these_ids_only(meta_dict, rail_list):
    meta_list = []
    # extract the metadata for the rail_id provided in the list.
    for rail_id in rail_list:
        try:
            meta_data = meta_dict[rail_id]
            meta_data[gs.snpt_col_rail_id] = rail_id
            meta_list.append(meta_data)
        except KeyError:
            # you shouldn't come here but need to put this in case there is typo in the rail id provided
            print(f'Rail ID: {rail_id} was not in meta data.')
            pass

    return pd.DataFrame(meta_list)


def generate_samples_srav3h(output_filename):
    rail_list = [499887, 988942, 988956, 1641727, 1641757, 2109561, 4199971, 4200482, 1000010, 1745655, 1127039,
                 2171668, 2566685, 2566161, 988777, 2566328, 2566230, 988795, 491716, 245855, 2033434]
    pruned_file = extract_meta_data_from_these_ids_only(utils.read_srav3h(paths.srav3h_meta), rail_list)
    pd.DataFrame.to_csv(pruned_file, output_filename, sep='\t')


def generate_samples_gtexv2(output_filename):
    rail_list = [9914021, 9783109, 4530990, 4498305, 4399966, 4301657, 4236071, 2462190, 2216416, 2199960]
    pruned_file = extract_meta_data_from_these_ids_only(utils.read_gtexv2(paths.gtexv2_meta), rail_list)
    pd.DataFrame.to_csv(pruned_file, output_filename, sep='\t')


def generate_samples_tcgav2(output_filename):
    rail_list = [858212, 220457, 886326, 219485, 54627, 870564, 869858, 234844, 428819, 117036, 213532, 939128, 472121,
                 472122]
    pruned_file = extract_meta_data_from_these_ids_only(utils.read_tcgav2(paths.tcgav2_meta), rail_list)
    pd.DataFrame.to_csv(pruned_file, output_filename, sep='\t')


def generate_samples_srav1m(output_filename):
    rail_list = [3072016, 669879, 669871, 669863, 3466847, 668214, 957629, 2885847, 2885781, 213136]
    pruned_file = extract_meta_data_from_these_ids_only(utils.read_srav1m(paths.srav1m_meta), rail_list)
    pd.DataFrame.to_csv(pruned_file, output_filename, sep='\t')


def generate_samples():
    generate_samples_srav3h(output_filename='test_srav3h_samples.tsv')
    generate_samples_gtexv2(output_filename='test_gtexv2_samples.tsv')
    generate_samples_tcgav2(output_filename='test_tcgav2_samples.tsv')
    generate_samples_srav1m(output_filename='test_srav1m_samples.tsv')


if __name__ == "__main__":
    # this will generate a sample metadata file for all 4 compilations given the rail id in the lists provided
    # take the files generated files and put them in snaptron-query/app/tests/data/
    # these files are just a small sample set of the Gigabyte files used for the app itself which includes all samples
    generate_samples()
