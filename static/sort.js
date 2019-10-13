var searchElements =  [];
var currentEnable = "1";

function changePage(page) {
    var oldPage = document.getElementById("page" + currentEnable);
    currentEnable = String(page);
    oldPage.classList.remove("active");
    
    var newPage = document.getElementById("page" + String(page));
    newPage.classList.add("active");

    var output = "";
    var upper = searchElements.length;
    if ((page * 50) < upper) {
        upper = page * 50;
    }
    for (var i = (page - 1) * 50; i < upper; i++) { 
        output += searchElements[i].outerHTML;
    }

    // append output to div 
    document.getElementById('deals-list').innerHTML = output;
    document.getElementById('deals-list').style.display = "block";
}

function makePagination(len) {
    var paginationIndex = document.getElementById('paginationIndex');
    console.log(len);
    for (var i = 1; (i < Math.floor(len / 50) + 2); i++) {
        var page = document.createElement("a");
        var textNode = document.createTextNode(String(i));
        if (i == 1) {
            page.classList.add("active");
        }
        page.appendChild(textNode);
        page.setAttribute("onclick", "changePage(" + String(i) + ")");
        page.setAttribute("id", "page" + String(i));
        paginationIndex.appendChild(page);
    }
}

function createSearchElements(items) {
    ret = [];

    for (var key in items) {
        if (items.hasOwnProperty(key)) {
            var spanItem = document.createElement("span");
            spanItem.setAttribute("class", "d-block p-2 bg-dark deal")
            
            var ulItem = document.createElement("ul");
            ulItem.setAttribute("class", "list-group");

            var aItem = document.createElement("a");
            aItem.setAttribute("href", items[key]['url']);
            aItem.setAttribute("target", "_blank");

            var divItem = document.createElement("div");
            divItem.setAttribute("class", "colorBg");

            var liItem = document.createElement("li");
            liItem.setAttribute("id", items[key]['uuid']);
            liItem.setAttribute("href", items[key]['url']);

            var bItem = document.createElement("b");
            var textnodeB = document.createTextNode(items[key]['name']);
            bItem.appendChild(textnodeB);

            var br1 = document.createElement("br");

            var label = document.createElement("label");
            var textnodeLabel = document.createTextNode("$" + items[key]['price']);
            label.appendChild(textnodeLabel);

            var divItem2 = document.createElement("div");
            divItem2.setAttribute("class", "deal-price");
            divItem2.setAttribute("style", "display:none");
            var textnodeDiv = document.createTextNode(items[key]['price']);
            divItem2.appendChild(textnodeDiv);

            var br2 = document.createElement("br");

            var textnodeSeller = document.createTextNode(items[key]['seller']);

            var br3 = document.createElement("br");

            var textnodeDate = document.createTextNode(items[key]['date']);

            var br4 = document.createElement("br");

            var textnodeFlair = document.createTextNode(items[key]['flair']);

            liItem.appendChild(bItem);
            liItem.appendChild(br1);
            liItem.appendChild(label);
            liItem.appendChild(divItem2);
            liItem.appendChild(br2);
            liItem.appendChild(textnodeSeller);
            liItem.appendChild(br3);
            liItem.appendChild(textnodeDate);
            liItem.appendChild(br4);
            liItem.appendChild(textnodeFlair);

            divItem.appendChild(liItem);

            aItem.appendChild(divItem);

            ulItem.appendChild(aItem);

            spanItem.appendChild(ulItem);

            ret.push(spanItem);
        }
    }

     // perform sort
    // ret.sort(function(a, b) {
    //     return Number(a.getElementsByClassName("deal-price")[0].innerText) - Number(b.getElementsByClassName("deal-price")[0].innerText);      
    // });
    ret.sort(function(a, b) {
        const first = a.getElementsByClassName("deal-price")[0].innerText;
        const second = b.getElementsByClassName("deal-price")[0].innerText;

        return Number(a.getElementsByClassName("deal-price")[0].innerText) - Number(b.getElementsByClassName("deal-price")[0].innerText);      
    });
    return ret;
}

function initialSort(items) {
    searchElements = createSearchElements(items);
    if (searchElements.length === 0) {
        document.getElementById('deals-list').style.display = "block";
        document.getElementById("NoSearchResults").className += " noSearch";
        return
    }

    makePagination(searchElements.length);

    changePage(1);
    }