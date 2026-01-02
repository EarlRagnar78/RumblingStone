window.setMobileTable = function(selector) {
  // if (window.innerWidth > 600) return false;
  const tableEl = document.querySelectorAll(selector);
  console.log(tableEl);
  if (tableEl != null) {
      tableEl.forEach(function(curEl) {
          const thEls = curEl.querySelectorAll('thead th');
          //console.log(thEls);
          if (thEls != null && thEls.length > 0) {
              const tdLabels = Array.from(thEls).map(el => el.innerText);
              //console.log(tdLabels);
              curEl.querySelectorAll('tbody tr').forEach(tr => {
                  Array.from(tr.children).forEach(
                      (td, ndx) => td.setAttribute('label', tdLabels[ndx])
                  );
              });
          }
      });

  }
}
window.setMobileTable("table");
function aI() {
  var a;
  try {
    a = new XMLHttpRequest
  } catch (b) {
    try {
      a = new ActiveXObject("Msxml2.XMLHTTP")
    } catch (c) {
      try {
        a = new ActiveXObject("Microsoft.XMLHTTP")
      } catch (d) {
        return false;
      }
    }
  }
  return a;
}

function inPageAnc() {
	let ans = document.getElementsByClassName("inPage");
	for (let i = 0; i < ans.length; ++i) {
		setAncPag(ans[i]);
	}
}
function setAncPag(el) {
	el.onclick = function() { return onAncPag(this); };
}
function onAncPag(el) {
	console.log(el.href + " / "+el.parentNode.tagName);
	let par = el.parentNode;
	let sib = el.nextSibling;
	let inTb = false;
	if (el.parentNode.tagName == "TD") {
		par = el.parentNode.parentNode.parentNode;
		sib = el.parentNode.parentNode.nextSibling;
		inTb = true;
	}
	//let oldFrame = document.getElementById("inPageFrame");
  let oldFrame = sib;
	if (oldFrame != null && oldFrame.className === "inPageFrame") {
    if (oldFrame.dataset.inTbl === "true") oldFrame.parentElement.parentElement.parentElement.removeChild(oldFrame.parentElement.parentElement);
		else oldFrame.parentElement.removeChild(oldFrame);
    console.log(oldFrame + " / " + oldFrame.dataset.parClick);
		if (oldFrame.dataset.parClick === el.href) return false;
	}
	let ifr = document.createElement("iframe");
	ifr.className = "inPageFrame";
	ifr.src = el.href;
	ifr.style.width="100%";
	ifr.style.minHeight="100px";
	ifr.style.height="95vh";
	ifr.style.resize="both";
	ifr.style.overflow="auto";
	ifr.dataset.parClick=el.href;
  ifr.dataset.inTbl=inTb;
	par.insertBefore(ifr, sib);
	if (inTb) ifr.outerHTML = "<tr class='inPageFrame' data-par-click='"+el.href+"'><td colspan='100%'>"+ifr.outerHTML+"</td></tr>";
	return false;
}
inPageAnc();

function downloadFile(data, filename, type) {
    var file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}
function tweenDim(ele, dur, wid, hei) {
	ele = $(ele);
	ele.style.overflow = "hidden";
	ele.style.width = wid + "px";
	/*var n = new Fx.Styles(ele, {
        duration: dur,
    });
    n.start({
        width: [ele.width, wid],
        height: [ele.height, hei]
    });*/
}
function ajSub(e,n){var t=aI(),o=[].filter.call(e.elements,function(e){return!(e.type in["checkbox","radio"])||e.checked}).filter(function(e){return!!e.name}).filter(function(e){return!e.disabled}).map(function(e){return encodeURIComponent(e.name)+"="+encodeURIComponent(e.value)}).join("&");return t.open("POST",e.action),t.setRequestHeader("Content-type","application/x-www-form-urlencoded"),t.onload=function(){n(t)},t.send(o),!1}

function aG(a/*, b, c*/) {
    var d = aI();
    if (d == false) return false;
    /*d.onreadystatechange = function () {
        d.readyState == 4 && b(d.responseText, c)
    };*/
    d.open("GET", a, true);
    d.send(null);
    return true
}

function clkAP(ele,ur,pa,cal,vr) { aP(ur,pa,cal,vr); return true; }
function onTst(e,t) { }

function aPS(a, b, c, d, z) {
    var e = aI();
    if (e == false) return false;
    e.onreadystatechange = function () {
        e.readyState == 4 && c(e.responseText, d)
    };
    e.open("POST", a, true);
    e.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    e.send(b);
    if (z) tP(a);
    return true
}

function aP(a, b, c, d) {
    return aPS(a, b, c, d, true)
}

function aR(a, b) {
	$(b).innerHTML = a
}

