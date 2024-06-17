// window.dash_clientside = Object.assign({}, window.dash_clientside, {
//     clientside: {
//         updatePlotType: function(figure) {
//             if (!figure)
//                 return null;
//
//             console.log("in here")
//             let newFigure = JSON.parse(JSON.stringify(figure)); // Deep copy of the figure
//
//             //if (toggle)
//             //{
//                 newFigure.data.forEach(trace => {
//                     trace.type = 'violin';
//                     trace.box = { visible: true }; // Show box within violin plot
//                     //trace.points = 'all'; // Show all points
//                 });
//                 newFigure.layout.title = 'Violin Plot';
//             //}
//             // else {
//             //     newFigure.data.forEach(trace => {
//             //         trace.type = 'box';
//             //         trace.boxmean = true;
//             //     });
//             //     newFigure.layout.title = 'Box Plot';
//             // }
//
//             return newFigure;
//         }
//     }
// });


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    // This function WORKS with:
    // app.clientside_callback(
    //     ClientsideFunction(namespace='clientside', function_name='update_histogram_log_y'),
    //     Output('id-row-graph-geq-hist', 'figure', allow_duplicate=True),
    //     Input("id-store-geq-hist", 'data'),  # figure data stored in session
    //     Input("id-switch-geq-log-y-histogram", 'value'),
    //     prevent_initial_call=True
    // )
    clientside: {
        update_histogram_log_y: function(figure, scale) {
            let newFigure = JSON.parse(JSON.stringify(figure)); // Deep copy of the figure

            if (scale) {
                newFigure.layout.title = 'Log is On';
                newFigure.layout.yaxis['type'] = 'log'
            }
            else{
                newFigure.layout.title = 'Log y is off';
            }
            return newFigure;
        }
    }
});


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    // This function WORKS with:
    // app.clientside_callback(
    //     ClientsideFunction(namespace='clientside', function_name='update_histogram_log_y_2'),
    //     Output('id-row-graph-geq-hist', 'figure', allow_duplicate=True),
    //     Input("id-switch-geq-log-y-histogram", 'value'),
    //     Input("id-switch-geq-log-count-histogram", 'value'),
    //     Input('id-ag-grid-geq', 'rowData'), # it doesn't like this format
    //     State('id-store-geq-rowData','data'),
    //     State("id-store-geq-hist", 'data'),  # figure data stored in session
    //     prevent_initial_call=True
    // )
    clientside: {
        // note both rowData in its raw form and rowData from the STORE WORK
        update_histogram_log_y_2: function(log_y,log_count,rowData,rowData_fromStore,figure) {
            let newFigure = JSON.parse(JSON.stringify(figure)); // Deep copy of the figure
            console.log("Figure Copy is "+newFigure)

            console.log("Log2 is "+log_count)
            console.log("log_y is "+log_y)
            //console.log("RowData is " + rowData) //not useful

            let parsedData = JSON.parse(JSON.stringify(rowData_fromStore));
            console.log(parsedData.map(item => item['log_2_plus_norm_count']))
            let parsedRowData = JSON.parse(JSON.stringify(rowData));
            console.log(parsedRowData.map(item => item['log_2_plus_norm_count']))

           if (log_y) {
                //newFigure.layout.title = 'Log Y is On';
                newFigure.layout.yaxis['type'] = 'log'
            }
            else{
                newFigure.layout.title = 'Log Y is off';
            }

            if (log_count) {
                //let x_values = parsedData.map(item => item['log_2_plus_norm_count']);
                newFigure.data[0].x = parsedData.map(item => item['log_2_plus_norm_count']);
            }
            else{
                newFigure.data[0].x = parsedData.map(item => item['normalized_count']);
            }


            return newFigure;
        }
    }
});

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    // This function WORKS with:
    //     app.clientside_callback(
    //     ClientsideFunction(namespace='clientside', function_name='update_histogram_3'),
    //     Output('id-row-graph-geq-hist', 'figure', allow_duplicate=True),
    //     Input("id-switch-geq-log-y-histogram", 'value'),
    //     Input("id-switch-geq-log-count-histogram", 'value'),
    //     Input('id-switch-geq-lock-with-table', 'value'),
    //     Input('id-ag-grid-geq', 'virtualRowData'),
    //     State('id-ag-grid-geq', 'rowData'),
    //     State("id-store-geq-hist", 'data'),
    //     prevent_initial_call=True
    // )

    clientside: {
        // note both rowData in its raw form and rowData from the STORE WORK
        update_histogram_3: function(log_y,log_count,lock_graphs,virtualData, rowData, figure) {

            console.log("Updating chart via javascript...")
            let newFigure = JSON.parse(JSON.stringify(figure)); // Deep copy of the figure

            //if (lock_graphs)
            //    let data = JSON.parse(JSON.stringify(virtualRowData));
            //else {
            let data = JSON.parse(JSON.stringify(rowData));
            if (lock_graphs && virtualData){
                console.log("Graph is locked: Changing Data to VIRTUAL")
                 data = JSON.parse(JSON.stringify(virtualData));
            }
            // TODO: this must be fixed
            //data = data.map(item => item['factor'] > -1);
            //console.log(" Data length after virtual= " + data.length)

           if (log_y) {
                newFigure.layout.yaxis['type'] = 'log'
            }

            if (log_count) {
                newFigure.data[0].x = data.map(item => item['log_2_plus_norm_count']);
            }
            else{
                newFigure.data[0].x = data.map(item => item['normalized_count']);
            }

            return newFigure;
        }
    }
});



