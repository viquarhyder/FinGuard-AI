/* ============================================================
   FinGuard AI
   Premium Security Dashboard JavaScript
   ============================================================ */

"use strict";


/* ============================================================
   GLOBAL DASHBOARD STATE
   ============================================================ */

const FinGuardDashboard = {

    charts: {},

    refreshTimer: null,

    isRefreshing: false

};


/* ============================================================
   DOM READY
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    initPremiumKPICards();

    initDashboardCharts();

    initDashboardRefresh();

    initDashboardInteractions();

});


/* ============================================================
   PREMIUM KPI CARD CLICK-TO-FLIP
   ============================================================ */

function initPremiumKPICards() {

    const cards = document.querySelectorAll(
        "[data-kpi-card]"
    );


    if (!cards.length) {

        return;

    }


    cards.forEach((card) => {


        /* ----------------------------------------------------
           CLICK
        ---------------------------------------------------- */

        card.addEventListener("click", (event) => {

            event.preventDefault();

            event.stopPropagation();


            const alreadyFlipped =
                card.classList.contains(
                    "is-flipped"
                );


            /* Close every other card */

            cards.forEach((otherCard) => {

                if (otherCard !== card) {

                    otherCard.classList.remove(
                        "is-flipped"
                    );

                }

            });


            /* Toggle selected card */

            if (alreadyFlipped) {

                card.classList.remove(
                    "is-flipped"
                );

            } else {

                card.classList.add(
                    "is-flipped"
                );

            }

        });


        /* ----------------------------------------------------
           KEYBOARD ACCESSIBILITY
        ---------------------------------------------------- */

        card.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {

                    event.preventDefault();

                    card.click();

                }

            }
        );


        /* ----------------------------------------------------
           HOVER DEPTH
        ---------------------------------------------------- */

        card.addEventListener(
            "mousemove",
            (event) => {

                if (
                    card.classList.contains(
                        "is-flipped"
                    )
                ) {

                    return;

                }


                const rect =
                    card.getBoundingClientRect();


                const x =
                    event.clientX -
                    rect.left;


                const y =
                    event.clientY -
                    rect.top;


                const centerX =
                    rect.width / 2;


                const centerY =
                    rect.height / 2;


                const rotateX =
                    ((y - centerY) /
                        centerY) *
                    -2;


                const rotateY =
                    ((x - centerX) /
                        centerX) *
                    2;


                card.style.setProperty(
                    "--card-rotate-x",
                    `${rotateX}deg`
                );


                card.style.setProperty(
                    "--card-rotate-y",
                    `${rotateY}deg`
                );

            }
        );


        /* ----------------------------------------------------
           RESET HOVER DEPTH
        ---------------------------------------------------- */

        card.addEventListener(
            "mouseleave",
            () => {

                card.style.setProperty(
                    "--card-rotate-x",
                    "0deg"
                );


                card.style.setProperty(
                    "--card-rotate-y",
                    "0deg"
                );

            }
        );

    });


    /* --------------------------------------------------------
       ESCAPE = CLOSE FLIPPED CARDS
    -------------------------------------------------------- */

    document.addEventListener(
        "keydown",
        (event) => {

            if (event.key !== "Escape") {

                return;

            }


            cards.forEach((card) => {

                card.classList.remove(
                    "is-flipped"
                );

            });

        }
    );


    /* --------------------------------------------------------
       CLICK OUTSIDE = CLOSE
    -------------------------------------------------------- */

    document.addEventListener(
        "click",
        (event) => {

            if (
                event.target.closest(
                    "[data-kpi-card]"
                )
            ) {

                return;

            }


            cards.forEach((card) => {

                card.classList.remove(
                    "is-flipped"
                );

            });

        }
    );

}


/* ============================================================
   DASHBOARD CHARTS
   ============================================================ */

function initDashboardCharts() {

    if (typeof Chart === "undefined") {

        console.warn(
            "FinGuard AI: Chart.js is not loaded."
        );

        return;

    }


    /* --------------------------------------------------------
       GLOBAL CHART DEFAULTS
    -------------------------------------------------------- */

    Chart.defaults.font.family =
        "Inter, Poppins, Arial, sans-serif";


    Chart.defaults.color =
        "#64748b";


    Chart.defaults.animation.duration =
        900;


    Chart.defaults.animation.easing =
        "easeOutQuart";


    initFraudDistributionChart();

    initRiskDistributionChart();

}


/* ============================================================
   READ CHART DATA
   ============================================================ */

