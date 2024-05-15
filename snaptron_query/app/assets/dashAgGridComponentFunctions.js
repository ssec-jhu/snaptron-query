var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.StudyLink = function (props) {
    var url = "https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=" + props.value;
    return React.createElement(
        window.dash_html_components.A,{
            children: props.value,
            href: url,
            target: '_blank',
            rel:"noopener noreferrer",
            className: 'study-link-color'
        }
    );
};
