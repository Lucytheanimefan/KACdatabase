//get user input

$(document).ready(function() {
    $('select').material_select();
});


$('#go').click(function() {
    var sortBy = $('#sortBy').val();
    console.log(sortBy);
    spinner = new Spinner(opts).spin(target);
    getpostdata();
})


var opts = {
    lines: 13 // The number of lines to draw
        ,
    length: 28 // The length of each line
        ,
    width: 14 // The line thickness
        ,
    radius: 42 // The radius of the inner circle
        ,
    scale: 1 // Scales overall size of the spinner
        ,
    corners: 1 // Corner roundness (0..1)
        ,
    color: '#000' // #rgb or #rrggbb or array of colors
        ,
    opacity: 0.25 // Opacity of the lines
        ,
    rotate: 0 // The rotation offset
        ,
    direction: 1 // 1: clockwise, -1: counterclockwise
        ,
    speed: 1 // Rounds per second
        ,
    trail: 60 // Afterglow percentage
        ,
    fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
        ,
    zIndex: 2e9 // The z-index (defaults to 2000000000)
        ,
    className: 'spinner' // The CSS class to assign to the spinner
        ,
    top: '50%' // Top position relative to parent
        ,
    left: '50%' // Left position relative to parent
        ,
    shadow: false // Whether to render a shadow
        ,
    hwaccel: false // Whether to use hardware acceleration
        ,
    position: 'absolute' // Element positioning
}

var target = document.getElementById('results')

function getpostdata() {
    $.ajax({
        type: 'POST',
        url: '/search',
        data: '',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            spinner.stop();
            console.log('ajax success');
            var data = response["result"];
            var newdata = []
            for (var i = 1; i < data.length; i++) {
                newdata.push(JSON.parse(data[i]));
            }
			console.log(newdata);
            //sort the data alphabetically (for now)
            sortByKey(newdata, "Name", "lastname");
            console.log('new sorted data');
            console.log(newdata);

        }
    });
}

function sortByKey(array, key, key2) {
    return array.sort(function(a, b) {
        var x = a[key][key2];
        var y = b[key][key2];

        if (typeof x == "string")
        {
            x = x.toLowerCase(); 
        }
        if (typeof y == "string")
        {
            y = y.toLowerCase();
        }

        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}