function getChartData(canvas, fallback) {

    if (!canvas) {

        return fallback;

    }


    const rawData =
        canvas.dataset.chart;


    if (!rawData) {

        return fallback;

    }


    try {

        const parsed =
            JSON.parse(rawData);


        if (
            !parsed ||
            typeof parsed !== "object"
        ) {

            return fallback;

        }


        const labels =
            Array.isArray(parsed.labels)
                ? parsed.labels
                : fallback.labels;


        const values =
            Array.isArray(parsed.values)
                ? parsed.values.map(
                    (value) => {

                        const number =
                            Number(value);

                        return Number.isFinite(
                            number
                        )
                            ? number
                            : 0;

                    }
                )
                : fallback.values;


        return {

            labels,

            values

        };

    } catch (error) {

        console.error(
            "FinGuard AI: Chart data parsing failed.",
            error
        );


        return fallback;

    }

}


/* ============================================================
   CREATE GRADIENT
   ============================================================ */

function createChartGradient(
    canvas,
    startColor,
    endColor
) {

    const ctx =
        canvas.getContext("2d");


    if (!ctx) {

        return startColor;

    }


    const height =
        canvas.clientHeight ||
        300;


    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            height
        );


    gradient.addColorStop(
        0,
        startColor
    );


    gradient.addColorStop(
        1,
        endColor
    );


    return gradient;

}


/* ============================================================
   FRAUD DISTRIBUTION CHART
   ============================================================ */

function initFraudDistributionChart() {

    const canvas =
        document.getElementById(
            "fraudDistributionChart"
        );


    if (!canvas) {

        return;

    }


    /* Destroy previous instance */

    if (
        FinGuardDashboard.charts.fraud
    ) {

        FinGuardDashboard.charts.fraud.destroy();

    }


    const data =
        getChartData(
            canvas,
            {
                labels: [
                    "Legitimate",
                    "Fraud"
                ],

                values: [
                    0,
                    0
                ]
            }
        );


    const values =
        data.values.length >= 2
            ? data.values
            : [0, 0];


    const total =
        values.reduce(
            (sum, value) =>
                sum + Number(value || 0),
            0
        );


    /* --------------------------------------------------------
       CENTER TEXT PLUGIN
    -------------------------------------------------------- */

    const centerTextPlugin = {

        id: "fraudCenterText",

        afterDraw(chart) {

            const {
                ctx
            } = chart;


            const meta =
                chart.getDatasetMeta(0);


            if (
                !meta ||
                !meta.data ||
                !meta.data.length
            ) {

                return;

            }


            const centerX =
                meta.data[0].x;


            const centerY =
                meta.data[0].y;


            ctx.save();


            ctx.textAlign = "center";

            ctx.textBaseline = "middle";


            /* Total */

            ctx.font =
                "800 28px Inter, Poppins, Arial";


            ctx.fillStyle =
                "#0f172a";


            ctx.fillText(
                formatNumber(total),
                centerX,
                centerY - 8
            );


            /* Label */

            ctx.font =
                "600 10px Inter, Poppins, Arial";


            ctx.fillStyle =
                "#94a3b8";


            ctx.fillText(
                "TRANSACTIONS",
                centerX,
                centerY + 17
            );


            ctx.restore();

        }

    };


    FinGuardDashboard.charts.fraud =
        new Chart(
            canvas,
            {

                type: "doughnut",


                data: {

                    labels:
                        data.labels.length
                            ? data.labels
                            : [
                                "Legitimate",
                                "Fraud"
                            ],


                    datasets: [

                        {

                            data: values,


                            backgroundColor: [

                                createChartGradient(
                                    canvas,
                                    "#4ade80",
                                    "#16a34a"
                                ),

                                createChartGradient(
                                    canvas,
                                    "#fb7185",
                                    "#dc2626"
                                )

                            ],


                            borderColor:
                                "#ffffff",


                            borderWidth: 5,


                            hoverBorderWidth: 5,


                            hoverOffset: 14,


                            spacing: 3

                        }

                    ]

                },


                plugins: [
                    centerTextPlugin
                ],


                options: {

                    responsive: true,


                    maintainAspectRatio:
                        false,


                    cutout: "72%",


                    rotation: -90,


                    circumference: 360,


                    interaction: {

                        intersect: false

                    },


                    plugins: {

                        legend: {

                            position: "bottom",


                            labels: {

                                usePointStyle:
                                    true,


                                pointStyle:
                                    "circle",


                                padding: 22,


                                color:
                                    "#475569",


                                font: {

                                    size: 12,

                                    weight:
                                        "700"

                                }

                            }

                        },


                        tooltip: {

                            enabled: true,


                            padding: 13,


                            cornerRadius: 10,


                            backgroundColor:
                                "#0f172a",


                            titleColor:
                                "#ffffff",


                            bodyColor:
                                "#cbd5e1",


                            displayColors:
                                true,


                            callbacks: {

                                label:
                                    function(
                                        context
                                    ) {

                                        const value =
                                            Number(
                                                context.raw ||
                                                0
                                            );


                                        const percentage =
                                            total > 0
                                                ? (
                                                    value /
                                                    total
                                                ) * 100
                                                : 0;


                                        return (
                                            " " +
                                            formatNumber(
                                                value
                                            ) +
                                            " (" +
                                            percentage.toFixed(
                                                1
                                            ) +
                                            "%)"
                                        );

                                    }

                            }

                        }

                    },


                    animation: {

                        animateRotate:
                            true,

                        animateScale:
                            true,

                        duration:
                            1100,

                        easing:
                            "easeOutQuart"

                    }

                }

            }
        );

}


