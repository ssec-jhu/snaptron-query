"""General Strings"""

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """
            General
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
web_title = "SnapMine"
log_epsilon = 0.01
tab_jiq = "Junction PSI Query"
tab_geq = "Gene Expression Query"
graphs_group_title = "Graphs"

compilation_srav3h = "SRAv3h"
compilation_gtexv2 = "GTEXv2"
compilation_tcgav2 = "TCGAv2"
compilation_srav1m = "SRAv1m"
compilation_names_dict = {
    compilation_srav3h: f"human ({compilation_srav3h})",
    compilation_gtexv2: f"human ({compilation_gtexv2})",
    compilation_tcgav2: f"human ({compilation_tcgav2})",
    compilation_srav1m: f"mouse ({compilation_srav1m})",
}
drop_compilation = "Select the organism of interest"
drop_compilation_placeholder = "Select a compilation"

switch_violin = "Violin Mode"
# switch_lock = 'Lock Graphs and Table'
switch_lock_help = "If locked, filters applied in the table below will be reflected in the graphs."
plot_label_rail_id = "Rail ID"
switch_log_geq_hist_y = "Log Y axis"

# Keep the space here because these come before an icon
download_results = " Download Results"
download_filtered = " Filtered"
download_original = " Unfiltered"
help_download = 'Download results in CSV format. Default is set to "Unfiltered" mode.'
help_download_mode_unfiltered = "Results will be downloaded without table filters applied."
help_download_mode_filtered = "Results will be downloaded WITH table filters applied."
help_box_plot_click = (
    " You can click on the points in the box plot to filter table by that point. "
    'Reset the "Rail ID" column to go back.'
)
help_reset = (
    "This will remove all filters applied to the table below. For individual columns, "
    'click on the "Reset" button on the desired column'
)
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """
            ERROR MESSAGES
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
bad_url = "Sorry, something must have gone wrong...try again in a couple minutes!"
empty_response = "Snaptron Empty response!"
missing_user_input = (
    "You are missing one or more required inputs...did you select a compilation? For each junction, "
    "are both inclusion and exclusion coordinates defined?"
)
bad_coordinates = "Input coordinates are invalid!"
empty_junction = "Junctions entered have no results!"
suggestion = (
    "Try running the query by adding gene coordinates to your query or double check gene coordinates if " "provided!"
)
query_gene_not_found = "Query gene returned empty results." + suggestion
normalization_gene_not_found = "Normalization gene was not found." + suggestion
httpx_remote_protocol_error = "Snaptron could not identify the Gene." + suggestion
httpx_connect_error = "Failed to establish a connection with Snaptron Web API!"
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """
            Junction Inclusion Query 
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
jiq_form_title = "Junction Information"
button_download = "Download"
jiq_button_add_junction = " Add Junction"
jiq_button_run = "Calculate PSI"
jiq_input_inc_placeholder = "ex: chr19:4491836-4492014"
jiq_input_inc_txt = "Inclusion Junction"
jiq_input_exc_placeholder = "ex: chr19:4491836-4493702"
jiq_input_exc_txt = "Exclusion Junction"
jiq_input_junction_txt_list = ["Junction 1", "Junction 2", "Junction 3", "Junction 4", "Junction 5"]
jiq_plot_title_hist = "PSI Histogram"
jiq_plot_title_box = "PSI Box Plot"
jiq_psi_plot_axes = "PSI"
jiq_log_psi = f"Log\u2082(psi+{log_epsilon})"
jiq_help_table = " Table initially loads with PSI\u22655 and Total\u226515."
jiq_help_add_junction = "Add more inclusion or exclusion junctions (up to 5) to the PSI query"
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """
            Gene Expression Query 
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
geq_form_title = "Gene Information"
geq_query_info = "Query Information"
geq_normalized_info = "Normalization Information"
geq_gene_id = "Gene Name"
# geq_gene_id_norm = 'Normalization Gene ID'
geq_gene_coord = "Gene Coordinates"
geq_normalized = "Normalized GEX"
geq_button_run = "Calculate GEX"
geq_gene_id_placeholder = "ex: TARDBP"
geq_gene_coord_placeholder = "ex: chr1:11012654-11025492"
geq_gene_id_norm_placeholder = "ex: EDF1"
geq_gene_coord_norm_placeholder = "chr9:136862119-136866308"
geq_plot_title_box_raw = "Raw Count Box Plot"
geq_plot_title_box_norm = "Raw vs Normalized Count Box Plot"
geq_plot_title_hist = "Normalized Count Histogram"
geq_plot_label_raw_count = "Raw Count"
geq_plot_label_norm_count = "Normalized Count"
geq_box_plot_y_axes = "Gene Expression Count"
geq_box_plot_y_axes_log = f"Log\u2082(Gene Expression Count+{log_epsilon})"
geq_log_count = f"Log\u2082(count+{log_epsilon})"
geq_help_checkbox = "Check this box if you need to enter gene coordinates in addition to gene name"
geq_provide_coordinates = "I want to provide gene coordinates in addition to Gene ID (use when Gene ID is not found)."
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """
    Strings beyond this point are related to the snaptron interface
    DO NOT TOUCH if you don't know what you are doing
    Strings here exists solely for the purpose of potential changes in the 
    snaptron client web interface and its internal data
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
snpt_col_rail_id = "rail_id"
snpt_col_samples = "samples"
snpt_col_external_id = "external_id"
snpt_col_gene_id = "gene_id:gene_name:gene_type:bp_length"
snpt_col_study = "study"
srav3h_meta_data_required_list = [
    snpt_col_rail_id,
    snpt_col_external_id,
    snpt_col_study,
    "study_title",
    "library_layout",
    "sample_description",
    "sample_name",
    "sample_title",
]

srav1m_meta_data_required_list = srav3h_meta_data_required_list  # SRA mouse and SRA human are similar

tcgav2_meta_data_required_list = [
    snpt_col_rail_id,
    "tcga_barcode",
    snpt_col_study,
    "gdc_cases.project.name",
    "gdc_cases.project.primary_site",
    "cgc_sample_sample_type",
    "gdc_state",
    "gdc_cases.demographic.race",
    "gdc_cases.demographic.ethnicity",
    "gdc_cases.diagnoses.tumor_stage",
    "gdc_cases.diagnoses.vital_status",
    "gdc_cases.samples.oct_embedded",
    "gdc_cases.samples.is_ffpe",
    "gdc_cases.samples.sample_type",
    "cgc_sample_country_of_sample_procurement",
    "cgc_case_tumor_status",
    "cgc_drug_therapy_pharmaceutical_therapy_type",
    "cgc_follow_up_tumor_status",
]

gtexv2_meta_data_required_list = [snpt_col_rail_id, "run_acc", snpt_col_study, "SEX", "AGE", "SAMPID", "SMTS", "SMTSD"]

# JIQ
table_jiq_col_inc = "inc"
table_jiq_col_exc = "exc"
table_jiq_col_total = "total"
table_jiq_col_psi = "psi"
table_jiq_col_log_2 = "log_2_plus"

# GEQ
table_geq_col_raw_count = "raw_count"
table_geq_col_norm_count = "normalized_count"
table_geq_col_factor = "factor"
table_geq_col_log_2_norm = "log_2_plus_norm_count"
table_geq_col_log_2_raw = "log_2_plus_raw"
dbc_template_name = "sandstone"
