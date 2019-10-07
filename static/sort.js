function sortFunction() {
    var elements = document.getElementsByClassName('deal');
    
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