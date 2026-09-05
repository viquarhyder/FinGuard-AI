/* =========================================================
   FINGUARD AI
   404 Error Page JavaScript
   ========================================================= */

"use strict";


document.addEventListener("DOMContentLoaded", () => {

    init404Page();
    init404Keyboard();
    init404Buttons();

});


/* =========================================================
   PAGE INITIALIZATION
   ========================================================= */

function init404Page() {

    const container =
        document.querySelector(
            ".fg404-container"
        );

    if (!container) {
        return;
    }


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (reducedMotion) {
        return;
    }


    container.style.opacity = "0";
    container.style.transform =
        "translateY(12px) scale(.99)";


    requestAnimationFrame(() => {

        container.style.transition =
            "opacity .5s ease, transform .5s ease";

        container.style.opacity = "1";
        container.style.transform =
            "translateY(0) scale(1)";

    });

}


/* =========================================================
   KEYBOARD SHORTCUTS
   H = HOME
   D = DASHBOARD
   ESC = BACK
   ========================================================= */

function init404Keyboard() {

    document.addEventListener(
        "keydown",
        event => {

            const target =
                event.target;

            if (
                target &&
                (
                    target.tagName === "INPUT" ||
                    target.tagName === "TEXTAREA" ||
                    target.isContentEditable
                )
            ) {
                return;
            }


            if (
                event.key.toLowerCase() === "h"
            ) {

                const home =
                    document.querySelector(
                        ".fg404-primary"
                    );

                if (home) {
                    home.click();
                }

            }


            if (
                event.key.toLowerCase() === "d"
            ) {

                const dashboard =
                    document.querySelector(
                        ".fg404-secondary"
                    );

                if (dashboard) {
                    dashboard.click();
                }

            }


            if (
                event.key === "Escape"
            ) {

                if (
                    window.history.length > 1
                ) {

                    window.history.back();

                }

            }

        }
    );

}


/* =========================================================
   BUTTON INTERACTIONS
   ========================================================= */

function init404Buttons() {

    const buttons =
        document.querySelectorAll(
            ".fg404-primary, .fg404-secondary"
        );


    buttons.forEach(button => {

        button.addEventListener(
            "mousedown",
            () => {

                button.style.transform =
                    "translateY(0) scale(.98)";

            }
        );


        button.addEventListener(
            "mouseup",
            () => {

                button.style.transform = "";

            }
        );


        button.addEventListener(
            "mouseleave",
            () => {

                button.style.transform = "";

            }
        );

    });

}


/* =========================================================
   PUBLIC API
   ========================================================= */

window.FinGuard404 = {

    goBack() {

        if (window.history.length > 1) {
            window.history.back();
        }

    }

};