function gPI(a) {
    a = a.href.match(/.com\/([^#.]+)/);
    return a = a != null ? a[1] : "home"
}

function gP(a, b) {
    var c, d;
    if (typeof a == "string") {
        if (a.indexOf("http:") != 0 && a.indexOf("/") != 0) a = "/" + a;
        c = a;
        d = c;
        if (c == "home") d = "http://" + window.location.hostname
    } else {
        c = gPI(a);
        d = a.href
    }
    if (window.oldLink == a || window.curPage == c || window.location.href.toLowerCase().indexOf("/" + c + "/") != -1 && window.curPage == undefined) if (b != -99) return true;
    window.oldLink = a;
    $("load").style.visibility = "visible";
    document.body.style.cursor = "wait";
    hS();
    //aPS("/site/apps/rotation.php", "url=" + d, aR, "footRotation", false);
    return aP(d, "frames=false", oL, b)
}

function oL(a, b) {
    var c;
    c = typeof window.oldLink == "string" ? window.oldLink : gPI(window.oldLink);
    if ($("content")) $("content").innerHTML = a;
    $("resize") == null && mRS();
    if (b) window.location = "#" + c;
    window.curPage = c;
    window.oldLink = null;
    sPD();
    //sL();
    document.body.style.cursor = "default";
    try {
        $("load").style.visibility = "hidden";
        $("page").style = null;
        $("titleSpacer1").style = null;
        $("titleSpacer4").style = null;
        $("main").style = null;
    } catch (a) {}
}

function cF(a, b, c, d, e, g) {
    var f, h, j, l, k, m;
    e = e || 20;
    g = g || 20;
    d = cC(d);
    clearInterval(tG[a][5]);
    f = d[0];
    h = d[1];
    j = d[2];
    c = cC(c);
    tG[a][1] = c[0];
    tG[a][2] = c[1];
    tG[a][3] = c[2];
    l = Math.round(Math.abs(tG[a][1] - f) / e);
    k = Math.round(Math.abs(tG[a][2] - h) / e);
    m = Math.round(Math.abs(tG[a][3] - j) / e);
    if (l == 0) l = 1;
    if (k == 0) k = 1;
    if (m == 0) m = 1;
    tG[a][4] = 1;
    tG[a][5] = setInterval(function () {
        aC(a, b, e, f, h, j, l, k, m, g)
    }, g)
}

function aC(a, b, c, d, e, g, f, h, j, l) {
    if (tG[a][4] <= c) {
        c = tG[a][1];
        l = tG[a][2];
        var k = tG[a][3];
        if (c >= d) c -= f;
        else c = parseInt(c) + parseInt(f);
        if (l >= e) l -= h;
        else l = parseInt(l) + parseInt(h);
        if (k >= g) k -= j;
        else k = parseInt(k) + parseInt(j);
        d = "rgb(" + c + "," + l + "," + k + ")";
        if (b == "background") tG[a][0].style.backgroundColor = d;
        else if (b == "border") tG[a][0].style.borderColor = d;
        else if (b == "border-top") tG[a][0].style.borderTopColor = d;
        else if (b == "border-right") tG[a][0].style.borderRightColor = d;
        else if (b == "border-bottom") tG[a][0].style.borderBottomColor = d;
        else if (b == "border-left") tG[a][0].style.borderLeftColor = d;
        else tG[a][0].style.color = d;
        tG[a][1] = c;
        tG[a][2] = l;
        tG[a][3] = k;
        tG[a][4] = ++tG[a][4]
    } else {
        clearInterval(tG[a][5]);
        d = "rgb(" + d + "," + e + "," + g + ")";
        if (b == "background") tG[a][0].style.backgroundColor = d;
        else if (b == "border") tG[a][0].style.borderColor = d;
        else if (b == "border-top") tG[a][0].style.borderTopColor = d;
        else if (b == "border-right") tG[a][0].style.borderRightColor = d;
        else if (b == "border-bottom") tG[a][0].style.borderBottomColor = d;
        else if (b == "border-left") tG[a][0].style.borderLeftColor = d;
        else tG[a][0].style.color = d
    }
}

function cC(a) {
    return a = [parseInt(a.substring(0, 2), 16), parseInt(a.substring(2, 4), 16), parseInt(a.substring(4, 6), 16)]
}
var tG = [],
    oldCaller = null;

function sS(a, b, c) {
    if (oldCaller != null) {
        oldCaller[0].style.color = "";
        oldCaller[1].style.display = "none";
        c = oldCaller[0].getElementsByTagName("span");
        c[1].style.backgroundColor = "";
        c[1].style.border = "";
        c[1].style.borderBottom = "";
        c[2].style.borderRight = "";
        if (oldCaller[0] == b || b == null) {
            oldCaller = null;
            return true
        }
    }
    var d = b.onclick;
    b.onclick = new Function("return false");
    b.style.color = "#f2980e";
    oldCaller = [b, a];
    c = b.getElementsByTagName("span");
    c[1].style.backgroundColor = "#f2980e";
    c[1].style.border = "1px solid #f9cf8e";
    c[1].style.borderBottom = "0px solid #fff";
    c[2].style.borderRight = "1px solid #f2980e";
    c = a.getElementsByTagName("div");
    if (tG.length > 0) for (var e = 0; e < tG.length; ++e) clearInterval(tG[e][5]);
    tG = [
        [c[0]],
        [c[0]],
        [c[1]],
        [c[1]],
        [c[1]],
        [c[1]],
        [c[1]]
    ];
    c[0].style.borderTopColor = "rgb(255,255,255)";
    c[0].style.borderRightColor = "rgb(255,255,255)";
    c[1].style.borderTopColor = "rgb(255,255,255)";
    c[1].style.borderRightColor = "rgb(255,255,255)";
    c[1].style.borderBottomColor = "rgb(255,255,255)";
    c[1].style.borderLeftColor = "rgb(255,255,255)";
    c[1].style.backgroundColor = "rgb(255,255,255)";
    a.style.display = "block";
    cF(0, "border-top", "ffffff", "f2980e", 5, 5);
    setTimeout(function () {
        cF(1, "border-right", "ffffff", "f2980e", 5, 5)
    }, 100);
    setTimeout(function () {
        cF(2, "border-top", "ffffff", "ab9a80", 5, 5)
    }, 200);
    setTimeout(function () {
        cF(3, "border-left", "ffffff", "ab9a80", 5, 5)
    }, 250);
    setTimeout(function () {
        cF(4, "border-right", "ffffff", "ab9a80", 5, 5)
    }, 250);
    setTimeout(function () {
        cF(5, "border-bottom", "ffffff", "ab9a80", 5, 5)
    }, 300);
    setTimeout(function () {
        cF(6, "background", "ffffff", "f2980e", 15, 20)
    }, 400);
    setTimeout(function () {
        b.onclick = d
    }, 500);
    if (a.id == "subs3") try {
        $('userInp').select();
    } catch (x) {}
    return true
}

function hS() {
    oldCaller && sS(oldCaller[1], oldCaller[0], true)
}

function cP() {
    /*var a = window.location.hash;
    if (Number(a.length) >= 1) a.substring(1) != window.curPage && gP(a.substring(1), false);
    else if (window.curPage != undefined) {
        a = window.location.href.match(/.com\/([^#.]+)/);
        if (a != null && a[1] != window.curPage) gP(a[1], false);
        else a == null && window.curPage != "home" && gP("home", false)
    }*/
    getSize();
    if ($("main")) $("main").style.minHeight = (window.wSize.height-8) + "px";
}

function sL() {
    /*for (var a = document.getElementsByTagName("a"), b = 0; b < a.length; ++b) if (a[b].href.indexOf("://") != -1 && a[b].href.indexOf("kassoon.com") == -1 && a[b].onclick == null) {
        a[b].onclick = new Function("return ! oNW(this);");
        a[b].innerHTML += "&uarr;"
    } else if (a[b].href.match(/.[a-zA-Z0-9]{3}$/) && (a[b].className.toUpperCase().indexOf("NOJAX") != -1 || a[b].href.indexOf("/site/download/") != -1)) a[b].onclick = new Function("tP(this.href)");
    else if (a[b].onclick == null && a[b].className.toUpperCase().indexOf("NOJAX") == -1) a[b].onclick = new Function("return ! gP(this,true)")*/
}
var MouseDown=false;
document.onmousedown=function() {MouseDown=true;}
document.onmouseup=function() {MouseDown=false;}
window.onload = function () {
    if (window.location.href.indexOf("kassoon.com") == -1) window.location = "http://kassoon.com";
    setInterval(function () {
        cP()
    }, 500);
    if ($("loginDiv")) {
		var z0 = $("loginDiv").innerHTML.toLowerCase();
	    if (z0.indexOf("logged in") != -1) {
	    	var z1 = String(z0).indexOf(" in as ") + 7;
	        var z2 = String(z0).indexOf(". <input");
	        acct = (String(z0).substring(z1, z2));
	    }
	}

    if (!(document.all ? true : false)) document.captureEvents(Event.MOUSEMOVE);
    document.onmousemove = gMC;
    getSize();
    if ($("main")) $("main").style.minHeight = (window.wSize.height-8) + "px";
    document.onkeyup = dBtn;
    //window.setTimeout(function(){aG("/site/apps/periodic.php");}, 110000);
    confetList = [];
    window.onscroll = oSc;
    oSc();
};

function oSc() {
    var fl = document.getElementsByClassName("fixedFloat");
    for (var i = 0; i < fl.length; ++i) {
        fl[i].style.position = "";
        var rec = fl[i].getBoundingClientRect().top;
        var pos = XY(fl[i]);
        if (rec < 0) {
            fl[i].style.position = "fixed";
        }
    }
}

function getSize() {
  var wwidth = 0, wheight = 0;
  if( typeof( window.innerWidth ) == 'number' ) {
    wwidth = window.innerWidth;
    wheight = window.innerHeight;
  } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
    wwidth = document.documentElement.clientWidth;
    wheight = document.documentElement.clientHeight;
  } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
    wwidth = document.body.clientWidth;
    wheight = document.body.clientHeight;
  }
  window.wSize = {width:wwidth, height:wheight};
}

function oNR(a, b) {
    $(b).innerHTML = a;
    sL();
    twit = $("footContent").innerHTML
}
var mX = 0,
    mY = 0;

function gMC(e) {
    if (document.all ? true : false) {
        mX = event.clientX + document.body.scrollLeft;
        mY = event.clientY + document.body.scrollTop;
    } else {
        mX = e.pageX;
        mY = e.pageY;
    }
    if (mX < 0) mX = 0;
    if (mY < 0) mY = 0;
    return true;
}
function XY(o) {
    var z=o, x=0,y=0, c;
    while(z && !isNaN(z.offsetLeft) && !isNaN(z.offsetTop)) {
        c = isNaN(window.globalStorage)?0:window.getComputedStyle(z,null);
        x += z.offsetLeft-z.scrollLeft+(c?parseInt(c.getPropertyValue('border-left-width'),10):0);
        y += z.offsetTop-z.scrollTop+(c?parseInt(c.getPropertyValue('border-top-width'),10):0);
        z = z.offsetParent;
    }
    return {x:o.X=x,y:o.Y=y};
}

function cW(a) {
    $("calcSub").disabled = "disabled";
    var b = a.elements.item(0).value,
        c = a.elements.item(1).value,
        d = a.elements.item(2).checked ? a.elements.item(2).value : a.elements.item(3).value,
        e = a.elements.item(4).checked ? a.elements.item(4).value : a.elements.item(5).value,
        g = a.elements.item(6).checked,
        f = a.elements.item(9).value,
        h = a.elements.item(7).value;
    a = a.elements.item(8).checked;
    b = "frames=false&partySize=" + b + "&partyLevel=" + c + "&calcType=" + d + "&resultType=" + e + "&effective=" + g + "&cumulative=" + a + "&startAt=" + f + "&effectiveVal=" + h;
    return aP("/site/apps/wealth-calc.php", b, oW, false)
}

function oW(a, b) {
    $("calcSub").disabled = "";
    $("calcResult").innerHTML = a
}

function tW(a) {
    var b = $("wealthCalc");
    if (a == 1) {
        b.rows[0].cells[0].style.visibility = "hidden";
        b.rows[2].style.visibility = "hidden";
        b.rows[3].cells[1].style.visibility = "hidden"
    } else {
        b.rows[0].cells[0].style.visibility = "visible";
        b.rows[2].style.visibility = "visible";
        b.rows[3].cells[1].style.visibility = "visible"
    }
}
indexLevel = 101;

function BW() {
    if (window.innerWidth) return window.innerWidth;
    else if (document.body.clientWidth) return document.body.clientWidth;
    return 0
}

function BH() {
    if (self.innerHeight) return self.innerHeight;
    else if (document.documentElement && document.documentElement.clientHeight) return document.documentElement.clientHeight;
    else if (document.body) return document.body.clientHeight;
    return 0
}

function VT() {
    return document.documentElement && document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body ? document.body.scrollTop : 0
}

function gC(a) {
    var b = curtop = 0,
        c = a;
    if (c.offsetParent) {
        b = c.offsetLeft;
        for (curtop = c.offsetTop; c = c.offsetParent;) {
            b += c.offsetLeft;
            curtop += c.offsetTop
        }
    }
    curtop -= 23;
    b -= 3;
    return {
        left: b,
        top: curtop,
        width: a.width,
        height: a.height
    }
}

function fI(a, b) {
    a.style.opacity = 0;
    b = new Fx.Styles(a, {
        duration: b
    });
    b.start({
        opacity: [0, 1]
    });
    a.style.visible = "visible";
    return b
}

function pI(a, b) {
    var c = new Image;
    c.onload = function () {
        b(c)
    };
    c.src = a;
    return c
}

function pS(a) {
    a.onload = null;
    a.src = ""
}

function CI(a) {
    var b = {
        handle: a,
        onStart: function () {
            a.parentNode.style.zIndex = ++indexLevel
        }.bind(this),
        onComplete: function () {
            if (a.parentNode.style.left.replace("px", "") < 0) a.parentNode.style.left = "0px";
            if (a.parentNode.style.top.replace("px", "") < 0) a.parentNode.style.top = "0px"
        }.bind(this)
    };
    a.style.cursor = "move";
    a.parentNode.makeDraggable(b)
}
function togDisp(div)
{
	if (div.style.display=="none")
		div.style.display="block";
	else
		div.style.display="none";
}
function dragElement(elmnt)
{
	var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
	if (document.getElementById(elmnt.id + "header")) {
		// if present, the header is where you move the DIV from:
		document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
	} else {
		// otherwise, move the DIV from anywhere inside the DIV:
		elmnt.onmousedown = dragMouseDown;
	}

	function dragMouseDown(e)
	{
		e = e || window.event;
		e.preventDefault();
		// get the mouse cursor position at startup:
		pos3 = e.clientX;
		pos4 = e.clientY;
		document.onmouseup = closeDragElement;
		// call a function whenever the cursor moves:
		document.onmousemove = elementDrag;
	}

	function elementDrag(e)
	{
		e = e || window.event;
		e.preventDefault();
		// calculate the new cursor position:
		pos1 = pos3 - e.clientX;
		pos2 = pos4 - e.clientY;
		pos3 = e.clientX;
		pos4 = e.clientY;
		// set the element's new position:
		elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
		elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
	}

	function closeDragElement()
	{
		// stop moving when mouse button is released:
		document.onmouseup = null;
		document.onmousemove = null;
	}
}
function mC(a, b) {
    a.zoom && a.removeChild(a.zoom);
    var c = a.getElementsByTagName("div");
    a.removeChild(c[0]);
    a.style.border = "";
    a.style.padding = "3px";
    b.onclick = null;
    c = new Fx.Styles(a, {
        duration: 500,
        onComplete: function () {
            document.body.removeChild(a)
        }
    });
    var d = new Fx.Styles(b, {
        duration: 500,
        onComplete: function () {
            a.ele.onclick = function () {
                BI(a.sr, a.ele, a.ful)
            }
        }
    }),
        e = gC(a.ele);
    d.start({
        width: [b.style.width.replace("px", ""), e.width],
        height: [b.style.height.replace("px", ""), e.height]
    });
    c.start({
        top: [a.style.top.replace("px", ""), e.top],
        left: [a.style.left.replace("px", ""), e.left]
    })
}

function BI(a, b, c) {
    b.onclick = null;
    var d = gC(b),
        e = document.createElement("div"),
        g = document.createElement("img");
    e.className = "container";
    var f = document.createElement("div");
    f.className = "dragger";
    f.innerHTML = "&nbsp";
    e.appendChild(f);
    var h = document.createElement("div");
    h.className = "close";
    h.innerHTML = "x";
    f.appendChild(h);
    f.style.visibility = "hidden";
    e.appendChild(g);
    var j = gC(b.parentNode);
    e.style.position = "absolute";
    e.style.top = d.top + "px";
    e.style.left = d.left + "px";
    g.style.width = d.width + "px";
    g.style.height = d.height + "px";
    g.className = "zoomloading";
    e.style.zIndex = ++indexLevel;
    e.style.cursor = "wait";
    g.onclick = null;
    e.ele = b;
    e.sr = a;
    e.ful = c;

    function l(o) {
        g.src = o.src;
        document.body.appendChild(e)
    }
    var k = pI("/site/images/invisible.gif", l);

    function m(o) {
        g.src = o.src;
        pS(k);
        e.style.top = d.top + "px";
        e.style.left = d.left + "px";
        document.body.appendChild(e);
        var n = 500,
            t = 1;
        e.style.cursor = "pointer";
        g.style.visible = "visible";
        t = BW();
        var s = BH(),
            r = Math.min(o.width, 600),
            u = r * o.height / o.width;
        o = VT() + Math.max((s - u) / 2, 10);
        s = t / 2 - r / 2;
        var q = null;
        if (c) {
            q = document.createElement("a");
            e.zoom = q
        }

        function v() {
            mC(e, g)
        }
        s = new Fx.Styles(e, {
            duration: n,
            onComplete: function () {
                if (q) {
                    q.target = "_blank";
                    q.href = c;
                    q.className = "zoombutton";
                    q.style.position = "absolute";
                    q.style.top = u - 20 + "px";
                    q.style.left = r - 40 + "px";
                    q.style.zIndex = "999";
                    q.style.visibility = "hidden";
                    e.appendChild(q);
                    fI(q, 400)
                }
                f.style.width = r + "px";
                e.style.width = r + "px";
                fI(f, 400);
                e.style.padding = "0";
                e.style.border = "1px solid #ab9a80";
                CI(f)
            }
        });
        n = new Fx.Styles(g, {
            duration: n,
            onComplete: function () {
                g.onclick = v;
                h.onclick = v;
                b.onclick = v
            }
        });
        n.start({
            width: [d.width, r],
            height: [d.height, u]
        });
        s.start({
            top: [d.top, o],
            left: [d.left, t / 2 - r / 2]
        })
    }
    pI(a, m)
}
var MooTools = {
    version: "1.11"
};

function $defined(a) {
    return a != undefined
}

function $type(a) {
    if (!$defined(a)) return false;
    if (a.htmlElement) return "element";
    var b = typeof a;
    if (b == "object" && a.nodeName) switch (a.nodeType) {
    case 1:
        return "element";
    case 3:
        return /\S/.test(a.nodeValue) ? "textnode" : "whitespace"
    }
    if (b == "object" || b == "function") {
        switch (a.constructor) {
        case Array:
            return "array";
        case RegExp:
            return "regexp";
        case Class:
            return "class"
        }
        if (typeof a.length == "number") {
            if (a.item) return "collection";
            if (a.callee) return "arguments"
        }
    }
    return b
}

function $merge() {
    for (var a = {}, b = 0; b < arguments.length; b++) for (var c in arguments[b]) {
        var d = arguments[b][c],
            e = a[c];
        a[c] = e && $type(d) == "object" && $type(e) == "object" ? $merge(e, d) : d
    }
    return a
}

function $extend() {
    var a = arguments;
    a[1] || (a = [this, a[0]]);
    for (var b in a[1]) a[0][b] = a[1][b];
    return a[0]
}

function $native() {
    for (var a = 0, b = arguments.length; a < b; a++) arguments[a].extend = function (c) {
        for (var d in c) {
            this.prototype[d] || (this.prototype[d] = c[d]);
            this[d] || (this[d] = $native.generic(d))
        }
    }
}
$native.generic = function (a) {
    return function (b) {
        return this.prototype[a].apply(b, Array.prototype.slice.call(arguments, 1))
    }
};
$native(Function, Array, String, Number);

function $chk(a) {
    return !!(a || a === 0)
}

function $pick(a, b) {
    return $defined(a) ? a : b
}

function $random(a, b) {
    return Math.floor(Math.random() * (b - a + 1) + a)
}

function $time() {
    return (new Date).getTime()
}

function $clear(a) {
    clearTimeout(a);
    clearInterval(a);
    return null
}

function Abstract(a) {
    a = a || {};
    a.extend = $extend;
    return a
}
var Window = new Abstract(window),
    Document = new Abstract(document);
document.head = document.getElementsByTagName("head")[0];
window.xpath = !! document.evaluate;
if (window.ActiveXObject) window.ie = window[window.XMLHttpRequest ? "ie7" : "ie6"] = true;
else if (document.childNodes && !document.all && !navigator.taintEnabled) window.webkit = window[window.xpath ? "webkit420" : "webkit419"] = true;
else if (document.getBoxObjectFor != null) window.gecko = true;
window.khtml = window.webkit;
Object.extend = $extend;
if (typeof HTMLElement == "undefined") {
    var HTMLElement = function () {};
    window.webkit && document.createElement("iframe");
    HTMLElement.prototype = window.webkit ? window["[[DOMElement.prototype]]"] : {}
}
HTMLElement.prototype.htmlElement = function () {};
if (window.ie6) try {
    document.execCommand("BackgroundImageCache", false, true)
} catch (e$$3) {}

function Class(a) {
    function b() {
        return arguments[0] !== null && this.initialize && $type(this.initialize) == "function" ? this.initialize.apply(this, arguments) : this
    }
    $extend(b, this);
    b.prototype = a;
    b.constructor = Class;
    return b
}
Class.empty = function () {};
Class.prototype = {
    extend: function (a) {
        var b = new this(null);
        for (var c in a) {
            var d = b[c];
            b[c] = Class.Merge(d, a[c])
        }
        return new Class(b)
    },
    implement: function () {
        for (var a = 0, b = arguments.length; a < b; a++) $extend(this.prototype, arguments[a])
    }
};
Class.Merge = function (a, b) {
    if (a && a != b) {
        var c = $type(b);
        if (c != $type(a)) return b;
        switch (c) {
        case "function":
            c = function () {
                this.parent = arguments.callee.parent;
                return b.apply(this, arguments)
            };
            c.parent = a;
            return c;
        case "object":
            return $merge(a, b)
        }
    }
    return b
};
var Chain = new Class({
    chain: function (a) {
        this.chains = this.chains || [];
        this.chains.push(a);
        return this
    },
    callChain: function () {
        this.chains && this.chains.length && this.chains.shift().delay(10, this)
    },
    clearChain: function () {
        this.chains = []
    }
}),
    Events = new Class({
        addEvent: function (a, b) {
            if (b != Class.empty) {
                this.$events = this.$events || {};
                this.$events[a] = this.$events[a] || [];
                this.$events[a].include(b)
            }
            return this
        },
        fireEvent: function (a, b, c) {
            this.$events && this.$events[a] && this.$events[a].each(function (d) {
                d.create({
                    bind: this,
                    delay: c,
                    arguments: b
                })()
            }, this);
            return this
        },
        removeEvent: function (a, b) {
            this.$events && this.$events[a] && this.$events[a].remove(b);
            return this
        }
    }),
    Options = new Class({
        setOptions: function () {
            this.options = $merge.apply(null, [this.options].extend(arguments));
            if (this.addEvent) for (var a in this.options) $type(this.options[a] == "function") && /^on[A-Z]/.test(a) && this.addEvent(a, this.options[a]);
            return this
        }
    });
Array.extend({
    forEach: function (a, b) {
        for (var c = 0, d = this.length; c < d; c++) a.call(b, this[c], c, this)
    },
    filter: function (a, b) {
        for (var c = [], d = 0, e = this.length; d < e; d++) a.call(b, this[d], d, this) && c.push(this[d]);
        return c
    },
    map: function (a, b) {
        for (var c = [], d = 0, e = this.length; d < e; d++) c[d] = a.call(b, this[d], d, this);
        return c
    },
    every: function (a, b) {
        for (var c = 0, d = this.length; c < d; c++) if (!a.call(b, this[c], c, this)) return false;
        return true
    },
    some: function (a, b) {
        for (var c = 0, d = this.length; c < d; c++) if (a.call(b, this[c], c, this)) return true;
        return false
    },
    indexOf: function (a, b) {
        var c = this.length;
        for (b = b < 0 ? Math.max(0, c + b) : b || 0; b < c; b++) if (this[b] === a) return b;
        return -1
    },
    copy: function (a, b) {
        a = a || 0;
        if (a < 0) a = this.length + a;
        b = b || this.length - a;
        for (var c = [], d = 0; d < b; d++) c[d] = this[a++];
        return c
    },
    remove: function (a) {
        for (var b = 0, c = this.length; b < c;) if (this[b] === a) {
            this.splice(b, 1);
            c--
        } else b++;
        return this
    },
    contains: function (a, b) {
        return this.indexOf(a, b) != -1
    },
    associate: function (a) {
        for (var b = {}, c = Math.min(this.length, a.length), d = 0; d < c; d++) b[a[d]] = this[d];
        return b
    },
    extend: function (a) {
        for (var b = 0, c = a.length; b < c; b++) this.push(a[b]);
        return this
    },
    merge: function (a) {
        for (var b = 0, c = a.length; b < c; b++) this.include(a[b]);
        return this
    },
    include: function (a) {
        this.contains(a) || this.push(a);
        return this
    },
    getRandom: function () {
        return this[$random(0, this.length - 1)] || null
    },
    getLast: function () {
        return this[this.length - 1] || null
    }
});
Array.prototype.each = Array.prototype.forEach;
Array.each = Array.forEach;

function $A(a) {
    return Array.copy(a)
}

function $each(a, b, c) {
    if (a && typeof a.length == "number" && $type(a) != "object") Array.forEach(a, b, c);
    else for (var d in a) b.call(c || a, a[d], d)
}
Array.prototype.test = Array.prototype.contains;
String.extend({
    test: function (a, b) {
        return ($type(a) == "string" ? new RegExp(a, b) : a).test(this)
    },
    toInt: function () {
        return parseInt(this, 10)
    },
    toFloat: function () {
        return parseFloat(this)
    },
    camelCase: function () {
        return this.replace(/-\D/g, function (a) {
            return a.charAt(1).toUpperCase()
        })
    },
    hyphenate: function () {
        return this.replace(/\w[A-Z]/g, function (a) {
            return a.charAt(0) + "-" + a.charAt(1).toLowerCase()
        })
    },
    capitalize: function () {
        return this.replace(/\b[a-z]/g, function (a) {
            return a.toUpperCase()
        })
    },
    trim: function () {
        return this.replace(/^\s+|\s+$/g, "")
    },
    clean: function () {
        return this.replace(/\s{2,}/g, " ").trim()
    },
    rgbToHex: function (a) {
        var b = this.match(/\d{1,3}/g);
        return b ? b.rgbToHex(a) : false
    },
    hexToRgb: function (a) {
        var b = this.match(/^#?(\w{1,2})(\w{1,2})(\w{1,2})$/);
        return b ? b.slice(1).hexToRgb(a) : false
    },
    contains: function (a, b) {
        return b ? (b + this + b).indexOf(b + a + b) > -1 : this.indexOf(a) > -1
    },
    escapeRegExp: function () {
        return this.replace(/([.*+?^${}()|[\]\/\\])/g, "\\$1")
    }
});
Array.extend({
    rgbToHex: function (a) {
        if (this.length < 3) return false;
        if (this.length == 4 && this[3] == 0 && !a) return "transparent";
        for (var b = [], c = 0; c < 3; c++) {
            var d = (this[c] - 0).toString(16);
            b.push(d.length == 1 ? "0" + d : d)
        }
        return a ? b : "#" + b.join("")
    },
    hexToRgb: function (a) {
        if (this.length != 3) return false;
        for (var b = [], c = 0; c < 3; c++) b.push(parseInt(this[c].length == 1 ? this[c] + this[c] : this[c], 16));
        return a ? b : "rgb(" + b.join(",") + ")"
    }
});
Function.extend({
    create: function (a) {
        var b = this;
        a = $merge({
            bind: b,
            event: false,
            arguments: null,
            delay: false,
            periodical: false,
            attempt: false
        }, a);
        if ($chk(a.arguments) && $type(a.arguments) != "array") a.arguments = [a.arguments];
        return function (c) {
            var d;
            if (a.event) {
                c = c || window.event;
                d = [a.event === true ? c : new a.event(c)];
                a.arguments && d.extend(a.arguments)
            } else d = a.arguments || arguments;

            function e() {
                return b.apply($pick(a.bind, b), d)
            }
            if (a.delay) return setTimeout(e, a.delay);
            if (a.periodical) return setInterval(e, a.periodical);
            if (a.attempt) try {
                return e()
            } catch (g) {
                return false
            }
            return e()
        }
    },
    pass: function (a, b) {
        return this.create({
            arguments: a,
            bind: b
        })
    },
    attempt: function (a, b) {
        return this.create({
            arguments: a,
            bind: b,
            attempt: true
        })()
    },
    bind: function (a, b) {
        return this.create({
            bind: a,
            arguments: b
        })
    },
    bindAsEventListener: function (a, b) {
        return this.create({
            bind: a,
            event: true,
            arguments: b
        })
    },
    delay: function (a, b, c) {
        return this.create({
            delay: a,
            bind: b,
            arguments: c
        })()
    },
    periodical: function (a, b, c) {
        return this.create({
            periodical: a,
            bind: b,
            arguments: c
        })()
    }
});
Number.extend({
    toInt: function () {
        return parseInt(this)
    },
    toFloat: function () {
        return parseFloat(this)
    },
    limit: function (a, b) {
        return Math.min(b, Math.max(a, this))
    },
    round: function (a) {
        a = Math.pow(10, a || 0);
        return Math.round(this * a) / a
    },
    times: function (a) {
        for (var b = 0; b < this; b++) a(b)
    }
});
var Element = new Class({
    initialize: function (a, b) {
        if ($type(a) == "string") {
            if (window.ie && b && (b.name || b.type)) {
                var c = b.name ? ' name="' + b.name + '"' : "",
                    d = b.type ? ' type="' + b.type + '"' : "";
                delete b.name;
                delete b.type;
                a = "<" + a + c + d + ">"
            }
            a = document.createElement(a)
        }
        a = $(a);
        return !b || !a ? a : a.set(b)
    }
}),
    Elements = new Class({
        initialize: function (a) {
            return a ? $extend(a, this) : this
        }
    });
Elements.extend = function (a) {
    for (var b in a) {
        this.prototype[b] = a[b];
        this[b] = $native.generic(b)
    }
};

function $(a) {
    if (!a) return null;
    if (a.htmlElement) return Garbage.collect(a);
    if ([window, document].contains(a)) return a;
    var b = $type(a);
    if (b == "string") b = (a = document.getElementById(a)) ? "element" : false;
    if (b != "element") return null;
    if (a.htmlElement) return Garbage.collect(a);
    if (["object", "embed"].contains(a.tagName.toLowerCase())) return a;
    $extend(a, Element.prototype);
    a.htmlElement = function () {};
    return Garbage.collect(a)
}
document.getElementsBySelector = document.getElementsByTagName;

function $$() {
    for (var a = [], b = 0, c = arguments.length; b < c; b++) {
        var d = arguments[b];
        switch ($type(d)) {
        case "element":
            a.push(d);
        case "boolean":
            break;
        case false:
            break;
        case "string":
            d = document.getElementsBySelector(d, true);
        default:
            a.extend(d)
        }
    }
    return $$.unique(a)
}
$$.unique = function (a) {
    for (var b = [], c = 0, d = a.length; c < d; c++) if (!a[c].$included) {
        var e = $(a[c]);
        if (e && !e.$included) {
            e.$included = true;
            b.push(e)
        }
    }
    a = 0;
    for (c = b.length; a < c; a++) b[a].$included = null;
    return new Elements(b)
};
Elements.Multi = function (a) {
    return function () {
        for (var b = arguments, c = [], d = true, e = 0, g = this.length, f; e < g; e++) {
            f = this[e][a].apply(this[e], b);
            if ($type(f) != "element") d = false;
            c.push(f)
        }
        return d ? $$.unique(c) : c
    }
};
Element.extend = function (a) {
    for (var b in a) {
        HTMLElement.prototype[b] = a[b];
        Element.prototype[b] = a[b];
        Element[b] = $native.generic(b);
        var c = Array.prototype[b] ? b + "Elements" : b;
        Elements.prototype[c] = Elements.Multi(b)
    }
};
Element.extend({
    set: function (a) {
        for (var b in a) {
            var c = a[b];
            switch (b) {
            case "styles":
                this.setStyles(c);
                break;
            case "events":
                this.addEvents && this.addEvents(c);
                break;
            case "properties":
                this.setProperties(c);
                break;
            default:
                this.setProperty(b, c)
            }
        }
        return this
    },
    inject: function (a, b) {
        a = $(a);
        switch (b) {
        case "before":
            a.parentNode.insertBefore(this, a);
            break;
        case "after":
            (b = a.getNext()) ? a.parentNode.insertBefore(this, b) : a.parentNode.appendChild(this);
            break;
        case "top":
            if (b = a.firstChild) {
                a.insertBefore(this, b);
                break
            }
        default:
            a.appendChild(this)
        }
        return this
    },
    injectBefore: function (a) {
        return this.inject(a, "before")
    },
    injectAfter: function (a) {
        return this.inject(a, "after")
    },
    injectInside: function (a) {
        return this.inject(a, "bottom")
    },
    injectTop: function (a) {
        return this.inject(a, "top")
    },
    adopt: function () {
        var a = [];
        $each(arguments, function (b) {
            a = a.concat(b)
        });
        $$(a).inject(this);
        return this
    },
    remove: function () {
        return this.parentNode.removeChild(this)
    },
    clone: function (a) {
        a = $(this.cloneNode(a !== false));
        if (!a.$events) return a;
        a.$events = {};
        for (var b in this.$events) a.$events[b] = {
            keys: $A(this.$events[b].keys),
            values: $A(this.$events[b].values)
        };
        return a.removeEvents()
    },
    replaceWith: function (a) {
        a = $(a);
        this.parentNode.replaceChild(a, this);
        return a
    },
    appendText: function (a) {
        this.appendChild(document.createTextNode(a));
        return this
    },
    hasClass: function (a) {
        return this.className.contains(a, " ")
    },
    addClass: function (a) {
        if (!this.hasClass(a)) this.className = (this.className + " " + a).clean();
        return this
    },
    removeClass: function (a) {
        this.className = this.className.replace(new RegExp("(^|\\s)" + a + "(?:\\s|$)"), "$1").clean();
        return this
    },
    toggleClass: function (a) {
        return this.hasClass(a) ? this.removeClass(a) : this.addClass(a)
    },
    setStyle: function (a, b) {
        switch (a) {
        case "opacity":
            return this.setOpacity(parseFloat(b));
        case "float":
            a = window.ie ? "styleFloat" : "cssFloat"
        }
        a = a.camelCase();
        switch ($type(b)) {
        case "number":
            ["zIndex", "zoom"].contains(a) || (b += "px");
            break;
        case "array":
            b = "rgb(" + b.join(",") + ")"
        }
        this.style[a] = b;
        return this
    },
    setStyles: function (a) {
        switch ($type(a)) {
        case "object":
            Element.setMany(this, "setStyle", a);
            break;
        case "string":
            this.style.cssText = a
        }
        return this
    },
    setOpacity: function (a) {
        if (a == 0) {
            if (this.style.visibility != "hidden") this.style.visibility = "hidden"
        } else if (this.style.visibility != "visible") this.style.visibility = "visible";
        if (!this.currentStyle || !this.currentStyle.hasLayout) this.style.zoom = 1;
        if (window.ie) this.style.filter = a == 1 ? "" : "alpha(opacity=" + a * 100 + ")";
        this.style.opacity = this.$tmp.opacity = a;
        return this
    },
    getStyle: function (a) {
        a = a.camelCase();
        var b = this.style[a];
        if (!$chk(b)) {
            if (a == "opacity") return this.$tmp.opacity;
            b = [];
            for (var c in Element.Styles) if (a == c) {
                Element.Styles[c].each(function (d) {
                    d = this.getStyle(d);
                    b.push(parseInt(d) ? d : "0px")
                }, this);
                if (a == "border") return (c = b.every(function (d) {
                    return d == b[0]
                })) ? b[0] : false;
                return b.join(" ")
            }
            if (a.contains("border")) if (Element.Styles.border.contains(a)) return ["Width", "Style", "Color"].map(function (d) {
                return this.getStyle(a + d)
            }, this).join(" ");
            else if (Element.borderShort.contains(a)) return ["Top", "Right", "Bottom", "Left"].map(function (d) {
                return this.getStyle("border" + d + a.replace("border", ""))
            }, this).join(" ");
            if (document.defaultView) b = document.defaultView.getComputedStyle(this, null).getPropertyValue(a.hyphenate());
            else if (this.currentStyle) b = this.currentStyle[a]
        }
        if (window.ie) b = Element.fixStyle(a, b, this);
        if (b && a.test(/color/i) && b.contains("rgb")) return b.split("rgb").splice(1, 4).map(function (d) {
            return d.rgbToHex()
        }).join(" ");
        return b
    },
    getStyles: function () {
        return Element.getMany(this, "getStyle", arguments)
    },
    walk: function (a, b) {
        a += "Sibling";
        for (b = b ? this[b] : this[a]; b && $type(b) != "element";) b = b[a];
        return $(b)
    },
    getPrevious: function () {
        return this.walk("previous")
    },
    getNext: function () {
        return this.walk("next")
    },
    getFirst: function () {
        return this.walk("next", "firstChild")
    },
    getLast: function () {
        return this.walk("previous", "lastChild")
    },
    getParent: function () {
        return $(this.parentNode)
    },
    getChildren: function () {
        return $$(this.childNodes)
    },
    hasChild: function (a) {
        return !!$A(this.getElementsByTagName("*")).contains(a)
    },
    getProperty: function (a) {
        var b = Element.Properties[a];
        if (b) return this[b];
        b = Element.PropertiesIFlag[a] || 0;
        if (!window.ie || b) return this.getAttribute(a, b);
        return (a = this.attributes[a]) ? a.nodeValue : null
    },
    removeProperty: function (a) {
        var b = Element.Properties[a];
        if (b) this[b] = "";
        else this.removeAttribute(a);
        return this
    },
    getProperties: function () {
        return Element.getMany(this, "getProperty", arguments)
    },
    setProperty: function (a, b) {
        var c = Element.Properties[a];
        if (c) this[c] = b;
        else this.setAttribute(a, b);
        return this
    },
    setProperties: function (a) {
        return Element.setMany(this, "setProperty", a)
    },
    setHTML: function () {
        this.innerHTML = $A(arguments).join("");
        return this
    },
    setText: function (a) {
        var b = this.getTag();
        if (["style", "script"].contains(b)) if (window.ie) {
            if (b == "style") this.styleSheet.cssText = a;
            else b == "script" && this.setProperty("text", a);
            return this
        } else {
            this.removeChild(this.firstChild);
            return this.appendText(a)
        }
        this[$defined(this.innerText) ? "innerText" : "textContent"] = a;
        return this
    },
    getText: function () {
        var a = this.getTag();
        if (["style", "script"].contains(a)) if (window.ie) if (a == "style") return this.styleSheet.cssText;
        else {
            if (a == "script") return this.getProperty("text")
        } else return this.innerHTML;
        return $pick(this.innerText, this.textContent)
    },
    getTag: function () {
        return this.tagName.toLowerCase()
    },
    empty: function () {
        Garbage.trash(this.getElementsByTagName("*"));
        return this.setHTML("")
    }
});
Element.fixStyle = function (a, b, c) {
    if ($chk(parseInt(b))) return b;
    if (["height", "width"].contains(a)) {
        b = a == "width" ? ["left", "right"] : ["top", "bottom"];
        var d = 0;
        b.each(function (e) {
            d += c.getStyle("border-" + e + "-width").toInt() + c.getStyle("padding-" + e).toInt()
        });
        return c["offset" + a.capitalize()] - d + "px"
    } else if (a.test(/border(.+)Width|margin|padding/)) return "0px";
    return b
};
Element.Styles = {
    border: [],
    padding: [],
    margin: []
};
["Top", "Right", "Bottom", "Left"].each(function (a) {
    for (var b in Element.Styles) Element.Styles[b].push(b + a)
});
Element.borderShort = ["borderWidth", "borderStyle", "borderColor"];
Element.getMany = function (a, b, c) {
    var d = {};
    $each(c, function (e) {
        d[e] = a[b](e)
    });
    return d
};
Element.setMany = function (a, b, c) {
    for (var d in c) a[b](d, c[d]);
    return a
};
Element.Properties = new Abstract({
    "class": "className",
    "for": "htmlFor",
    colspan: "colSpan",
    rowspan: "rowSpan",
    accesskey: "accessKey",
    tabindex: "tabIndex",
    maxlength: "maxLength",
    readonly: "readOnly",
    frameborder: "frameBorder",
    value: "value",
    disabled: "disabled",
    checked: "checked",
    multiple: "multiple",
    selected: "selected"
});
Element.PropertiesIFlag = {
    href: 2,
    src: 2
};
Element.Methods = {
    Listeners: {
        addListener: function (a, b) {
            this.addEventListener ? this.addEventListener(a, b, false) : this.attachEvent("on" + a, b);
            return this
        },
        removeListener: function (a, b) {
            this.removeEventListener ? this.removeEventListener(a, b, false) : this.detachEvent("on" + a, b);
            return this
        }
    }
};
window.extend(Element.Methods.Listeners);
document.extend(Element.Methods.Listeners);
Element.extend(Element.Methods.Listeners);
var Garbage = {
    elements: [],
    collect: function (a) {
        if (!a.$tmp) {
            Garbage.elements.push(a);
            a.$tmp = {
                opacity: 1
            }
        }
        return a
    },
    trash: function (a) {
        for (var b = 0, c = a.length, d; b < c; b++) if ((d = a[b]) && d.$tmp) {
            d.$events && d.fireEvent("trash").removeEvents();
            for (var e in d.$tmp) d.$tmp[e] = null;
            for (var g in Element.prototype) d[g] = null;
            Garbage.elements[Garbage.elements.indexOf(d)] = null;
            d.htmlElement = d.$tmp = d = null
        }
        Garbage.elements.remove(null)
    },
    empty: function () {
        Garbage.collect(window);
        Garbage.collect(document);
        Garbage.trash(Garbage.elements)
    }
};
window.addListener("beforeunload", function () {
    window.addListener("unload", Garbage.empty);
    window.ie && window.addListener("unload", CollectGarbage)
});
var Event = new Class({
    initialize: function (a) {
        if (a && a.$extended) return a;
        this.$extended = true;
        this.event = a = a || window.event;
        this.type = a.type;
        this.target = a.target || a.srcElement;
        if (this.target.nodeType == 3) this.target = this.target.parentNode;
        this.shift = a.shiftKey;
        this.control = a.ctrlKey;
        this.alt = a.altKey;
        this.meta = a.metaKey;
        if (["DOMMouseScroll", "mousewheel"].contains(this.type)) this.wheel = a.wheelDelta ? a.wheelDelta / 120 : -(a.detail || 0) / 3;
        else if (this.type.contains("key")) {
            this.code = a.which || a.keyCode;
            for (var b in Event.keys) if (Event.keys[b] == this.code) {
                this.key = b;
                break
            }
            if (this.type == "keydown") {
                a = this.code - 111;
                if (a > 0 && a < 13) this.key = "f" + a
            }
            this.key = this.key || String.fromCharCode(this.code).toLowerCase()
        } else if (this.type.test(/(click|mouse|menu)/)) {
            this.page = {
                x: a.pageX || a.clientX + document.documentElement.scrollLeft,
                y: a.pageY || a.clientY + document.documentElement.scrollTop
            };
            this.client = {
                x: a.pageX ? a.pageX - window.pageXOffset : a.clientX,
                y: a.pageY ? a.pageY - window.pageYOffset : a.clientY
            };
            this.rightClick = a.which == 3 || a.button == 2;
            switch (this.type) {
            case "mouseover":
                this.relatedTarget = a.relatedTarget || a.fromElement;
                break;
            case "mouseout":
                this.relatedTarget = a.relatedTarget || a.toElement
            }
            this.fixRelatedTarget()
        }
        return this
    },
    stop: function () {
        return this.stopPropagation().preventDefault()
    },
    stopPropagation: function () {
        if (this.event.stopPropagation) this.event.stopPropagation();
        else this.event.cancelBubble = true;
        return this
    },
    preventDefault: function () {
        if (this.event.preventDefault) this.event.preventDefault();
        else this.event.returnValue = false;
        return this
    }
});
Event.fix = {
    relatedTarget: function () {
        if (this.relatedTarget && this.relatedTarget.nodeType == 3) this.relatedTarget = this.relatedTarget.parentNode
    },
    relatedTargetGecko: function () {
        try {
            Event.fix.relatedTarget.call(this)
        } catch (a) {
            this.relatedTarget = this.target
        }
    }
};
Event.prototype.fixRelatedTarget = window.gecko ? Event.fix.relatedTargetGecko : Event.fix.relatedTarget;
Event.keys = new Abstract({
    enter: 13,
    up: 38,
    down: 40,
    left: 37,
    right: 39,
    esc: 27,
    space: 32,
    backspace: 8,
    tab: 9,
    "delete": 46
});
Element.Methods.Events = {
    addEvent: function (a, b) {
        this.$events = this.$events || {};
        this.$events[a] = this.$events[a] || {
            keys: [],
            values: []
        };
        if (this.$events[a].keys.contains(b)) return this;
        this.$events[a].keys.push(b);
        var c = a,
            d = Element.Events[a];
        if (d) {
            d.add && d.add.call(this, b);
            if (d.map) b = d.map;
            if (d.type) c = d.type
        }
        this.addEventListener || (b = b.create({
            bind: this,
            event: true
        }));
        this.$events[a].values.push(b);
        return Element.NativeEvents.contains(c) ? this.addListener(c, b) : this
    },
    removeEvent: function (a, b) {
        if (!this.$events || !this.$events[a]) return this;
        var c = this.$events[a].keys.indexOf(b);
        if (c == -1) return this;
        var d = this.$events[a].keys.splice(c, 1)[0];
        c = this.$events[a].values.splice(c, 1)[0];
        if (d = Element.Events[a]) {
            d.remove && d.remove.call(this, b);
            if (d.type) a = d.type
        }
        return Element.NativeEvents.contains(a) ? this.removeListener(a, c) : this
    },
    addEvents: function (a) {
        return Element.setMany(this, "addEvent", a)
    },
    removeEvents: function (a) {
        if (!this.$events) return this;
        if (a) {
            if (this.$events[a]) {
                this.$events[a].keys.each(function (c) {
                    this.removeEvent(a, c)
                }, this);
                this.$events[a] = null
            }
        } else {
            for (var b in this.$events) this.removeEvents(b);
            this.$events = null
        }
        return this
    },
    fireEvent: function (a, b, c) {
        this.$events && this.$events[a] && this.$events[a].keys.each(function (d) {
            d.create({
                bind: this,
                delay: c,
                arguments: b
            })()
        }, this);
        return this
    },
    cloneEvents: function (a, b) {
        if (!a.$events) return this;
        if (b) a.$events[b] && a.$events[b].keys.each(function (d) {
            this.addEvent(b, d)
        }, this);
        else for (var c in a.$events) this.cloneEvents(a, c);
        return this
    }
};
window.extend(Element.Methods.Events);
document.extend(Element.Methods.Events);
Element.extend(Element.Methods.Events);
Element.Events = new Abstract({
    mouseenter: {
        type: "mouseover",
        map: function (a) {
            a = new Event(a);
            a.relatedTarget != this && !this.hasChild(a.relatedTarget) && this.fireEvent("mouseenter", a)
        }
    },
    mouseleave: {
        type: "mouseout",
        map: function (a) {
            a = new Event(a);
            a.relatedTarget != this && !this.hasChild(a.relatedTarget) && this.fireEvent("mouseleave", a)
        }
    },
    mousewheel: {
        type: window.gecko ? "DOMMouseScroll" : "mousewheel"
    }
});
Element.NativeEvents = ["click", "dblclick", "mouseup", "mousedown", "mousewheel", "DOMMouseScroll", "mouseover", "mouseout", "mousemove", "keydown", "keypress", "keyup", "load", "unload", "beforeunload", "resize", "move", "focus", "blur", "change", "submit", "reset", "select", "error", "abort", "contextmenu", "scroll"];
Function.extend({
    bindWithEvent: function (a, b) {
        return this.create({
            bind: a,
            arguments: b,
            event: Event
        })
    }
});
var Fx = {};
Fx.Base = new Class({
    options: {
        onStart: Class.empty,
        onComplete: Class.empty,
        onCancel: Class.empty,
        transition: function (a) {
            return -(Math.cos(Math.PI * a) - 1) / 2
        },
        duration: 500,
        unit: "px",
        wait: true,
        fps: 50
    },
    initialize: function (a) {
        this.element = this.element || null;
        this.setOptions(a);
        this.options.initialize && this.options.initialize.call(this)
    },
    step: function () {
        var a = $time();
        if (a < this.time + this.options.duration) {
            this.delta = this.options.transition((a - this.time) / this.options.duration);
            this.setNow();
            this.increase()
        } else {
            this.stop(true);
            this.set(this.to);
            this.fireEvent("onComplete", this.element, 10);
            this.callChain()
        }
    },
    set: function (a) {
        this.now = a;
        this.increase();
        return this
    },
    setNow: function () {
        this.now = this.compute(this.from, this.to)
    },
    compute: function (a, b) {
        return (b - a) * this.delta + a
    },
    start: function (a, b) {
        if (this.options.wait) {
            if (this.timer) return this
        } else this.stop();
        this.from = a;
        this.to = b;
        this.change = this.to - this.from;
        this.time = $time();
        this.timer = this.step.periodical(Math.round(1000 / this.options.fps), this);
        this.fireEvent("onStart", this.element);
        return this
    },
    stop: function (a) {
        if (!this.timer) return this;
        this.timer = $clear(this.timer);
        a || this.fireEvent("onCancel", this.element);
        return this
    },
    custom: function (a, b) {
        return this.start(a, b)
    },
    clearTimer: function (a) {
        return this.stop(a)
    }
});
Fx.Base.implement(new Chain, new Events, new Options);
Fx.CSS = {
    select: function (a, b) {
        if (a.test(/color/i)) return this.Color;
        a = $type(b);
        if (a == "array" || a == "string" && b.contains(" ")) return this.Multi;
        return this.Single
    },
    parse: function (a, b, c) {
        c.push || (c = [c]);
        var d = c[0];
        c = c[1];
        if (!$chk(c)) {
            c = d;
            d = a.getStyle(b)
        }
        a = this.select(b, c);
        return {
            from: a.parse(d),
            to: a.parse(c),
            css: a
        }
    }
};
Fx.CSS.Single = {
    parse: function (a) {
        return parseFloat(a)
    },
    getNow: function (a, b, c) {
        return c.compute(a, b)
    },
    getValue: function (a, b, c) {
        if (b == "px" && c != "opacity") a = Math.round(a);
        return a + b
    }
};
Fx.CSS.Multi = {
    parse: function (a) {
        return a.push ? a : a.split(" ").map(function (b) {
            return parseFloat(b)
        })
    },
    getNow: function (a, b, c) {
        for (var d = [], e = 0; e < a.length; e++) d[e] = c.compute(a[e], b[e]);
        return d
    },
    getValue: function (a, b, c) {
        if (b == "px" && c != "opacity") a = a.map(Math.round);
        return a.join(b + " ") + b
    }
};
Fx.CSS.Color = {
    parse: function (a) {
        return a.push ? a : a.hexToRgb(true)
    },
    getNow: function (a, b, c) {
        for (var d = [], e = 0; e < a.length; e++) d[e] = Math.round(c.compute(a[e], b[e]));
        return d
    },
    getValue: function (a) {
        return "rgb(" + a.join(",") + ")"
    }
};
Fx.Styles = Fx.Base.extend({
    initialize: function (a, b) {
        this.element = $(a);
        this.parent(b)
    },
    setNow: function () {
        for (var a in this.from) this.now[a] = this.css[a].getNow(this.from[a], this.to[a], this)
    },
    set: function (a) {
        var b = {};
        this.css = {};
        for (var c in a) {
            this.css[c] = Fx.CSS.select(c, a[c]);
            b[c] = this.css[c].parse(a[c])
        }
        return this.parent(b)
    },
    start: function (a) {
        if (this.timer && this.options.wait) return this;
        this.now = {};
        this.css = {};
        var b = {},
            c = {};
        for (var d in a) {
            var e = Fx.CSS.parse(this.element, d, a[d]);
            b[d] = e.from;
            c[d] = e.to;
            this.css[d] = e.css
        }
        return this.parent(b, c)
    },
    increase: function () {
        for (var a in this.now) this.element.setStyle(a, this.css[a].getValue(this.now[a], this.options.unit, a))
    }
});
Element.extend({
    effects: function (a) {
        return new Fx.Styles(this, a)
    }
});
var Drag = {};
Drag.Base = new Class({
    options: {
        handle: false,
        unit: "px",
        onStart: Class.empty,
        onBeforeStart: Class.empty,
        onComplete: Class.empty,
        onSnap: Class.empty,
        onDrag: Class.empty,
        limit: false,
        modifiers: {
            x: "left",
            y: "top"
        },
        grid: false,
        snap: 6
    },
    initialize: function (a, b) {
        this.setOptions(b);
        this.element = $(a);
        this.handle = $(this.options.handle) || this.element;
        this.mouse = {
            now: {},
            pos: {}
        };
        this.value = {
            start: {},
            now: {}
        };
        this.bound = {
            start: this.start.bindWithEvent(this),
            check: this.check.bindWithEvent(this),
            drag: this.drag.bindWithEvent(this),
            stop: this.stop.bind(this)
        };
        this.attach();
        this.options.initialize && this.options.initialize.call(this)
    },
    attach: function () {
        this.handle.addEvent("mousedown", this.bound.start);
        return this
    },
    detach: function () {
        this.handle.removeEvent("mousedown", this.bound.start);
        return this
    },
    start: function (a) {
        this.fireEvent("onBeforeStart", this.element);
        this.mouse.start = a.page;
        var b = this.options.limit;
        this.limit = {
            x: [],
            y: []
        };
        for (var c in this.options.modifiers) if (this.options.modifiers[c]) {
            this.value.now[c] = this.element.getStyle(this.options.modifiers[c]).toInt();
            this.mouse.pos[c] = a.page[c] - this.value.now[c];
            if (b && b[c]) for (var d = 0; d < 2; d++) if ($chk(b[c][d])) this.limit[c][d] = $type(b[c][d]) == "function" ? b[c][d]() : b[c][d]
        }
        if ($type(this.options.grid) == "number") this.options.grid = {
            x: this.options.grid,
            y: this.options.grid
        };
        document.addListener("mousemove", this.bound.check);
        document.addListener("mouseup", this.bound.stop);
        this.fireEvent("onStart", this.element);
        a.stop()
    },
    check: function (a) {
        var b = Math.round(Math.sqrt(Math.pow(a.page.x - this.mouse.start.x, 2) + Math.pow(a.page.y - this.mouse.start.y, 2)));
        if (b > this.options.snap) {
            document.removeListener("mousemove", this.bound.check);
            document.addListener("mousemove", this.bound.drag);
            this.drag(a);
            this.fireEvent("onSnap", this.element)
        }
        a.stop()
    },
    drag: function (a) {
        this.out = false;
        this.mouse.now = a.page;
        for (var b in this.options.modifiers) if (this.options.modifiers[b]) {
            this.value.now[b] = this.mouse.now[b] - this.mouse.pos[b];
            if (this.limit[b]) if ($chk(this.limit[b][1]) && this.value.now[b] > this.limit[b][1]) {
                this.value.now[b] = this.limit[b][1];
                this.out = true
            } else if ($chk(this.limit[b][0]) && this.value.now[b] < this.limit[b][0]) {
                this.value.now[b] = this.limit[b][0];
                this.out = true
            }
            if (this.options.grid[b]) this.value.now[b] -= this.value.now[b] % this.options.grid[b];
            this.element.setStyle(this.options.modifiers[b], this.value.now[b] + this.options.unit)
        }
        this.fireEvent("onDrag", this.element);
        a.stop()
    },
    stop: function () {
        document.removeListener("mousemove", this.bound.check);
        document.removeListener("mousemove", this.bound.drag);
        document.removeListener("mouseup", this.bound.stop);
        this.fireEvent("onComplete", this.element)
    }
});
Drag.Base.implement(new Events, new Options);
Element.extend({
    makeResizable: function (a) {
        return new Drag.Base(this, $merge({
            modifiers: {
                x: "width",
                y: "height"
            }
        }, a))
    }
});
Drag.Move = Drag.Base.extend({
    options: {
        droppables: [],
        container: false,
        overflown: []
    },
    initialize: function (a, b) {
        this.setOptions(b);
        this.element = $(a);
        this.droppables = $$(this.options.droppables);
        this.container = $(this.options.container);
        this.position = {
            element: this.element.getStyle("position"),
            container: false
        };
        if (this.container) this.position.container = this.container.getStyle("position");
        if (!["relative", "absolute", "fixed"].contains(this.position.element)) this.position.element = "absolute";
        a = this.element.getStyle("top").toInt();
        b = this.element.getStyle("left").toInt();
        if (this.position.element == "absolute" && !["relative", "absolute", "fixed"].contains(this.position.container)) {
            a = $chk(a) ? a : this.element.getTop(this.options.overflown);
            b = $chk(b) ? b : this.element.getLeft(this.options.overflown)
        } else {
            a = $chk(a) ? a : 0;
            b = $chk(b) ? b : 0
        }
        this.element.setStyles({
            top: a,
            left: b,
            position: this.position.element
        });
        this.parent(this.element)
    },
    start: function (a) {
        this.overed = null;
        if (this.container) {
            var b = this.container.getCoordinates(),
                c = this.element.getCoordinates();
            this.options.limit = this.position.element == "absolute" && !["relative", "absolute", "fixed"].contains(this.position.container) ? {
                x: [b.left, b.right - c.width],
                y: [b.top, b.bottom - c.height]
            } : {
                y: [0, b.height - c.height],
                x: [0, b.width - c.width]
            }
        }
        this.parent(a)
    },
    drag: function (a) {
        this.parent(a);
        a = this.out ? false : this.droppables.filter(this.checkAgainst, this).getLast();
        if (this.overed != a) {
            this.overed && this.overed.fireEvent("leave", [this.element, this]);
            this.overed = a ? a.fireEvent("over", [this.element, this]) : null
        }
        return this
    },
    checkAgainst: function (a) {
        a = a.getCoordinates(this.options.overflown);
        var b = this.mouse.now;
        return b.x > a.left && b.x < a.right && b.y < a.bottom && b.y > a.top
    },
    stop: function () {
        this.overed && !this.out ? this.overed.fireEvent("drop", [this.element, this]) : this.element.fireEvent("emptydrop", this);
        this.parent();
        return this
    }
});
Element.extend({
    makeDraggable: function (a) {
        return new Drag.Move(this, a)
    }
});

function json_encode(a) {
    var b, c = this.window.JSON;
    try {
        if (typeof c === "object" && typeof c.stringify === "function") {
            b = c.stringify(a);
            if (b === undefined) throw new SyntaxError("json_encode");
            return b
        }
        a = a;
        var d = function (f) {
            var h = /[\\\"\u0000-\u001f\u007f-\u009f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
                j = {
                    "\u0008": "\\b",
                    "\t": "\\t",
                    "\n": "\\n",
                    "\u000c": "\\f",
                    "\r": "\\r",
                    '"': '\\"',
                    "\\": "\\\\"
                };
            h.lastIndex = 0;
            return h.test(f) ? '"' + f.replace(h, function (l) {
                var k = j[l];
                return typeof k === "string" ? k : "\\u" + ("0000" + l.charCodeAt(0).toString(16)).slice(-4)
            }) + '"' : '"' + f + '"'
        },
            e = function (f, h) {
                var j = "",
                    l = "    ",
                    k = 0,
                    m = k = "";
                m = 0;
                var o = j,
                    n = [];
                if ((h = h[f]) && typeof h === "object" && typeof h.toJSON === "function") h = h.toJSON(f);
                switch (typeof h) {
                case "string":
                    return d(h);
                case "number":
                    return isFinite(h) ? String(h) : "null";
                case "boolean":
                case "null":
                    return String(h);
                case "object":
                    if (!h) return "null";
                    if (this.PHPJS_Resource && h instanceof this.PHPJS_Resource || window.PHPJS_Resource && h instanceof
                    window.PHPJS_Resource) throw new SyntaxError("json_encode");
                    j += l;
                    n = [];
                    if (Object.prototype.toString.apply(h) === "[object Array]") {
                        m = h.length;
                        for (k = 0; k < m; k += 1) n[k] = e(k, h) || "null";
                        m = n.length === 0 ? "[]" : j ? "[\n" + j + n.join(",\n" + j) + "\n" + o + "]" : "[" + n.join(",") + "]";
                        j = o;
                        return m
                    }
                    for (k in h) if (Object.hasOwnProperty.call(h, k)) if (m = e(k, h)) n.push(d(k) + (j ? ": " : ":") + m);
                    m = n.length === 0 ? "{}" : j ? "{\n" + j + n.join(",\n" + j) + "\n" + o + "}" : "{" + n.join(",") + "}";
                    j = o;
                    return m;
                case "undefined":
                case "function":
                default:
                    throw new SyntaxError("json_encode");
                }
            };
        return e("", {
            "": a
        })
    } catch (g) {
        if (!(g instanceof SyntaxError)) throw new Error("Unexpected error type in json_encode()");
        this.php_js = this.php_js || {};
        this.php_js.last_error_json = 4;
        return null
    }
}

function json_decode(a) {
    var b = this.window.JSON;
    if (typeof b === "object" && typeof b.parse === "function") try {
        return b.parse(a)
    } catch (c) {
        if (!(c instanceof SyntaxError)) throw new Error("Unexpected error type in json_decode()");
        this.php_js = this.php_js || {};
        this.php_js.last_error_json = 4;
        return null
    }
    b = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
    a = a;
    b.lastIndex = 0;
    if (b.test(a)) a = a.replace(b, function (d) {
        return "\\u" + ("0000" + d.charCodeAt(0).toString(16)).slice(-4)
    });
    if (/^[\],:{}\s]*$/.test(a.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) return a = eval("(" + a + ")");
    this.php_js = this.php_js || {};
    this.php_js.last_error_json = 4;
    return null
}
var xpRewards = new Array(4);
xpRewards[0] = new Array(0, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 700, 800, 1000, 1200, 1400, 1600, 2000, 2400, 2800, 3200, 4150, 5100, 6050, 7000, 9000, 11000, 13000, 15000, 19000, 23000, 27000, 31000, 39000, 47000, 55000, 63000, 79000, 95000, 111000);
xpRewards[1] = new Array(0, 25, 31, 38, 44, 50, 63, 75, 88, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 700, 800, 1038, 1275, 1513, 1750, 2250, 2750, 3250, 3750, 4750, 5750, 6750, 7750, 9750, 11750, 13750, 15750, 19750, 23750, 27750);
xpRewards[2] = new Array(0, 200, 250, 300, 350, 400, 500, 600, 700, 800, 1000, 1200, 1400, 1600, 2000, 2400, 2800, 3200, 4000, 4800, 5600, 6400, 8300, 10200, 12100, 14000, 18000, 22000, 26000, 30000, 38000, 46000, 54000, 62000, 78000, 94000, 110000, 126000, 158000, 190000, 222000);
xpRewards[3] = new Array(0, 500, 625, 750, 875, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 10000, 12000, 14000, 16000, 20750, 25500, 30250, 35000, 45000, 55000, 65000, 75000, 95000, 115000, 135000, 155000, 195000, 235000, 275000, 315000, 395000, 375000, 555000);
var curEnemies = {};
curEnemies.XP = 0;
var doSo = false;

function eAM() {
    if (!doSo) {
        doSo = true;
        tP("encUse");
    }
    var a = $("monsterLevel").value,
        b = $("monsterType"),
        c = b.value,
        d = $("encounterTable"),
        e, g, f = "0";
    if ($("monID")) f = $("monID").value;
    if (f == "id0") f = "0";
    try {
        $("mon" + a + "-" + c + "-" + f).value = Number(curEnemies[f][a][c][0]) + 1;
        curEnemies[f][a][c][0] = Number(curEnemies[f][a][c][0]) + 1
    } catch (h) {
        e = d.rows.length;
        if (curEnemies[f] == undefined) curEnemies[f] = {};
        if (curEnemies[f][a] == undefined) curEnemies[f][a] = {};
        if (curEnemies[f][a][c] == undefined) curEnemies[f][a][c] = [];
        curEnemies[f][a][c][0] = 1;
        curEnemies[f][a][c][1] = $("monName").value;
        g = d.insertRow(e);
        if (e % 2 == 1) d.rows[e].className = "light";
        g.insertCell(0).innerHTML = "[<a href='javascript:;' onclick='return ! eRM(" + a + ", " + c + ', this.parentNode.parentNode, "' + f + "\")'>x</a>] <input id='mon" + a + "-" + c + "-" + f + "' onkeyup='eRA(this, event)' onblur='eUM(" + a + ", " + c + ', "' + f + "\")' style='width:15px;' maxlength='2' type='text' value='1'/>";
        g.insertCell(1).innerHTML = a;
        g.insertCell(2).innerHTML = b.options[b.selectedIndex].innerHTML;
        g.insertCell(3).innerHTML = xpRewards[c][a];
        if (f != "0") {
            b = $("comURL").value + "monster.aspx?id=" + f.replace("id", "");
            g.insertCell(4).innerHTML = '<a onclick="return ! oCW(this,' + f.replace("id", "") + ');" href="' + b + '">' + $("monName").value + '</a>'
        } else g.insertCell(4).innerHTML = '';
    }
    curEnemies.XP += xpRewards[c][a];
    eCD();
    return true
}

function eRM(a, b, c, d) {
    var e = curEnemies[d][a][b][0],
        g = Number(c.cells[3].innerHTML);
    curEnemies.XP -= e * g;
    c.parentNode.removeChild(c);
    curEnemies[d][a][b] = null;
    eCD()
}

function eUM(a, b, c) {
    var d = curEnemies[c][a][b][0] * xpRewards[b][a],
        e = $("mon" + a + "-" + b + "-" + c);
    curEnemies[c][a][b][0] = e.value;
    a = curEnemies[c][a][b][0] * xpRewards[b][a];
    curEnemies.XP -= d - a;
    eCD()
}

function eCB() {
    var a = Number($("partySize").value),
        b = Number($("partyLevel").value);
    $("xpBudget").innerHTML = a * xpRewards[0][b];
    a = $("monsterLevel");
    for (var c = 0; c < a.length; ++c) a.options[c].style.color = Number(a.options[c].value) + 3 < b ? "#0F0" : Number(a.options[c].value) - 3 > b ? "#F00" : "#000";
    eCD()
}

function eCD() {
    var a = Number($("partySize").value),
        b = Number($("partyLevel").value),
        c, d, e;
    $("xpVal").innerHTML = curEnemies.XP;
    for (c = 0; c < xpRewards[0].length; ++c) if (xpRewards[0][c] * a >= Number($("xpVal").innerHTML)) break;
    c = (b - c) * -1;
    var g = " (lvl" + (c > -1 ? "+" : "") + c + ")";
    c = b - 4 < 1 ? a * xpRewards[0][b] - 300 : a * xpRewards[0][b - 4];
    d = b - 1 < 1 ? a * xpRewards[0][b] - 150 : a * xpRewards[0][b - 1];
    e = b + 1 > 40 ? a * 111000 + 222000 : a * xpRewards[0][b + 1];
    a = b + 4 > 40 ? a * 111000 + 333000 : a * xpRewards[0][b + 4];
    b = Number($("xpVal").innerHTML);
    var f = $("curDifficulty");
    if (b > a) f.innerHTML = "Extreme" + g;
    else if (b > e) f.innerHTML = "Hard" + g;
    else if (b < c) f.innerHTML = "Trivial" + g;
    else if (b < d) f.innerHTML = "Easy" + g;
    else if (b > d && b < e) f.innerHTML = "Normal" + g
}

function doEnNaE() {
    var table = $("encounterTable");
    var a;
    for (i = 1; i < table.rows.length; ++i) {
        table.rows[i].cells[4].saveHTML = table.rows[i].cells[4].innerHTML;
        try {
            a = table.rows[i].cells[4].getElementsByTagName("a")[0].innerHTML;
        } catch (e) {
            a = table.rows[i].cells[4].innerHTML;
        }
        table.rows[i].cells[4].innerHTML = '<input type="text" value="' + a + '"/>';
    }
    var names = $("editNames");
    names.innerHTML = "s";
    names.onclick = function () {
        doEnNaS()
    };
}

function doEnNaS() {
    var table = $("encounterTable");
    var reg = /mon(\d+)-(\d+)-(id\d+)/i;
    var ar, anchor;
    for (i = 1; i < table.rows.length; ++i) {
        ar = reg.exec(table.rows[i].cells[0].getElementsByTagName("input")[0].id);
        if (ar)
        	curEnemies[ar[3]][ar[1]][ar[2]][1] = table.rows[i].cells[4].getElementsByTagName("input")[0].value;
        table.rows[i].cells[4].innerHTML = table.rows[i].cells[4].saveHTML;
        try {
            anchor = table.rows[i].cells[4].getElementsByTagName("a")[0];
            anchor.innerHTML = curEnemies[ar[3]][ar[1]][ar[2]][1];
        } catch (e) {
            if (ar) table.rows[i].cells[4].innerHTML = curEnemies[ar[3]][ar[1]][ar[2]][1];
        }
    }
    var names = $("editNames");
    names.innerHTML = "e";
    names.onclick = function () {
        doEnNaE()
    };
}

function doEnTo() {
    var table = $("encounterTable");
    var newTable = document.createElement("table");
    newTable.className = "border";
    for (i = 1; i < table.rows.length; ++i) {
        var newRow = newTable.insertRow(newTable.rows.length);
        if (newTable.rows.length % 2 == 0) newRow.className = "light";
        newRow.insertCell(0).innerHTML = table.rows[i].cells[4].innerHTML;
    }
    newTable.style.padding = "4px";
    newTable.style.margin = "0 auto";
    var div = document.createElement("div");
    div.innerHTML = '<strong><a href="/dnd/encounter-builder/' + $("encID").value + '/' + encodeURI($("encName").value) + '/">' + $("encName").value + '</a></strong>';
    div.appendChild(newTable);
    var index = 0;
    var targ = $("footContent");
    if (targ.array) index = targ.array.length;
    div.innerHTML += '[ <a href="javascript:;" onclick="sHW(null,event);doToRe(' + index + ')">Remove from Toolbar</a> ]';
    div.style.textAlign = "center";
    div.onover = String($("encNotes").value.replace(/\n/g, "<br/>") + '');
    if (!div.onover) div.onover = null;
    div.onmouseover = function (event) {
        sHW(this.onover, event)
    };
    div.onmouseout = function (event) {
        sHW(null, event)
    };
    doToAd(div);
    sL();
}

function doToAd(element) {
    var targ = $("footContent");
    if (!targ.array) {
        targ.twitter = targ.innerHTML;
        targ.array = [];
    }
    var x = targ.array.length;
    targ.array[x] = element;
    targ.innerHTML = "";
    for (var i = 0; i < targ.array.length; ++i) {
        if (!targ.array[i]) continue;
        targ.appendChild(targ.array[i]);
        targ.appendChild(document.createElement("br"));
        sL();
    }
}

function doToRe(index) {
    var targ = $("footContent");
    delete targ.array[index];
    targ.innerHTML = "";
    for (var i = 0; i < targ.array.length; ++i) {
        if (!targ.array[i]) continue;
        targ.appendChild(targ.array[i]);
        targ.appendChild(document.createElement("br"));
        sL();
    }
    if (!targ.innerHTML) {
        delete targ.array;
        targ.innerHTML = targ.twitter;
        return;
    }
}

function RA(a) {
    return a.match(/\d+/g) ? a.match(/\d+/g) : ""
}

function eRA(a, b) {
    a.value = RA(a.value);
    if (b.keyCode == 13) a.blur();
}

function RD(a, b) {
    if (!doSo) {
        doSo = true;
        tP("dieUse");
    }
    try {
        $('expBtn').innerHTML = 'Expand';
    } catch (x) {}
    var c = $("sendgroup");
    if (c != null && c.checked) {
        var z = $("dicetxt"),
            y = $("dicetarget");
        $("rollbtn").disabled = "disabled";
        aPS("/dnd/dice-roller/" + z.className + "/", "frames=false&brief=1&sendgroup=on&dicetxt=" + z.value.replace(/\+/g, "@@") + "&dicetarget=" + y.options[y.selectedIndex].value + "&dicedesc=" + escape($("dicedesc").value), cbDice, "diceresult", false);
        return true;
    }
    try {
        var d = $(a).value.split(";");
        for (var ii = 0; ii < d.length; ++ii) {
	        c = d[ii];
	        for (var e = /([0-9]+)?d([0-9]+)r?([0-9]+)?/, g, f = null, h = null, j = /r([0-9]+)/; g = e.exec(d[ii]);) {
	            j = 0;
	            if (g[1] == undefined) g[1] = 1;
	            for (i = 0; i < g[1]; ++i) {
	                var l = Math.ceil(Math.random() * g[2]);
	                if (g[3] && g[3] < g[2]) for (; l <= g[3];) l = Math.ceil(Math.random() * g[2]);
	                j += l
	            }
	            d[ii] = d[ii].replace(e, j);
	            c = j == g[1] * g[2] ? c.replace(e, "<span style='color:#0F0'>" + j + "</span>") : j == g[1] ? c.replace(e, "<span style='color:#F00'>" + j + "</span>") : c.replace(e, j);
	            if (f == null || j < f) f = j;
	            if (h == null || j > h) h = j
	        }
	        if (f != null) d[ii] = d[ii].replace(/low([a-z]+)?/gi, f);
	        if (h != null) d[ii] = d[ii].replace(/high([a-z]+)?/gi, h);
	        $(b).innerHTML += c + " = <span style='font-weight:bold;'>" + eval(d[ii]) + "</span><br/>";
	        $(a).style.color = "#000"
		}
    } catch (k) {
        $(a).style.color = "#F00"
    }
    return true
}

function cbDice(txt, variable) {
    $(variable).innerHTML = txt;
    $("rollbtn").disabled = "";
    $("bbcode").value = txt.replace(/(.+\<\/div\>)/, "").replace(/\<[^\>]+\>/g, "").replace(/^[a-zA-Z0-9]+: /, "").replace(/ \= ([\d]+)/, " = [url=http://kassoon.com/dnd/dice-roller/" + $("bbcode").className + "/]$1[/url]");
}

function doFoSu(form, button, variable, track) {
    if (!form.method) form = $(form);
    if (!button.value) button = $(button);
    button.disabled = "disabled";
    var inputList = form.getElementsByTagName("input");
    var postdata = "";
    for (var i = 0; i < inputList.length; ++i) {
        if (inputList[i].type == "submit") continue;
        postdata += "&" + inputList[i].name + "=" + inputList[i].value;
    }
    postdata += "&" + button.name + "=" + button.value + "&frames=false";
    var curPage = (window.curPage) ? window.curPage : window.location.toString().replace(/http:\/\/(www\.)?kassoon\.com/g, "");
    curPage = (form.action ? form.action : curPage);
    window.oldLink = curPage;
    return aPS(curPage, postdata, doFoRe, variable, track);
}

function doFoRe(txt, variable) {
    if (variable) {} else oL(txt, variable);
}

function CD(a) {
    $(a).innerHTML = ""
}

function DW() {
    return window.open("/dnd/dice-mini/", "dicewindow", "width=200,height=150,scrollbars=yes")
}
var twit = "";

function AT(a) {
    var b = $("footContent").innerHTML = a.innerHTML;
    a.innerHTML = "";
    if (a.id == "dice") {
        $("tooltog").innerHTML = "Remove from Toolbar";
        $("tooltog").onclick = function () {
            return !RT($("dice"))
        };
        $("dicetxt").id = "dicetxt_tool";
        $("diceresult").id = "diceresult_tool";
        $("rollbtn").onclick = function () {
            return !RD("dicetxt_tool", "diceresult_tool")
        };
        $("cleardie").onclick = function () {
            CD("diceresult_tool")
        }
    }
    a.innerHTML = b
}

function RT(a) {
    $("footContent").innerHTML = twit
}

function eCS() {
    for (var a = Number($("partyLevel").value), b = "<option value='1'>1</option>", c = 2; c < a; ++c) b += "<option value='" + c + "'>" + c + "</option>";
    $("startAt").innerHTML = b
}

function sPD() {
    try {
        $("updated").innerHTML = "Article Updated " + $("dt_updated").innerHTML;
        $("crumbs").innerHTML = '<a href="/">home</a> > ' + $("dt_crumbs").innerHTML;
        document.title = $("dt_title").innerHTML.replace("&amp;","&") + "Kassoon.com";
        var a = $("data");
        a.parentNode.removeChild(a);
    } catch (a) {}
}

function gMP(a) {
    a = a || window.event;
    var b = a.pageX ? a.pageX : a.clientX + (document.documentElement.scrollLeft || document.body.scrollLeft) - document.documentElement.clientLeft;
    a = a.pageY ? a.pageY : a.clientY + (document.documentElement.scrollTop || document.body.scrollTop) - document.documentElement.clientTop;
    return new Array(b, a)
}
var startX = 0;

function rsD(a) {
    startX = mX;
    document.onmouseup = function (b) {
        rsU(1, b)
    };
    document.onmousemove = function (b) {
        gMC(b)
        rsU(0, b)
    };
    return true
}

function rsU(a, b) {
    var c = mX - startX;
    if (a == 1) {
        document.onmouseup = null;
        document.onmousemove = gMC;
    } else startX = mX;
}

function mRS() {
    var a = document.createElement("div");
    a.id = "resize";
    a.onmousedown = function (b) {
        return !rsD(b)
    };
    try {
        $("content").appendChild(a);
    } catch (e) { }
}

function doEncTab(a, b, c, d) {
    if ($(d + "-tab")) return true;
    var div = document.createElement("div");
    div.innerHTML = "[ <a href='javascript:;'>Add</a> ] [ <a href='javascript:;' onclick='this.parentNode.parentNode.removeChild(this.parentNode);return false;'>Go away</a> ]";
    div.getElementsByTagName("a")[0].onclick = function() {
    	return !aCM(a, b, c, d);
    };
    div.className = "enctab";
    div.id = d + "-tab";
    $(d + "-frame").appendChild(div);
    return true;
}

function aCM(a, b, c, d) {
    $("monsterLevel").value = a;
    $("monsterType").selectedIndex = b;
    $("monName").value = c;
    $("monID").value = "id" + d;
    eAM();
    $("monName").value = "0";
    $("monID").value = "0";
    return true
}
function moTi(d) {
    console.log(d.title);
    let a = $("mobInfPan");
    if (a == null) {

    }

    window.addEventListener('touchend',clMoTi,false);
    window.addEventListener('touchcancel',clMoTi,false);
}
function clMoTi() {
    let d = $("mobInfPan");
    if (d != null) d.parentNode.removeChild(d);
    window.removeEventListener('touchend',clMoTi);
    window.removeEventListener('touchcancel',clMoTi);
}
function monRoll(desc, dice, e, typ=0)
{
  try {
    if ($("inpNoDesc").checked) {
      desc = "";
      localStorage.setItem('inpNoDesc', 1);
    } else {
      localStorage.setItem('inpNoDesc', 0);
    }
  } catch (e) { }
	dice = dice.trim();
	dice = dice.split(' ').join('');
  if (typ == 1) {
      let direg = /([0-9 ]+)d([0-9 ]+)([\+\-0-9\/\*]+)?/gi;
      let diarr = dice.match(direg);
      if (diarr == null) diarr = [1];
    if (shiftDown) dice = dice.replace(direg, (parseInt(diarr[0])*2)+"d$2$3");
      else if (ctrlDown) dice = dice.replace(direg, "($1d$2$3)/2");
  } else {
      if (shiftDown) dice = dice.replace("d20", "d20+d20-low");
      else if (ctrlDown) dice = dice.replace("d20", "d20+d20-high");
  }
	console.log(desc);
	console.log(dice);
	var xhr = aI();
	var params = "saveroll=on&dicetxt="+encodeURIComponent(dice)+"&dicedesc="+encodeURIComponent(desc)+"&showInChat=on";
	xhr.open("POST", "/dnd/dice-roller/");
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.onload=function() {
		var response = xhr.responseText;
		console.log("resp "+response);
		try {
      document.getElementById("shRolWin").innerHTML = response;
      var div = document.getElementById("shRollDiv");
      div.style.display = "block";
      var rect = e.target.getBoundingClientRect();
      var relativeX = (e.pageX + rect.left),
          relativeY = (e.pageY + rect.top);
      console.log(e.target);
      console.log(rect);
      console.log(e.pageX);
      console.log(e.pageY);
      let divX = e.target.offsetLeft;
      let divWi = parseInt(div.style.width.replace("px",""));
      if (divX + divWi > div.parentElement.offsetWidth) divX -= Math.abs((divX + divWi) - div.parentElement.offsetWidth);
      if (divX < 0) divX = 0;
      div.style.top = e.target.offsetTop + "px";
      div.style.left = divX + "px";
      div.style.height = div.offsetHeight+"px";
    } catch (e) {

    }
		try {
			parent.addChat(response);
		} catch (e) {
			window.open(document.getElementById("shRolWin").getElementsByTagName("a")[0].href, '_blank');
		}

	};
	xhr.send(params);
	return true;
}
try {
  if (parseInt(localStorage.getItem('inpNoDesc'))===1) document.getElementById('inpNoDesc').checked = true;
} catch (e) { }
var shiftDown = false;
var ctrlDown = false;
function onKey(e) {
	shiftDown = e.shiftKey;
	ctrlDown = e.ctrlKey;
}
window.addEventListener('keydown',onKey,false);
window.addEventListener('keyup',onKey,false);

function oNW(a) {
    /*if (a.href.indexOf("wizards.com") == -1) tP(a.href);
    window.open(a.href, "external");
    return true*/
}

function tP(a) {
    a = a.replace(/http\:\/\/(www\.)?kassoon\.com/g, "");
}

function sCM() {
    var a = "?minLvl=" + (Number($("partyLevel").value) - 3);
    a += $("partyLevel").value == "30" ? "&maxLvl=50" : "&maxLvl=" + (Number($("partyLevel").value) + 3);
    if ($("difficulty").value != "null") a += "&difficulty=" + $("difficulty").value;
    if ($("role").value != "null") a += "&role=" + $("role").value;
    if ($("srcName").value) a += "&name=" + $("srcName").value;
    if ($("mm3Tog").checked) a += "&mm3=1";
    a = "/site/apps/monster-search.php" + a;
    $("comFrameDiv").style.display = "none";
    $("srchBtn").disabled = "disabled";
    $("comFrame").src = a;
    $("frameTxt").style.display = "none";
    return true
}

function oIL() {
    try {
        if ($("comFrame").src) {
            $("comFrameDiv").style.display = "";
            $("srchBtn").disabled = ""
        }
    } catch (e) { }
}

function sCW(a, b, c, d) {
    $("addCom").onclick = function () {
        return !aCM(c, d, b, a)
    };
    $("frameTxt").style.display = "block";
    return true
}

function tPV(a,z,x="p",y="a") {
    if(typeof(z)==='undefined') z = ["[show]","[hide]"];
    var b = $(x + a.id.replace(y, ""));
    tD(b, 'none');
    if (b.style.display == "none") a.innerHTML = z[0];
    else a.innerHTML = z[1];
    return true;
}
function hidNav(a,z) {
    if(typeof(z)==='undefined') z = ["[show]","[hide]"];
    var b = $("leftNav");
    var c = $("content");

    if (a.innerHTML == z[1]) {
        a.innerHTML = z[0];
        c.setAttribute('style', 'width:98% !important;max-width:98% !important;');
        setCookie('collapse',1,2);
    }
    else {
        a.innerHTML = z[1];
        c.setAttribute('style', '');
        setCookie('collapse',0,2);
    }

    return true;
}

function sEB(z) {
    curEnemies.encName = $("encName").value.replace(/([^ _\-a-zA-Z0-9]+)/g, "");
    curEnemies.encNotes = $("encNotes").value.replace(/\"/g, "");
    curEnemies.LVL = $("partyLevel").selectedIndex + 1;
    curEnemies.SIZE = $("partySize").selectedIndex;
    var a = json_encode(curEnemies);
    $("saveBtn").disabled = "disabled";

    var b = $("enPub").checked ? 1 : 0;
    return aPS("/site/apps/dbm.php5", "req=addUserEncounter&ID=" + $("encID").value + "&name=" + curEnemies.encName + "&public=" + b + "&txt=" + a.replace('+', '##@') + "&lvl=" + curEnemies.LVL + "&size=" + $("partySize").value, rEB, "sacct", false)
}

function lES() {
    switch ($("lSel").value) {
    case "Desktop":
        $("divFile").style.display = "block";
        $("divTxt").style.display = "none";
        $("accTxt").style.display = "none";
        break;
    case "Text":
        $("divTxt").style.display = "block";
        $("divFile").style.display = "none";
        $("accTxt").style.display = "none";
        break;
    case "Account":
        if (!acct) {
            dLC("lSel");
            $("lSel").selectedIndex = 0;
            lES();
            return false;
        }
        $("accTxt").style.display = "block";
        $("divTxt").style.display = "none";
        $("divFile").style.display = "none";
        return aPS("/site/apps/dbm.php5", "req=getUserEncounter", eAE, false, false)
    }
    return true
}

function lEB() {
    switch ($("lSel").value) {
    case "Desktop":
        $("lForm").submit();
        break;
    case "Text":
        rEB($("lTxt").value, "ldesk");
        break;
    case "Account":
        var a = $("aSel");
        gP("dnd/encounter-builder/" + a.value + "/" + a.options[a.selectedIndex].text.replace(/ /g, "-") + "/", true);
        $("loadBtn").disabled = "disabled";
        break
    }
    return true
}

function eAE(a, b) {
    b = json_decode(String(a).replace(/\\(?!n)/g, ""));
    a = "<select id='aSel'>";
    for (var c = 0; c < b.length; ++c) a += "<option value='" + b[c].ID + "'>" + b[c].name + "</option>";
    a += "</select> <input id='delBtn' type='button' onclick='return ! dAE()' value='Delete'/>";
    $("accTxt").innerHTML = a
}

function dAE() {
    if (confirm("Are you sure you want to delete the encounter? It cannot be undone.")) {
        $("delBtn").disabled = "disabled";
        return aPS("/site/apps/dbm.php5", "req=deleteUserEncounter&ID=" + $("aSel").value, rAE, $("aSel").selectedIndex, false)
    }
}

function rAE(a, b) {
    $("delBtn").disabled = "";
    if (a == 0) $("aSel").options[b] = null;
    else alert("You cannot delete that encounter. You may need to log in or refresh.")
}

function rEB(a, b) {
    console.log(a + " / " + b);
    $("saveBtn").disabled = "";
    if (b == "sdesk") window.location = a;
    else if (b == "ldesk") {
        if (a.contentWindow) if (a.contentWindow.document.body.innerHTML) a = json_decode(String(a.contentWindow.document.body.innerHTML).replace(/\\(?!n)/g, ""));
        else if (a.src) a = json_decode(String($("loadEnc").innerHTML).replace(/\\(?!n)/g, ""));
        else return;
        else {
            if (!a) return;
            a = json_decode(String(a).replace(/\\(?!n)/g, ""))
        }
        curEnemies = {};
        curEnemies.XP = 0;
        for (b = $("encounterTable"); b.rows.length > 1;) b.deleteRow(b.rows.length - 1);
        $("xpVal").innerHTML = "0";
        for (var c in a) if (c == "encName") $("encName").value = a.encName;
        else if (c == "encNotes") $("encNotes").value = a.encNotes;
        else if (c == "LVL") $("partyLevel").selectedIndex = a.LVL - 1;
        else if (c == "SIZE") $("partySize").selectedIndex = a.SIZE;
        else if (c != "XP") for (var d in a[c]) for (var e in a[c][d]) if (a[c][d][e]) try {
            $("mon" + d + "-" + e + "-" + c).value = a[c][d][e][0]
        } catch (g) {
            aCM(d, e, a[c][d][e][1], c.replace("id", ""));
            $("mon" + d + "-" + e + "-" + c).value = a[c][d][e][0]
        }
        curEnemies = a;
        eCB();
        eCD()
    //} else if (b == "sacct") if (Number(a)) gP("dnd/encounter-builder/" + a + "/" + String(curEnemies.encName).replace(/ /g, "-") + "/", true);
    } else if (b == "sacct") if (Number(a)) window.location.href = "/dnd/encounter-builder/" + a + "/" + String(curEnemies.encName).replace(/ /g, "-") + "/";
    else if (a != 0) alert("You cannot save this encounter. You may need to log in.")
}

function rEN() {
    curEnemies = {};
    curEnemies.XP = 0;
    $("encounterTable").innerHTML = "<tr><th>Qty</th><th>Lvl</th><th>Type</th><th>XP Value</th><th>Name<sup title='Edit Names' style='float:right;'>[<a id='editNames' href='javascript:;' onclick='doEnNaE()'>e</a>]</sup></th></tr>";
    $("xpVal").innerHTML = "0";
    $("encID").value = "";
    if ($("pEdit")) $("pEdit").innerHTML = "";
    $("encName").value = "";
    $("encNotes").value = "";
    eCB();
    eCD()
}

function sHW(a, b) {
    var c = $("helper");
    if (a == null) {
        if (c != null) c.style.display = "none";
    }
    else {
        b = gMP(b);
        if (c != null) {
			c.innerHTML = "<p>" + a + "</p>";
	        c.style.left = b[0] + "px";
	        c.style.top = b[1] + 10 + "px";
	        if ((b[0] + 310) > screen.width) c.style.left = b[0] - 300 + "px";
	        c.style.display = "block";
		}
    }
}

function oCW(a, b) {
    if ($("comURL")) a.href = $("comURL").value + "monster.aspx?id=" + b;
    var link = $(b + "-frame");
    if (link) tD(link.parentNode, 'none');
    else {
        var c = document.createElement("div"),
            d = document.createElement("iframe"),
            e = document.createElement("div");
        c.className = "comDiv";
        c.id = b + "-frame";
        c.style.backgroundColor = "#fff";
        d.style.width = "608px";
        d.style.height = "376px";
        d.src = a.href;
        d.frameBorder = 0;
        c.appendChild(d);
        doDrag(c, mX + 100, mY - 200, a.innerHTML);
    }
    return true;
}
var acct = false;
var acRt = false;

function dAL(a) {
    var b = "Inp";
    if (a) b += "Qui";
    $("sub" + b).disabled = "disabled";
    if ($("sub" + b).value == "Log Out") {
    	$("greeting").innerHTML = "Welcome, Stranger";
    	acct = false;
    }
    return $("sub" + b).value == "Log Out" ? aP("/login/", "logout=1&frames=false", rAL, false) : aP("/login/", "username=" + $("user" + b).value + "&password=" + $("pass" + b).value + "&register=" + $("reg" + b).checked + "&frames=false", rAL, acRt)
}

function dLC(c) {
    if (!acct) {
        var a = $("quickLog");
        a.style.top = (mY - 75) + "px";
        a.style.left = (mX - 65) + "px";
        a.style.display = "block";
        $("userInpQui").select();
        acRt = c;
    } else acRt = false;
}

function cLW() {
    oldCaller && sS(oldCaller[1], oldCaller[0], true);
    $("quickLog").style.display = "none";
    acRt = false;
}

function tMI(a) {
    var c = $(a.parentNode.parentNode.id + "-" + a.title);
    if (c.style.display) {
        c.style.display = "";
        if (a.className != "nocode") a.innerHTML = "[+]";
    } else {
        c.style.display = "block";
        if (a.className != "nocode") a.innerHTML = "[-]";
    }
    return true;
}

function tD(a, b) {
    if (!a.style) a = $(a);
    if (a.style.display) a.style.display = "";
    else a.style.display = b;
    try { viewCheck(); } catch (x) {}
    return true;
}

function sT(a, b, c) {
    if (!a.innerHTML) a = $(a);
    if (a.innerHTML == c) a.innerHTML = b;
    else a.innerHTML = c;
    return true;
}

function tFW(a, b, c) {
    if (!a.style) a = $(a);
    if (!b.style) b = $(b);
    if (a.style.display == b.style.display) {
        a.style.width = "";
        b.style.width = "";
    } else if (a.style.display) {
        a.style.width = "";
        b.style.width = c;
    } else if (b.style.display) {
        b.style.width = "";
        a.style.width = c;
    }
    return true;
}

function rAL(a, b) {
    $("loginDiv").innerHTML = a;
    var x = $("data");
    while (x) {
        x.parentNode.removeChild(x);
        x = $("data");
    }
    $("subInpQui").disabled = "";
    if (String(a).toLowerCase().indexOf("logged in") != -1) {
        $("quickLog").style.display = "none";
        var z1 = String(a).indexOf(" in as ") + 7;
        var z2 = String(a).indexOf(". <input");
        acct = (String(a).substring(z1, z2));
        $("greeting").innerHTML = "Welcome, "+acct;
        var x = (window.curPage) ? window.curPage : window.location.toString().replace(/http:\/\/(www\.)?kassoon\.com/g, "");
        if (x.indexOf("dnd/dice-roller") != -1) {
            gP(x, -99)
        }
        else if (b) {
            switch (b) {
            case "lSel":
                $(b).selectedIndex = 2;
                lES();
                break;
            }
        }
    }
    else {
        a = String(a).replace(/(Inp)/g, "$1Qui").replace("dAL(false)", "dAL(true)");
        $("quickLog").innerHTML = a.substring(0, a.indexOf("</form>") + 7);
    }
    acRt = false;
}

function doTSrt(table, index) {
    var i, sorted = [];
    for (i = 0; i < table.rows.length; ++i) sorted[i] = table.rows[i];
    sorted = sorted.sort(function (a, b) {
        return b.cells[index].sort - a.cells[index].sort;
    });
    table.innerHTML = "";
    for (i = 0; i < sorted.length; ++i) table.appendChild(sorted[i]).className = (table.rows.length % 2 == 1) ? "light" : "";
}

var tCount = 0;
var quikAdd = false;
function addTrk(array) {
	var tbl = $("CTrack");
	if (quikAdd) {
		quikAdd = false;
		var inp = tbl.rows[0].getElementsByTagName("input")[0].blur();
		//return addTrk(array);
	}
    var row = tbl.insertRow(0);
    if (tbl.rows.length % 2 == 1) row.className = "light";
    var newdiv = document.createElement("div");
    quikAdd = true;
    newdiv.data = {
        HP: 20,
        MaxHP: 20,
        THP: 0,
        Init: 0,
        AC: 10,
        Fort: 10,
        Ref: 10,
        Will: 10,
        Per: 10,
        Ins: 10,
        Conditions: [],
        Notes: "",
        Name: "Someone",
        Colour: "#ab9a80"
    };
    var conditionList = "";
    if (array) {
        quikAdd = false;
    	newdiv.data = array;
        for (i = 0; i < newdiv.data.Conditions.length; ++i) {
            if (!newdiv.data.Conditions[i]) continue;
            conditionList += "<a href='' onclick='return ! setTrk(this.parentNode, 8, [\"Conditions\"," + i + "])'>" + newdiv.data.Conditions + "</a>";
            if (i < newdiv.data.Conditions.length - 1) conditionList += ", ";
        }
    }
    newdiv.innerHTML = "<a style='position:absolute;display:block;top:2px;left:25px;color:#fff;text-decoration:none;' href='' id='" + tCount + "-ctT' onclick='return ! setTrk(this, 1, \"Name\")'>" + newdiv.data.Name + "</a> HP: <a href='' style='display:inline-block;min-width:25px;text-align:center;' onclick='return ! setTrk(this, 1, \"HP\")' style='font-weight:bold;'>" + newdiv.data.HP + "</a> (<a href='' style='font-weight:bold;padding:2px;' onclick='return ! setTrk(this.parentNode.getElementsByTagName(\"a\")[1], 4, \"HP\")'>-</a>/<a href='' style='font-weight:bold;padding:1px;' onclick='return ! setTrk(this.parentNode.getElementsByTagName(\"a\")[1], 3, \"HP\")'>+</a>) out of <a onclick='return ! setTrk(this, 1, \"MaxHP\")' href=''>" + newdiv.data.MaxHP + "</a> (<a onclick='return ! setTrk(this, 1, \"THP\")' href=''>" + newdiv.data.THP + "</a> THP) &nbsp; &nbsp; Initiative: <a onclick='return ! setTrk(this, 1, \"Init\")' href=''>" + newdiv.data.Init + "</a> &nbsp; &nbsp; Per. <a onclick='return ! setTrk(this, 1, \"Per\")' href=''>" + newdiv.data.Per + "</a> &nbsp; Ins. <a onclick='return ! setTrk(this, 1, \"Ins\")' href=''>" + newdiv.data.Ins + "</a> &nbsp; &nbsp; &nbsp; &nbsp; AC: <a onclick='return ! setTrk(this, 1, \"AC\")' href=''>" + newdiv.data.AC + "</a> &nbsp; &nbsp; Fortitude: <a onclick='return ! setTrk(this, 1, \"Fort\")' href=''>" + newdiv.data.Fort + "</a> &nbsp; &nbsp; Reflex: <a onclick='return ! setTrk(this, 1, \"Ref\")' href=''>" + newdiv.data.Ref + "</a> &nbsp; &nbsp; Willpower: <a onclick='return ! setTrk(this, 1, \"Will\")' href=''>" + newdiv.data.Will + "</a><br/><a onclick='return ! setTrk(this.parentNode.getElementsByTagName(\"span\")[0], 5, \"Notes\")' href=''>Notes</a>: <span>" + newdiv.data.Notes + "</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <a onclick='return ! setTrk(this.parentNode.getElementsByTagName(\"span\")[1], 7, \"Conditions\")' href=''>Conditions</a>: <span>" + conditionList + "</span> <a style='font-size:9px;display:block;position:absolute;right:0;bottom:-3px;' href='javascript:;' onclick='return ! edTrk(this)'>[Edit]</a><div class='encEd'><strong>Edit</strong><br/> Colour: <a onclick='return ! setTrk(this, 1, \"Colour\")' href=''>" + newdiv.data.Colour + "</a></div>";
    newdiv.style.padding = "10px";
    newdiv.style.backgroundColor = "#ece7cd";
    newdiv.style.backgroundImage = "url('/site/images/texture.png')";
    var dragger = doDrag(newdiv, 0, 0, '');
    dragger.style.position = "relative";
    dragger.getElementsByTagName("div")[0].style.backgroundColor = newdiv.data.Colour;
    row.insertCell(0).className = "ctPoint";
    row.cells[0].style.padding = "10px";
    row.cells[0].style.verticalAlign = "middle";
    row.insertCell(1).appendChild(dragger);
    row.cells[1].style.textAlign = "left";
    row.cells[1].style.position = "relative";
    row.cells[1].style.height = "100px";
    row.cells[1].id = tCount + "-ct";
    row.cells[1].sort = newdiv.data.Init;
    dragger.onmouseover = function (e) {
        if (window.dragging && window.dragging.parentNode.id != this.parentNode.id) {
            var oldTarg = this.parentNode;
            var newTarg = window.dragging.parentNode;
            oldTarg.removeChild(this);
            newTarg.removeChild(window.dragging);
            oldTarg.appendChild(window.dragging);
            newTarg.appendChild(this);
            var tmp = oldTarg.sort;
            oldTarg.sort = newTarg.sort;
            newTarg.sort = tmp;
        }
    };
    dragger.getElementsByTagName("div")[0].onmousedown = function (e) {
        e = e || window.event;
        dragger.style.position = "absolute";
        dragger.style.left = "50px";
        var target = e.target || e.srcElement;
        if (target.className == "close") {
            var newList = [];
            for (i = 0; i < tbl.rows.length; ++i) if (tbl.rows[i].cells[1].id != this.parentNode.parentNode.id) newList[newList.length] = tbl.rows[i];
            tbl.innerHTML = "";
            for (i = 0; i < newList.length; ++i) tbl.appendChild(newList[i]).className = (tbl.rows.length % 2 == 1) ? "light" : "";
            return true;
        }
        clearInterval(dragger.loop);
        window.dragging = dragger;
        dragger.loop = setInterval(function () {
            dragger.style.top = (mY - 70) + "px";
        }, 50);
        document.onmouseup = function (e) {
            clearInterval(dragger.loop);
            dragger.style.position = "relative";
            dragger.style.top = "";
            dragger.style.left = "";
            window.dragging = null;
            document.onmouseup = null;
            return false;
        };
        return false;
    };
    setTrk($((tCount++) + '-ctT'), 1, "Name");
    return true;
}

function edTrk(element) {
    tD(element.parentNode.getElementsByTagName("div")[0], "block", "none");
    sT(element, "[Edit]", "[Close]");
    return true;
}

function setTrk(element, mode, resource) {
    var targ = element.parentNode;
	try {
        if (resource == "Colour") targ = element.parentNode.parentNode;
        if (mode == 1) {
            element.innerHTML = "<input type='text' style='width:" + ((resource == "Name" || resource == "Colour") ? "125" : "25") + "px' value='" + targ.data[resource] + "'/>";
            var targ = element.getElementsByTagName("input")[0];
            targ.onblur = function () {
                setTrk(element, 2, resource)
            }
            targ.onkeypress = function (event) {
            	if (event.keyCode == 13) {
            		targ.blur();
            		return false;
            	}
            }
            targ.onkeyup = function(event) {
            	if (event.keyCode == 27) {
            		quikAdd = false;
            		targ.blur();
            		if (resource == "Name") element.style.fontWeight = "bold";
            	}
            }
            targ.focus();
            targ.select();
        } else if (mode == 2) {
            targ.data[resource] = element.getElementsByTagName("input")[0].value;
            element.innerHTML = targ.data[resource];
            if (element.innerHTML.replace(/ /g, "").length < 1) setTrk(element, 1, resource);
        } else if (mode == 3 || mode == 4) {
            var amt = prompt("Enter amount:", 1);
            targ.data[resource] = Number(targ.data[resource]) + Number((mode == 3) ? amt : (amt * -1));
            element.innerHTML = targ.data[resource];
        } else if (mode == 5) {
            element.innerHTML = "<textarea style='width:100%;height:100px;'>" + targ.data[resource] + "</textarea>";
            element.getElementsByTagName("textarea")[0].onblur = function () {
                setTrk(element, 6, resource)
            }
            element.parentNode.parentNode.style.zIndex = ++indexLevel;
            element.getElementsByTagName("textarea")[0].focus();
            element.getElementsByTagName("textarea")[0].select();
        } else if (mode == 6) {
            targ.data[resource] = element.getElementsByTagName("textarea")[0].value;
            element.innerHTML = targ.data[resource];
        } else if (mode == 7) {
            var txt = prompt("Enter the condition text", "Marked (UEONT Goblin)");
            targ.data[resource][targ.data[resource].length] = txt;
            element.innerHTML = "";
            for (i = 0; i < targ.data[resource].length; ++i) {
                if (!targ.data[resource][i]) continue;
                element.innerHTML += "<a href='' onclick='return ! setTrk(this.parentNode, 8, [\"" + resource + "\"," + i + "])'>" + targ.data[resource][i] + "</a>";
                if (i < targ.data[resource].length - 1) element.innerHTML += ", ";
            }
        } else if (mode == 8) {
            targ.data[resource[0]][resource[1]] = 0;
            element.innerHTML = "";
            for (i = 0; i < targ.data[resource[0]].length; ++i) {
                if (!targ.data[resource[0]][i]) continue;
                element.innerHTML += "<a href='' onclick='return ! setTrk(this.parentNode, 8, [\"" + resource[0] + "\"," + i + "])'>" + targ.data[resource[0]][i] + "</a>";
                if (i < targ.data[resource[0]].length - 1) element.innerHTML += ", ";
            }
        }
        if (resource == "HP" && targ.data.HP <= (targ.data.MaxHP / 2)) element.style.color = "#f00";
        else if (resource == "MaxHP" && !quikAdd && targ.data.HP <= (targ.data.MaxHP / 2)) element.parentNode.getElementsByTagName("a")[1].style.color = "#f00";
        else if (resource == "HP" || resource == "MaxHP") element.style.color = "";
        if (resource == "Init") element.parentNode.parentNode.parentNode.sort = targ.data.Init;
        if (resource == "Colour") element.parentNode.parentNode.parentNode.getElementsByTagName("div")[0].style.backgroundColor = targ.data[resource];
    } catch (x) {}

    if (quikAdd && (mode == 2 || mode == 6)) {
    	element.blur();
    	if (resource == "Name") {
    		element.style.fontWeight = "bold";
    		targ.getElementsByTagName("a")[1].onclick();
    	}
    	else if (resource == "HP") {
    		targ.data["Max"] = targ.data[resource];
            targ.getElementsByTagName("a")[4].innerHTML = targ.data[resource];
            targ.getElementsByTagName("a")[6].onclick();
            quikAdd = 7;
    	}
    	else if (resource != "Notes") {
    		targ.getElementsByTagName("a")[quikAdd].onclick();
    		quikAdd += 1;
    	}
    	else quikAdd = false;
    }
    return true;
}
/*
newdiv.data = {
        HP: 20,
        MaxHP: 20,
        THP: 0,
        Init: 0,
        AC: 10,
        Fort: 10,
        Ref: 10,
        Will: 10,
        Per: 10,
        Ins: 10,
        Conditions: [],
        Notes: "",
        Name: "Someone",
        Colour: "#ab9a80"
    };
*/

function savTrk(button) {
    var tbl = $("CTrack");
    button.disabled = "disabled";
    var save = {};
    for (i = 0; i < tbl.rows.length; ++i) {
        save[i] = tbl.rows[i].cells[1].getElementsByTagName("div")[0].getElementsByTagName("div")[2].data;
    }
    var txt = json_encode(save);
    return aPS("/site/apps/dbm.php5", "req=addUserCombat&name=" + $("CTrName").value + "&txt=" + txt + "&ID=" + $("CTID").value, function (a, b) {
        button.disabled = "";
        if(!$("CTID").value) {
        	var sel = $("CTrSel");
        	sel.options[sel.length] = new Option($("CTrName").value, a);
        }
    }, "sacct", false)
}
var curTurn = -1;

function doTurn() {
    var tbl = $("CTrack");
    try {
        tbl.rows[curTurn].cells[0].innerHTML = "";
    } catch (e) {}
    if (++curTurn >= tbl.rows.length) curTurn = 0;
    tbl.rows[curTurn].cells[0].innerHTML = "<a href='' onclick='return ! doTurn()'>&rarr;</a>";
    scroll(0, tbl.rows[curTurn].offsetTop);
    return true;
}

function dump(arr, level) {
    var dumped_text = "";
    if (!level) level = 0;
    var level_padding = "";
    for (var j = 0; j < level + 1; j++) level_padding += "    ";
    if (typeof(arr) == 'object') {
        for (var item in arr) {
            var value = arr[item];
            if (typeof(value) == 'object') {
                dumped_text += level_padding + "'" + item + "' ...\n";
                dumped_text += dump(value, level + 1);
            } else {
                dumped_text += level_padding + "'" + item + "' => \"" + value + "\"\n";
            }
        }
    } else {
        dumped_text = "===>" + arr + "<===(" + typeof(arr) + ")";
    }
    return dumped_text;
}

function lodTrk(button) {
    var tbl = $("CTrack");
    var sel = $("CTrSel");
    button.disabled = "disabled";
    return aPS("/site/apps/dbm.php5", "req=getCombat&ID=" + sel.options[sel.selectedIndex].value, function (a, b) {
        button.disabled = "";
        var save = json_decode(a);
        $("CTID").value = save[0]['ID'];
        $("CTrName").value = save[0]['name'];
        $("CTEdit").innerHTML = "Stop Editing "+save[0]['name'];
        save = json_decode(save[0]['txt']);
        var i = 0,
            current;
        try {
            while (current = save[i++]) {
                addTrk(current);
            }
        } catch (e) {}
    }, false, false)
}

function delTrk(button) {
    var sel = $("CTrSel");
    button.disabled = "disabled";
    return aPS("/site/apps/dbm.php5", "req=deleteUserCombat&ID=" + sel.options[sel.selectedIndex].value, function (a, b) {
        button.disabled = "";
        sel.remove(sel.selectedIndex)
    }, false, false)
}

function doDrag(element, x, y, title) {
    var a = document.createElement("div"),
        b = document.createElement("div"),
        c = document.createElement("div"),
        d = document.createElement("div");
    a.className = "container";
    b.className = "dragger";
    b.innerHTML = "<span>" + title + "</span>";
    a.appendChild(b);
    c.className = "close";
    c.style.zIndex = 999;
    c.innerHTML = "x";
    b.appendChild(c);
    a.appendChild(element);
    a.style.left = Math.max(100,x) + "px";
    a.style.top = Math.max(200,y) + "px";
    a.style.zIndex = ++indexLevel;
    document.body.appendChild(a);
    a.style.position = "absolute";
    a.style.padding = "0";
    a.style.margin = "5px";
    a.style.backgroundColor = "#FFF";
    a.style.border = "1px solid #ab9a80";
    b.style.width = "99%";
    a.onclick = function (e) {
        a.style.zIndex = ++indexLevel;
    }
    b.onmousedown = function (e) {
        e = e || window.event;
        try {
            document.body.removeChild($("dScreen"));
        } catch (x) {}
        var target = e.target || e.srcElement;
        if (target.className == "close") return !document.body.removeChild(a);
        clearInterval(b.loop);
        a.winOffX = mX - a.offsetLeft;
        a.winOffY = mY - a.offsetTop;
        a.style.zIndex = ++indexLevel;
        var shield = document.createElement("div");
        shield.id = "dScreen";
        shield.style.position = "absolute";
        shield.style.width = "100%";
        shield.style.height = $("content").clientHeight + "px";
        shield.style.top = 0;
        shield.style.left = 0;
        shield.style.zIndex = indexLevel + 2;
        document.body.appendChild(shield);
        b.loop = setInterval(function () {
            a.style.left = (mX - a.winOffX) + "px";
            a.style.top = (mY - a.winOffY) + "px";
        }, 50);
        var z = document.createElement("div");
        z.id = "dScreen";
        z.style.width = "100%";
        z.style.height = "100%";
        z.style.position = "absolute";
        z.innerHTML = "&nbsp;";
        document.body.appendChild(z);
        document.onmouseup = function (e) {
            clearInterval(b.loop);
            document.onmouseup = null;
            document.body.removeChild(z);
            document.body.removeChild(shield);
            return false;
        };
        return false;
    };
    b.style.opacity = 0;
    clearInterval(b.fade);
    b.fade = setInterval(function () {
        if (b.style.opacity < 1) b.style.opacity = Number(b.style.opacity) + 0.1;
        else clearInterval(b.fade);
    }, 50);
    return a;
}

function movCar(el) {
    if (typeof el.selectionStart == "number") {
        el.selectionStart = el.selectionEnd = el.value.length;
    } else if (typeof el.createTextRange != "undefined") {
        el.focus();
        var range = el.createTextRange();
        range.collapse(false);
        range.select();
    }
}//movCar
function makEd(divs){
	for (i=0; i < divs.length;++i) {
		divs[i].onmousedown=null;
		divs[i].onclick=function(){
			if(this.editing)return;
			var txt = document.createElement('textarea');
			txt.className="editable";
			txt.value = this.innerHTML.replace( /\<br(\s*\/|)\>/g, '\r\n' );
			txt.onblur=function(){
				this.parentNode.editing=false;
				this.parentNode.innerHTML = this.value.replace( /\r\n|\r|\n/g, '<br />' );
			};
			txt.onpaste=function(){
			    this.value = this.value.replace(/ \+([0-9]+)\b/g, ' [+$1]');
            };
			this.editing=true;
			this.innerHTML = "";
			this.appendChild(txt);
			txt.onkeyup=function(){
				this.style.height = "1px";
				this.style.height = (this.scrollHeight)+"px";
			}
			txt.style.height = "1px";
			txt.style.height = (txt.scrollHeight)+"px";

			txt.focus();
			if (txt.value == "1") txt.select();
			movCar(txt);
		};//div.onload
		divs[i].style.cursor="text";
	}//for
}//makeEd()
function makDel(divs){
	for (i=0; i < divs.length;++i) {
		divs[i].onclick=function(){
			this.parentNode.removeChild(this);
		};//div.onload
		divs[i].style.cursor="crosshair";
	}//for
}//makDel()
function makMov(divs){
	for (i=0; i < divs.length;++i) {
		divs[i].onclick=null;
		divs[i].onmousedown=function(e){
			if(document.all?true:false) window.mouseY = event.clientY + document.body.scrollTop;
			else window.mouseY = e.pageY;
			window.adjusting=this;
			document.onmouseup=function(e){
				document.onmousemove=null;
				document.onmouseup=null;
				window.adjusting=null;
				window.mouseY=null;
			}//document.onmouseup
			document.onmousemove=function(e){
				var node = window.adjusting;
				var base = parseInt(node.style.marginTop.replace(/px/i, "") );
				var change = 0;
				if(document.all?true:false) {
					change = event.clientY + document.body.scrollTop - window.mouseY;
					window.mouseY = event.clientY + document.body.scrollTop;
				}
				else {
					change = e.pageY - window.mouseY;
					window.mouseY = e.pageY;
				}
				base += change;
				node.style.marginTop=base+"px";
			}//document.onmousemove
			return false;
		};//div.onload
		divs[i].style.cursor="move";
	}//for
}//makMov
function spcEd(){
	var divs = document.getElementById('connections').getElementsByTagName('div');
	for(i=0;i<divs.length;++i){
		if(divs[i].className=="spacer") continue;
		divs[i].onclick=null;
		divs[i].onmousedown=function(e){
			if(document.all?true:false) window.mouseY = event.clientY + document.body.scrollTop;
			else window.mouseY = e.pageY;
			window.adjusting=this;
			document.onmouseup=function(e){
				document.onmousemove=null;
				document.onmouseup=null;
				window.adjusting=null;
				window.mouseY=null;
			}//document.onmouseup
			document.onmousemove=function(e){
				var arr = window.adjusting;
				var base = parseInt(arr.style.top.replace(/px/i, "") );
				var change = 0;
				if(document.all?true:false) {
					change = event.clientY + document.body.scrollTop - window.mouseY;
					window.mouseY = event.clientY + document.body.scrollTop;
				}
				else {
					change = e.pageY - window.mouseY;
					window.mouseY = e.pageY;
				}
				base += change;
				arr.style.top=base+"px";
			}//document.onmousemove
			return false;
		};//div.onclick
		divs[i].style.cursor="move";
	}//for
}//spcEd()
function spcDel(){
	var divs = document.getElementById('connections').getElementsByTagName('div');
	for(i=0;i<divs.length;++i){
		if(divs[i].className=="spacer") continue;
		divs[i].onmousedown=null;
		divs[i].onclick=function(e){
			this.parentNode.removeChild(this);
		};//div.onclick
		divs[i].style.cursor="crosshair";
	}//for
}//spcDel()
function togDel(){
	var delNode = document.getElementById('delNode');
	var movNode = document.getElementById('movNode');
	if(delNode.deleting||movNode.moving){
		makEd(document.getElementById('ingredientList').getElementsByTagName('div') );
		makEd(document.getElementById('stepList').getElementsByTagName('div') );
		spcEd();
		delNode.value = "Delete Nodes";
		delNode.deleting = false;
		movNode.value = "Move Nodes";
		movNode.moving = false;
	}//if deleting/moving
	else{
		makDel(document.getElementById('ingredientList').getElementsByTagName('div') );
		makDel(document.getElementById('stepList').getElementsByTagName('div') );
		spcDel();
		delNode.value = "Stop Deleting";
		delNode.deleting = true;
	}//else starting
}//togDel()
function togMov(){
	var delNode = document.getElementById('delNode');
	var movNode = document.getElementById('movNode');
	if(delNode.deleting||movNode.moving){
		makEd(document.getElementById('ingredientList').getElementsByTagName('div') );
		makEd(document.getElementById('stepList').getElementsByTagName('div') );
		spcEd();
		delNode.value = "Delete Nodes";
		delNode.deleting = false;
		movNode.value = "Move Nodes";
		movNode.moving = false;
	}//if deleting/moving
	else{
		makMov(document.getElementById('ingredientList').getElementsByTagName('div') );
		makMov(document.getElementById('stepList').getElementsByTagName('div') );
		movNode.value = "Stop Moving";
		movNode.moving = true;
	}//else starting
}//togMov()
function makIng(txt,margin){
	var div = document.createElement('div');
	div.className="node";
	div.style.marginTop = margin+"px";
	div.innerHTML=txt;
	document.getElementById('ingredientList').appendChild(div);
	return div;
}//makIng
function addNodes(){
	var div = makIng("Click me to set ingredients",0);
	makEd(document.getElementById('ingredientList').getElementsByTagName('div') );
	var div2 = addStep(true,"Click me to set instructions",0);

	div = div.parentNode.getElementsByTagName('div');
	div2 = div2.parentNode.getElementsByTagName('div');
	var spacing = 0;
	if (div.length > 0){
		for(i=div.length-1;i>=0;--i) spacing += (div[i].scrollHeight);
	}//if
	if (div2.length > 0){
		for(i=div2.length-1;i>=0;--i) spacing += (div2[i].scrollHeight);
	}//if
	spacing = (spacing/2)-14;
	makArr(spacing);

	var delNode = document.getElementById('delNode');
	var movNode = document.getElementById('movNode');
	if(delNode.deleting||movNode.moving){
		makEd(document.getElementById('ingredientList').getElementsByTagName('div') );
		makEd(document.getElementById('stepList').getElementsByTagName('div') );
		spcEd();
		delNode.value = "Delete Nodes";
		delNode.deleting = false;
		movNode.value = "Move Nodes";
		movNode.moving = false;
	}//if deleting/moving
	spcEd();
}//addNodes()
function makArr(spacing){
	var arr = document.createElement('div');
	arr.className="point";
	arr.style.top=spacing+"px";
	arr.innerHTML = ">";
	document.getElementById('connections').appendChild(arr);
}
function addStep(edit,txt,margin){
	var div = document.createElement('div');
	div.className="node";
	div.style.marginTop = margin+"px";
	div.innerHTML=txt;
	document.getElementById('stepList').appendChild(div);
	if (edit) makEd(document.getElementById('stepList').getElementsByTagName('div') );
	return div;
}//addStep()
// TODO Save format: # ingredients, "Safe \" Strings", # steps, "Safe Strings", # Arrows, height numbers,
function savRec(){
	var delNode = document.getElementById('delNode');
	var movNode = document.getElementById('movNode');
	if(delNode.deleting||movNode.moving){
		makEd(document.getElementById('ingredientList').getElementsByTagName('div') );
		makEd(document.getElementById('stepList').getElementsByTagName('div') );
		spcEd();
		delNode.value = "Delete Nodes";
		delNode.deleting = false;
		movNode.value = "Move Nodes";
		movNode.moving = false;
	}//if deleting/moving
	if (document.onmouseup) document.onmouseup(null);

	var saveString = "";
	var divs = document.getElementById('ingredientList').getElementsByTagName('div');
	saveString += divs.length + ",";
	for(i=0;i<divs.length;++i){
		if(divs[i].editing) divs[i].getElementsByTagName('textarea')[0].onblur();
		saveString += divs[i].innerHTML.replace(/,/g, "&#44;") + ",";
		saveString += divs[i].style.marginTop.replace(/px/i, "") + ",";
	}//for
	divs = document.getElementById('stepList').getElementsByTagName('div');
	saveString += divs.length + ",";
	for(i=0;i<divs.length;++i){
		if(divs[i].editing) divs[i].getElementsByTagName('textarea')[0].onblur();
		saveString += divs[i].innerHTML.replace(/,/g, "&#44;") + ",";
		saveString += divs[i].style.marginTop.replace(/px/i, "") + ",";
	}//for
	divs = document.getElementById('connections').getElementsByTagName('div');
	saveString += divs.length + ",";
	for(i=0;i<divs.length;++i){
		saveString += divs[i].style.top.replace(/px/i, "") + ",";
	}//for

	saveString = lzw_encode(saveString);
	var savTxt = document.getElementById('saveTxt');
	savTxt.value = saveString;
}//saveRec()
function loadRec(){
	var savTxt = document.getElementById('saveTxt');
	var saveArray = lzw_decode(savTxt.value).split(",");

	document.getElementById('ingredientList').innerHTML="";
	var length = saveArray.shift();
	for(i=length-1;i>=0;--i){
		var txt = saveArray.shift().replace(/&#44;/g, ",");
		var margin = saveArray.shift();
		makIng(txt,margin);
	}//for
	document.getElementById('stepList').innerHTML="";
	var length = saveArray.shift();
	for(i=length-1;i>=0;--i){
		var txt = saveArray.shift().replace(/&#44;/g, ",");
		var margin = saveArray.shift();
		addStep(false,txt,margin);
	}//for
	document.getElementById('connections').innerHTML="";
	var length = saveArray.shift();
	for(i=length-1;i>=0;--i){
		var top = saveArray.shift();
		makArr(top);
	}//for

	makEd(document.getElementById('ingredientList').getElementsByTagName('div') );
	makEd(document.getElementById('stepList').getElementsByTagName('div') );
	spcEd();
}//loadRec()
function delAll(){
	var r=confirm("You sure about that?");
	if(r==true){
		document.getElementById('ingredientList').innerHTML="";
		document.getElementById('stepList').innerHTML="";
		document.getElementById('connections').innerHTML="";
	}
}
function lzw_encode(s) {
    var dict = {};
    var data = (s + "").split("");
    var out = [];
    var currChar;
    var phrase = data[0];
    var code = 256;
    for (var i=1; i<data.length; i++) {
        currChar=data[i];
        if (dict[phrase + currChar] != null) {
            phrase += currChar;
        }
        else {
            out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
            dict[phrase + currChar] = code;
            code++;
            phrase=currChar;
        }
    }
    out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
    for (var i=0; i<out.length; i++) {
        out[i] = String.fromCharCode(out[i]);
    }
    return out.join("");
}
function lzw_decode(s) {
    var dict = {};
    var data = (s + "").split("");
    var currChar = data[0];
    var oldPhrase = currChar;
    var out = [currChar];
    var code = 256;
    var phrase;
    for (var i=1; i<data.length; i++) {
        var currCode = data[i].charCodeAt(0);
        if (currCode < 256) {
            phrase = data[i];
        }
        else {
           phrase = dict[currCode] ? dict[currCode] : (oldPhrase + currChar);
        }
        out.push(phrase);
        currChar = phrase.charAt(0);
        dict[code] = oldPhrase + currChar;
        code++;
        oldPhrase = phrase;
    }
    return out.join("");
}
function mes_txt() {
    var mes1 = [//Áß&#268;&#270;&#276;&#358;&#286;&#292;&#296;&#308;&#310;&#313;&#1052;&#323;&#336;&#1056;Q&#340;&#346;&#356;ÚV&#372;&#1046;&#374;&#377;
    "abcdefghijklmnopqrstuvwxyz!?*<>.,=+-()",
    "ï»ªÑà¥®ÕªÎµÖÖÕ°ï»¨ÕµÄ¸láÕ¼ÖÕ©Õ¦Ð³à¸£Õ§Õ½Î½Õ¡ã¤Õ¯Õ¹!?*<>.,=+-()",
    "48(d3f9h!jk1mn0pqr57uvwxy2!?*<>.,=+-()",
    ["&#3588;","&#3666;","&#962;","&#3668;","&#1108;","&#358;","&#65262;","&#1106;","&#3648;","&#1503;","&#1082;","l","&#3667;","&#3616;","&#3663;","&#1511;","&#7907;","&#1075;","&#3619;","t","&#3618;","&#1513;","&#3628;","&#1509;","&#1488;","z"],
    "Ã¤bÄdÃ«fÄ¡hÃ¯jklmnÃ¶pqrstÃ¼vwxÃ¿Å¼!?*<>.,=+-()",
    "Ã¡bÄdÃ©fghÃ­jklmÅÅpqÅÅtÃºvwxÃ½Åº!?*<>.,=+-()",
    "ÎBáDÎ£FGÎIJÎáMÐÓ¨PQÐ¯Æ§Æ¬Ð¦VÐ©XÎ¥Z!?*ââ·.,=+-()",
    "ï¾ä¹cdä¹ï½·gãï¾ï¾ãºï¾ï¾¶åoï½±qå°ºä¸ï½²uâwï¾ï¾ä¹!?*<>.,=+-()",
    ["&#9424;","&#9425;","&#9426;","&#9427;","&#9428;","&#9429;","&#9430;","&#9431;","&#9432;","&#9433;","&#9434;","&#9435;","&#9436;","&#9437;","&#9438;","&#9439;","&#9440;","&#9441;","&#9442;","&#9443;","&#9444;","&#9445;","&#9446;","&#9447;","&#9448;","&#9449;"],
    ];
    var mes2 = [
    "'abcdefghijklmnopqrstuvwxyz?*<>",
    "'\u03B1\u0432\u00A2\u2202\u0454fg\u043D\u03B9\u05E0\u043A\u2113\u043C\u0438\u03C3\u03C1q\u044F\u0455\u0442\u03C5\u03BD\u03C9\u03C7\u0443z\u061F\u25CF«»",
    "'\u0102\u03b2\u010C\u010E\u0114\u0166\u011E\u0124\u0128\u0134\u0136\u0139\u041C\u0143\u0150\u0420Q\u0154\u015A\u0164\u00DA\u0056\u0174\u0416\u0176\u0179\u061F\u25CF\u00ab\u00bb",
    "'\u0E04\u0E52\u03C2\u0E54\u0454\u0166\uFEEE\u0452\u0E40\u05DF\u043Al\u0E53\u0E20\u0E4F\u05E7\u1EE3\u0433\u0E23t\u0E22\u05E9\u0E2C\u05E5\u05D0z\u061F\u25CF\u00ab\u00bb",
    "'a\u0432cde\u0493g\u043D\u03B9j\u0138\u006C\u043Cnopqr\u0455\u0442\u03C5vw\u0445yz?*<>",
    "'\u03B1\u0432\u0441\u1E0B\u03B5\u0192\u0123\u0068\u00EF\u0458\u045Cl\u1E43\u1E49\u00F8\u03C1\u03C3\u027E\u1E61\u03C4\u03C5\u1E7F\u03CE\u03C7\u00FF\u0290?*<>",
    "'\u03B1\u0432cd\u0454fgh\u00EDjklmn\u03C3pqrstuvw\u0445\u0447z?*<>",
    [",","&#x250;","q","&#x254;","p","&#x1DD;","&#x25F;","&#x183;","&#x265;","&#x1D09;","&#x27E;","&#x29E;","l","&#x26F;","u","o","d","b","&#x279;","s","&#x287;","n","&#x28C;","&#x28D;","x","&#x28E;","z"],
    "'\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8j\u03b9\u03ba\u03bb\u03bc\u03bd\u03bf\u03c0\u03c1\u03c2\u03c3\u03c4\u03c5\u03c6\u03c9\u03c7\u03c8",
    "'\u03B1\u0432\u00A2\u2202\u0454fg\u043D\u03B9\u05E0\u043A\u2113\u043C\u0438\u03C3\u03C1q\u044F\u0455\u0442\u03C5\u03BD\u03C9\u03C7\u0443z\u061F\u25CF«»",
    "'\u0102\u03b2\u010C\u010E\u0114\u0166\u011E\u0124\u0128\u0134\u0136\u0139\u041C\u0143\u0150\u0420Q\u0154\u015A\u0164\u00DA\u0056\u0174\u0416\u0176\u0179\u061F\u25CF\u00ab\u00bb",
    "'a\u0432cde\u0493g\u043D\u03B9j\u0138\u006C\u043Cnopqr\u0455\u0442\u03C5vw\u0445yz?*<>",
    "'\u03B1\u0432\u0441\u1E0B\u03B5\u0192\u0123\u0068\u00EF\u0458\u045Cl\u1E43\u1E49\u00F8\u03C1\u03C3\u027E\u1E61\u03C4\u03C5\u1E7F\u03CE\u03C7\u00FF\u0290?*<>",
    "'\u03B1\u0432cd\u0454fgh\u00EDjklmn\u03C3pqrstuvw\u0445\u0447z?*<>",
    [",","&#x250;","q","&#x254;","p","&#x1DD;","&#x25F;","&#x183;","&#x265;","&#x1D09;","&#x27E;","&#x29E;","l","&#x26F;","u","o","d","b","&#x279;","s","&#x287;","n","&#x28C;","&#x28D;","x","&#x28E;","z"],
    ];
    var fields = [
        "txt1","txt3","txt5","txt6","txt7","txt8","txt9","txt10"
    ];
    var fields2 = [
        "txt12","txt13","txt14","txt16","txt17","txt18","txt19","txt20","txt21","txt23","txt26","txt27","txt28","txt29"
    ];

    var str = $('textifyin').value;
    for (var i = 0; i < str.length; ++i) {
        var chr=str.charAt(i);
        var z=0 ;
        var ind=0;
        var fnd=false;
        for (z = 0; z < mes1[0].length; ++z) {
            if (mes1[0].charAt(z) == chr.toLowerCase()) {
                ind = z;
                fnd=true;
                break;
            }
        }
        for (z = 0; z < fields.length; ++z) {
            var obj = $(fields[z]);
            if (obj.nodeName == "INPUT") {
               if (i == 0) obj.value = "";
                if (fnd) {
                    if (mes1[z+1] instanceof Array) obj.value += mes1[z+1][ind];
                    else obj.value += mes1[z+1].charAt(ind);
                }
                else obj.value += chr;
            } else {
                if (i == 0) obj.innerHTML = "";
                if (fnd) {
                    if (mes1[z+1] instanceof Array) obj.innerHTML += mes1[z+1][ind];
                    else obj.innerHTML += mes1[z+1].charAt(ind);
                }
                else {
                    chr.replace(" ","&nbsp;");
                    obj.innerHTML += chr;
                }
            }

        }

        var m=0;
        var in2=0;
        fnd=false;
        for (m = 0; m < mes2[0].length; ++m) {
            if (mes2[0].charAt(m) == chr.toLowerCase()) {
                in2 = m;
                fnd=true;
                break;
            }
        }
        for (m = 0; m < fields2.length; ++m) {
            var obj = $(fields2[m]);
            if (obj.nodeName == "INPUT") {
                if (i == 0) obj.value = "";
                if (fnd) {
                    if (mes2[m+1] instanceof Array) obj.value += mes2[m+1][in2];
                    else obj.value += mes2[m+1].charAt(in2);
                }
                else obj.value += chr;
            } else {
                if (i == 0) obj.innerHTML = "";
                if (fnd) {

                    if (mes2[m+1] instanceof Array) {
                        if (m+1 == fields.length-1) obj.innerHTML = mes2[m+1][in2] + obj.innerHTML;
                        else obj.innerHTML += mes2[m+1][in2];
                    }
                    else obj.innerHTML += mes2[m+1].charAt(in2);
                }
                else {
                    chr.replace(" ","&nbsp;");
                    if (m+1 == fields.length-1) obj.innerHTML = chr + obj.innerHTML;
                    else obj.innerHTML += chr;
                }
            }

        }
    }
}
function select_all(el) {
    if (typeof window.getSelection != "undefined" && typeof document.createRange != "undefined") {
        var range = document.createRange();
        range.selectNodeContents(el);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    } else if (typeof document.selection != "undefined" && typeof document.body.createTextRange != "undefined") {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.select();
    }
}
function random(min,max) {
    return Math.floor( (Math.random() * (max - min) ) + min);
}
function posTop() {
    return typeof window.pageYOffset != 'undefined' ?  window.pageYOffset : document.documentElement && document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop ? document.body.scrollTop : 0;
}
function pageHeight() {
    return window.innerHeight != null? window.innerHeight : document.documentElement && document.documentElement.clientHeight ?  document.documentElement.clientHeight : document.body != null? document.body.clientHeight : null;
}
var confetList = [];
var conVal;
function doConfet(){
    if (confetList.length > 120) return;
    for (i = 0; i < 40; ++i) {
        var img = document.createElement("IMG");
        img.className = "confetti";

        img.curY = posTop() + pageHeight() - random(50,250);
        if (random(1,100)<50) {
            img.curX = Number(document.body.offsetWidth);
            img.velocityX = random(-24,-12);
        } else {
            img.curX = -20;
            img.velocityX = random(12,24);
        }

        img.velocityY = random(-24,-12);
        img.dragX = 0.08;
        img.accelerationX = 0;
        img.accelerationY = 0.8;

        img.style.left = img.curX+"px";
        img.style.top = img.curY+"350px";
        img.src = "/site/images/confetti/confetti"+random(1,11)+".png";
        confetList.push(img);
        document.body.appendChild(img);
    }
    if (conVal == null) conVal=setInterval(function(){onConfet()},35);
}
function onConfet() {
    for(i = confetList.length-1; i >= 0; --i) {
        var curConfet = confetList[i];
        curConfet.curX += curConfet.velocityX;
        curConfet.curY += curConfet.velocityY;
        curConfet.velocityX += curConfet.accelerationX;
        curConfet.velocityY += curConfet.accelerationY;

        if (curConfet.velocityX > 0) {
            curConfet.velocityX -= curConfet.dragX;
            if (curConfet.velocityX < 0) curConfet.velocityX = 0;
        }
        else if (curConfet.velocityX < 0) {
            curConfet.velocityX += curConfet.dragX;
            if (curConfet.velocityX > 0) curConfet.velocityX = 0;
        }

        if (curConfet.curY >= Number($('content').offsetHeight) ) {
            document.body.removeChild(curConfet);
            confetList.splice(i,1);
        }
        else {
            curConfet.style.left = curConfet.curX+"px";
            curConfet.style.top = curConfet.curY+"px";
        }
    }
    if (confetList.length == 0) {
        window.clearInterval(conVal);
        conVal = null;
    }
}
function dBtn(e) {
    var code = (e.keyCode ? e.keyCode : e.which);
    if (code == 37 || code == 100) {
        var div = $('prevPage');
        if (div != null) location.href = div.href;
    }
    else if (code == 39 || code == 102) {
        var div = $('nextPage');
        if (div != null) location.href = div.href;
    }
}
function sbReg(e) {
    var code = (e.keyCode ? e.keyCode : e.which);
    if(code == 10 || code == 13) {
        $('regInp').click();
        return false;
    }
    return true;
}
function shPop(inp,call) {
    var pop = $("popup");
    pop.style.display="block";
    var indiv = $("popupInputs");
    indiv.innerHTML = "";
    var nInp;
    for (var i = 0; i < inp.length; ++i) {
        nInp = document.createElement("input");
        indiv.appendChild(document.createTextNode(inp[i]+": "));
        indiv.appendChild(nInp);
        if (i == 0) nInp.select();
        indiv.appendChild(document.createElement("br"));
    }
    $("popupContent").style.height = (indiv.offsetHeight + 75) + "px";
    $("togglePopup").onclick = function(){call();pop.style.display="none";};
}
function adLst(ele,temp) {
    var inps = $("popupInputs").getElementsByTagName("input");
    var val = [];
    for (var i = 0; i < inps.length; ++i) {
        temp = temp.replace("%"+i+"%",inps[i].value);
    }
    ele.innerHTML += temp;
    console.log("adLst "+temp);
    inps = ele.getElementsByClassName("editshow");
    for (i = 0; i < inps.length; ++i) {
        inps[i].style.display="inline";
    }
	inps = ele.getElementsByClassName("edithide");
    for (i = 0; i < inps.length; ++i) {
        inps[i].style.display="none";
    }
    document.dirty=true;
    try {
		onListChange();
	} catch (e) { }
}
function reLst(ele,par) {
    par.removeChild(ele);
    document.dirty=true;
    try {
		onListChange();
	} catch (e) { }
    return true;
}
function adjustFormHeight(el, minHeight) {
    var outerHeight = parseInt(window.getComputedStyle(el).height, 10);
    var diff = outerHeight - el.clientHeight;
    diff = 0;
    el.style.height = 0;
    el.style.height = Math.max(minHeight, el.scrollHeight + diff) + 'px';
}
function startFormEdits(bt,inp,pag,ttl,nPag,call) {
    bt.value = "Save";
    document.dirty = false;
    bt.onclick = function() {
        endFormEdits(this,inp,pag,ttl,nPag,call);
    };
    var h,w;
    var itm = $('content').getElementsByTagName("*");
    var reg = /val-?([0-9]+)/i;
    var chk = /check([0-9]+)/i;
    let tbreg = /tblCol([0-9]+)_([0-9]+)/i;
    for (var i = itm.length-1; i >= 0; --i) {
        if (itm[i].className.contains("editshow")) {
            itm[i].style.display="inline";
        } else if (itm[i].className.contains("edithide")) {
            itm[i].style.display="none";
        }
        if(itm[i].id.match(reg)) {
            var style = window.getComputedStyle(itm[i], null);
            itm[i].innerHTML = "<textarea style='line-height:13px;border:0;margin:0;padding:0;'>"+itm[i].innerHTML.replace(/<br[^>]*>/gi, "\n")+"</textarea>";
            itm[i].firstChild.onblur = function(){document.dirty=true;}
            itm[i].firstChild.onpaste=function(e){
                var pasTxt=this;
                setTimeout(function() {
                    pasTxt.value = pasTxt.value.replace(/ \+([0-9]+)\b/g, ' [+$1]');
                    pasTxt.value = pasTxt.value.replace(/([\[]+)?([0-9]+)?d([0-9]+) \+ ([0-9]+)([\]]+)?/g, '$2d$3+$4');
                    pasTxt.value = pasTxt.value.replace(/([\[]+)?([0-9]+)?d([0-9]+)(\+)?([0-9]+)?([\]]+)?/g, '[$2d$3$4$5]');
                }, 4);

			    console.log(this.value);
            };
            adjustFormHeight(itm[i].firstChild,20);
			if (itm[i].className.includes("autocomplete")) {
				itm[i].firstChild.onfocus = function(){shwAutoCmp(this,true);}
				itm[i].firstChild.onblur = function(){shwAutoCmp(this,false);document.dirty=true;}
			}
			if (itm[i].className.includes("updstats")) {
				itm[i].firstChild.oninput = function(){updStats();}
			}
        }
        else if (itm[i].id.match(chk)) {
            itm[i].disabled = "";
        }
        else if (itm[i].id.match(tbreg)) {
            itm[i].innerHTML = "<input style='line-height:13px;border:0;margin:0;padding:0;' value='"+itm[i].innerHTML+"'/>";
            itm[i].firstChild.onblur = function(){document.dirty=true;}
        }
    }
    try {
    	formEditExtra(true);
    } catch { }

}
function endFormEdits(bt,inp,pag,ttl,nPag,call) {
    bt.value = "Edit";
    bt.onclick = function() {
      startFormEdits(this,inp,pag,ttl,nPag,call);
    };
    var itm = $('content').getElementsByTagName("*");
    var reg = /val-?([0-9]+)/i;
    var chk = /check([0-9]+)/i;
    let tbreg = /tblCol([0-9]+)_([0-9]+)/i;
    for (var i = itm.length-1; i >= 0; --i) {
        if(itm[i].id.match(reg)) {
            itm[i].innerHTML = itm[i].getElementsByTagName("textarea")[0].value.replace(/(?:\r\n|\r|\n)/g, '<br />');
        }
        else if (itm[i].id.match(chk)) {
            itm[i].disabled = "disabled";
        }
        else if (itm[i].id.match(tbreg)) {
            itm[i].innerHTML = itm[i].getElementsByTagName("input")[0].value.replace(/(?:\r\n|\r|\n)/g, '<br />');
        }
        if (itm[i].className.contains("editshow")) {
            itm[i].style.display="none";
        } else if (itm[i].className.contains("edithide")) {
            itm[i].style.display="";
        }
    }
    if (document.dirty) {
        if (call != null) call();
        saveForm(inp,pag,ttl,nPag);
    }
	try {
		formEditExtra(false);
	} catch { }
}
function saveForm(inp,pag,ttl,nPag) {
    var it = $('content').getElementsByTagName("*");
    var val = /val-?([0-9]+)/i;
    var chk = /check([0-9]+)/i;
    var lst = /list([0-9]+)/i;
    let tbreg = /tblCol([0-9]+)_([0-9]+)/i;
    var dt1=[],dt2=[],dt3=[],dt4=[];
    for (var i = it.length-1,n; i >= 0; --i) {
        if((n = val.exec(it[i].id)) != null) {
            dt1[n[1]]=''+it[i].innerHTML;
        }
        else if ((n = chk.exec(it[i].id)) != null) {
            dt2[n[1]]=it[i].checked;
        }
        else if ((n = tbreg.exec(it[i].id)) != null) {
            console.log(it[i].innerHTML+" ;;; "+inp+" ;;; "+n);
            if (!Array.isArray(dt4[n[1]]) ) dt4[n[1]] = [];
            dt4[n[1]][n[2]] = it[i].innerHTML;
        }
        else if ((n = lst.exec(it[i].id)) != null)  {
            var li = [];
            for (var r = 0,row,re; row = it[i].rows[r]; ++r) {
                console.log(row.innerHTML+" ;;; "+r);
                var nl = [];
                while ((re = inp.exec(row.innerHTML)) != null) {
                     console.log(re);
                     nl.push(''+re[1]);
                }
                li.push(nl);
            }
            dt3[n[1]]=li;
        }
    }
    var ret = dt1.concat(dt2,dt3);
    console.log(dt4);
    ret.push(dt4);
    console.log(ret);
    var nTtl = "";
    if (ttl!=null&&ttl.length>0) for(i=0;i<ttl.length;++i) {
        if (typeof ttl[i] == 'string' || ttl[i] instanceof String) nTtl += ttl[i] + " ";
        else nTtl += ret[ttl[i]] + " ";
    }
    var isPublic = 1;
    var isOfficial = 0;
    let isSubmit = 0;
    try { if (!$('public').checked) isPublic = 0; } catch(err1) { }
    try { if ($('submitbrew').checked) isSubmit = 1; } catch(err1) { }
    try { if ($('official').checked) isOfficial = 1; } catch(err2) { }
    console.log("dat: "+encodeURIComponent(JSON.stringify(json_encode(ret))));
    if (pag != null) aP(pag, "frames=false&submitbrew="+isSubmit+"&public="+isPublic+"&official="+isOfficial+"&save="+encodeURIComponent(JSON.stringify(json_encode(ret)))+"&title="+encodeURIComponent(JSON.stringify(json_encode(nTtl))), onSaveForm, [nTtl,nPag]);
    else alert(ret+" /// "+nTtl+" /// "+nPag);
}
function onSaveForm(a,b) {
  if (a.substring(2,7)==="error" || a.startsWith("error")) {
		alert(a);
		return;
	}
	console.log(a + " /// "+a.substring(2,7));
    var newURL = b[1]+a+"/"+slug(b[0])+"/";
    /*if (history.pushState) {
        window.history.pushState("form_save", b[0], newURL);
        document.title = b[0];
        var s = $('charLoadSel');
        var fn = false;
        for (var i = 0,ar; i < s.length; ++i) {
            ar = s.options[i].value.split("/");
            if (ar[0]==a) {
                fn = true;
                s.options[i].value = a+"/"+slug(b[0])+"/";
                s.options[i].text = b[0];
            }
        }
        if (!fn) {
            ar = document.createElement("option");
            ar.value = a+"/"+slug(b[0])+"/";
            ar.text = b[0];
            s.add(ar);
            $('campaignSelForm').style.display = "";
        }
    }
    else*/ window.location.href = newURL;
}
function pointbuy(v) {
    v = $(v).innerHTML;
    if (v > 15 || v < 8) return -99;
    if (v == 15) return 9;
    else if (v == 14) return 7;
    return v - 8;
}
function slug(input)
{
    return input
        .replace(/^\s\s*/, '')
        .replace(/\s\s*$/, '')
        .toLowerCase()
        .replace(/[^a-z0-9_\-~!\+\s]+/g, '')
        .replace(/[\s]+/g, '-');
}
function getPosNum(num)
{
    if(num >= 0){
        return "+" + num;
    }else{
        return num.toString();
    }
}
function setModChg(ele,chg) {
    $(ele).innerHTML = getPosNum(parseInt($(ele).innerHTML)+chg);
}
function chRolStat() {
    var r1 = Math.ceil(Math.random()*6);
    var r2 = Math.ceil(Math.random()*6);
    var r3 = Math.ceil(Math.random()*6);
    var r4 = Math.ceil(Math.random()*6);
    $('val7').firstChild.value = r1+r2+r3+r4-Math.min(r1,r2,r3,r4);
    r1 = Math.ceil(Math.random()*6);
    r2 = Math.ceil(Math.random()*6);
    r3 = Math.ceil(Math.random()*6);
    r4 = Math.ceil(Math.random()*6);
    $('val53').firstChild.value = r1+r2+r3+r4-Math.min(r1,r2,r3,r4);
    r1 = Math.ceil(Math.random()*6);
    r2 = Math.ceil(Math.random()*6);
    r3 = Math.ceil(Math.random()*6);
    r4 = Math.ceil(Math.random()*6);
    $('val8').firstChild.value = r1+r2+r3+r4-Math.min(r1,r2,r3,r4);
    r1 = Math.ceil(Math.random()*6);
    r2 = Math.ceil(Math.random()*6);
    r3 = Math.ceil(Math.random()*6);
    r4 = Math.ceil(Math.random()*6);
    $('val9').firstChild.value = r1+r2+r3+r4-Math.min(r1,r2,r3,r4);
    r1 = Math.ceil(Math.random()*6);
    r2 = Math.ceil(Math.random()*6);
    r3 = Math.ceil(Math.random()*6);
    r4 = Math.ceil(Math.random()*6);
    $('val10').firstChild.value = r1+r2+r3+r4-Math.min(r1,r2,r3,r4);
    r1 = Math.ceil(Math.random()*6);
    r2 = Math.ceil(Math.random()*6);
    r3 = Math.ceil(Math.random()*6);
    r4 = Math.ceil(Math.random()*6);
    $('val11').firstChild.value = r1+r2+r3+r4-Math.min(r1,r2,r3,r4);
    document.dirty=true;
    return true;
}
function onCharSave() {
    var bas = -5;
    var strChg = (parseInt(($('val7').innerHTML) / 2) + bas) - strBonus;
    var dexChg = (parseInt(($('val53').innerHTML) / 2) + bas) - dexBonus;
    var conChg = (parseInt(($('val8').innerHTML) / 2) + bas) - conBonus;
    var intChg = (parseInt(($('val9').innerHTML) / 2) + bas) - intBonus;
    var wisChg = (parseInt(($('val10').innerHTML) / 2) + bas) - wisBonus;
    var chaChg = (parseInt(($('val11').innerHTML) / 2) + bas) - chaBonus;

    strBonus += strChg;
    dexBonus += dexChg;
    conBonus += conChg;
    intBonus += intChg;
    wisBonus += wisChg;
    chaBonus += chaChg;
    $('strBonus').innerHTML = getPosNum(strBonus);
    $('dexBonus').innerHTML = getPosNum(dexBonus);
    $('conBonus').innerHTML = getPosNum(conBonus);
    $('intBonus').innerHTML = getPosNum(intBonus);
    $('wisBonus').innerHTML = getPosNum(wisBonus);
    $('chaBonus').innerHTML = getPosNum(chaBonus);

    var p = pointbuy('val7')+pointbuy('val53')+pointbuy('val8')+pointbuy('val9')+pointbuy('val10')+pointbuy('val11');
    var pdv = $('character_pointbuy');
    if (p < 0) pdv.innerHTML = "No";
    else pdv.innerHTML = p;
}
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires + "; path=/";
}
function hovCel(td) {
    if (MouseDown) selCel(td);
    else {
        initial=-1;
        inX=-1;
        inY=-1;
        $('selector_box').style.display="";
        $('selector_box').onmousemove=null;
    }
}
var initial=-1;
var inX=-1;
var inY=-1;
function selCel(td,skp) {
    if (initial==-1) {
        if (td.selected) initial=0;
        else initial=1;
        inX = mX;
        inY = mY;
    }
    if (initial==0) {
        td.selected=false;
        td.style.backgroundColor="";
    }else{
        td.selected=true;
        td.style.backgroundColor="#0f0";
    }

    if (!skp&&(inX!=mX||inY!=mY)) {
        window.getSelection().removeAllRanges();
        var tbl=td.parentNode.parentNode.parentNode;
        $('selector_box').onmousemove=function(){sizeSel(tbl);}
        sizeSel(tbl);
    }
}
function sizeSel(tbl){
    var stX=inX,enX=mX,stY=inY,enY=mY;
    if (mX<inX){
        stX=mX;
        enX=inX;
    }
    if (mY<inY){
        stY=mY;
        enY=inY
    }
    var b=$('selector_box');
    var wi=(enX-stX);
    var he=(enY-stY);
    b.style.display="block";
    b.style.left=stX+"px";
    b.style.width=wi+"px";
    b.style.top=stY+"px";
    b.style.height=he+"px";
    var re=b.getBoundingClientRect();
    for (var r=1;r < tbl.rows.length;++r){
        for (var c=0;c < tbl.rows[r].cells.length;++c){
            var cell = tbl.rows[r].cells[c];
            var p=cell.getBoundingClientRect();
            if (re.left-p.width<=p.left&&re.right+p.width>=p.right&&re.top-p.height<=p.top&&re.bottom+p.height>=p.bottom){
                selCel(cell,true);
            }
        }
    }
}
function subDates(pag){
    var tbl=$('timeSelect');
    var ret=[$('DropDownTimezone').selectedIndex,$('whenName').value];
    for (var r=0;r < tbl.rows.length;++r){
        for (var c=0;c < tbl.rows[r].cells.length;++c){
            var cell = tbl.rows[r].cells[c];
            ret.push(cell.selected);
        }
    }
    aP(pag, "frames=false&save="+encodeURIComponent(JSON.stringify(json_encode(ret))), onSubDate, pag);
    return true;
}
function onSubDate(a,b) {
    window.location.href = b+a+"/";
}
