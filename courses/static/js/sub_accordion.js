function toggleAccordion(subAccordion){
    var expand = document.getElementById(subAccordion + "-expand")
    var collapse = document.getElementById(subAccordion + "-collapse")

    expand.classList.toggle("hidden")
    collapse.classList.toggle("hidden")

    for(var i=0; i<=4; i++){
        var accordionBody = document.getElementById(subAccordion + i)
        if(accordionBody){
            accordionBody.classList.toggle("hidden")
        }
    }
}