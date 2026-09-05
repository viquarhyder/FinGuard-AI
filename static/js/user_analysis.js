/* =========================================================
   FINGUARD AI
   USER ANALYSIS
   PREMIUM INTERACTIVE INTELLIGENCE ENGINE
   ========================================================= */

"use strict";


document.addEventListener("DOMContentLoaded", () => {

    initUserAnalysis();
    initUserSearch();
    initKpiInteractions();
    initRiskDistribution();
    initRiskInteractions();
    initScoreAnimations();
    initTableInteractions();
    initKeyboardShortcut();

});


/* =========================================================
   GLOBAL SETTINGS
   ========================================================= */

const UA_CONFIG = {

    animationDuration: 650,

    scrollOffset: 90,

    selectors: {

        search: "[data-user-search]",

        filter: "[data-user-filter]",

        rows: "[data-user-row]",

        kpiCards: ".ua-kpi-card",

        riskLegend: ".ua-legend-item",

        riskBadge: ".ua-risk-badge",

        scoreBars:
            ".ua-user-progress span, .ua-score-cell > div span"

    }

};


/* =========================================================
   MAIN PAGE ANIMATION
   ========================================================= */

function initUserAnalysis() {

    const elements = document.querySelectorAll(
        `
        .ua-hero,
        .ua-kpi-card,
        .ua-card,
        .ua-footer-status
        `
    );

    if (!elements.length) {
        return;
    }


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (reducedMotion) {

        elements.forEach(element => {

            element.style.opacity = "1";
            element.style.transform = "none";

        });

        return;
    }


    elements.forEach((element, index) => {

        element.style.opacity = "0";
        element.style.transform =
            "translateY(14px)";


        setTimeout(() => {

            element.style.transition =
                "opacity .45s ease, transform .45s cubic-bezier(.2,.8,.2,1)";

            element.style.opacity = "1";
            element.style.transform =
                "translateY(0)";

        }, 60 + index * 55);

    });

}


/* =========================================================
   KPI INTERACTIONS
   ========================================================= */

function initKpiInteractions() {

    const cards =
        document.querySelectorAll(
            UA_CONFIG.selectors.kpiCards
        );


    if (!cards.length) {
        return;
    }


    cards.forEach(card => {

        card.setAttribute(
            "tabindex",
            "0"
        );


        card.addEventListener(
            "click",
            event => {

                createRipple(
                    card,
                    event
                );

                activateKpiCard(
                    card
                );

            }
        );


        card.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {

                    event.preventDefault();

                    activateKpiCard(
                        card
                    );

                }

            }
        );

    });

}


/* =========================================================
   ACTIVATE KPI
   ========================================================= */

function activateKpiCard(card) {

    const cards =
        document.querySelectorAll(
            UA_CONFIG.selectors.kpiCards
        );


    cards.forEach(item => {

        item.classList.remove(
            "active"
        );

    });


    card.classList.add(
        "active"
    );


    const label =
        getKpiLabel(card);


    if (!label) {
        return;
    }


    const riskMap = {

        "total users": "all",

        "high risk users": "high",

        "medium risk": "medium",

        "low risk users": "low"

    };


    const risk =
        riskMap[
            label.toLowerCase()
        ];


    if (
        typeof risk === "undefined"
    ) {
        return;
    }


    setUserRiskFilter(
        risk
    );


    if (risk !== "all") {

        scrollToUserTable();

    }

}


/* =========================================================
   GET KPI LABEL
   ========================================================= */

function getKpiLabel(card) {

    const label =
        card.querySelector(
            ".ua-kpi-label"
        );


    if (label) {
        return label.textContent.trim();
    }


    const spans =
        card.querySelectorAll(
            "span"
        );


    for (const span of spans) {

        const text =
            span.textContent
                .trim()
                .toLowerCase();


        if (
            text === "total users" ||
            text === "high risk users" ||
            text === "medium risk" ||
            text === "low risk users"
        ) {

            return span.textContent.trim();

        }

    }


    return null;

}


/* =========================================================
   USER SEARCH + FILTER
   ========================================================= */

