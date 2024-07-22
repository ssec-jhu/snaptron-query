window.dash_clientside = Object.assign({}, window.dash_clientside, {
    snapmine_clientside: {
        get_data: function (lock_graphs, virtual_data, rowData){
            let data
            if (lock_graphs && virtual_data) {
                    data = JSON.parse(JSON.stringify(virtual_data));
                } else {
                    data = JSON.parse(JSON.stringify(rowData));
                }
            return data
        },
        update_histogram_log_y: function (log_y, histogram_figure_data) {
            if (histogram_figure_data) {
                let newFigure = JSON.parse(JSON.stringify(histogram_figure_data)); // Deep copy of the figure
                newFigure.layout.yaxis['type'] = log_y ? 'log' : 'linear'
                return newFigure;
            }
        },
        update_histogram_data_geq: function (log_x, lock_graphs, virtual_data, rowData, histogram_figure_data) {
            if (histogram_figure_data && virtual_data) {
                let newFigure = JSON.parse(JSON.stringify(histogram_figure_data)); // Deep copy of the figure
                let data = this.get_data(lock_graphs,virtual_data,rowData)
                const key = log_x ? 'log2_norm_count' : 'normalized_count'
                newFigure.data[0].x = data.map(item => item[key]); //gs.table_geq_col_log_2_norm
                newFigure.layout.xaxis.title = log_x ? "Log\u2082(count+0.01)" : "Normalized Count"
                newFigure.data[0].hovertemplate =  log_x ? "Log(count)=%{x}<br>count=%{y}<extra></extra>" : "Normalized Count=%{x}<br>count=%{y}<extra></extra>"
                return newFigure;
            }
        },
        update_histogram_data_jiq: function (log_x, lock_graphs, virtual_data, rowData, histogram_figure_data) {
            if (histogram_figure_data && virtual_data) {
                let newFigure = JSON.parse(JSON.stringify(histogram_figure_data)); // Deep copy of the figure
                let data = this.get_data(lock_graphs,virtual_data,rowData)
                const numTraces = newFigure.data.length
                if (numTraces===1){
                    const key = log_x ? 'log2' : 'psi' // gs.table_jiq_col_psi gs.table_jiq_col_log_2
                    const hover_string = log_x ? "Log(psi+0.01)=%{x}<br>count=%{y}<extra></extra>" : "PSI=%{x}<br>count=%{y}<extra></extra>"
                    newFigure.data[0].x = data.map(item => item[key]);
                    newFigure.data[0].hovertemplate = hover_string
                }
                else {
                    newFigure.data.forEach((trace, index) => {
                        const key = log_x? `log2_${index + 1}` :`psi_${index + 1}` ;
                        trace.x = data.map(item => item[key]);
                    });
                }
                newFigure.layout.xaxis.title = log_x ? "Log\u2082(psi+0.01)" : "PSI"
                return newFigure;
            }
        },
        update_box_plot_violin_and_points_display: function (violin_mode, point_mode, boxplot_figure_data) {
            if (boxplot_figure_data) {
                let newFigure = JSON.parse(JSON.stringify(boxplot_figure_data)); // Deep copy of the figure
                const boxpointsValue = point_mode ? 'all' : 'outliers';
                if (violin_mode) {
                    newFigure.data.forEach(trace => {
                        trace.type = 'violin';
                        trace.box = {visible: true}; // Show box within violin plot
                        trace.points = boxpointsValue;
                    });
                    newFigure.layout.violinmode = 'group'
                } else {
                    newFigure.data.forEach(trace => {
                        trace.type = 'box';
                        trace.boxpoints = boxpointsValue;
                    });
                    newFigure.layout.boxmode = 'group'
                }
                return newFigure;
            }
        },
        update_box_plot_data_geq: function (log_x, lock_graphs, virtual_data, rowData, boxplot_figure_data) {
            if (boxplot_figure_data && virtual_data) {
                let newFigure = JSON.parse(JSON.stringify(boxplot_figure_data)); // Deep copy of the figure
                let data = this.get_data(lock_graphs,virtual_data,rowData)
                //there is only max two traces in the GEX box plot
                //so precomputing the map outside makes it slower
                newFigure.data.forEach(trace => {
                        trace.customdata = data.map(item => [item['rail_id']])
                });
                let raw_string = log_x ? 'log2_raw' : 'raw_count'
                let norm_string = log_x ? 'log2_norm_count' : 'normalized_count'
                newFigure.data.forEach(trace => {
                    if (trace.name === "Normalized Count") {
                        trace.y = data.map(item => item[norm_string])
                    } else {
                        trace.y = data.map(item => item[raw_string])
                    }
                        });
                newFigure.layout.yaxis.title = log_x ? "Log\u2082(Gene Expression Count+0.01)" : "Gene Expression Count"
                return newFigure;
            }
        },
        update_box_plot_data_jiq: function (log_x, lock_graphs, virtual_data, rowData, boxplot_figure_data) {
            if (boxplot_figure_data && virtual_data) {
                let newFigure = JSON.parse(JSON.stringify(boxplot_figure_data)); // Deep copy of the figure
                let data = this.get_data(lock_graphs,virtual_data,rowData)
                newFigure.data.forEach(trace => {
                        trace.customdata = data.map(item => [item['rail_id']])
                });
                const numTraces = newFigure.data.length
                if (numTraces===1){
                    const key = log_x ? 'log2' : 'psi' // gs.table_jiq_col_psi gs.table_jiq_col_log_2
                    newFigure.data[0].y = data.map(item => item[key]);
                }else{
                    newFigure.data.forEach((trace, index) => {
                        const key = log_x? `log2_${index + 1}` :`psi_${index + 1}` ;
                        trace.y = data.map(item => item[key]);
                    });
                }
                newFigure.layout.yaxis.title = log_x ? "Log\u2082(PSI+0.01)" : "PSI"
                return newFigure;
            }
        },
    }

});