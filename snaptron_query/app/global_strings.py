"""
    Strings used in the Junction Inclusion Query Form
"""
compilation_list = ['srav3h', 'gtexv2', 'srav1m', 'tcaga2']
drop_compilation = 'Select the organism of interest'
drop_compilation_placeholder = 'Select a compilation'
jiq_form_title = 'Junction Information'

tab_jiq = "Junction Inclusion Query"
tab_geq = "Gene Expression Query"

jiq_graphs_group_title = 'Graphs'
button_download_str = 'Download'
switch_log_str = 'log'
switch_lock_str = 'Lock Table with Graphs'

button_add_junction = 'Add Junction'
button_run = 'Run Query'  # TODO: strings: should this be Calculate or Run?

input_chr_placeholder = 'ex: 19'
input_chr_txt = 'Chromosome'
input_inc_placeholder = 'ex: 4491836-4492014'
input_inc_txt = 'Inclusion Junction'
input_exc_placeholder = 'ex: 4491836-4493702'
input_exc_txt = 'Exclusion Junction'
input_junction_txt_list = ['Junction 1', 'Junction 2', 'Junction 3', 'Junction 4', 'Junction 5']

"""
    Strings used in the Graphs and Tables 
"""
# histogram_label_y = 'PSI'
histogram_title = 'PSI Histogram'

# boxplot_label_y = 'PSI'
boxplot_label = 'Rail ID'
box_plot_title = 'PSI Box Plot'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Strings beyond this point are related to the snaptron interface
    DO NOT TOUCH if you don't know what you are doing
    Strings here exists solely for the purpose of potential changed in the 
    snaptron client interface and its internal data
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# req_cols = ['rail_id', 'external_id', 'study', 'study_title', 'library_layout']
snaptron_col_rail_id = 'rail_id'
snaptron_col_external_id = 'external_id'
snaptron_col_study = 'study'
snaptron_col_study_title = 'study_title'
snaptron_col_library_layout = 'library_layout'

meta_data_required_list = [snaptron_col_rail_id,
                           snaptron_col_external_id,
                           snaptron_col_study,
                           snaptron_col_study_title,
                           snaptron_col_library_layout
                           ]

# columns=['rail_id', 'external_id', 'study', 'inc', 'exc', 'total', 'psi'])
table_jiq_col_inc = 'inc'
table_jiq_col_exc = 'exc'
table_jiq_col_total = 'total'
table_jiq_col_psi = 'psi'
