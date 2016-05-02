var extensionOrigin = 'chrome-extension://' + chrome.runtime.id;

$(document).ready(function () {
    loadUI();
});

var iframeDiv;

function loadUI() {
    var imageUrl = chrome.runtime.getURL('270b.png');

    document.querySelector('.top-story-main').style.position = 'relative';

    var link, icon;

    link = document.querySelector('.top-story-main a').href;

    icon = $('<div>')
        .addClass('ynet-actBack-icon-1')
        .attr('style', 'z-index:999999;cursor:pointer;position:absolute; left:10px; top: 10px; width:40px; height:40px;background-color:rgba(255,255,255,0.8); padding:2px; background-image:url("' + imageUrl + '");background-repeat:no-repeat;background-size:100% auto;')
        .attr('data-link', link)
        .appendTo('.top-story-main')
        .on('click', onClick);

    var articles = $('.str3s');

    for (var cnt = 0; cnt < articles.length; cnt++) {

        var article = articles[cnt];

        link = $(article)
            .css('position', 'relative')
            .find('a').attr('href');

        link  = 'http://www.ynet.co.il' + link;

        icon = $('<div>')
            .addClass('ynet-actBack-icon-' + (cnt + 2))
            .attr('style', 'z-index:999999;cursor:pointer;position:absolute; left:10px; top: 10px; width:40px; height:40px;background-color:rgba(255,255,255,0.8); padding:2px; background-image:url("' + imageUrl + '");background-repeat:no-repeat;background-size:100% auto;')
            .attr('data-link', link)
            .appendTo(article)
            .on('click', onClick);
    }

    iframeDiv = $('<div>')
        .addClass('ynet-actBack-iframe-wrapper')
        .attr('style', 'z-index:999999;position:absolute; left:60px; top: 10px; width:418px; height:400px;border:1px solid green;background-color:rgba(255,255,255,1);')
        .appendTo('body')
        .hide();

    var url = chrome.runtime.getURL('frame.html');

    $('<iframe>')
        .addClass('ynet-actBack-iframe')
        .attr('src', url)
        .attr('style', 'border: none; width: 100%; height: 100%;')
        .appendTo(iframeDiv);
}


function onClick(e) {
    var url = chrome.runtime.getURL('frame.html');

    var data = $(e.target).attr('data-link'),
        offset = $(e.target).offset();

    url += '?sourceUrl=' + data;

    $('.ynet-actBack-iframe-wrapper').toggle();
    iframeDiv.css({top: offset.top, left: offset.left + 60});

    if (!$('.ynet-actBack-iframe-wrapper').is(':visible')) {
        return;
    }

    $('.ynet-actBack-iframe')
        .attr('src', url);

}