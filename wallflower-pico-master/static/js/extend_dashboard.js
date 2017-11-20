var ul = $('ul#side-menu');
$.ajax({
    url : '/static/extend_dashboard_links.html',
    type: "get",
    success : function(response){
        console.log("Load /static/extend_dashboard_links.html");
        ul.append(response);
    }
});

var wrapper = $('div#wrapper');
$.ajax({
    url : '/static/extend_dashboard_pages.html',
    type: "get",
    success : function(response){
        console.log("Load /static/extend_dashboard_pages.html");
        wrapper.append(response);
        
        // Form submit call goes here.
        $("form#form-input").submit( onInputFormSubmit );
    }
});

/* Add function to get points for report page */
function getPoints( the_network_id, the_object_id, the_stream_id, callback ){
    var query_data = {};
    var query_string = '?'+$.param(query_data);
    var url = '/networks/'+the_network_id+'/objects/'+the_object_id;
    url += '/streams/'+the_stream_id+'/points'+query_string; 
    
    // Send the request to the server
    $.ajax({
        url : url,
        type: "get",
        success : function(response){
            console.log( response );
            if( response['points-code'] == 200 ){
                var num_points = response.points.length
                var most_recent_value = response.points[0].value
                console.log("Most recent value: "+most_recent_value);
                console.log("Number of points retrieved: "+num_points);
                callback( response.points );
            }
        },
        error : function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
        }
    });
}

// Call getPoints if Input or Report is selected
// ...added feature to dynamically update plot as new data becomes available
custom_sidebar_link_callback = function( select ){
    if (select == 'input') {
    }
    else if (select == 'report'){
        var plotCalls = 0;
        var plotTimer1 = setInterval(function(){
            getPoints('local','arduino-uno','parking-spot1', function(points){
                console.log( "The points request was successful!" );
                loadPlot1( points );
            });
            if(plotCalls > 60){
                console.log('Clear timer');
                clearInterval (plotTimer);
            }
            else{
            plotCalls += 1;
            }
        }, 1000);
        var plotTimer2 = setInterval(function(){
            getPoints('local','arduino-uno','parking-spot2', function(points){
                console.log( "The points request was successful!" );
                loadPlot2( points );
            });
            if(plotCalls > 60){
                console.log('Clear timer');
                clearInterval (plotTimer);
            }
            else{
            plotCalls += 1;
            }
        }, 1000);
    }
}

/* Function to plot temperature points using Highcharts */
function loadPlot1( points ){
    var plot = $('#content-report1');
    // Check if plot has a Highcharts element
    if( plot.highcharts() === undefined ){
        // Create a Highcharts element
        plot.highcharts( report_plot_options1 );
    }
    // Iterate over points to place in Highcharts format
    var datapoints = [];
    for ( var i = 0; i < points.length; i++){
        var at_date = new Date(points[i].at);
        var at = at_date.getTime() - at_date.getTimezoneOffset()*60*1000;
        datapoints.unshift( [ at, points[i].value] );
    }
    // Update Highcharts plot
    if( plot.highcharts().series.length > 0 ){
        plot.highcharts().series[0].setData( datapoints ); 
    }
    else{
        plot.highcharts().addSeries({
            name: "Parking Spot 1",
            data: datapoints
        });
    }
} 

var report_plot_options1 = {
    title: {
        text: 'Parking Spot 1'
    },
    chart: {
        type: 'spline'
    },
    xAxis: { type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
            
        },
    },
    yAxis: { title: {
                     text: 'Spots Available'
                    }
    },
};

/* Function to plot light intensity points using Highcharts */
function loadPlot2( points ){
    var plot = $('#content-report2');
    // Check if plot has a Highcharts element
    if( plot.highcharts() === undefined ){
        // Create a Highcharts element
        plot.highcharts( report_plot_options2 );
    }
    // Iterate over points to place in Highcharts format
    var datapoints = [];
    for ( var i = 0; i < points.length; i++){
        var at_date = new Date(points[i].at);
        var at = at_date.getTime() - at_date.getTimezoneOffset()*60*1000;
        datapoints.unshift( [ at, points[i].value] );
    }
    // Update Highcharts plot
    if( plot.highcharts().series.length > 0 ){
        plot.highcharts().series[0].setData( datapoints ); 
    }
    else{
        plot.highcharts().addSeries({
            name: "Parking Spot 2",
            data: datapoints
        });
    }
} 

var report_plot_options2 = {
    title: {
        text: 'Parking Spot 2'
    },
    chart: {
        type: 'spline'
    },
    xAxis: { type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
            
        },
    },
    yAxis: { title: {
                     text: 'Spots Available'
                    }
    },
};