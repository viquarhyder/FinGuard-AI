/**
 * FinGuard AI
 * Charts Controller
 * =================
 * Dashboard + Analytics chart engine.
 */

"use strict";

document.addEventListener("DOMContentLoaded", () => {
    initFinGuardCharts();
});


/* ============================================================
   MAIN INITIALIZER
   ============================================================ */

function initFinGuardCharts() {

    if (
        typeof window.Chart === "undefined"
    ) {
        console.warn(
            "FinGuard AI: Chart.js is not loaded."
        );
        return;
    }

    initFraudDistributionChart();
    initTransactionTrendChart();
    initRiskDistributionChart();
    initAmountChart();
}


/* ============================================================
   CHART DEFAULTS
   ============================================================ */

function setChartDefaults() {

    if (
        typeof Chart === "undefined"
    ) {
        return;
    }

    Chart.defaults.font.family =
        "Inter, Arial, sans-serif";

    Chart.defaults.font.size = 12;

    Chart.defaults.color =
        "#64748b";

    Chart.defaults.animation.duration =
        900;

    Chart.defaults.animation.easing =
        "easeOutQuart";

    Chart.defaults.plugins.legend.labels.usePointStyle =
        true;

    Chart.defaults.plugins.legend.labels.padding =
        18;
}

setChartDefaults();


/* ============================================================
   FRAUD DISTRIBUTION
   ============================================================ */

function initFraudDistributionChart() {

    const canvas =
        document.querySelector(
            "#fraudDistributionChart"
        );

    if (!canvas) {
        return;
    }

    const legitimate =
        getDataValue(
            canvas,
            "legitimate",
            0
        );

    const fraud =
        getDataValue(
            canvas,
            "fraud",
            0
        );

    const existing =
        Chart.getChart(canvas);

    if (existing) {
        existing.destroy();
    }

    new Chart(
        canvas.getContext("2d"),
        {
            type: "doughnut",

            data: {
                labels: [
                    "Legitimate",
                    "Fraud"
                ],

                datasets: [
                    {
                        data: [
                            legitimate,
                            fraud
                        ],

                        backgroundColor: [
                            "#2563eb",
                            "#ef4444"
                        ],

                        borderWidth: 0,

                        hoverOffset: 8
                    }
                ]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                cutout: "72%",

                plugins: {

                    legend: {
                        position: "bottom"
                    },

                    tooltip: {
                        callbacks: {

                            label: function(
                                context
                            ) {

                                const value =
                                    context.raw ||
                                    0;

                                return (
                                    " " +
                                    context.label +
                                    ": " +
                                    Number(
                                        value
                                    ).toLocaleString()
                                );
                            }
                        }
                    }
                }
            }
        }
    );
}


/* ============================================================
   TRANSACTION TREND
   ============================================================ */

function initTransactionTrendChart() {

    const canvas =
        document.querySelector(
            "#transactionTrendChart"
        );

    if (!canvas) {
        return;
    }

    const labels =
        getJSONData(
            canvas,
            "labels",
            [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6"
            ]
        );

    const values =
        getJSONData(
            canvas,
            "values",
            [
                0,
                0,
                0,
                0,
                0,
                0
            ]
        );

    const existing =
        Chart.getChart(canvas);

    if (existing) {
        existing.destroy();
    }

    new Chart(
        canvas.getContext("2d"),
        {
            type: "line",

            data: {

                labels: labels,

                datasets: [
                    {
                        label:
                            "Transactions",

                        data: values,

                        borderColor:
                            "#2563eb",

                        backgroundColor:
                            "rgba(37, 99, 235, 0.10)",

                        borderWidth: 3,

                        pointRadius: 3,

                        pointHoverRadius: 6,

                        fill: true,

                        tension: 0.4
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction: {
                    intersect: false,
                    mode: "index"
                },

                scales: {

                    x: {
                        grid: {
                            display: false
                        },

                        border: {
                            display: false
                        }
                    },

                    y: {

                        beginAtZero: true,

                        border: {
                            display: false
                        },

                        grid: {
                            color:
                                "rgba(148, 163, 184, 0.14)"
                        },

                        ticks: {
                            precision: 0
                        }
                    }
                },

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        backgroundColor:
                            "#0f172a",

                        padding: 12,

                        cornerRadius: 8
                    }
                }
            }
        }
    );
}


/* ============================================================
   RISK DISTRIBUTION
   ============================================================ */

