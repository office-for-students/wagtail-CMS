function setLanguageSwitcherUrlListener() {
    window.addEventListener("querychange", (e) => {
        const languageButton = document.getElementById("language_select")
        languageButton.href = window.location.search
    })
}

window.addEventListener("load", () => {
    setLanguageSwitcherUrlListener()
})