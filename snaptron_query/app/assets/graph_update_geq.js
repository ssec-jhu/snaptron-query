window.dash_clientside = Object.assign({}, window.dash_clientside, {
    geq_clientside: {
        update_histogram_log_y: function(log_y,histogram_figure_data){
            let newFigure = JSON.parse(JSON.stringify(histogram_figure_data)); // Deep copy of the figure
            if (log_y) {
                newFigure.layout.yaxis['type'] = 'log'
            }
            else{
               newFigure.layout.yaxis['type'] = 'linear'
            }
                return newFigure;
        },
        update_histogram_data: function(log_x,lock_graphs,virtual_data, rowData, histogram_figure_data){
            if (histogram_figure_data && virtual_data) {
                let newFigure = JSON.parse(JSON.stringify(histogram_figure_data)); // Deep copy of the figure
                let data;
                if (lock_graphs && virtual_data) {
                    data = JSON.parse(JSON.stringify(virtual_data));
                } else {
                    data = JSON.parse(JSON.stringify(rowData));
                }

                if (log_x) {
                    newFigure.data[0].x = data.map(item => item['log2_norm_count']); //gs.table_geq_col_log_2_norm
                    newFigure.layout.xaxis.title = "Log\u2082(count+0.01)"; //gs.geq_log_count
                    newFigure.data[0].hovertemplate = "Log(count)=%{x}<br>count=%{y}<extra></extra>"
                } else {
                    newFigure.data[0].x = data.map(item => item['normalized_count']); //gs.table_geq_col_norm_count
                    newFigure.layout.xaxis.title = "Normalized Count"   //gs.geq_plot_label_norm_count
                    newFigure.data[0].hovertemplate = "Normalized Count=%{x}<br>count=%{y}<extra></extra>"
                }
                return newFigure;
            }
        },

        update_box_plot_violin: function(violin_mode, point_mode, boxplot_figure_data){
            if (boxplot_figure_data) {
                let newFigure = JSON.parse(JSON.stringify(boxplot_figure_data)); // Deep copy of the figure
                //let newFigure = boxplot_figure_data // TODO: why doesn't this work?
                const boxpointsValue = point_mode ? 'all' : 'outliers';
                if (violin_mode) {
                    newFigure.data.forEach(trace => {
                        trace.type = 'violin';
                        trace.box = { visible: true }; // Show box within violin plot
                        trace.points = boxpointsValue;
                    });
                    newFigure.layout.violinmode = 'group'
                }
                else{
                    newFigure.data.forEach(trace => {
                        trace.type = 'box';
                        trace.boxpoints = boxpointsValue;
                    });
                    newFigure.layout.boxmode = 'group'
                }
                return newFigure;
            }
        },
        update_box_plot_data: function(log_x,lock_graphs,virtual_data, rowData, boxplot_figure_data){
            if (boxplot_figure_data && virtual_data) {
                let newFigure = JSON.parse(JSON.stringify(boxplot_figure_data)); // Deep copy of the figure
                let data;
                if (lock_graphs && virtual_data) {
                    data = JSON.parse(JSON.stringify(virtual_data));
                } else {
                    data = JSON.parse(JSON.stringify(rowData));
                }
                //there is only max two traces in the GEX box plot
                //so precomputing the map outside makes it slower
                if (log_x) {
                    newFigure.data.forEach(trace => {
                        trace.customdata = data.map(item => [item['rail_id']])
                        if (trace.name === "Raw Count") {
                            trace.y = data.map(item => item['log2_raw'])
                        }
                        else{
                            trace.y = data.map(item => item['log2_norm_count'])
                        }
                    });
                    newFigure.layout.yaxis.title = "Log\u2082(Gene Expression Count+0.01)"
                }else{
                    newFigure.data.forEach(trace => {
                        trace.customdata = data.map(item => [item['rail_id']])
                        if (trace.name === "Raw Count") {
                            trace.y = data.map(item => item['raw_count'])
                        } else {
                            trace.y = data.map(item => item['normalized_count'])
                        }
                    });
                    newFigure.layout.yaxis.title = "Gene Expression Count"
                }
                return newFigure;
            }
        },
    }

});