// noinspection DuplicatedCode

var Highcharts;
var optionSelected;
var dropdown = $('#option_selector');

var url = '../assets/menu/bullet.json'


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

    $.getJSON('../../warehouse/card/bullet/' + fileNameKey + '.json', function (calculations) {


        // Indices
        const iNegative = calculations.columns.indexOf('False Negative Rate');
        const iPositive = calculations.columns.indexOf('False Positive Rate');

        // Categories
        const categories = calculations.index;

        // Variables
        var fnr = [],
            fpr = [];

        // Curves
        for (let i = 0; i < calculations.data.length; i += 1) {
            fnr.push({
                y: calculations.data[i][iNegative],
                target: calculations.target[iNegative]
            });

            fpr.push({
                y: calculations.data[i][iPositive],
                target: calculations.target[iPositive]
            });
        }



        Highcharts.setOptions({
            chart: {
                inverted: true,
                marginLeft: 135,
                type: 'bullet',
                height: 125
            },
            title: {
                text: null
            },
            legend: {
                enabled: false
            },
            yAxis: {
                gridLineWidth: 0
            },
            plotOptions: {
                series: {
                    pointPadding: 0.25,
                    borderWidth: 0,
                    color: '#000',
                    targetOptions: {
                        width: '200%',
                        color: 'orange'
                    }
                }
            },
            credits: {
                enabled: false
            },
            exporting: {
                enabled: false
            }
        });


        Highcharts.chart('container0001', {
            xAxis: {
                categories: categories
            },
            yAxis: {
                plotBands: [{
                    from: 0,
                    to: 0.1,
                    color: '#666'
                }, {
                    from: 0.1,
                    to: 0.5,
                    color: '#999'
                }, {
                    from: 0.5,
                    to: 1,
                    color: '#bbb'
                }],
                labels: {
                    format: '{value}'
                },
                title: null,
                min: 0,
                max: 1
            },
            series: [{
                data: fnr
            }],
            tooltip: {
                pointFormat: '<b>{point.y}</b> (with expected maximum at {point.target})'
            }
        });


        Highcharts.chart('container0002', {
            xAxis: {
                categories: categories
            },
            yAxis: {
                plotBands: [{
                    from: 0,
                    to: 0.1,
                    color: '#666'
                }, {
                    from: 0.1,
                    to: 0.5,
                    color: '#999'
                }, {
                    from: 0.5,
                    to: 1,
                    color: '#bbb'
                }],
                labels: {
                    format: '{value}'
                },
                title: null,
                min: 0,
                max: 1
            },
            series: [{
                data: fpr
            }],
            tooltip: {
                pointFormat: '<b>{point.y}</b> (with expected maximum at {point.target})'
            }
        });


    }).fail(function () {
        console.log("Missing");
    });

}







