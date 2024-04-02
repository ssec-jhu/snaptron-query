var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.StudyLink = function (props) {
    return React.createElement(
        'a',
        {href: 'https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=' + props.value,
            target: '_blank',
            rel:"noopener noreferrer"},
        props.value
    );
};
