/* =========================================================
   FINGUARD AI
   PREMIUM ANALYTICS JAVASCRIPT
   ========================================================= */

"use strict";


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initAnalyticsAnimations();
        initFraudChart();
        initRiskBars();
        initFeatureSearch();
        initAnalyticsTooltips();

    }
);


/* =========================================================
   ENTRY ANIMATION
   ========================================================= */

function initAnalyticsAnimations() {

    const elements =
        document.querySelectorAll(
            ".analytics-kpi, " +
            ".analytics-highlight, " +
            ".analytics-card, " +
            ".analytics-footer"
        );

    if (!elements.length) {
        return;
    }

    if (
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    ) {
        return;
    }

    elements.forEach(
        (element, index) => {

            element.style.opacity = "0";
            element.style.transform =
                "translateY(10px)";

            setTimeout(
                () => {

                    element.style.transition =
                        "opacity .42s ease, " +
                        "transform .42s ease";

                    element.style.opacity = "1";

                    element.style.transform =
                        "translateY(0)";

                },
                50 + index * 45
            );

        }
    );

}


/* =========================================================
   FRAUD DOUGHNUT
   ========================================================= */

function initFraudChart() {

    const canvas =
        document.getElementById(
            "fraudChart"
        );

    if (!canvas) {
        return;
    }

    const ctx =
        canvas.getContext("2d");

    const legitimate =
        readLegendNumber(
            ".legend-legitimate"
        );

    const fraud =
        readLegendNumber(
            ".legend-fraud"
        );

    const total =
        legitimate + fraud || 1;

    const fraudRatio =
        fraud / total;

    const dpr =
        window.devicePixelRatio || 1;

    const size = 190;

    canvas.width =
        size * dpr;

    canvas.height =
        size * dpr;

    canvas.style.width =
        size + "px";

    canvas.style.height =
        size + "px";

    ctx.scale(
        dpr,
        dpr
    );

    const center =
        size / 2;

    const radius = 72;

    const lineWidth = 20;

    let progress = 0;


    function drawChart() {

        ctx.clearRect(
            0,
            0,
            size,
            size
        );


        /* TRACK */

        ctx.beginPath();

        ctx.arc(
            center,
            center,
            radius,
            -Math.PI / 2,
            Math.PI * 1.5
        );

        ctx.lineWidth =
            lineWidth;

        ctx.lineCap =
            "round";

        ctx.strokeStyle =
            "#edf2f7";

        ctx.stroke();


        /* LEGITIMATE */

        const legitimateEnd =
            -Math.PI / 2 +
            (
                1 - fraudRatio
            ) *
            Math.PI *
            2 *
            progress;

        ctx.beginPath();

        ctx.arc(
            center,
            center,
            radius,
            -Math.PI / 2,
            legitimateEnd
        );

        ctx.lineWidth =
            lineWidth;

        ctx.strokeStyle =
            "#2563eb";

        ctx.stroke();


        /* FRAUD */

        const fraudStart =
            legitimateEnd;

        const fraudEnd =
            fraudStart +
            fraudRatio *
            Math.PI *
            2 *
            progress;

        ctx.beginPath();

        ctx.arc(
            center,
            center,
            radius,
            fraudStart,
            fraudEnd
        );

        ctx.lineWidth =
            lineWidth;

        ctx.strokeStyle =
            "#ef4444";

        ctx.stroke();


        if (progress < 1) {

            progress += .025;

            requestAnimationFrame(
                drawChart
            );

        }

    }


    drawChart();

}


/* =========================================================
   READ LEGEND NUMBER
   ========================================================= */

function readLegendNumber(
    selector
) {

    const element =
        document.querySelector(
            selector
        );

    if (!element) {
        return 0;
    }

    const parent =
        element.closest("div");

    if (!parent) {
        return 0;
    }

    const value =
        parent.querySelector("b");

    if (!value) {
        return 0;
    }

    const number =
        Number(
            value.textContent
                .replace(/,/g, "")
                .trim()
        );

    return Number.isFinite(number)
        ? number
        : 0;
}


/* =========================================================
   RISK BARS
   ========================================================= */

function initRiskBars() {

    const bars =
        document.querySelectorAll(
            ".risk-fill"
        );

    if (!bars.length) {
        return;
    }

    let total = 0;

    bars.forEach(
        bar => {

            total += Number(
                bar.dataset.value || 0
            );

        }
    );

    total = total || 1;


    requestAnimationFrame(
        () => {

            bars.forEach(
                bar => {

                    const value =
                        Number(
                            bar.dataset.value || 0
                        );

                    const percentage =
                        Math.min(
                            (
                                value /
                                total
                            ) * 100,
                            100
                        );

                    bar.style.width =
                        percentage + "%";

                }
            );

        }
    );

}


/* =========================================================
   FEATURE SEARCH
   ========================================================= */

function initFeatureSearch() {

    const search =
        document.querySelector(
            "[data-analytics-search]"
        );

    const features =
        Array.from(
            document.querySelectorAll(
                ".analytics-feature"
            )
        );

    if (
        !search ||
        !features.length
    ) {
        return;
    }


    search.addEventListener(
        "input",
        () => {

            const query =
                search.value
                    .trim()
                    .toLowerCase();


            features.forEach(
                feature => {

                    const text =
                        feature.textContent
                            .trim()
                            .toLowerCase();


                    feature.style.display =
                        !query ||
                        text.includes(query)
                            ? ""
                            : "none";

                }
            );

        }
    );

}


/* =========================================================
   TOOLTIP
   ========================================================= */

function initAnalyticsTooltips() {

    const elements =
        document.querySelectorAll(
            ".analytics-feature strong"
        );

    elements.forEach(
        element => {

            const text =
                element.textContent.trim();

            if (
                text.length > 22
            ) {

                element.title =
                    text;

            }

        }
    );

}


/* =========================================================
   REFRESH API
   ========================================================= */

async function refreshAnalytics() {

    try {

        const response =
            await fetch(
                "/api/dashboard",
                {
                    method: "GET",

                    headers: {
                        "Accept":
                            "application/json"
                    },

                    cache: "no-store"
                }
            );


        if (!response.ok) {

            throw new Error(
                `Analytics request failed: ${
                    response.status
                }`
            );

        }


        return await response.json();


    } catch (error) {

        console.error(
            "FinGuard Analytics:",
            error
        );

        return null;

    }

}


/* =========================================================
   NUMBER FORMATTER
   ========================================================= */

function formatAnalyticsNumber(
    value
) {

    const number =
        Number(value);

    if (
        !Number.isFinite(number)
    ) {
        return "0";
    }

    return new Intl.NumberFormat(
        "en-IN"
    ).format(number);

}


/* =========================================================
   PUBLIC API
   ========================================================= */

window.FinGuardAnalytics = {

    refresh:
        refreshAnalytics,

    formatNumber:
        formatAnalyticsNumber

};