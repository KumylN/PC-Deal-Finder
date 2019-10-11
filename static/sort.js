function changePage(page) {

}

function makePagination(len) {
    var paginationIndex = document.getElementById('paginationIndex');
    console.log(len);
    for (var i = 1; (i < Math.floor(len / 50) + 2); i++) {
        console.log("Running pagination...")
        var page = document.createElement("a");
        var textNode = document.createTextNode(String(i));
        page.appendChild(textNode);
        page.setAttribute("onclick", "changePage(" + String(i) + ")");
        paginationIndex.appendChild(page);
        console.log("SUCCESS")
    }
}

function sortFunction(pageMin=0) {
    var elements = document.getElementsByClassName('deal');

    if (elements.length === 0) {
        document.getElementById('deals-list').style.display = "block";
        document.getElementById("NoSearchResults").className += " noSearch";
        return
    }

    makePagination(elements.length);

    var array = [];
    for (var i = elements.length >>> 0; i--;) {
        array[i] = elements[i];
    }

    // perform sort
    array.sort(function(a, b) {
    return Number(a.getElementsByClassName("deal-price")[0].innerText) - Number(b.getElementsByClassName("deal-price")[0].innerText);      
    });

    // join the array back into HTML
    var output = "";
    for (var i = 0; i < array.length; i++) { 
        output += array[i].outerHTML;
    }

    // append output to div 
    document.getElementById('deals-list').innerHTML = output;
    document.getElementById('deals-list').style.display = "block";
    }