/* ============================================================
   RISK DISTRIBUTION CHART
   ============================================================ */

function initRiskDistributionChart() {

    const canvas =
        document.getElementById(
            "riskDistributionChart"
        );


    if (!canvas) {

        return;

    }


    /* Destroy previous instance */

    if (
        FinGuardDashboard.charts.risk
    ) {

        FinGuardDashboard.charts.risk.destroy();

    }


    const data =
        getChartData(
            canvas,
            {
                labels: [
                    "Low Risk",
                    "Medium Risk",
                    "High Risk"
                ],

                values: [
                    0,
                    0,
                    0
                ]
            }
        );


    const values =
        data.values.length >= 3
            ? data.values
            : [0, 0, 0];


    const maxValue =
        Math.max(
            ...values.map(
                value =>
                    Number(value || 0)
            ),
            0
        );


    /* Better axis when all values are zero */

    const suggestedMax =
        maxValue === 0
            ? 5
            : Math.ceil(
                maxValue * 1.25
            );


    FinGuardDashboard.charts.risk =
        new Chart(
            canvas,
            {

                type: "bar",


                data: {

                    labels:
                        data.labels.length
                            ? data.labels
                            : [
                                "Low Risk",
                                "Medium Risk",
                                "High Risk"
                            ],


                    datasets: [

                        {

                            label:
                                "Transactions",


                            data:
                                values,


                            backgroundColor: [

                                createChartGradient(
                                    canvas,
                                    "#4ade80",
                                    "#16a34a"
                                ),

                                createChartGradient(
                                    canvas,
                                    "#fbbf24",
                                    "#d97706"
                                ),

                                createChartGradient(
                                    canvas,
                                    "#fb7185",
                                    "#dc2626"
                                )

                            ],


                            borderColor: [

                                "#16a34a",

                                "#d97706",

                                "#dc2626"

                            ],


                            borderWidth: 1,


                            borderRadius: 12,


                            borderSkipped:
                                false,


                            barThickness:
                                42,


                            maxBarThickness:
                                52,


                            hoverBackgroundColor: [

                                "#22c55e",

                                "#f59e0b",

                                "#ef4444"

                            ]

                        }

                    ]

                },


                options: {

                    responsive: true,


                    maintainAspectRatio:
                        false,


                    interaction: {

                        mode: "index",

                        intersect: false

                    },


                    scales: {

                        y: {

                            beginAtZero:
                                true,


                            suggestedMax:
                                suggestedMax,


                            border: {

                                display:
                                    false

                            },


                            grid: {

                                color:
                                    "rgba(226, 232, 240, 0.7)",


                                drawTicks:
                                    false

                            },


                            ticks: {

                                color:
                                    "#64748b",


                                padding:
                                    10,


                                font: {

                                    size: 11,

                                    weight:
                                        "600"

                                },


                                precision:
                                    0

                            }

                        },


                        x: {

                            border: {

                                display:
                                    false

                            },


                            grid: {

                                display:
                                    false

                            },


                            ticks: {

                                color:
                                    "#475569",


                                padding:
                                    10,


                                font: {

                                    size: 11,

                                    weight:
                                        "800"

                                }

                            }

                        }

                    },


                    plugins: {

                        legend: {

                            display:
                                false

                        },


                        tooltip: {

                            enabled:
                                true,


                            padding:
                                13,


                            cornerRadius:
                                10,


                            backgroundColor:
                                "#0f172a",


                            titleColor:
                                "#ffffff",


                            bodyColor:
                                "#cbd5e1",


                            callbacks: {

                                label:
                                    function(
                                        context
                                    ) {

                                        return (
                                            " Transactions: " +
                                            formatNumber(
                                                context.raw ||
                                                0
                                            )
                                        );

                                    }

                            }

                        }

                    },


                    animation: {

                        duration:
                            1000,

                        easing:
                            "easeOutQuart"

                    }

                }

            }
        );

}


