var csvReadyData = "";

//get user input

$(document).ready(function() {
    $('select').material_select();
    $("#downloadCSV").prop("disabled",true);
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
    "robotics": "Robotics"
}
var checkBoxValues = [];

function submitQuery(accountType = null) {
    $("#results").empty();
    var university = $("#university").val();
    var name = $("#name").val();
    var locationPref = "";
    var sortBy = "";
    var sortByYear = "";
    var word  = "";
    if (accountType == "admin" || accountType == "company") {
        locationPref = $("#sortByLocation").val();
        sortBy = $('#sortBy').val();
        sortByYear = $('#sortByYear').val();
        word = $("#search").val();
        getCheckedBoxes();
    }
    if (sortByYear == null) {
        sortByYear = "";
    }

    spinner = new Spinner(opts).spin(target);
    var query = createQuery(sortBy, sortByYear, checkBoxValues, locationPref, word, university, name);
    getpostdata(query);
    $("#downloadCSV").prop("disabled",false);

    //console.log(checkBoxValues);
}

function getCheckedBoxes() {
    checkBoxValues = [];
    $(".check").each(function() {
        if ($(this).prop('checked')) {
            checkBoxValues.push(interestMap[$(this).val()]);
        }
    });
}

function createQuery(sortBy, year, interests, location, word, university, name) {
    var query = { "sortBy": sortBy, "year": year, "interests": interests, "location": location, "word": word, "university": university, "name": name };
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
    $.ajax({
        type: 'POST',
        url: '/search',
        data: JSON.stringify(sortdata),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            spinner.stop();
            console.log('ajax success');
            var data = response["result"];
            csvReadyData = Papa.unparse(data); //onvertToCSV(data);
            //console.log(csvReadyData);
            sortByKey(data, "Name");
            populateData(data);

        }
    });
}

function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key];
        var y = b[key];

        if (typeof x == "string") {
            x = x.toLowerCase();
        }
        if (typeof y == "string") {
            y = y.toLowerCase();
        }

        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}

$("#downloadCSV").click(function() {
    if (csvReadyData.length < 1) {
        alert("No data to write");
    } else {
        writeDataToCSV(csvReadyData);
    }
})

function writeDataToCSV(csvContent = "") {
    var encodedUri = encodeURI(csvContent);
    //console.log(encodedUri);
    var link = document.createElement("a");
    link.setAttribute("href", "data:text/csv;charset=utf-8," + encodedUri);
    link.setAttribute("download", "RTC_scholar_data.csv");
    document.body.appendChild(link); // Required for FF
    link.click();

}

function convertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var str = '';

    for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ',';
            /*if (index == "name") {
                line += array[i][index]["firstname"]+'\r\n'+array[i][index]["lastname"]
            } else {*/
            var value = '\"' + array[i][index].toString() + '\"';
            line += value;
            //}
        }

        str += line + '\r\n';
    }

    return str;
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
                nameInfo = "<div class='name'>" + data[i]["Name"] + "</div>";
            } else {
                studentdata = studentdata + "<h4 class='title'>" +
                    key + "</h4> " + data[i][key] + "<hr>";
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
