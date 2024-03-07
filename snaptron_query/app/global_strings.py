"""General Strings"""

tab_jiq = "Junction PSI Query"
tab_geq = "Gene Expression Query"

"""Strings used in the Junction Inclusion Query Form"""

compilation_srav3h = 'SRAv3h'
compilation_gtexv2 = 'GTEXv2'
compilation_tcgav2 = 'TCGAv2'
compilation_srav1m = 'SRAv1m'
compilation_names_dict = {
    compilation_srav3h: f'human ({compilation_srav3h})',
    compilation_gtexv2: f'human ({compilation_gtexv2})',
    compilation_tcgav2: f'human ({compilation_tcgav2})',
    compilation_srav1m: f'mouse ({compilation_srav1m})',
}
drop_compilation = 'Select the organism of interest'
drop_compilation_placeholder = 'Select a compilation'
jiq_form_title = 'Junction Information'
jiq_graphs_group_title = 'Graphs'
button_download = 'Download'
switch_log = 'Log₂(y)'
switch_violin = 'Violin Mode'
switch_lock = 'Lock Table with Graphs'
button_add_junction = 'Add Junction'
button_run = 'Calculate PSI'
input_inc_placeholder = 'ex: chr19:4491836-4492014'
input_inc_txt = 'Inclusion Junction'
input_exc_placeholder = 'ex: chr19:4491836-4493702'
input_exc_txt = 'Exclusion Junction'
input_junction_txt_list = ['Junction 1', 'Junction 2', 'Junction 3', 'Junction 4', 'Junction 5']

"""Strings used in the Graphs and Tables """

histogram_title = 'PSI Histogram'
boxplot_label = 'Rail ID'
box_plot_title = 'PSI Box Plot'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            Gene Expression Query 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
geq_form_title = 'Gene Information'
geq_query = 'Query Information'
geq_normalized_info = 'Normalization Information'
geq_gene_id = 'Gene ENSG ID'
geq_gene_coord = 'Gene Coordinates'
geq_normalized = 'Normalized GEX'
geq_button_run = 'Calculate GEX'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Strings beyond this point are related to the snaptron interface
    DO NOT TOUCH if you don't know what you are doing
    Strings here exists solely for the purpose of potential changes in the 
    snaptron client web interface and its internal data
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
snaptron_col_rail_id = 'rail_id'
snaptron_col_external_id = 'external_id'
srav3h_meta_data_required_list = [snaptron_col_rail_id, snaptron_col_external_id,
                                  'study', 'study_title', 'library_layout',
                                  'sample_description', 'sample_name', 'sample_title']

srav1m_meta_data_required_list = srav3h_meta_data_required_list  # SRA mouse and SRA human are similar

tcgav2_meta_data_required_list = [snaptron_col_rail_id,
                                  "tcga_barcode", "study", "gdc_cases.project.name",
                                  "gdc_cases.project.primary_site", "cgc_sample_sample_type",
                                  "gdc_state", "gdc_cases.demographic.race",
                                  "gdc_cases.demographic.ethnicity", "gdc_cases.diagnoses.tumor_stage",
                                  "gdc_cases.diagnoses.vital_status", "gdc_cases.samples.oct_embedded",
                                  "gdc_cases.samples.is_ffpe", "gdc_cases.samples.sample_type",
                                  "cgc_sample_country_of_sample_procurement", "cgc_case_tumor_status",
                                  "cgc_drug_therapy_pharmaceutical_therapy_type", "cgc_follow_up_tumor_status"]

gtexv2_meta_data_required_list = [snaptron_col_rail_id, "run_acc", "study", "SEX", "AGE", "SAMPID", "SMTS", "SMTSD"]

table_jiq_col_inc = 'inc'
table_jiq_col_exc = 'exc'
table_jiq_col_total = 'total'
table_jiq_col_psi = 'psi'
