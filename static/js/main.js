"use strict";


/* =========================================================
   DOM READY
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initHomeCounters();

        initStatCards();

        initFeatureSlider();

        initHomeReveal();

        initImageProtection();

    }
);


/* =========================================================
   NUMBER COUNTERS
========================================================= */

function initHomeCounters() {

    const counters =
        document.querySelectorAll(
            "[data-count]"
        );


    counters.forEach(counter => {

        const target =
            Number(
                counter.dataset.count
            );


        if (!Number.isFinite(target)) {
            return;
        }


        const duration = 1000;

        const start =
            performance.now();


        function animate(now) {

            const progress =
                Math.min(
                    (now - start) /
                    duration,
                    1
                );


            const eased =
                1 -
                Math.pow(
                    1 - progress,
                    3
                );


            const value =
                target * eased;


            counter.textContent =
                Math.round(
                    value
                ).toLocaleString(
                    "en-IN"
                );


            if (progress < 1) {

                requestAnimationFrame(
                    animate
                );

            }

        }


        requestAnimationFrame(
            animate
        );

    });

}


/* =========================================================
   STAT CARD ACTIVE COLOR
========================================================= */

function initStatCards() {

    const cards =
        document.querySelectorAll(
            "[data-stat-card]"
        );


    if (!cards.length) {
        return;
    }


    cards.forEach(card => {

        card.addEventListener(
            "click",
            () => {

                cards.forEach(
                    item => {

                        item.classList.remove(
                            "active"
                        );

                    }
                );


                card.classList.add(
                    "active"
                );

            }
        );

    });

}


/* =========================================================
   FEATURE SLIDER
========================================================= */

function initFeatureSlider() {

    const cards =
        Array.from(
            document.querySelectorAll(
                "[data-feature-card]"
            )
        );


    const dots =
        Array.from(
            document.querySelectorAll(
                ".slider-dot"
            )
        );


    const previous =
        document.querySelector(
            ".slider-prev"
        );


    const next =
        document.querySelector(
            ".slider-next"
        );


    if (!cards.length) {
        return;
    }


    let currentIndex = 0;

    let autoSlide = null;


    function showSlide(index) {

        currentIndex =
            (
                index +
                cards.length
            ) %
            cards.length;


        cards.forEach(
            (card, cardIndex) => {

                card.classList.toggle(
                    "feature-active",
                    cardIndex === currentIndex
                );

            }
        );


        dots.forEach(
            (dot, dotIndex) => {

                dot.classList.toggle(
                    "active",
                    dotIndex === currentIndex
                );

            }
        );


        if (
            window.innerWidth <= 600
        ) {

            const activeCard =
                cards[currentIndex];


            if (activeCard) {

                activeCard.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest"
                });

            }

        }

    }


    function nextSlide() {

        showSlide(
            currentIndex + 1
        );

    }


    function previousSlide() {

        showSlide(
            currentIndex - 1
        );

    }


    if (next) {

        next.addEventListener(
            "click",
            nextSlide
        );

    }


    if (previous) {

        previous.addEventListener(
            "click",
            previousSlide
        );

    }


    dots.forEach(
        (dot, index) => {

            dot.addEventListener(
                "click",
                () => {

                    showSlide(
                        index
                    );

                    restartAutoSlide();

                }
            );

        }
    );


    cards.forEach(
        (card, index) => {

            card.addEventListener(
                "click",
                event => {

                    /*
                     * Don't hijack actual
                     * links/buttons.
                     */

                    if (
                        event.target.closest(
                            "a"
                        )
                    ) {
                        return;
                    }


                    showSlide(
                        index
                    );

                    restartAutoSlide();

                }
            );

        }
    );


    function startAutoSlide() {

        autoSlide =
            setInterval(
                nextSlide,
                4500
            );

    }


    function restartAutoSlide() {

        clearInterval(
            autoSlide
        );

        startAutoSlide();

    }


    showSlide(0);

    startAutoSlide();


    const slider =
        document.querySelector(
            ".feature-slider"
        );


    if (slider) {

        slider.addEventListener(
            "mouseenter",
            () => {

                clearInterval(
                    autoSlide
                );

            }
        );


        slider.addEventListener(
            "mouseleave",
            () => {

                startAutoSlide();

            }
        );

    }

}


/* =========================================================
   SCROLL REVEAL
========================================================= */

function initHomeReveal() {

    const elements =
        document.querySelectorAll(
            ".home-stats .stat-card, " +
            ".feature-card, " +
            ".preview-section, " +
            ".engine-section, " +
            ".developer-section"
        );


    if (!elements.length) {
        return;
    }


    elements.forEach(
        element => {

            element.classList.add(
                "home-reveal"
            );

        }
    );


    if (
        !("IntersectionObserver" in window)
    ) {

        elements.forEach(
            element => {

                element.classList.add(
                    "home-reveal-visible"
                );

            }
        );

        return;

    }


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(
                    entry => {

                        if (
                            entry.isIntersecting
                        ) {

                            entry.target.classList.add(
                                "home-reveal-visible"
                            );


                            observer.unobserve(
                                entry.target
                            );

                        }

                    }
                );

            },
            {
                threshold: 0.12
            }
        );


    elements.forEach(
        element => {

            observer.observe(
                element
            );

        }
    );

}


/* =========================================================
   IMAGE ERROR PROTECTION
========================================================= */

function initImageProtection() {

    const images =
        document.querySelectorAll(
            ".home-page img"
        );


    images.forEach(
        image => {

            image.addEventListener(
                "error",
                () => {

                    image.classList.add(
                        "image-error"
                    );

                }
            );

        }
    );

}


/* =========================================================
   PAGE VISIBILITY
========================================================= */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            document.visibilityState ===
            "hidden"
        ) {

            return;

        }

    }
);