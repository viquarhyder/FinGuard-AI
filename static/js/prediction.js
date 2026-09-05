/* =========================================================
   FINGUARD AI
   PREMIUM PREDICTION ENGINE
   ========================================================= */

"use strict";


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initQuickAmounts();
        initPredictionForm();
        initRiskGauge();
        initProbability();
        initNumberAnimations();
        initHelpButtons();
        initAdvancedState();

    }
);



/* =========================================================
   QUICK AMOUNT
   ========================================================= */

function initQuickAmounts() {

    const buttons =
        document.querySelectorAll(
            "[data-amount]"
        );


    const amountInput =
        document.querySelector(
            "[data-core-amount]"
        );


    if (
        !buttons.length ||
        !amountInput
    ) {
        return;
    }


    buttons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const amount =
                    button.dataset.amount;


                amountInput.value =
                    amount;


                buttons.forEach(item => {

                    item.classList.remove(
                        "active"
                    );

                });


                button.classList.add(
                    "active"
                );


                amountInput.dispatchEvent(
                    new Event(
                        "input",
                        {
                            bubbles: true
                        }
                    )
                );


                amountInput.focus();

            }
        );

    });

}



/* =========================================================
   FORM
   ========================================================= */

function initPredictionForm() {

    const form =
        document.querySelector(
            ".fg-prediction-form"
        );


    const button =
        document.querySelector(
            ".fg-analyze-button"
        );


    if (
        !form ||
        !button
    ) {
        return;
    }


    form.addEventListener(
        "submit",
        event => {

            if (
                button.disabled
            ) {
                event.preventDefault();
                return;
            }


            button.classList.add(
                "loading"
            );


            button.innerHTML = `
                <span class="fg-spinner"></span>

                <span class="fg-button-text">
                    <strong>Analyzing Transaction...</strong>
                    <small>FinGuard AI Security Engine is processing</small>
                </span>
            `;

        }
    );


    const inputs =
        form.querySelectorAll(
            "input[type='number']"
        );


    inputs.forEach(input => {

        input.addEventListener(
            "input",
            () => {

                input.style.borderColor =
                    "";

            }
        );

    });

}



/* =========================================================
   RISK GAUGE
   ========================================================= */

function initRiskGauge() {

    const gauge =
        document.querySelector(
            ".fg-risk-gauge"
        );


    if (!gauge) {
        return;
    }


    let score =
        Number(
            gauge.dataset.riskScore
        );


    if (
        !Number.isFinite(score)
    ) {
        score = 0;
    }


    score =
        Math.max(
            0,
            Math.min(
                100,
                score
            )
        );


    gauge.style.setProperty(
        "--score",
        "0"
    );


    requestAnimationFrame(
        () => {

            setTimeout(
                () => {

                    gauge.style.setProperty(
                        "--score",
                        score
                    );

                },
                100
            );

        }
    );

}



/* =========================================================
   FRAUD PROBABILITY
   ========================================================= */

function initProbability() {

    const probability =
        document.querySelector(
            "[data-fraud-probability]"
        );


    const bar =
        document.querySelector(
            "[data-probability-fill]"
        );


    if (
        !probability ||
        !bar
    ) {
        return;
    }


    let value =
        Number(
            probability.dataset
                .fraudProbability
        );


    if (
        !Number.isFinite(value)
    ) {
        value = 0;
    }


    value =
        Math.max(
            0,
            Math.min(
                100,
                value
            )
        );


    requestAnimationFrame(
        () => {

            setTimeout(
                () => {

                    bar.style.width =
                        `${value}%`;

                },
                120
            );

        }
    );

}



/* =========================================================
   NUMBER ANIMATION
   ========================================================= */

