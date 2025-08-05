// batch_detail.js

document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".nav-link");
    const contents = document.querySelectorAll(".tab-pane");

    tabs.forEach((tab) => {
        tab.addEventListener("click", function (e) {
            e.preventDefault();

            // Remove active class from all tabs and content
            tabs.forEach((t) => t.classList.remove("active"));
            contents.forEach((c) => c.classList.remove("show", "active"));

            // Add active class to clicked tab
            tab.classList.add("active");

            // Show corresponding content
            const targetId = tab.getAttribute("href");
            const target = document.querySelector(targetId);
            if (target) {
                target.classList.add("show", "active");
            }
        });
    });
});
