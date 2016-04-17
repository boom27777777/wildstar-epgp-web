$(document).ready(function () {
    $('#guild-table').tablesorter();
});

$("tbody#guild-body > tr.guild-index").hover(
    function () {
        $(this).addClass("active");
    },
    function () {
        $(this).removeClass("active");
    }
).click(function () {
        window.location.href = $(this).find("td.epgp_bold > a").attr("href");
    });

$("#form-filter").keyup(function () {
    //split the current value of searchInput
    var data = this.value.split(" ");
    //create a jquery object of the rows
    var jo = $("#guild-body").find("tr");
    if (this.value == "") {
        jo.show();
        return;
    }
    //hide all the rows
    jo.hide();

    //Recusively filter the jquery object to get results.
    jo.filter(function (i, v) {
        var $t = $(this);
        var search = $t.context.outerHTML
            .toLowerCase()
            .replace(/<(?:.|\n)*?>/gm, '')
            .replace(/\r?\n|\r|\W/gm, '');
        var substring = data.slice(0, data.length)
            .toString()
            .replace(/\W/gm, '');
        return search.indexOf(substring.toLowerCase()) > -1;
    })
        //show the rows that match.
        .show();
}).focus(function () {
    this.value = "";
    $(this).css({
        "color": "black"
    });
    $(this).unbind('focus');
}).css({
    "background-color": "#E6E6E6"
});
