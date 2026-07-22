function popitup(url) {
    "use strict";
    var newwindow=window.open(url,'name','height=250,width=800,resizable,scrollbars');
    if (window.focus) {newwindow.focus();}
    return false;
}
