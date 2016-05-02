Parse.initialize("6YoHwLPVTyMmN71PXvd78w4jWElbvUBzoGEm2YCg", "JLNEVdY3KWo42t89GzSo5yi2BmUUwafZfELyuio4");
var current_url;
chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
     current_url = tabs[0].url;
});

function addView(sourceUrl) {
    var View = Parse.Object.extend("View");
    var view = new View();

    var data = {
        sourceUrl: sourceUrl,
    };

    view.save(data);
}


function addNewCloud(data) {
    Parse.Cloud.run('addActBack', data, {
        success: function (response) {
            console.log('addNewCloud response ->', response);
            alert("תודה! נוסף בהצלחה וממתין לאישור!");
            showAdd(false);
        },
        error: function (error) {
            console.log('addNewCloud error ->', error);
            alert("סליחה, חלה שגיאה בהוספה, נסה/י מאוחר יותר.");
            showAdd(false);
        }
    });
}

function addNew(sourceUrl, destinationUrl, title, subtitle, actType) {
    var data = {
        sourceUrl: sourceUrl,
        destinationUrl: destinationUrl,
        title: title,
        subtitle: subtitle,
        actType: actType
    };

    addNewCloud(data);

    //var Actback = Parse.Object.extend("Actback");
    //var actback = new Actback();
    //
    //actback.save(data).then(function (object) {
    //    console.log('object ->', object);
    //    alert("תודה! נוסף בהצלחה!");
    //    showAdd(false);
    //});

}

function addEvent(title, link, subtitle, actType) {
    var div = document.querySelector('.events');

    var eventDiv = document.querySelector('.event');
    var cln = eventDiv.cloneNode(true);
    cln.querySelector('.title a').innerHTML = title;
    cln.querySelector('.title a').href = link;
    cln.querySelector('.subtitle .text').innerHTML = subtitle;

    switch (actType) {
        case 1:
            cln.querySelector('.label.demonstration').className += ' on';
            break;

        case 2:
            cln.querySelector('.label.donation').className += ' on';
            break;

        case 3:
            cln.querySelector('.label.cause').className += ' on';
            break;

        case 4:
            cln.querySelector('.label.event').className += ' on';
            break;

        case 5:
            cln.querySelector('.label.volunteer').className += ' on';
            break;
    }

    div.appendChild(cln);
}

function loadActbacks(actbacks) {

    if (actbacks.length) {

        document.querySelector('.actHeader').style.display = 'block';
        document.querySelector('.actCount').innerHTML = actbacks.length;

    } else {
        document.querySelector('.section-empty').style.display = 'block';
    }

    actbacks.forEach(function (actback) {
        var data = actback.toJSON();
        console.log('data ->', data);
        addEvent(data.title, data.destinationUrl, data.subtitle, data.actType);
    });
}

function loadParseData(_sourceUrl) {
    var Actback = Parse.Object.extend("Actback");
    var query = new Parse.Query(Actback);
    query.equalTo("active", true);
    query.equalTo("sourceUrl", _sourceUrl);
    query.find({
        success: function (results) {
            console.log("Successfully retrieved " + results.length + " scores.");
            // Do something with the returned Parse.Object values
            loadActbacks(results);
        },
        error: function (error) {
            console.log("Error: " + error.code + " " + error.message);
        }
    });
}

function showAdd(show) {
    if (show) {
        document.querySelector('.section-add').style.display = 'block';
        document.querySelector('.section-main').style.display = 'none';
        document.querySelector('.section-empty').style.display = 'none';
        document.querySelector('form .destinationUrl').value = current_url;
    } else {
        document.querySelector('.section-main').style.display = 'block';
        document.querySelector('.section-add').style.display = 'none';
        document.querySelector('.section-empty').style.display = 'none';
    }
}

var search = document.location.search,
    searchParts = search.split('='),
    sourceUrl = searchParts[1];

addView(sourceUrl);

if (searchParts[0] === '?sourceUrl') {
    loadParseData(sourceUrl);
}


document.querySelector('form .cancel').onclick = function () {
    showAdd(false);
};

document.querySelector('.button.add').onclick = function () {
    showAdd(true);
};

document.querySelector('.button.add-big').onclick = function () {
    showAdd(true);
};

document.querySelector('form .parse.add').onclick = function () {
    var title = document.querySelector('form .title').value,
        destinationUrl = document.querySelector('form .destinationUrl').value,
        actType = parseInt(document.querySelector('form .actType').value, 10),
        subtitle = document.querySelector('form .subtitle').value;

    if (title.length < 1) {
        alert('יש למלא כותרת לפעולה. נניח שם האירוע בפייסבוק.');
        return;
    }

    if (destinationUrl.length < 1) {
        alert('יש להזין לינק לפעולה. נניח של דף האירוע בפייסבוק.');
        return;
    }

    if (actType < 1) {
        alert('יש לבחור סוג פעולה מתוך הרשימה.');
        return;
    }

    if (subtitle.length < 6) {
        alert('יש להזין מידע נוסף בשדה האחרון.');
        return;
    }

    addNew(sourceUrl, destinationUrl, title, subtitle, actType);
};

//addNew('http://www.ynet.co.il/articles/0,7340,L-4719997,00.html', 'https://www.facebook.com/events/710949225660153/', 'היום הבינלאומי נגד מקדונלדס - הפגנה בחיפה!', 'מחר ב- 18:30.', 1);

