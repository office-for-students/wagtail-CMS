function closeAllInstitutions(){
    $('.inst-chk').prop('checked', false);
    document.getElementById("sort_by_subject").value = false
    $('.filters-block__form').first().submit();
}

function closeFilter(filter) {
    document.getElementById(filter).checked = false;
    document.getElementById("sort_by_subject").value = false
    document.getElementById("filterForm").submit();
}