var Highcharts;
var optionSelected;
var dropdown = $('#option_selector');

var url = '../assets/menu/cost.json'


// Menu details
$.getJSON(url, function (data) {

    $.each(data, function (key, entry) {
        dropdown.append($('<option></option>').attr('value', entry.desc).text(entry.name));
    });

    // Load the first Option by default
    var defaultOption = dropdown.find("option:first-child").val();
    optionSelected = dropdown.find("option:first-child").text();

    // Generate
    generateChart(defaultOption);

});


// Dropdown
dropdown.on('change', function (e) {

    $('#option_selector_title').remove();

    // Save name and value of the selected option
    optionSelected = this.options[e.target.selectedIndex].text;
    var valueSelected = this.options[e.target.selectedIndex].value;

    //Draw the Chart
    generateChart(valueSelected);
});


// Graphs/s
function generateChart(fileNameKey) {

    $.getJSON('../../warehouse/numerics/cost/fnr/' + fileNameKey + '.json', function (calculations) {

        let data = calculations.data;
        let numbers = calculations.approximate_annual_numbers;
        let latest = numbers.map(function (value){
            return parseInt(value);
        });

        Highcharts.chart("container0001", {
            chart: {
                type: "arearange",
                zooming: {
                    type: "x",
                },
                scrollablePlotArea: {
                    scrollPositionX: 1,
                }
            },
            credits: {
                enabled: false
            },
            title: {
                text: "By false negative rates<br>"
            },
            subtitle: {
                text:
                    '~ # of Missed Entities per Annum: [' + Math.min(...latest).toLocaleString('en') + ', ...]<br>' +
                    'Cost per Missed Entity: £' + Highcharts.numberFormat(calculations.cost, 2)
            },
            xAxis: {
            },
            yAxis: {
                type: 'logarithmic',
                title: {
                    text: null,
                },
            },
            tooltip: {
                crosshairs: true,
                shared: true,
                valueSuffix: "£",
                headerFormat: '<b>FNR: {point.x:,.3f}</b><br>',
                pointFormat: '<b>Est. Cost Range</b> (£): <b>[{point.low:,.2f}, {point.high:,.2f}]</b><br>'
            },
            legend: {
                enabled: false,
            },
            series: [
                {
                    name: "Cost",
                    color: {
                        linearGradient: {
                            x1: 0,
                            x2: 0,
                            y1: 0,
                            y2: 1,
                        },
                        stops: [
                            [0, "#ff0000"],
                            [1, "#000000"],
                        ],
                    },
                    data: data
                }
            ]
        });


    }).fail(function () {
        console.log("Missing");
        $('#container0001').empty();
    });


    $.getJSON('../../warehouse/numerics/cost/fpr/' + fileNameKey + '.json', function (calculations) {

        var data = calculations.data;

        Highcharts.chart("container0002", {
            chart: {
                type: "arearange",
                zooming: {
                    type: "x",
                },
                scrollablePlotArea: {
                    scrollPositionX: 1,
                },
            },
            credits: {
                enabled: false
            },
            title: {
                text: "By false positive rates<br>"
            },
            subtitle: {
                text:
                    '~ # of Missed Entities per Annum: [..., ...]<br>' +
                    'Cost per Missed Entity: ...<br>'
            },
            xAxis: {

            },
            yAxis: {
                type: 'logarithmic',
                title: {
                    text: null,
                },
            },
            tooltip: {
                crosshairs: true,
                shared: true,
                valueSuffix: "£",
                headerFormat: '<b>FPR: {point.x:,.3f}</b><br>',
                pointFormat: '<b>Est. Cost Range</b> (£): <b>[{point.low:,.2f}, {point.high:,.2f}]</b><br>'
            },
            legend: {
                enabled: false,
            },
            series: [
                {
                    name: "Cost",
                    color: {
                        linearGradient: {
                            x1: 0,
                            x2: 0,
                            y1: 0,
                            y2: 1,
                        },
                        stops: [
                            [0, "#ff0000"],
                            [1, "#000000"],
                        ],
                    },
                    data: data
                }
            ]
        });


    }).fail(function () {
        console.log("Missing");
        $('#container0002').empty();
    });


}
