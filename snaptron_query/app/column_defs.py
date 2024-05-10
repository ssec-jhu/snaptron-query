from snaptron_query.app import global_strings as gs


def get_rail_id():
    return [{"field": gs.snpt_col_rail_id, "headerName": gs.plot_label_rail_id, 'width': 125, "pinned": "left",
             "filterParams": {"buttons": ["reset"]}}]


def get_study():
    return [{"field": 'study', "headerName": "Study", 'width': 120, "cellRenderer": "StudyLink",
             "filterParams": {"buttons": ["reset"]}}]


def get_col_meta_srav3h_a():
    column_def = get_rail_id()
    column_def += [{"field": gs.snpt_col_external_id, "headerName": "External ID", 'width': 130,
                    "filterParams": {"buttons": ["reset"]}}]
    column_def += get_study()

    return column_def


def get_col_meta_tcgav2_a():
    return get_rail_id()


def get_col_meta_gtexv2_a():
    return get_rail_id()


def get_col_meta_srav3h_b():
    return [
        {"field": 'study_title', "headerName": "Study Title", 'width': 350, "filterParams": {"buttons": ["reset"]},
         'cellClass': 'cell-wrap-dash-ag-grid', 'autoHeight': True},  # must have this here, it is not a style option
        {"field": 'sample_name', "headerName": "Sample Name", 'width': 150 + 20, "filterParams": {"buttons": ["reset"]},
         "tooltipField": 'sample_name'},
        {"field": 'sample_title', "headerName": "Sample Title", 'width': 150, "filterParams": {"buttons": ["reset"]},
         "tooltipField": 'sample_title'},
        {"field": 'library_layout', "headerName": "Library", 'width': 100, "filterParams": {"buttons": ["reset"]}},
        {"field": 'sample_description', "headerName": "Sample Description", 'width': 200,
         "filterParams": {"buttons": ["reset"]}, "tooltipField": "sample_description"},
    ]


def get_col_meta_tcgav2_b():
    meta_data = [{"field": item, "headerName": item, "tooltipField": item, "filterParams": {"buttons": ["reset"]}}
                 for item in gs.tcgav2_meta_data_required_list[1:len(gs.tcgav2_meta_data_required_list)]]
    return meta_data


def get_col_meta_gtexv2_b():
    meta_data = [{"field": item, "headerName": item, "tooltipField": item, "filterParams": {"buttons": ["reset"]}}
                 for item in gs.gtexv2_meta_data_required_list[1:len(gs.gtexv2_meta_data_required_list)]]
    return meta_data


def get_col_jiq():
    return [
        {"field": gs.table_jiq_col_inc, "headerName": "Inc_Count", "filter": "agNumberColumnFilter", 'width': 130,
         "filterParams": {"buttons": ["reset"]}},
        {"field": gs.table_jiq_col_exc, "headerName": "Exc_Count", "filter": "agNumberColumnFilter", 'width': 130,
         "filterParams": {"buttons": ["reset"]}, },
        {"field": gs.table_jiq_col_total, "headerName": "Total_Count", "filter": "agNumberColumnFilter", 'width': 160,
         "filterParams": {"buttons": ["reset"]},
         # Performance Note: adding header tooltips creates a horizontal scroll performance issue!
         # "headerTooltip": "Inclusion Count + Exclusion Count"
         },
        {"field": gs.table_jiq_col_psi, "headerName": "PSI", "filter": "agNumberColumnFilter", 'initialSort': 'desc',
         'width': 120, "filterParams": {"buttons": ["reset"]}},
        {"field": gs.table_jiq_col_log_2, "headerName": gs.jiq_log_psi, "filter": "agNumberColumnFilter",
         'width': 145, "filterParams": {"buttons": ["reset"]}}
    ]


def get_junction_query_column_def(compilation):
    """Wrapper for ag-grid column definitions and their individual style"""
    if compilation == gs.compilation_srav3h:
        return get_col_meta_srav3h_a() + get_col_jiq() + get_col_meta_srav3h_b()
    elif compilation == gs.compilation_gtexv2:
        return get_col_meta_gtexv2_a() + get_col_jiq() + get_col_meta_gtexv2_b()
    elif compilation == gs.compilation_tcgav2:
        return get_col_meta_tcgav2_a() + get_col_jiq() + get_col_meta_tcgav2_b()
    elif compilation == gs.compilation_srav1m:
        # SRAV1m is similar to SRAV3h
        return get_col_meta_srav3h_a() + get_col_jiq() + get_col_meta_srav3h_b()


def get_gene_expression_query_column_def(compilation, normalized=False):
    """Wrapper for ag-grid column definitions and their individual style"""
    if normalized:
        gex_col = [
            {"field": gs.table_geq_col_raw_count, "headerName": gs.geq_plot_label_raw_count,
             "filter": "agNumberColumnFilter", 'width': 130, "filterParams": {"buttons": ["reset"]}},
            {"field": gs.table_geq_col_factor, "headerName": "Factor", "filter": "agNumberColumnFilter",
             'width': 130, "filterParams": {"buttons": ["reset"]}},
            {"field": gs.table_geq_col_norm_count, "headerName": gs.geq_plot_label_norm_count, 'initialSort': 'desc',
             "filter": "agNumberColumnFilter", 'width': 170, "filterParams": {"buttons": ["reset"]}},
            {"field": gs.table_geq_col_log_2_norm, "headerName": gs.geq_log_count,
             "filter": "agNumberColumnFilter", 'width': 145, "filterParams": {"buttons": ["reset"]}}
        ]
    else:
        gex_col = [
            {"field": gs.table_geq_col_raw_count, "headerName": gs.geq_plot_label_raw_count, 'initialSort': 'desc',
             "filter": "agNumberColumnFilter", 'width': 130, "filterParams": {"buttons": ["reset"]}},
            {"field": gs.table_geq_col_log_2_raw, "headerName": gs.geq_log_count,
             "filter": "agNumberColumnFilter", 'width': 145, "filterParams": {"buttons": ["reset"]}}
        ]

    if compilation == gs.compilation_srav3h:
        return get_col_meta_srav3h_a() + gex_col + get_col_meta_srav3h_b()
    elif compilation == gs.compilation_gtexv2:
        return get_col_meta_gtexv2_a() + gex_col + get_col_meta_gtexv2_b()
    elif compilation == gs.compilation_tcgav2:
        return get_col_meta_tcgav2_a() + gex_col + get_col_meta_tcgav2_b()
    elif compilation == gs.compilation_srav1m:
        # SRAV1m is similar to SRAV3h
        return get_col_meta_srav3h_a() + gex_col + get_col_meta_srav3h_b()
