//--------------------------------------------------------------------------------
// Chart 
// (from highcharts.com)
//--------------------------------------------------------------------------------
function init_chart() {
    var chart = Highcharts.chart('container', {
	chart: {
        type: 'line',
        animation: false, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {
                series = [];
            }
        }
    },
    title: {
        text: 'Share Prices by Day'
    },
    yAxis: {
        title: {
            text: 'Price [$]'
        },
        gridLineWidth: 1,
    },
    xAxis: {
    	title: {
            text: 'Days'
        },
        min: 0,
        max: length-1,
        allowDecimals: true,
    },
    plotOptions: {
        series: {
            states: {
                hover: {
                    enabled: true
                }
            },
            marker: {
                enabled: false
            }
        }
    },
    legend: {
        enabled: true,
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        borderWidth: 1
    },
    tooltip: {
        animation:true,
        enabled: true,
    },
    series: [{
        name: 'Share 1',
        data: [],
    }, {
        name: 'Share 2',
        data: [],
    }, {
        name: 'Share 3',
        data: [],
    }, {
        name: 'Share 4',
        data: [],
    }, {
        name: 'Share 5',
        data: [],
    }, {
        name: 'Share 6',
        data: [],
    }],
    });
return chart;
}
