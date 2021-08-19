let lastKnownScrollPosition = 0;
let ticking = false;


function doSomething(last_position){
    console.log("do something, ", lastKnownScrollPosition);
}

document.addEventListener('scroll', function (e) {
    lastKnownScrollPosition = window.scrollY;

    if (!ticking) {
        window.requestAnimationFrame(function () {
            doSomething(lastKnownScrollPosition);
            ticking = false;
        });

        ticking = true;
    }
});