function initUserSearch() {

    const search =
        document.querySelector(
            UA_CONFIG.selectors.search
        );


    const filter =
        document.querySelector(
            UA_CONFIG.selectors.filter
        );


    const rows =
        Array.from(
            document.querySelectorAll(
                UA_CONFIG.selectors.rows
            )
        );


    if (!rows.length) {
        return;
    }


    function filterUsers() {

        const query =
            search
                ? search.value
                    .trim()
                    .toLowerCase()
                : "";


        const selectedRisk =
            filter
                ? filter.value.toLowerCase()
                : "all";


        let visibleCount = 0;


        rows.forEach(row => {

            const text =
                row.textContent
                    .trim()
                    .toLowerCase();


            const risk =
                (
                    row.dataset.risk || ""
                ).toLowerCase();


            const matchesSearch =
                !query ||
                text.includes(query);


            const matchesRisk =
                selectedRisk === "all" ||
                risk === selectedRisk;


            const visible =
                matchesSearch &&
                matchesRisk;


            row.classList.toggle(
                "is-hidden",
                !visible
            );


            if (visible) {

                visibleCount++;

                animateVisibleRow(
                    row
                );

            }

        });


        updateEmptyTableState(
            visibleCount
        );


        updateTableMeta(
            visibleCount
        );


        updateActiveFilter(
            selectedRisk
        );

    }


    if (search) {

        search.addEventListener(
            "input",
            filterUsers
        );

    }


    if (filter) {

        filter.addEventListener(
            "change",
            filterUsers
        );

    }


    window.FinGuardUserAnalysis = {

        refresh: filterUsers,


        reset() {

            if (search) {
                search.value = "";
            }


            if (filter) {
                filter.value = "all";
            }


            removeKpiActiveState();


            removeRiskLegendActiveState();


            filterUsers();

        },


        filterRisk(risk) {

            setUserRiskFilter(
                risk
            );

        }

    };


    filterUsers();

}


/* =========================================================
   SET RISK FILTER
   ========================================================= */

function setUserRiskFilter(
    risk
) {

    const filter =
        document.querySelector(
            UA_CONFIG.selectors.filter
        );


    if (!filter) {
        return;
    }


    const allowed = [
        "all",
        "high",
        "medium",
        "low"
    ];


    if (
        !allowed.includes(risk)
    ) {

        risk = "all";

    }


    filter.value = risk;


    filter.dispatchEvent(
        new Event(
            "change",
            {
                bubbles: true
            }
        )
    );


    syncRiskLegend(
        risk
    );

}


/* =========================================================
   RISK DISTRIBUTION INTERACTIONS
   ========================================================= */

function initRiskDistribution() {

    const legends =
        document.querySelectorAll(
            UA_CONFIG.selectors.riskLegend
        );


    if (!legends.length) {
        return;
    }


    legends.forEach(legend => {

        legend.setAttribute(
            "tabindex",
            "0"
        );


        legend.addEventListener(
            "click",
            event => {

                createRipple(
                    legend,
                    event
                );


                const risk =
                    detectLegendRisk(
                        legend
                    );


                if (!risk) {
                    return;
                }


                activateRiskLegend(
                    legend
                );


                setUserRiskFilter(
                    risk
                );


                scrollToUserTable();

            }
        );


        legend.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {

                    event.preventDefault();

                    legend.click();

                }

            }
        );

    });

}


/* =========================================================
   DETECT LEGEND RISK
   ========================================================= */

function detectLegendRisk(
    legend
) {

    const dot =
        legend.querySelector(
            ".dot, .ua-legend-dot"
        );


    if (dot) {

        if (
            dot.classList.contains(
                "high"
            )
        ) {
            return "high";
        }


        if (
            dot.classList.contains(
                "medium"
            )
        ) {
            return "medium";
        }


        if (
            dot.classList.contains(
                "low"
            )
        ) {
            return "low";
        }

    }


    const text =
        legend.textContent
            .trim()
            .toLowerCase();


    if (text.includes("high")) {
        return "high";
    }


    if (text.includes("medium")) {
        return "medium";
    }


    if (text.includes("low")) {
        return "low";
    }


    return null;

}


/* =========================================================
   ACTIVE RISK LEGEND
   ========================================================= */

function activateRiskLegend(
    activeLegend
) {

    const legends =
        document.querySelectorAll(
            UA_CONFIG.selectors.riskLegend
        );


    legends.forEach(
        legend => {

            legend.classList.toggle(
                "active",
                legend === activeLegend
            );

        }
    );

}


/* =========================================================
   SYNC LEGEND WITH FILTER
   ========================================================= */

function syncRiskLegend(
    risk
) {

    const legends =
        document.querySelectorAll(
            UA_CONFIG.selectors.riskLegend
        );


    legends.forEach(legend => {

        const legendRisk =
            detectLegendRisk(
                legend
            );


        legend.classList.toggle(
            "active",
            legendRisk === risk
        );

    });

}


/* =========================================================
   REMOVE LEGEND ACTIVE STATE
   ========================================================= */

function removeRiskLegendActiveState() {

    document
        .querySelectorAll(
            UA_CONFIG.selectors.riskLegend
        )
        .forEach(
            legend =>
                legend.classList.remove(
                    "active"
                )
        );

}


/* =========================================================
   REMOVE KPI ACTIVE STATE
   ========================================================= */