function initRiskDistributionChart() {

    const canvas =
        document.querySelector(
            "#riskDistributionChart"
        );

    if (!canvas) {
        return;
    }

    const low =
        getDataValue(
            canvas,
            "low",
            0
        );

    const medium =
        getDataValue(
            canvas,
            "medium",
            0
        );

    const high =
        getDataValue(
            canvas,
            "high",
            0
        );

    const existing =
        Chart.getChart(canvas);

    if (existing) {
        existing.destroy();
    }

    new Chart(
        canvas.getContext("2d"),
        {
            type: "bar",

            data: {

                labels: [
                    "Low",
                    "Medium",
                    "High"
                ],

                datasets: [
                    {
                        label:
                            "Risk Level",

                        data: [
                            low,
                            medium,
                            high
                        ],

                        backgroundColor: [
                            "#22c55e",
                            "#f59e0b",
                            "#ef4444"
                        ],

                        borderRadius: 8,

                        borderSkipped: false
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                scales: {

                    x: {
                        grid: {
                            display: false
                        },

                        border: {
                            display: false
                        }
                    },

                    y: {

                        beginAtZero: true,

                        border: {
                            display: false
                        },

                        grid: {
                            color:
                                "rgba(148, 163, 184, 0.14)"
                        },

                        ticks: {
                            precision: 0
                        }
                    }
                },

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {
                        backgroundColor:
                            "#0f172a",

                        padding: 12,

                        cornerRadius: 8
                    }
                }
            }
        }
    );
}


/* ============================================================
   TRANSACTION AMOUNT CHART
   ============================================================ */

function initAmountChart() {

    const canvas =
        document.querySelector(
            "#amountChart"
        );

    if (!canvas) {
        return;
    }

    const labels =
        getJSONData(
            canvas,
            "labels",
            []
        );

    const values =
        getJSONData(
            canvas,
            "values",
            []
        );

    if (!labels.length || !values.length) {
        return;
    }

    const existing =
        Chart.getChart(canvas);

    if (existing) {
        existing.destroy();
    }

    new Chart(
        canvas.getContext("2d"),
        {
            type: "bar",

            data: {

                labels: labels,

                datasets: [
                    {
                        label:
                            "Transaction Amount",

                        data: values,

                        backgroundColor:
                            "#2563eb",

                        borderRadius: 7,

                        borderSkipped: false
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                scales: {

                    x: {
                        grid: {
                            display: false
                        }
                    },

                    y: {

                        beginAtZero: true,

                        grid: {
                            color:
                                "rgba(148, 163, 184, 0.14)"
                        },

                        ticks: {

                            callback:
                                function(value) {

                                    return (
                                        "₹" +
                                        Number(
                                            value
                                        ).toLocaleString()
                                    );
                                }
                        }
                    }
                },

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        callbacks: {

                            label:
                                function(context) {

                                    return (
                                        " ₹" +
                                        Number(
                                            context.raw ||
                                            0
                                        ).toLocaleString()
                                    );
                                }
                        }
                    }
                }
            }
        }
    );
}


/* ============================================================
   DATA HELPERS
   ============================================================ */

function getDataValue(
    element,
    name,
    fallback = 0
) {

    const value =
        element.dataset[name];

    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {
        return fallback;
    }

    const number =
        Number(value);

    return Number.isFinite(number)
        ? number
        : fallback;
}


function getJSONData(
    element,
    name,
    fallback = []
) {

    const value =
        element.dataset[name];

    if (!value) {
        return fallback;
    }

    try {

        const parsed =
            JSON.parse(value);

        return Array.isArray(parsed)
            ? parsed
            : fallback;

    } catch (error) {

        console.warn(
            "FinGuard AI chart data error:",
            error
        );

        return fallback;
    }
}


/* ============================================================
   CHART UPDATE API
   ============================================================ */

function updateChart(
    canvasId,
    labels,
    values
) {

    const canvas =
        document.getElementById(
            canvasId
        );

    if (!canvas) {
        return;
    }

    const chart =
        Chart.getChart(canvas);

    if (!chart) {
        return;
    }

    chart.data.labels =
        labels;

    if (
        chart.data.datasets &&
        chart.data.datasets[0]
    ) {

        chart.data.datasets[0].data =
            values;
    }

    chart.update();
}


/* ============================================================
   WINDOW RESIZE
   ============================================================ */

let chartResizeTimer;

window.addEventListener(
    "resize",
    () => {

        clearTimeout(
            chartResizeTimer
        );

        chartResizeTimer =
            setTimeout(
                () => {

                    Object.values(
                        Chart.instances || {}
                    ).forEach(
                        (chart) => {

                            try {
                                chart.resize();
                            } catch {
                                // Ignore destroyed charts.
                            }
                        }
                    );

                },
                180
            );
    }
);


/* ============================================================
   PUBLIC API
   ============================================================ */

window.FinGuardCharts = {

    update:
        updateChart,

    refresh:
        initFinGuardCharts
};