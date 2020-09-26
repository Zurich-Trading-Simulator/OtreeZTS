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
        allowDecimals: false,
    },
    plotOptions: {
        series: {
            states: {
                hover: {
                    enabled: false
                }
            },
            marker: {
                enabled: false
            }
        }
    },
    legend: {
        enabled: false,
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        borderWidth: 1
    },
    tooltip: {
        animation:false,
        enabled: false,
    },
    series: [{
        //name: 'Random data',
        data: [],
        label: {
    		enabled: false,
		}
    }],
    });
return chart;
}
