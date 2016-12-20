//get user input

$(document).ready(function() {
    $('select').material_select();
});

var interestMap = {
    "frontend": "Front-End",
    "backend": "Back-End",
    "mobile": "Mobile",
    "database": "Database",
    "testing_qa": "Testing/QA",
    "ui_ux": "UI/UX",
    "3dprinting": "3D Printing",
    "hardware": "Hardware",
    "fintech": "Finance/ FinTech",
    "cyber_security": "Cyber Security",
    "AI": "Artificial Intelligence",
    "robotics":"Robotics"
}
var checkBoxValues = [];

$('#go').click(function() {
    $("#results").empty();
    var locationPref="";
    var university = "";
    var sortBy = $('#sortBy').val();
    var sortByYear = $('#sortByYear').val();
    university = $("#university").val();
    locationPref = $("#sortByLocation").val();
    if (sortByYear == null){
        sortByYear="";
    }
    var word = $("#search").val();
    console.log("Search word: "+word);
    getCheckedBoxes();
    console.log(checkBoxValues)
    spinner = new Spinner(opts).spin(target);
    console.log(sortByYear);
    var query = createQuery(sortBy, sortByYear, checkBoxValues, locationPref, word, university);
    getpostdata(query);

    //console.log(checkBoxValues);
})

function getCheckedBoxes() {
    checkBoxValues = [];
    $(".check").each(function() {
        if ($(this).prop('checked')) {
            checkBoxValues.push(interestMap[$(this).val()]);
        }
    });
}

function createQuery(sortBy, year, interests, location, word, university) {
    var query = { "sortBy": sortBy, "year": year, "interests": interests, "location":location, "word":word,"university":university };
    return query;
}

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

function getpostdata(sortdata = {}) {
    console.log("sortdata: ");
    console.log(sortdata);
    $.ajax({
        type: 'POST',
        url: '/search',
        data: JSON.stringify(sortdata),
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
            //sort the data alphabetically (for now)
            sortByKey(newdata, "Name", "lastname");
            console.log('new sorted data');
            console.log(newdata);
            populateData(newdata);

        }
    });
}

function sortByKey(array, key, key2) {
    return array.sort(function(a, b) {
        var x = a[key][key2];
        var y = b[key][key2];

        if (typeof x == "string") {
            x = x.toLowerCase();
        }
        if (typeof y == "string") {
            y = y.toLowerCase();
        }

        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}


function populateData(data) {
    console.log("Data length: " + data.length);
    var nameInfo = "";
    var totalData = "";
    for (var i = 0; i < data.length; i++) {
        var studentdata = "<div class='profile'>";
        for (var key in data[i]) {
            if (key == "_id") {
                //do nothing
            } else if (key == "Name") {
                nameInfo = "<div class='name'>" + data[i]["Name"]["lastname"] + ", " + data[i]["Name"]["firstname"] + "</div>";
            } else {
                studentdata = studentdata + "<h5 class='title'>" +
                    key + "</h5> " + data[i][key] + "<hr>";
            }
        }
        studentdata = '<li><div class="collapsible-header">' + nameInfo +
            "</div><div class='collapsible-body'>" +
            studentdata + "</div></li>";

        totalData = totalData + studentdata;
    }
    $('#results').html("<ul class='collapsible popout' data-collapsible='accordion'>" +
        $('#results').html() + totalData + "</ul>");

    $('.collapsible').collapsible();
}
