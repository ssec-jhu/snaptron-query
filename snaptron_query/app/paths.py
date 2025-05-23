from pathlib import Path

# path to the directory where the metadata for the compilations reside
# switch to the first line for deployment and
# switch to the line below it for running locally
meta_data_directory = Path("/srv/nvme2/snaptron_data/snapmine_samples")
# meta_data_directory = Path(__file__).parent / 'data/'


# specify the file name to the metadata files for each compilation here
filename_srav3h = "srav3h_samples.tsv"
filename_gtexv2 = "gtexv2_samples.tsv"
filename_tcgav2 = "tcgav2_samples.tsv"
filename_srav1m = "srav1m_samples.tsv"
filename_encode = "encode1159_samples.tsv"

srav3h_meta = meta_data_directory / filename_srav3h
gtexv2_meta = meta_data_directory / filename_gtexv2
tcgav2_meta = meta_data_directory / filename_tcgav2
srav1m_meta = meta_data_directory / filename_srav1m
encode_meta = meta_data_directory / filename_encode
