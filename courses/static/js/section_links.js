function persistingHover(){
    let parent = document.querySelector(".section-links")
    let links = Array.from(parent.children) //includes the random pipe before last link
    links.splice(3, 1) //removes pipe

    links.forEach(link => {
        link.addEventListener("mouseover", (event) => {
            for (let i=0; i < links.length; i++) {
                if (links[i] !== event.target){
                     links[i].classList.remove("active-link");
                }
                else {
                    links[i].classList.add("active-link");
                }
            }
        })
    })
}


window.addEventListener("load", (event) => {
    persistingHover();
})