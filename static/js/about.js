/* =========================================================
   FINGUARD AI
   ABOUT PAGE — PREMIUM INTERACTIVE ENGINE
   ========================================================= */

"use strict";


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initAboutReveal();
        initPipelineInteractions();
        initCapabilityInteractions();
        initTechnologyInteractions();
        initIntelligenceCards();
        initImageFallbacks();
        respectReducedMotion();

    }
);


/* =========================================================
   REVEAL ANIMATIONS
   ========================================================= */

function initAboutReveal() {

    const elements =
        document.querySelectorAll(
            ".about-hero-content, " +
            ".about-hero-visual, " +
            ".about-intelligence-card, " +
            ".about-panel, " +
            ".about-technology-panel, " +
            ".about-security-card, " +
            ".about-system-status"
        );


    if (!elements.length) {
        return;
    }


    const reduced =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (reduced) {

        elements.forEach(
            element => {

                element.classList.add(
                    "about-visible"
                );

            }
        );

        return;

    }


    elements.forEach(
        (element, index) => {

            element.classList.add(
                "about-reveal"
            );

            element.style.transitionDelay =
                Math.min(
                    index * 45,
                    300
                ) + "ms";

        }
    );


    if (
        "IntersectionObserver" in window
    ) {

        const observer =
            new IntersectionObserver(
                entries => {

                    entries.forEach(
                        entry => {

                            if (
                                !entry.isIntersecting
                            ) {
                                return;
                            }


                            entry.target.classList.add(
                                "about-visible"
                            );


                            observer.unobserve(
                                entry.target
                            );

                        }
                    );

                },
                {
                    threshold: .08,
                    rootMargin:
                        "0px 0px -30px 0px"
                }
            );


        elements.forEach(
            element => {

                observer.observe(
                    element
                );

            }
        );

    } else {

        elements.forEach(
            element => {

                element.classList.add(
                    "about-visible"
                );

            }
        );

    }

}


/* =========================================================
   PIPELINE INTERACTIONS
   ========================================================= */

function initPipelineInteractions() {

    const steps =
        document.querySelectorAll(
            ".pipeline-step"
        );


    if (!steps.length) {
        return;
    }


    steps.forEach(
        step => {

            step.addEventListener(
                "mouseenter",
                () => {

                    activatePipelineStep(
                        step,
                        steps
                    );

                }
            );


            step.addEventListener(
                "focus",
                () => {

                    activatePipelineStep(
                        step,
                        steps
                    );

                }
            );


            step.addEventListener(
                "mouseleave",
                () => {

                    step.classList.remove(
                        "active"
                    );

                }
            );


            step.addEventListener(
                "blur",
                () => {

                    step.classList.remove(
                        "active"
                    );

                }
            );


            step.addEventListener(
                "click",
                () => {

                    steps.forEach(
                        item => {

                            item.classList.remove(
                                "active"
                            );

                        }
                    );


                    step.classList.add(
                        "active"
                    );

                }
            );

        }
    );

}


function activatePipelineStep(
    selected,
    steps
) {

    steps.forEach(
        step => {

            step.classList.remove(
                "active"
            );

        }
    );


    selected.classList.add(
        "active"
    );

}


/* =========================================================
   CAPABILITY INTERACTIONS
   ========================================================= */

function initCapabilityInteractions() {

    const capabilities =
        document.querySelectorAll(
            ".about-capability"
        );


    capabilities.forEach(
        capability => {

            capability.addEventListener(
                "click",
                () => {

                    capabilities.forEach(
                        item => {

                            item.classList.remove(
                                "selected"
                            );

                        }
                    );


                    capability.classList.add(
                        "selected"
                    );

                }
            );


            capability.addEventListener(
                "keydown",
                event => {

                    if (
                        event.key === "Enter" ||
                        event.key === " "
                    ) {

                        event.preventDefault();

                        capability.click();

                    }

                }
            );

        }
    );

}


/* =========================================================
   TECHNOLOGY INTERACTIONS
   ========================================================= */

function initTechnologyInteractions() {

    const technologies =
        document.querySelectorAll(
            ".technology-item"
        );


    technologies.forEach(
        technology => {

            technology.addEventListener(
                "mouseenter",
                () => {

                    technology.classList.add(
                        "tech-active"
                    );

                }
            );


            technology.addEventListener(
                "mouseleave",
                () => {

                    technology.classList.remove(
                        "tech-active"
                    );

                }
            );


            technology.addEventListener(
                "focus",
                () => {

                    technology.classList.add(
                        "tech-active"
                    );

                }
            );


            technology.addEventListener(
                "blur",
                () => {

                    technology.classList.remove(
                        "tech-active"
                    );

                }
            );

        }
    );

}


/* =========================================================
   INTELLIGENCE CARD INTERACTIONS
   ========================================================= */

function initIntelligenceCards() {

    const cards =
        document.querySelectorAll(
            ".about-intelligence-card"
        );


    cards.forEach(
        card => {

            card.addEventListener(
                "mouseenter",
                () => {

                    cards.forEach(
                        item => {

                            if (
                                item !== card
                            ) {

                                item.style.opacity =
                                    ".72";

                            }

                        }
                    );

                }
            );


            card.addEventListener(
                "mouseleave",
                () => {

                    cards.forEach(
                        item => {

                            item.style.opacity =
                                "1";

                        }
                    );

                }
            );

        }
    );

}


/* =========================================================
   IMAGE FALLBACK
   ========================================================= */

function initImageFallbacks() {

    const images =
        document.querySelectorAll(
            ".about-page img"
        );


    images.forEach(
        image => {

            image.addEventListener(
                "error",
                () => {

                    image.style.opacity =
                        "0";

                },
                {
                    once: true
                }
            );

        }
    );

}


/* =========================================================
   REDUCED MOTION
   ========================================================= */

function respectReducedMotion() {

    const reduced =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (reduced) {

        document.documentElement.classList.add(
            "reduce-motion"
        );

    }

}


/* =========================================================
   PUBLIC API
   ========================================================= */

window.FinGuardAbout = {

    refresh() {

        initAboutReveal();
        initPipelineInteractions();
        initCapabilityInteractions();
        initTechnologyInteractions();

    },

    resetPipeline() {

        document
            .querySelectorAll(
                ".pipeline-step"
            )
            .forEach(
                step => {

                    step.classList.remove(
                        "active"
                    );

                }
            );

    }

};