window.addEventListener("load", () => {
    if (document.referrer.indexOf(location.protocol + "//" + location.host) !== 0) {
        $('#discover-modal').modal('show');
    }
})