/* ============================================================
   NUMBER FORMATTER
   ============================================================ */

function formatNumber(value) {

    const number =
        Number(value || 0);


    if (
        !Number.isFinite(number)
    ) {

        return "0";

    }


    return number.toLocaleString(
        "en-IN"
    );

}


/* ============================================================
   REFRESH BUTTON
   ============================================================ */

function initDashboardRefresh() {

    const button =
        document.querySelector(
            "[data-dashboard-refresh]"
        );


    if (!button) {

        return;

    }


    button.addEventListener(
        "click",
        handleDashboardRefresh
    );

}


/* ============================================================
   HANDLE DASHBOARD REFRESH
   ============================================================ */

function handleDashboardRefresh() {

    if (
        FinGuardDashboard.isRefreshing
    ) {

        return;

    }


    FinGuardDashboard.isRefreshing =
        true;


    const button =
        document.querySelector(
            "[data-dashboard-refresh]"
        );


    if (!button) {

        window.location.reload();

        return;

    }


    const originalHTML =
        button.innerHTML;


    button.disabled =
        true;


    button.classList.add(
        "is-refreshing"
    );


    button.innerHTML = `
        <span class="refresh-icon">↻</span>
        <span>Refreshing...</span>
    `;


    button.style.opacity =
        "0.72";


    /*
     * We intentionally reload the dashboard directly.
     *
     * This avoids depending on a separate
     * /api/dashboard endpoint.
     *
     * Flask will rebuild the dashboard data
     * when the page loads.
     */

    FinGuardDashboard.refreshTimer =
        window.setTimeout(
            () => {

                window.location.reload();

            },
            450
        );


    /*
     * Fallback in case browser/page navigation
     * behaves unexpectedly.
     */

    window.setTimeout(
        () => {

            if (
                document.visibilityState ===
                "visible"
            ) {

                button.disabled =
                    false;


                button.classList.remove(
                    "is-refreshing"
                );


                button.innerHTML =
                    originalHTML;


                button.style.opacity =
                    "1";


                FinGuardDashboard.isRefreshing =
                    false;

            }

        },
        5000
    );

}


/* ============================================================
   DASHBOARD INTERACTIONS
   ============================================================ */

function initDashboardInteractions() {


    /* --------------------------------------------------------
       SMOOTH INTERNAL LINK BEHAVIOUR
    -------------------------------------------------------- */

    const viewAllButton =
        document.querySelector(
            ".dashboard-view-all"
        );


    if (viewAllButton) {

        viewAllButton.addEventListener(
            "click",
            () => {

                viewAllButton.classList.add(
                    "is-loading"
                );

            }
        );

    }


    /* --------------------------------------------------------
       EMPTY STATE ACTION
    -------------------------------------------------------- */

    const emptyAction =
        document.querySelector(
            ".dashboard-empty-action"
        );


    if (emptyAction) {

        emptyAction.addEventListener(
            "click",
            () => {

                emptyAction.classList.add(
                    "is-loading"
                );

            }
        );

    }


    /* --------------------------------------------------------
       REDUCED MOTION SUPPORT
    -------------------------------------------------------- */

    const prefersReducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        );


    if (
        prefersReducedMotion.matches
    ) {

        document.documentElement.classList.add(
            "reduce-motion"
        );

    }

}


/* ============================================================
   WINDOW RESIZE
   ============================================================ */

let dashboardResizeTimer;


window.addEventListener(
    "resize",
    () => {

        clearTimeout(
            dashboardResizeTimer
        );


        dashboardResizeTimer =
            setTimeout(
                () => {

                    Object.values(
                        FinGuardDashboard.charts
                    ).forEach(
                        (chart) => {

                            if (chart) {

                                chart.resize();

                            }

                        }
                    );

                },
                180
            );

    }
);


/* ============================================================
   PAGE VISIBILITY
   ============================================================ */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            document.visibilityState ===
            "visible"
        ) {

            Object.values(
                FinGuardDashboard.charts
            ).forEach(
                (chart) => {

                    if (chart) {

                        chart.resize();

                    }

                }
            );

        }

    }
);