// window.dash_clientside = Object.assign({}, window.dash_clientside, {
//     // This function WORKS with:
//
//     clientside: {
//         // note both rowData in its raw form and rowData from the STORE WORK
//         update_histogram_4: function(log_y,log_count,lock_graphs,virtualData, rowData) {
//             let data = JSON.parse(JSON.stringify(rowData));
//             //console.log(" Data length before virtual = " + data.length)
//             if (lock_graphs && virtualData){
//                 console.log("Graph is locked: Changing Data to VIRTUAL")
//                  data = JSON.parse(JSON.stringify(virtualData));
//             }
//
//             //data = data.map(item => item['factor'] > -1);
//             console.log(" Data length after virtual= " + data.length)
//
//             //let newFigure = JSON.parse(JSON.stringify(figure)); // Deep copy of the figure
//             let newFigure =
//                 {
//                     "data": [
//                         {
//                             'bingroup': 'x',
//                             'hovertemplate': 'Log₂(count+0.01)=%{x}<br>count=%{y}<extra></extra>',
//                             'legendgroup': '',
//                             'marker': {'color': '#385682', 'pattern': {'shape': ''}},
//                             'name': '',
//                             'nbinsx': 50,
//                             'offsetgroup': '',
//                             'orientation': 'v',
//                             'showlegend': False,
//                             'type': 'histogram',
//
//                             "x": data.map(item => item['log_2_plus_norm_count']),
//
//                             "xaxis": "x",
//                             "yaxis": "y"
//                         }
//                         ],
//                 "layout": {
//                     'barmode': 'relative',
//                     'legend': {'tracegroupgap': 0},
//                     'margin': {'b': 0, 't': 60},
//                     'template': '...',
//                     'title': {'text': '<b>Normalized Count Histogram</b>', 'x': 0.5},
//                     'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Log₂(count+0.01)'}},
//                     'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'count'}}
//                 }
//             }
//
//
//
//            // if (log_y) {
//            //      //console.log("Changing Data to LOG Y")
//            //      newFigure.layout.yaxis['type'] = 'log'
//            //  }
//            //
//            //  if (log_count) {
//            //      //console.log("Changing Data to log_2_plus_norm_count")
//            //      //let x_values = parsedData.map(item => item['log_2_plus_norm_count']);
//            //      newFigure.data[0].x = data.map(item => item['log_2_plus_norm_count']);
//            //  }
//            //  else{
//            //      //console.log("Changing Data to normalized_count")
//            //      newFigure.data[0].x = data.map(item => item['normalized_count']);
//            //  }
//
//             return newFigure;
//         }
//     }
// });

// window.dash_clientside = Object.assign({}, window.dash_clientside, {
//     clientside: {
//         make_histogram: function(figure, scale) {
//             var trace = {
//                 x: x,
//                 type: 'histogram',
//               };
//             var data = [trace];
//             return Plotly.newPlot('myDiv', data);
//
//
//             let newFigure = JSON.parse(JSON.stringify(figure)); // Deep copy of the figure
//             if (scale) {
//                 newFigure.layout.title = 'Log is On';
//                 newFigure.layout.yaxis['type'] = 'log'
//             }
//             else {
//                 newFigure.layout.title = 'Log y is off';
//             }
//             return newFigure;
//         }
//     }
// });



// // show legend
// if(!window.dash_clientside) {window.dash_clientside = {};}
// window.dash_clientside.clientside = {
//     display:{
//         show_legend: function(figure_data, input_showlegend) {
//
//             console.log('input_showlegend: ' + input_showlegend)
//
//             var show_legend_ind = false
//
//             if (input_showlegend === "Y") {
//                 show_legend_ind = true
//             }
//
//             const fig = Object.assign({}, figure_data, {
//                 'layout': {
//                     ...figure_data.layout,
//                     'showlegend': show_legend_ind
//                 }
//             });
//             return fig;
//         }
//     }
// }


// window.dash_clientside = Object.assign({}, window.dash_clientside, {
//     clientside: {
//         update_histogram: function(figData,log_y,) {
//             // //let newFig = {...figData};
//             // let newFig = JSON.parse(JSON.stringify(figData));
//             // if (log_count) {
//             //     newFig.data.forEach(trace => {
//             //         trace.x = trace.x.map(value => Math.log2(value + 0.01));
//             //         //trace.x = trace.x.map(value => value+100);
//             //     });
//             // }
//             // // else {
//             // //     newFig = {...figData};
//             // //
//             // // }
//             //
//             // if (log_y) {
//             //     newFig.layout.yaxis.type = 'log';
//             // } else {
//             //     newFig.layout.yaxis.type = 'linear';
//             // }
//             // // if (violin) {
//             // //     newFig.data.forEach(trace => {
//             // //         trace.type = 'violin';
//             // //         //trace.box = {visible: true}; // Show box within violin plot
//             // //         //trace.points = 'all'; // Show all points
//             // //     });
//             // // }
//             console.log(figData)
//             if(figData === undefined) {
//                 return {'data': [], 'layout': {}};
//             }
//             const fig = Object.assign({}, figData, {
//                 'layout': {
//                     ...figData.layout,
//                     'yaxis': {
//                         ...figData.layout.yaxis,
//                         type: log_y
//                     }
//                  }
//             });
//             return fig;
//
//             // return [newFig, newFig];
//         }
//     }
// });