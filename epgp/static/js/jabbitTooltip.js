function JHassignTooltips() {
    var t = {items: [], spells: [], schematics: []};
    JHJQ("a").each(function (a, e) {
        e.hostname.toLowerCase() == JH_HOST && (e.pathname && 0 == e.pathname.indexOf("/items/") && "/items/" != e.pathname && (JHJQ(e).attr("data-jh-tt", "1"), JHJQ(e).addClass("jh-tt-item"), t.items[t.items.length] = e.pathname.substr(e.pathname.lastIndexOf("/") + 1)), e.pathname && 0 == e.pathname.indexOf("/spells/") && "/spells/" != e.pathname && (JHJQ(e).attr("data-jh-tt", "1"), JHJQ(e).addClass("jh-tt-spell"), t.spells[t.spells.length] = e.pathname.substr(e.pathname.lastIndexOf("/") + 1)), e.pathname && 0 == e.pathname.indexOf("/schematics/") && "/schematics/" != e.pathname && (JHJQ(e).attr("data-jh-tt", "1"), JHJQ(e).addClass("jh-tt-sch"), t.schematics[t.schematics.length] = e.pathname.substr(e.pathname.lastIndexOf("/") + 1)))
    }), JH_options && JH_options.preload && (t.items.length && JHJQ.ajax("http://" + JH_HOST + "/items/preload", {
        type: "POST",
        data: {items: t.items},
        complete: function (t, a) {
        },
        error: function (t, a, e) {
        },
        success: function (t, a, e) {
            var s = JHJQ.parseJSON(t);
            JHJQ("a[data-jh-tt]").each(function (t, a) {
                if (JHJQ(a).hasClass("jh-tt-item")) {
                    var e = a.pathname.substr(a.pathname.lastIndexOf("/") + 1);
                    s[e] && (JH_options.colors && (JH_options.whitebg && 2 == parseInt(s[e].q) ? JHJQ(a).addClass("jhitemquality" + s[e].q + "b") : JHJQ(a).addClass("jhitemquality" + s[e].q)), JH_options.names && s[e].n && "" != s[e].n && JHJQ(a).text(s[e].n))
                }
            })
        }
    }), t.spells.length && JHJQ.ajax("http://" + JH_HOST + "/spells/preload", {
        type: "POST",
        data: {spells: t.spells},
        complete: function (t, a) {
        },
        error: function (t, a, e) {
        },
        success: function (t, a, e) {
            var s = JHJQ.parseJSON(t);
            JHJQ("a[data-jh-tt]").each(function (t, a) {
                if (JHJQ(a).hasClass("jh-tt-spell")) {
                    var e = a.pathname.substr(a.pathname.lastIndexOf("/") + 1);
                    s[e] && JH_options.names && s[e].n && "" != s[e].n && JHJQ(a).text(s[e].n)
                }
            })
        }
    }), t.schematics.length && JHJQ.ajax("http://" + JH_HOST + "/schematics/preload", {
        type: "POST",
        data: {schematics: t.schematics},
        complete: function (t, a) {
        },
        error: function (t, a, e) {
        },
        success: function (t, a, e) {
            var s = JHJQ.parseJSON(t);
            JHJQ("a[data-jh-tt]").each(function (t, a) {
                if (JHJQ(a).hasClass("jh-tt-sch")) {
                    var e = a.pathname.substr(a.pathname.lastIndexOf("/") + 1);
                    s[e] && JH_options.names && s[e].n && "" != s[e].n && JHJQ(a).text(s[e].n)
                }
            })
        }
    })), JHJQ("a[data-jh-tt]").mouseout(function (t) {
        window._jhttl = null
    }), JHJQ(document).tooltip({
        position: {my: "left bottom", at: "left top-10", collision: "flipfit"},
        items: "a[data-jh-tt]",
        close: function (t, a) {
            JHJQ(".ui-tooltip").hide(), window._jhttl = null
        },
        open: function (t, a) {
            JH_options && (JH_options.zIndex ? a.tooltip.css("z-index", JH_options.zIndex) : JH_options.zindex && a.tooltip.css("z-index", JH_options.zindex))
        },
        content: function (t) {
            window._jhttl = this;
            var a = this, e = this.pathname;
            if (JH_tooltip_cache[e]) {
                if (JH_options) {
                    var s = JHJQ(JH_tooltip_cache[e]);
                    if (JH_options.colors) {
                        var n = s.attr("data-q");
                        JH_options.whitebg && 2 == parseInt(n) ? JHJQ(a).addClass("jhitemquality" + n + "b") : JHJQ(a).addClass("jhitemquality" + n)
                    }
                    if (JH_options.names) {
                        var i = s.attr("data-n");
                        i && "" != i && JHJQ(a).text(i)
                    }
                }
                return JH_tooltip_cache[e]
            }
            JHJQ.ajax("http://" + JH_HOST + e + "?i", {
                type: "GET", complete: function (t, a) {
                }, error: function (a, e, s) {
                    t('<div class="jhttsp fleft" data-q="none"><div class="jhttt" style="color:#fff">Unable to load tooltip at this moment</div></div>')
                }, success: function (s, n, i) {
                    if (JH_tooltip_cache[e] = s, a == window._jhttl) {
                        if (JH_options) {
                            var o = JHJQ(s);
                            if (JH_options.colors) {
                                var J = o.attr("data-q");
                                JH_options.whitebg && 2 == parseInt(J) ? JHJQ(a).addClass("jhitemquality" + J + "b") : JHJQ(a).addClass("jhitemquality" + J)
                            }
                            if (JH_options.names) {
                                var l = o.attr("data-n");
                                JHJQ(a).text(l)
                            }
                        }
                        t(s)
                    }
                }
            })
        }
    })
}
function JHinitialize() {
    JHJQ(document).ready(function () {
        JHJQ("head").append(JHJQ('<link rel="stylesheet" type="text/css" />').attr("href", "http://" + JH_HOST + "/api/tooltips.css")), JHassignTooltips(), JHJQ(".ui-tooltip").mouseover(function () {
            JHJQ(".ui-tooltip").hide()
        }).remove()
    })
}
var JH_tooltip_cache = [], JH_HOST = "www.jabbithole.com", JHOldJQuery = window.jQuery, JHOldCashSign = window.$;
$(document).ready(function () {
    var t = document.createElement("script");
    t.src = "http://" + JH_HOST + "/api/jquery-ui-min.js", t.onload = function () {
        window.JHJQ = window.jQuery, JHinitialize(), window.jQuery = JHOldJQuery, window.$ = JHOldCashSign
    }, document.head.appendChild(t)
});
