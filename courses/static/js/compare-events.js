(function ($) {
    function getSavedCourses() {
        return JSON.parse(localStorage.getItem("bookmarkedCourses") || "[]");
    }

    function updateUI() {
        const saved = getSavedCourses();

        document.querySelectorAll(".saved-counter").forEach(counter => {
            counter.textContent = saved.length || "";
            counter.classList.toggle("active", saved.length > 0);
        });
    }

    function init() {
        window.addEventListener("savedForComparison", () => {
            setTimeout(() => {
                updateUI();
            }, 0);
        });
    }


    $(document).on('page:load', init)
    $(init)
})(jQuery)
