export function setDonuts() {
    let donuts = document.querySelectorAll(".custom-donut")

    for (let donut of donuts) {
        let circularProgress = donut.querySelector(".circular-progress")
        let progressValue = donut.querySelector(".progress-value")
        const progressEndValue = parseInt(progressValue.dataset.percent)

        progressValue.textContent = `${progressEndValue}%`
        circularProgress.style.background = `conic-gradient(#FCD833 ${progressEndValue * 3.6}deg, #ededed 0deg)`
    }
}
