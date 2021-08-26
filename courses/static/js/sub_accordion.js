function toggleAccordion(subAccordion){
    let expand = document.getElementById(subAccordion + "-expand")
    let collapse = document.getElementById(subAccordion + "-collapse")
    const items = document.getElementsByClassName("accordion-body")

    expand.classList.toggle("hidden")
    collapse.classList.toggle("hidden")

    for(let i=0; i < items.length; i++){
        const accordionBody = document.getElementById(subAccordion + i)
        if(accordionBody){
            accordionBody.classList.toggle("hidden")
        }
    }
}