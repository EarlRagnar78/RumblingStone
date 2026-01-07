
var	totalOffset = 100;

function getGlobalOffsets(anElement)
{
    var theElement;

    var totalLeftOffset;
    var totalTopOffset;

    var widthOffset;
    var heightOffset;

    totalLeftOffset = 0;
    totalTopOffset = 0;

    widthOffset = 0;
    heightOffset = 0;

    //  Traverse up the *offset* parent chain of anElement
    theElement = anElement;
    while (theElement != null)
    {
        totalLeftOffset += theElement.offsetLeft;
        totalTopOffset += theElement.offsetTop;

        if (widthOffset == 0)
        {
            widthOffset = theElement.offsetWidth;
        };

        if (heightOffset == 0)
        {
            heightOffset = theElement.offsetHeight;
        };

        theElement = theElement.offsetParent;
    };

    return [totalLeftOffset, totalTopOffset, widthOffset, heightOffset];
};

function scrollToAnchor(linkElem)
{
	var	globalOffsets;
	
	globalOffsets = getGlobalOffsets(linkElem);

	//  If the body doesn't have any value here, that means we're
	//  running in strict mode, which means we need to tweak the
	//  documentElement's scrollTop, not the body's.
	if (document.body.scrollTop == 0)
	{
		document.documentElement.scrollTop = globalOffsets[1] - totalOffset;
	}
	else
	{
		document.body.scrollTop = globalOffsets[1] - totalOffset;
	};
};

function setupPage()
{
	if (navigator.userAgent.indexOf("Opera") != -1)
	{
		// Don't return... Opera will do the right thing here. It's just
		// that Opera also has a 'document.all' property and we need to
		// distinguish between the two.
	}
	else if (document.all)
	{
		//  We're on IE... return now, as IE doesn't do anything here.
		return;
	};

	prepLinks();
	scrollOnLoad();
};

function scrollOnLoad()
{
	var	windowURL;

	var	fragmentIndex;
	
	var	anchorID;
	var	anchorElement;

	windowURL = window.location.toString();

	//	If the windows location URL contains a '#', then we scroll the
	//	top down by 100 pixels from the name of the anchor.
	if ((fragmentIndex = windowURL.indexOf('#')) != -1)
	{
		anchorID = windowURL.slice(fragmentIndex + 1);

		if (anchorElement = document.getElementById(anchorID))
		{
			scrollToAnchor(anchorElement);
		};
	};
};

function prepLinks()
{
	var	linkElems;
	var	i;

	var	fragmentIndex;

	var	anchorID;
	var	anchorElement;

	linkElems = document.getElementsByTagName('a');
	
	for (i = 0; i < linkElems.length; i++)
	{
		if ((fragmentIndex = linkElems[i].getAttribute('href').indexOf('#')) != -1)
		{
			anchorID = linkElems[i].getAttribute('href').slice(fragmentIndex + 1);

			if (anchorElement = document.getElementById(anchorID))
			{
				linkElems[i].onclick = function ()
					{
						//	Capture the anchor in a local
						//	variable to form a closure.
						var	theAnchorElem;
							
						theAnchorElem = this.ourAnchor;
						setTimeout(
							function ()
							{
								scrollToAnchor(theAnchorElem);
							},100);
					};
				linkElems[i].ourAnchor = anchorElement;
			};
		};
	};
};
