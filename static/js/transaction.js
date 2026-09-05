/* =========================================================
   FINGUARD AI
   TRANSACTION MONITOR
   Premium Search + Filter + Pagination Engine
   ========================================================= */

"use strict";


document.addEventListener("DOMContentLoaded", () => {

    initTransactionMonitor();

});


/* =========================================================
   MAIN
   ========================================================= */

function initTransactionMonitor() {

    const rows = Array.from(
        document.querySelectorAll(
            "[data-transaction-row]"
        )
    );

    const searchInput =
        document.querySelector(
            "[data-transaction-search]"
        );

    const filter =
        document.querySelector(
            "[data-transaction-filter]"
        );

    const countElement =
        document.querySelector(
            "[data-transaction-count]"
        );

    const pagination =
        document.querySelector(
            "[data-transaction-pagination]"
        );

    const previousButton =
        document.querySelector(
            "[data-page-prev]"
        );

    const nextButton =
        document.querySelector(
            "[data-page-next]"
        );

    const pageInfo =
        document.querySelector(
            "[data-page-info]"
        );


    if (!rows.length) {
        return;
    }


    /* =====================================================
       STATE
       ===================================================== */

    let currentPage = 1;

    let pageSize = 8;

    let filteredRows = [...rows];


    if (pagination) {

        const configuredSize =
            Number(
                pagination.dataset.pageSize
            );

        if (
            Number.isFinite(configuredSize) &&
            configuredSize > 0
        ) {

            pageSize =
                configuredSize;

        }

    }


    /* =====================================================
       SEARCH + FILTER
       ===================================================== */

    function applyFilters(
        animate = true
    ) {

        const query =
            searchInput
                ? searchInput.value
                    .trim()
                    .toLowerCase()
                : "";


        const selectedFilter =
            filter
                ? filter.value.toLowerCase()
                : "all";


        filteredRows =
            rows.filter(row => {

                const rowText =
                    row.textContent
                        .trim()
                        .toLowerCase();


                const status =
                    (
                        row.dataset.status ||
                        ""
                    ).toLowerCase();


                const risk =
                    (
                        row.dataset.risk ||
                        ""
                    ).toLowerCase();


                const matchesSearch =
                    !query ||
                    rowText.includes(query);


                let matchesFilter =
                    true;


                switch (
                    selectedFilter
                ) {

                    case "fraud":

                        matchesFilter =
                            status ===
                            "fraud";

                        break;


                    case "legitimate":

                        matchesFilter =
                            status ===
                            "legitimate";

                        break;


                    case "low":

                        matchesFilter =
                            risk ===
                            "low";

                        break;


                    case "high":

                        matchesFilter =
                            risk ===
                            "high";

                        break;

                }


                return (
                    matchesSearch &&
                    matchesFilter
                );

            });


        currentPage = 1;


        renderRows(
            animate
        );


        updateFilterVisualState(
            selectedFilter
        );

    }


    /* =====================================================
       RENDER ROWS
       ===================================================== */

    function renderRows(
        animate = true
    ) {

        rows.forEach(row => {

            row.classList.add(
                "is-hidden"
            );

            row.classList.remove(
                "is-highlighted"
            );

        });


        const totalPages =
            Math.max(
                1,
                Math.ceil(
                    filteredRows.length /
                    pageSize
                )
            );


        if (
            currentPage >
            totalPages
        ) {

            currentPage =
                totalPages;

        }


        const start =
            (
                currentPage - 1
            ) *
            pageSize;


        const end =
            start +
            pageSize;


        const visibleRows =
            filteredRows.slice(
                start,
                end
            );


        visibleRows.forEach(
            (row, index) => {

                row.classList.remove(
                    "is-hidden"
                );


                if (animate) {

                    row.style.opacity =
                        "0";

                    row.style.transform =
                        "translateY(6px)";


                    requestAnimationFrame(
                        () => {

                            setTimeout(
                                () => {

                                    row.style.transition =
                                        "opacity .25s ease, transform .25s ease";

                                    row.style.opacity =
                                        "1";

                                    row.style.transform =
                                        "translateY(0)";

                                },
                                index * 25
                            );

                        }
                    );

                }

            }
        );


        updateCount();

        updatePagination(
            totalPages
        );


        updateEmptyState();

    }


    /* =====================================================
       COUNT
       ===================================================== */

    function updateCount() {

        if (!countElement) {
            return;
        }


        const target =
            filteredRows.length;


        const current =
            Number(
                countElement.dataset.currentCount ||
                0
            );


        countElement.dataset.currentCount =
            String(target);


        animateCounter(
            countElement,
            current,
            target
        );

    }


    /* =====================================================
       COUNTER ANIMATION
       ===================================================== */

    function animateCounter(
        element,
        start,
        end
    ) {

        if (
            window.matchMedia(
                "(prefers-reduced-motion: reduce)"
            ).matches
        ) {

            element.textContent =
                end.toLocaleString(
                    "en-IN"
                );

            return;

        }


        const duration =
            350;


        const startTime =
            performance.now();


        function frame(
            currentTime
        ) {

            const progress =
                Math.min(
                    (
                        currentTime -
                        startTime
                    ) /
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
                Math.round(
                    start +
                    (
                        end -
                        start
                    ) *
                    eased
                );


            element.textContent =
                value.toLocaleString(
                    "en-IN"
                );


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


    /* =====================================================
       PAGINATION
       ===================================================== */

    function updatePagination(
        totalPages
    ) {

        if (!pagination) {
            return;
        }


        if (previousButton) {

            previousButton.disabled =
                currentPage <= 1;

        }


        if (nextButton) {

            nextButton.disabled =
                currentPage >=
                totalPages;

        }


        if (pageInfo) {

            pageInfo.textContent =
                `Page ${currentPage} of ${totalPages}`;

        }


        updatePageButtons(
            totalPages
        );

    }


    /* =====================================================
       PAGE BUTTONS
       ===================================================== */

    function updatePageButtons(
        totalPages
    ) {

        if (!pagination) {
            return;
        }


        const existingButtons =
            pagination.querySelectorAll(
                "[data-page]"
            );


        existingButtons.forEach(
            button => {

                button.remove();

            }
        );


        const next =
            pagination.querySelector(
                "[data-page-next]"
            );


        if (!next) {
            return;
        }


        const fragment =
            document.createDocumentFragment();


        const pages =
            buildPageList(
                currentPage,
                totalPages
            );


        pages.forEach(page => {

            if (
                page === "..."
            ) {

                const ellipsis =
                    document.createElement(
                        "span"
                    );


                ellipsis.className =
                    "transaction-page-info";


                ellipsis.textContent =
                    "…";


                fragment.appendChild(
                    ellipsis
                );


                return;

            }


            const button =
                document.createElement(
                    "button"
                );


            button.type =
                "button";


            button.className =
                "transaction-page-btn";


            if (
                page ===
                currentPage
            ) {

                button.classList.add(
                    "active"
                );

            }


            button.dataset.page =
                String(page);


            button.textContent =
                String(page);


            button.setAttribute(
                "aria-label",
                `Go to page ${page}`
            );


            button.addEventListener(
                "click",
                () => {

                    if (
                        page ===
                        currentPage
                    ) {

                        return;

                    }


                    currentPage =
                        page;


                    renderRows();

                    scrollTableIntoView();

                }
            );


            fragment.appendChild(
                button
            );

        });


        pagination.insertBefore(
            fragment,
            next
        );

    }


    /* =====================================================
       PAGE LIST
       ===================================================== */

    function buildPageList(
        current,
        total
    ) {

        if (
            total <= 5
        ) {

            return Array.from(
                {
                    length: total
                },
                (_, index) =>
                    index + 1
            );

        }


        if (
            current <= 3
        ) {

            return [
                1,
                2,
                3,
                4,
                "...",
                total
            ];

        }


        if (
            current >=
            total - 2
        ) {

            return [
                1,
                "...",
                total - 3,
                total - 2,
                total - 1,
                total
            ];

        }


        return [
            1,
            "...",
            current - 1,
            current,
            current + 1,
            "...",
            total
        ];

    }


    /* =====================================================
       PREVIOUS
       ===================================================== */

    if (previousButton) {

        previousButton.addEventListener(
            "click",
            () => {

                if (
                    currentPage <= 1
                ) {

                    return;

                }


                currentPage--;


                renderRows();


                scrollTableIntoView();

            }
        );

    }


    /* =====================================================
       NEXT
       ===================================================== */

    if (nextButton) {

        nextButton.addEventListener(
            "click",
            () => {

                const totalPages =
                    Math.max(
                        1,
                        Math.ceil(
                            filteredRows.length /
                            pageSize
                        )
                    );


                if (
                    currentPage >=
                    totalPages
                ) {

                    return;

                }


                currentPage++;


                renderRows();


                scrollTableIntoView();

            }
        );

    }


    /* =====================================================
       SEARCH
       ===================================================== */

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            () => {

                applyFilters();

            }
        );


        /* Clear search with Escape */

        searchInput.addEventListener(
            "keydown",
            event => {

                if (
                    event.key ===
                    "Escape"
                ) {

                    searchInput.value =
                        "";

                    applyFilters();

                    searchInput.blur();

                }

            }
        );

    }


    /* =====================================================
       FILTER
       ===================================================== */

    if (filter) {

        filter.addEventListener(
            "change",
            () => {

                applyFilters();

            }
        );

    }


    /* =====================================================
       FILTER VISUAL STATE
       ===================================================== */

    function updateFilterVisualState(
        value
    ) {

        if (!filter) {
            return;
        }


        filter.dataset.activeFilter =
            value;

    }


    /* =====================================================
       EMPTY STATE
       ===================================================== */

    function updateEmptyState() {

        const table =
            document.querySelector(
                ".transaction-table"
            );


        if (!table) {
            return;
        }


        let emptyMessage =
            document.querySelector(
                ".transaction-filter-empty"
            );


        if (
            filteredRows.length === 0
        ) {

            table.style.display =
                "none";


            if (!emptyMessage) {

                emptyMessage =
                    document.createElement(
                        "div"
                    );


                emptyMessage.className =
                    "transaction-filter-empty";


                emptyMessage.innerHTML = `
                    <div class="transaction-empty-icon">
                        <span>⌕</span>
                    </div>

                    <h3>No Matching Transactions</h3>

                    <p>
                        No transaction records match
                        your current search or filter.
                    </p>

                    <button
                        type="button"
                        class="transaction-empty-btn"
                        data-clear-transactions
                    >
                        Clear Filters
                    </button>
                `;


                const wrapper =
                    document.querySelector(
                        ".transaction-table-wrapper"
                    );


                if (wrapper) {

                    wrapper.parentNode.insertBefore(
                        emptyMessage,
                        wrapper.nextSibling
                    );

                }


                const clearButton =
                    emptyMessage.querySelector(
                        "[data-clear-transactions]"
                    );


                if (clearButton) {

                    clearButton.addEventListener(
                        "click",
                        reset
                    );

                }

            }


            emptyMessage.style.display =
                "flex";

        } else {

            table.style.display =
                "";


            if (emptyMessage) {

                emptyMessage.style.display =
                    "none";

            }

        }

    }


    /* =====================================================
       SCROLL
       ===================================================== */

    function scrollTableIntoView() {

        const tableCard =
            document.querySelector(
                ".transaction-table-card"
            );


        if (!tableCard) {
            return;
        }


        const rect =
            tableCard.getBoundingClientRect();


        if (
            rect.top < 70 ||
            rect.top > window.innerHeight
        ) {

            tableCard.scrollIntoView({
                behavior:
                    "smooth",
                block:
                    "start"
            });

        }

    }


    /* =====================================================
       KEYBOARD SUPPORT
       ===================================================== */

    document.addEventListener(
        "keydown",
        event => {

            /* "/" = focus search */

            if (
                event.key === "/" &&
                document.activeElement !==
                    searchInput
            ) {

                if (searchInput) {

                    event.preventDefault();

                    searchInput.focus();

                }

            }


            /* Escape = clear */

            if (
                event.key === "Escape" &&
                document.activeElement !==
                    searchInput
            ) {

                reset();

            }

        }
    );


    /* =====================================================
       RESET
       ===================================================== */

    function reset() {

        if (searchInput) {

            searchInput.value =
                "";

        }


        if (filter) {

            filter.value =
                "all";

        }


        currentPage =
            1;


        applyFilters();

    }


    /* =====================================================
       INITIAL RENDER
       ===================================================== */

    countElement &&
        (
            countElement.dataset.currentCount =
                "0"
        );


    renderRows(
        false
    );


    /* =====================================================
       PUBLIC API
       ===================================================== */

    window.FinGuardTransactions = {

        refresh() {

            applyFilters(
                false
            );

        },


        reset() {

            reset();

        },


        nextPage() {

            if (nextButton) {

                nextButton.click();

            }

        },


        previousPage() {

            if (previousButton) {

                previousButton.click();

            }

        }

    };

}