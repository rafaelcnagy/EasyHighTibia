function filterDate(filter) {
    var all_months = document.getElementsByClassName("all-presences")
    var last_month = document.getElementsByClassName("last-presences")
    if (filter.selectedIndex === 0) {
        for (var i = 0; i < all_months.length; i++) {
            all_months[i].style.display="none";
        }
        for (var i = 0; i < last_month.length; i++) {
            last_month[i].style.display="block";
        }
    }
    else if (filter.selectedIndex === 1) {
        for (var i = 0; i < all_months.length; i++) {
            all_months[i].style.display="block";
        }
        for (var i = 0; i < last_month.length; i++) {
            last_month[i].style.display="none";
        }
    }
}
