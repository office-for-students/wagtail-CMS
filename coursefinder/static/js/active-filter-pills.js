function closeAllInstitutions(){
    $('.inst-chk').prop('checked', false);
    $('.filters-block__form').first().submit();
}

function closeFilter(filter) {  
    document.getElementById(filter).checked = false;
    document.getElementById("filterForm").submit();
}