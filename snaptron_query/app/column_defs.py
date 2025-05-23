from snaptron_query.app import global_strings as gs


def capitalize_underscored_string(s):
    return "_".join([word.capitalize() for word in s.split("_")])


def get_generic_col(item):
    """
    this column is used for most of the meta-data strings not the calculations
    no specific formatting or fixed width is set
    """

    return [
        {
            "field": item,
            "headerName": item,
            "tooltipField": item,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        }
    ]


def get_rail_id():
    return [
        {
            "field": gs.snpt_col_rail_id,
            "headerName": capitalize_underscored_string(gs.snpt_col_rail_id),
            "width": 125,
            "pinned": "left",  # pinned the column to the left for all results
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        }
    ]


def get_col_meta_srav3h_before():
    """
    These columns go BEFORE the calculations in the order below
    """
    column_def = get_rail_id()
    column_def += [
        {  # external_id
            "field": gs.snpt_col_external_id,
            "headerName": capitalize_underscored_string(gs.snpt_col_external_id),
            "width": 130,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {  # study column
            "field": gs.snpt_col_study,
            "headerName": "Study",
            "width": 120,
            "cellRenderer": "StudyLink",  # this created the hyperlinks for the srav external ids
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {  # study_title column
            "field": gs.snpt_col_study_title,
            "headerName": capitalize_underscored_string(gs.snpt_col_study_title),
            "width": 350,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "cellClass": "cell-wrap-dash-ag-grid",  # special class just for the study title to fit it in a nice way
            "autoHeight": True,
        },
    ]
    return column_def


def get_col_meta_srav3h_after():
    """
    These columns go AFTER the calculations in the order below
    """
    return [
        {
            "field": gs.snpt_col_sample_name,
            "headerName": "Sample_Name",
            "width": 150 + 20,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "tooltipField": gs.snpt_col_sample_name,
        },
        {
            "field": gs.snpt_col_sample_title,
            "headerName": "Sample_Title",
            "width": 150,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "tooltipField": gs.snpt_col_sample_title,
        },
        {
            "field": gs.snpt_col_library_layout,
            "headerName": "Library",
            "width": 100,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_sample_description,
            "headerName": "Sample_Description",
            "width": 200,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            "tooltipField": gs.snpt_col_sample_description,
        },
    ]


def get_col_meta_tcgav2_before():
    """
    These columns go BEFORE the calculations in the order below
    """
    column_def = get_rail_id()
    column_def += [
        {  # gdc_cases.project.primary_site
            "field": gs.snpt_col_gdc_prim_site,
            "headerName": "gdc_cases.project.primary_site",
            "tooltipField": gs.snpt_col_gdc_prim_site,
            "width": 200,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {  # study column
            "field": gs.snpt_col_study,
            "headerName": "Study",
            "width": 120,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
    ]
    return column_def


def get_col_meta_tcgav2_after():
    """
    These columns go AFTER the calculations in the order below
    rail_id,gdc_cases.project.primary_site, study come before the calculations
    rest of the metadata, from the second item on the metadata list onwards, comes after the calculations
    """
    meta_data = []
    for item in gs.tcgav2_meta_data_required_list[3 : len(gs.tcgav2_meta_data_required_list)]:
        meta_data += get_generic_col(item)
    return meta_data


def get_col_meta_gtexv2_before():
    """
    These columns go BEFORE the calculations in the order below
    add run_acc and study
    rest of the metadata, from the second item on the metadata list onwards, comes after the calculations
    """
    column_def = get_rail_id()
    column_def += [
        {  # run_acc column
            "field": gs.snpt_col_run_acc,
            "headerName": capitalize_underscored_string(gs.snpt_col_run_acc),
            "width": 130,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {  # study column
            "field": gs.snpt_col_study,
            "headerName": "Study",
            "tooltipField": gs.snpt_col_study,
            "width": 150,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
    ]
    return column_def


def get_col_meta_gtexv2_after():
    """
    These columns go AFTER the calculations in the order below
    rest of the metadata, from the second item on the metadata list onwards, comes after the calculations
    """
    return [
        {
            "field": gs.snpt_col_sex,
            "headerName": gs.snpt_col_sex,
            "width": 80,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_caps_age,
            "headerName": "AGE",
            "width": 90,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_SUBJID,
            "headerName": gs.snpt_col_SUBJID,
            "tooltipField": gs.snpt_col_SUBJID,
            "width": 180,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_SAMPID,
            "headerName": gs.snpt_col_SAMPID,
            "tooltipField": gs.snpt_col_SAMPID,
            "width": 180,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_smts,
            "headerName": gs.snpt_col_smts,
            "tooltipField": gs.snpt_col_smts,
            "width": 150,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_smtsd,
            "headerName": gs.snpt_col_smtsd,
            "tooltipField": gs.snpt_col_smtsd,
            "width": 230,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
    ]


def get_col_meta_encode_before():
    """
    These columns go BEFORE the calculations in the order below
    """
    column_def = get_rail_id()
    column_def += [
        {  # "Experiment accession"
            "field": gs.snpt_col_exp_acc,
            "headerName": "Accession",
            "tooltipField": gs.snpt_col_exp_acc,
            "width": 120,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {  # "Biosample term name"
            "field": gs.snpt_col_cell_line,
            "headerName": "Cell Type",
            "tooltipField": gs.snpt_col_cell_line,
            "width": 100,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {  # "Experiment target"
            "field": gs.snpt_col_exp_target,
            "headerName": "shRNA",
            "tooltipField": gs.snpt_col_exp_target,
            "width": 150,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
    ]
    return column_def


def get_col_meta_encode_after():
    """
    These columns go AFTER the calculations in the order below
    rest of the metadata, from the second item on the metadata list onwards, comes after the calculations
    """
    return [
        {
            "field": gs.snpt_col_biosamp_life_stage,
            "headerName": "Life Stage",
            "width": 100,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_biosamp_life_sex,
            "headerName": "Sex",
            "width": 80,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_biosamp_life_age,
            "headerName": "Age",
            "width": 100,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_assay,
            "headerName": gs.snpt_col_assay,
            "width": 180,
            "tooltipField": gs.snpt_col_assay,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.snpt_col_exp_date_rel,
            "headerName": "Release Date",
            "width": 150,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
    ]


def get_col_jiq_calculations():
    return [
        {
            "field": gs.table_jiq_col_inc,
            "headerName": "Inc_Count",
            "filter": "agNumberColumnFilter",
            "width": 130,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.table_jiq_col_exc,
            "headerName": "Exc_Count",
            "filter": "agNumberColumnFilter",
            "width": 130,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.table_jiq_col_total,
            "headerName": "Total_Count",
            "filter": "agNumberColumnFilter",
            "width": 160,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
            # Performance Note: adding header tooltips creates a horizontal scroll performance issue!
            # "headerTooltip": "Inclusion Count + Exclusion Count"
        },
        {
            "field": gs.table_jiq_col_psi,
            "headerName": "PSI",
            "filter": "agNumberColumnFilter",
            "initialSort": "desc",
            "width": 120,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.table_jiq_col_log_2,
            "headerName": gs.jiq_log_psi,
            "filter": "agNumberColumnFilter",
            "width": 145,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
    ]


def get_col_multi_jiq_calculations(junctions_count):
    # add the average PSI and set this column for sort
    multi_jiq_fields_indexed = [
        {
            "field": gs.table_jiq_col_avg_psi,
            "headerName": "avg_PSI",
            "filter": "agNumberColumnFilter",
            "initialSort": "desc",
            "width": 155,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        }
    ]

    multi_jiq_fields = [
        {
            "field": gs.table_jiq_col_psi,
            "headerName": "PSI",
            "filter": "agNumberColumnFilter",
            "width": 120,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.table_jiq_col_total,
            "headerName": "Total",
            "filter": "agNumberColumnFilter",
            "width": 120,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
        {
            "field": gs.table_jiq_col_log_2,
            "headerName": gs.jiq_log_psi,
            "filter": "agNumberColumnFilter",
            "width": 145,
            "filterParams": {
                "buttons": ["reset", "apply"],
                "closeOnApply": True,
            },
        },
    ]
    # for each junction add an index to PSI, TOTAL and LOG
    for f in range(len(multi_jiq_fields)):
        for i in range(junctions_count):
            new_dict = multi_jiq_fields[f].copy()
            # Modify the values by appending the index
            new_dict["field"] = f"{multi_jiq_fields[f]['field']}_{i + 1}"
            new_dict["headerName"] = f"{multi_jiq_fields[f]['headerName']}_{i + 1}"
            # Append the modified dictionary to the list
            multi_jiq_fields_indexed.append(new_dict)

    return multi_jiq_fields_indexed


def get_junction_query_column_def(compilation, junction_count):
    """Wrapper for ag-grid column definitions and their individual style"""

    # get the main jiq calculations for either single or multi junction query
    col_jiq = get_col_jiq_calculations() if junction_count == 1 else get_col_multi_jiq_calculations(junction_count)

    # add on the other common data in the table
    if compilation == gs.compilation_srav3h:
        return get_col_meta_srav3h_before() + col_jiq + get_col_meta_srav3h_after()
    elif compilation == gs.compilation_gtexv2:
        return get_col_meta_gtexv2_before() + col_jiq + get_col_meta_gtexv2_after()
    elif compilation == gs.compilation_tcgav2:
        return get_col_meta_tcgav2_before() + col_jiq + get_col_meta_tcgav2_after()
    elif compilation == gs.compilation_srav1m:
        # SRAV1m is similar to SRAV3h
        return get_col_meta_srav3h_before() + col_jiq + get_col_meta_srav3h_after()
    elif compilation == gs.compilation_encode:
        return get_col_meta_encode_before() + col_jiq + get_col_meta_encode_after()


def get_gene_expression_query_column_def(compilation, normalized=False):
    """Wrapper for ag-grid column definitions and their individual style"""
    if normalized:
        gex_col = [
            {
                "field": gs.table_geq_col_raw_count,
                "headerName": capitalize_underscored_string(gs.table_geq_col_raw_count),
                "filter": "agNumberColumnFilter",
                "width": 130,
                "filterParams": {
                    "buttons": ["reset", "apply"],
                    "closeOnApply": True,
                },
            },
            {
                "field": gs.table_geq_col_factor,
                "headerName": "Factor",
                "filter": "agNumberColumnFilter",
                "width": 130,
                "filterParams": {
                    "buttons": ["reset", "apply"],
                    "closeOnApply": True,
                },
            },
            {
                "field": gs.table_geq_col_norm_count,
                "headerName": capitalize_underscored_string(gs.table_geq_col_norm_count),
                "initialSort": "desc",
                "filter": "agNumberColumnFilter",
                "width": 170,
                "filterParams": {
                    "buttons": ["reset", "apply"],
                    "closeOnApply": True,
                },
            },
            {
                "field": gs.table_geq_col_log_2_norm,
                "headerName": gs.geq_log_count,
                "filter": "agNumberColumnFilter",
                "width": 145,
                "filterParams": {
                    "buttons": ["reset", "apply"],
                    "closeOnApply": True,
                },
            },
        ]
    else:
        gex_col = [
            {
                "field": gs.table_geq_col_raw_count,
                "headerName": capitalize_underscored_string(gs.geq_plot_label_raw_count),
                "initialSort": "desc",
                "filter": "agNumberColumnFilter",
                "width": 130,
                "filterParams": {
                    "buttons": ["reset", "apply"],
                    "closeOnApply": True,
                },
            },
            {
                "field": gs.table_geq_col_log_2_raw,
                "headerName": gs.geq_log_count,
                "filter": "agNumberColumnFilter",
                "width": 145,
                "filterParams": {
                    "buttons": ["reset", "apply"],
                    "closeOnApply": True,
                },
            },
        ]

    if compilation == gs.compilation_srav3h:
        return get_col_meta_srav3h_before() + gex_col + get_col_meta_srav3h_after()
    elif compilation == gs.compilation_gtexv2:
        return get_col_meta_gtexv2_before() + gex_col + get_col_meta_gtexv2_after()
    elif compilation == gs.compilation_tcgav2:
        return get_col_meta_tcgav2_before() + gex_col + get_col_meta_tcgav2_after()
    elif compilation == gs.compilation_srav1m:
        # SRAV1m is similar to SRAV3h
        return get_col_meta_srav3h_before() + gex_col + get_col_meta_srav3h_after()
    elif compilation == gs.compilation_encode:
        return get_col_meta_encode_before() + gex_col + get_col_meta_encode_after()


def make_dash_ag_grid_greater_than_or_equal_filter(filter_value):
    return {
        "filterType": "number",
        "type": "greaterThanOrEqual",
        "filter": filter_value,
    }


def get_jiq_table_filter_model(junction_count):
    if junction_count == 1:
        # filter psi and total_count
        filter_model = {
            gs.table_jiq_col_total: make_dash_ag_grid_greater_than_or_equal_filter(gs.const_filter_total),
            gs.table_jiq_col_psi: make_dash_ag_grid_greater_than_or_equal_filter(gs.const_filter_psi),
        }
    else:
        # filter average psi
        filter_model = {gs.table_jiq_col_avg_psi: make_dash_ag_grid_greater_than_or_equal_filter(gs.const_filter_psi)}
        # filter total columns indexed
        indexed_filter_model = {}
        for index in range(1, junction_count + 1):
            new_key = f"{gs.table_jiq_col_total}_{index}"
            indexed_filter_model[new_key] = make_dash_ag_grid_greater_than_or_equal_filter(gs.const_filter_total)
        filter_model.update(indexed_filter_model)

    return filter_model


def get_geq_table_filter_model(normalized_data):
    if normalized_data:
        filter_model = {
            gs.table_geq_col_factor: make_dash_ag_grid_greater_than_or_equal_filter(0),
        }
    else:
        filter_model = {}

    return filter_model
