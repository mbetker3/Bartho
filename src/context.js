function getContext(el) {
    return (el?.innerText || "").replace(/\n{3,}/g, "\n\n").trim();
}

function setRowContext(table) {
    const rows = Array.from(table?.querySelectorAll("tr") || []);
    rows.map((tr) => {
        Array.from(tr.querySelectorAll("td, th")).map((cell) => getContext(cell))
    });
}

function extractProblems(){
    const problemElements = document.querySelectorAll('[id*=question], .question, .Question, .assignmentQuestion');

    const seen = new Set();
    const uniqueProblems = [];

    problemElements.forEach((el) => {
        const context = getContext(el);
        if (context && !seen.has(context)) {
            seen.add(context);
            uniqueProblems.push(context);
        }
    });

    return {url: location.href, title: document.title, problems: uniqueProblems};
}


window.__WA__EXTRACT__ = extractProblems