function removeKpiActiveState() {

    document
        .querySelectorAll(
            UA_CONFIG.selectors.kpiCards
        )
        .forEach(
            card =>
                card.classList.remove(
                    "active"
                )
        );

}


/* =========================================================
   RISK BADGE INTERACTION
   ========================================================= */

function initRiskInteractions() {

    const badges =
        document.querySelectorAll(
            UA_CONFIG.selectors.riskBadge
        );


    badges.forEach(badge => {

        badge.addEventListener(
            "mouseenter",
            () => {

                badge.style.transform =
                    "translateY(-2px) scale(1.02)";

            }
        );


        badge.addEventListener(
            "mouseleave",
            () => {

                badge.style.transform =
                    "translateY(0) scale(1)";

            }
        );

    });

}


/* =========================================================
   TABLE ROW INTERACTIONS
   ========================================================= */

function initTableInteractions() {

    const rows =
        document.querySelectorAll(
            UA_CONFIG.selectors.rows
        );


    rows.forEach(row => {

        row.addEventListener(
            "click",
            () => {

                rows.forEach(
                    item =>
                        item.classList.remove(
                            "is-highlighted"
                        )
                );


                row.classList.add(
                    "is-highlighted"
                );

            }
        );

    });

}


/* =========================================================
   SCORE BAR ANIMATION
   ========================================================= */

function initScoreAnimations() {

    const bars =
        document.querySelectorAll(
            UA_CONFIG.selectors.scoreBars
        );


    if (!bars.length) {
        return;
    }


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    bars.forEach(bar => {

        const target =
            bar.style.width;


        if (!target) {
            return;
        }


        if (reducedMotion) {
            return;
        }


        bar.style.width = "0%";


        requestAnimationFrame(
            () => {

                setTimeout(
                    () => {

                        bar.style.width =
                            target;

                    },
                    120
                );

            }
        );

    });

}


/* =========================================================
   ROW ANIMATION
   ========================================================= */

function animateVisibleRow(
    row
) {

    if (
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    ) {
        return;
    }


    if (
        row.dataset.animated === "true"
    ) {
        return;
    }


    row.dataset.animated =
        "true";


    row.animate(
        [
            {
                opacity: 0.35,
                transform:
                    "translateX(-5px)"
            },

            {
                opacity: 1,
                transform:
                    "translateX(0)"
            }
        ],
        {
            duration: 260,
            easing:
                "cubic-bezier(.2,.8,.2,1)"
        }
    );

}


/* =========================================================
   TABLE EMPTY STATE
   ========================================================= */

function updateEmptyTableState(
    visibleCount
) {

    const tbody =
        document.querySelector(
            ".ua-table tbody"
        );


    if (!tbody) {
        return;
    }


    let empty =
        tbody.querySelector(
            ".ua-filter-empty"
        );


    if (visibleCount === 0) {

        if (!empty) {

            empty =
                document.createElement(
                    "tr"
                );


            empty.className =
                "ua-filter-empty";


            const cell =
                document.createElement(
                    "td"
                );


            cell.colSpan = 5;


            cell.innerHTML = `
                <div style="
                    padding:32px 20px;
                    text-align:center;
                ">

                    <div style="
                        width:46px;
                        height:46px;
                        margin:0 auto 10px;
                        display:grid;
                        place-items:center;
                        border-radius:12px;
                        background:#eff6ff;
                        color:#2563eb;
                        font-size:18px;
                        font-weight:900;
                    ">
                        —
                    </div>

                    <strong style="
                        display:block;
                        color:#334155;
                        font-size:12px;
                        font-weight:900;
                    ">
                        No matching users
                    </strong>

                    <span style="
                        display:block;
                        margin-top:5px;
                        color:#94a3b8;
                        font-size:9px;
                    ">
                        Try another search or risk level.
                    </span>

                </div>
            `;


            empty.appendChild(
                cell
            );


            tbody.appendChild(
                empty
            );

        }

    } else if (empty) {

        empty.remove();

    }

}


/* =========================================================
   TABLE META COUNT
   ========================================================= */

function updateTableMeta(
    visibleCount
) {

    const counter =
        document.querySelector(
            "[data-visible-count]"
        );


    if (!counter) {
        return;
    }


    counter.textContent =
        Number(visibleCount)
            .toLocaleString();

}


/* =========================================================
   ACTIVE FILTER UI
   ========================================================= */

function updateActiveFilter(
    risk
) {

    const filter =
        document.querySelector(
            UA_CONFIG.selectors.filter
        );


    if (!filter) {
        return;
    }


    filter.dataset.activeRisk =
        risk;

}


/* =========================================================
   SCROLL TO USER TABLE
   ========================================================= */

