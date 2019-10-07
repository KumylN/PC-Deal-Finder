function searchFunction(l) {
    var element = document.getElementById(l["uuid"]);
    if (l["alert"] == "true") {
        element.classList.toggle("list-group-item-warning");
    }
}

function goToSite(url) {
    window.location = url;
}