function initNumberAnimations() {

    const risk =
        document.querySelector(
            ".fg-risk-number"
        );


    if (risk) {

        const gauge =
            document.querySelector(
                ".fg-risk-gauge"
            );


        const target =
            Number(
                gauge?.dataset.riskScore
            );


        if (
            Number.isFinite(target)
        ) {

            animateNumber(
                risk,
                0,
                target,
                700,
                0
            );

        }

    }


    const probability =
        document.querySelector(
            "[data-fraud-probability]"
        );


    if (probability) {

        const target =
            Number(
                probability.dataset
                    .fraudProbability
            );


        if (
            Number.isFinite(target)
        ) {

            animateNumber(
                probability,
                0,
                target,
                800,
                2,
                "%"
            );

        }

    }

}



/* =========================================================
   NUMBER ENGINE
   ========================================================= */

function animateNumber(
    element,
    start,
    end,
    duration,
    decimals = 0,
    suffix = ""
) {

    if (
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    ) {

        element.textContent =
            end.toFixed(decimals) +
            suffix;

        return;

    }


    const started =
        performance.now();


    function frame(now) {

        const elapsed =
            now - started;


        const progress =
            Math.min(
                elapsed / duration,
                1
            );


        const eased =
            1 -
            Math.pow(
                1 - progress,
                3
            );


        const value =
            start +
            (
                end - start
            ) * eased;


        element.textContent =
            value.toFixed(decimals) +
            suffix;


        if (
            progress < 1
        ) {

            requestAnimationFrame(
                frame
            );

        }

    }


    requestAnimationFrame(
        frame
    );

}



/* =========================================================
   HELP TOOLTIP
   ========================================================= */

function initHelpButtons() {

    const buttons =
        document.querySelectorAll(
            "[data-help]"
        );


    buttons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const message =
                    button.dataset.help;


                if (!message) {
                    return;
                }


                showHelpMessage(
                    button,
                    message
                );

            }
        );

    });

}



function showHelpMessage(
    button,
    message
) {

    const old =
        document.querySelector(
            ".fg-help-tooltip"
        );


    if (old) {
        old.remove();
    }


    const tooltip =
        document.createElement(
            "div"
        );


    tooltip.className =
        "fg-help-tooltip";


    tooltip.textContent =
        message;


    Object.assign(
        tooltip.style,
        {
            position: "fixed",
            zIndex: "99999",
            maxWidth: "300px",
            padding: "9px 11px",
            borderRadius: "8px",
            background: "#071a3a",
            color: "#ffffff",
            fontSize: "10px",
            lineHeight: "1.45",
            boxShadow:
                "0 10px 30px rgba(15,23,42,.22)"
        }
    );


    document.body.appendChild(
        tooltip
    );


    const rect =
        button.getBoundingClientRect();


    let left =
        rect.left;


    let top =
        rect.bottom + 7;


    if (
        left + 300 >
        window.innerWidth
    ) {

        left =
            window.innerWidth -
            310;

    }


    tooltip.style.left =
        `${Math.max(10, left)}px`;


    tooltip.style.top =
        `${top}px`;


    setTimeout(
        () => {

            tooltip.remove();

        },
        4000
    );

}



/* =========================================================
   ADVANCED INPUT STATE
   ========================================================= */

function initAdvancedState() {

    const advanced =
        document.querySelector(
            "#advancedInputs"
        );


    if (!advanced) {
        return;
    }


    /*
     * Keep advanced fields collapsed
     * initially so the page remains
     * compact and professional.
     */

    advanced.removeAttribute(
        "open"
    );

}



/* =========================================================
   PUBLIC API
   ========================================================= */

window.FinGuardPrediction = {

    refresh() {

        initRiskGauge();
        initProbability();
        initNumberAnimations();

    },

    openAdvanced() {

        const advanced =
            document.querySelector(
                "#advancedInputs"
            );


        if (advanced) {
            advanced.open = true;
        }

    },

    closeAdvanced() {

        const advanced =
            document.querySelector(
                "#advancedInputs"
            );


        if (advanced) {
            advanced.open = false;
        }

    }

};