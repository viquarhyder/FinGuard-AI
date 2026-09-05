document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("a[href]").forEach(function (link) {
        link.addEventListener("click", function () {
            link.classList.add("is-loading");
        });
    });
});