function scrollToUserTable() {

    const table =
        document.querySelector(
            ".ua-table-card"
        );


    if (!table) {
        return;
    }


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    const top =
        table.getBoundingClientRect().top +
        window.scrollY -
        UA_CONFIG.scrollOffset;


    window.scrollTo({

        top: Math.max(
            top,
            0
        ),

        behavior:
            reducedMotion
                ? "auto"
                : "smooth"

    });


    pulseElement(
        table
    );

}


/* =========================================================
   TABLE PULSE
   ========================================================= */

function pulseElement(
    element
) {

    if (
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    ) {
        return;
    }


    element.animate(
        [
            {
                boxShadow:
                    "0 12px 38px rgba(37,99,235,.18)"
            },

            {
                boxShadow:
                    "0 12px 38px rgba(15,23,42,.055)"
            }
        ],
        {
            duration: 850,
            easing: "ease-out"
        }
    );

}


/* =========================================================
   RIPPLE EFFECT
   ========================================================= */

function createRipple(
    element,
    event
) {

    if (
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    ) {
        return;
    }


    const rect =
        element.getBoundingClientRect();


    const ripple =
        document.createElement(
            "span"
        );


    const size =
        Math.max(
            rect.width,
            rect.height
        );


    ripple.style.position =
        "absolute";


    ripple.style.width =
        `${size}px`;


    ripple.style.height =
        `${size}px`;


    ripple.style.left =
        `${event.clientX - rect.left - size / 2}px`;


    ripple.style.top =
        `${event.clientY - rect.top - size / 2}px`;


    ripple.style.borderRadius =
        "50%";


    ripple.style.pointerEvents =
        "none";


    ripple.style.background =
        "rgba(37, 99, 235, .12)";


    ripple.style.transform =
        "scale(0)";


    ripple.style.opacity =
        "1";


    ripple.style.zIndex =
        "20";


    element.style.position =
        "relative";


    element.style.overflow =
        "hidden";


    element.appendChild(
        ripple
    );


    ripple.animate(
        [
            {
                transform:
                    "scale(0)",

                opacity: 1
            },

            {
                transform:
                    "scale(1.8)",

                opacity: 0
            }
        ],
        {
            duration: 520,
            easing:
                "cubic-bezier(.2,.8,.2,1)"
        }
    );


    setTimeout(
        () => {

            ripple.remove();

        },
        550
    );

}


/* =========================================================
   KEYBOARD SHORTCUT
   "/" → SEARCH
   ESC → RESET
   ========================================================= */

function initKeyboardShortcut() {

    const search =
        document.querySelector(
            UA_CONFIG.selectors.search
        );


    if (!search) {
        return;
    }


    document.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "/" &&
                document.activeElement !== search &&
                !isTypingElement(
                    document.activeElement
                )
            ) {

                event.preventDefault();

                search.focus();

                search.select();

            }


            if (
                event.key === "Escape"
            ) {

                const active =
                    document.activeElement;


                if (
                    active === search
                ) {

                    search.value = "";

                    search.dispatchEvent(
                        new Event(
                            "input",
                            {
                                bubbles: true
                            }
                        )
                    );

                    search.blur();

                }

                else {

                    resetUserAnalysis();

                }

            }

        }
    );

}


/* =========================================================
   RESET USER ANALYSIS
   ========================================================= */

function resetUserAnalysis() {

    if (
        window.FinGuardUserAnalysis &&
        typeof
        window.FinGuardUserAnalysis.reset ===
        "function"
    ) {

        window.FinGuardUserAnalysis.reset();

    }

}


/* =========================================================
   TYPING ELEMENT CHECK
   ========================================================= */

function isTypingElement(
    element
) {

    if (!element) {
        return false;
    }


    const tag =
        element.tagName
            ? element.tagName.toLowerCase()
            : "";


    return (

        tag === "input" ||

        tag === "textarea" ||

        tag === "select" ||

        element.isContentEditable

    );

}


/* =========================================================
   SAFE NUMBER FORMATTER
   ========================================================= */

function formatUserRisk(
    value
) {

    const number =
        Number(value);


    if (
        !Number.isFinite(number)
    ) {

        return "0.0";

    }


    return number.toFixed(1);

}


/* =========================================================
   SAFE INTEGER FORMATTER
   ========================================================= */

function formatUserCount(
    value
) {

    const number =
        Number(value);


    if (
        !Number.isFinite(number)
    ) {

        return "0";

    }


    return number.toLocaleString();

}


/* =========================================================
   PUBLIC FIN GUARD API
   ========================================================= */

window.FinGuardUserTools = {

    formatRisk:
        formatUserRisk,

    formatCount:
        formatUserCount,

    scrollToTable:
        scrollToUserTable,

    filterRisk:
        setUserRiskFilter

};