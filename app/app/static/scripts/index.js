function parseData(data) {
    try {
        // console.log("data->", data);
        if (data) {
            return JSON5.parse(data.replace(/None/g, null));
        } else {
            return null;
        }
    } catch (error) {
        console.error("Помилка парсингу JSON:", error);
        return null;
    }
}

// const theadParseData = parseData(container.dataset.tablehead);