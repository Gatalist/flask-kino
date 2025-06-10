
const formFiltersID = "form_args";
const formFilterYearsID = "#select-years";
const formFilterGenresID = "#select-genres";
const formFilterCountriesID = "#select-countries";
const formFilterDirectorsID = "#select-directors";
const formFilterSortingID = "#select-sorting";
const formClearFilterID = "#clear-filter";
const formApplyFilterID = "#apply-filter";

const formFilters = document.getElementById(formFiltersID);
const formFilterYears = formFilters.querySelector(formFilterYearsID);
const formFilterGenres = formFilters.querySelector(formFilterGenresID);
const formFilterCountries = formFilters.querySelector(formFilterCountriesID);
const formFilterDirectors = formFilters.querySelector(formFilterDirectorsID);
const formFilterSorting = formFilters.querySelector(formFilterSortingID);
const formClearFilter = formFilters.querySelector(formClearFilterID);
const formApplyFilter = formFilters.querySelector(formApplyFilterID);

const dataYears = parseData(formFilterYears.dataset.filteryears);
const dataGenres = parseData(formFilterGenres.dataset.filtergenres);
const dataCountries = parseData(formFilterCountries.dataset.filtercountries);
const dataDirectors = parseData(formFilterDirectors.dataset.filterdirectors);
const dataSorting = parseData(formFilterSorting.dataset.filtersorting);

const activeDataYears = parseData(formFilterYears.dataset.activefilteryears);
const activeDataGenres = parseData(formFilterGenres.dataset.activefiltergenres);
const activeDataCountries = parseData(formFilterCountries.dataset.activefiltercountries);
const activeDataDirectors = parseData(formFilterDirectors.dataset.activefilterdirectors);
const activeDataSorted = formFilterSorting.dataset.activesorted;

console.log("activeDataYears:", activeDataYears);
console.log("activeDataGenres:", activeDataGenres);
console.log("activeDataCountries:", activeDataCountries);
console.log("activeDataDirectors:", activeDataDirectors);
console.log("activeDataSorted:", activeDataSorted);

formClearFilter.addEventListener('click', function () {
    clear_options({FilterId: formFilterYearsID});
    clear_options({FilterId: formFilterGenresID});
    clear_options({FilterId: formFilterCountriesID});
    clear_options({FilterId: formFilterDirectorsID});
    clear_options({FilterId: formFilterSortingID, multiple: false});
    formApplyFilter.click();
});

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

function set_options({FilterId, setList=[], setValue='', multiple=true}) {
    const value = `${FilterId} .selectpicker`;
    if (multiple === true && setList.length > 0) {
        const newSetList = setList.map(String);
        $(value).val(newSetList);
    } else {
        $(value).val(setValue);
    }
}

function clear_options({FilterId, multiple=true}) {
    const value = `${FilterId} .selectpicker`;
    console.log("clear", value);
    if (multiple === true) {
        $(value).val([]).selectpicker('deselectAll');
    } else {
        $(value).val('');
    }
}

function createFilter({element, labelName, labelText, placeholder, dataList, multiple=true}) {
    const oldSelect = element.querySelector('.selectpicker');
    if (oldSelect) {
        $(oldSelect).selectpicker('destroy'); // Уничтожаем bootstrap-select instance
    }

    const label = document.createElement('label');
    label.setAttribute('for', labelName);
    label.classList.add('form-label');
    label.textContent = labelText;

    const select = document.createElement('select');
    select.classList.add('selectpicker');
    if (multiple === true) {
        select.setAttribute('multiple', '');
    }
    select.setAttribute('data-placeholder', placeholder);
    select.setAttribute('name', labelName);
    select.setAttribute('id', labelName);

    dataList.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.value;
        select.appendChild(option);
    });

    element.innerHTML = '';
    element.appendChild(label);
    element.appendChild(select);
}

function renderFilter() {
    createFilter({
        element: formFilterYears, labelName: 'years',
        labelText: 'Год', placeholder: 'Все годы', dataList: dataYears
    });

    createFilter({
        element: formFilterGenres, labelName: 'genres',
        labelText: 'Жанр', placeholder: 'Все жанры', dataList: dataGenres
    });

    createFilter({
        element: formFilterCountries, labelName: 'countries',
        labelText: 'Страна', placeholder: 'Все страны', dataList: dataCountries
    });

    createFilter({
        element: formFilterDirectors, labelName: 'directors',
        labelText: 'Режиссер', placeholder: 'Все режиссеры', dataList: dataDirectors
    });

    createFilter({
        element: formFilterSorting, labelName: 'sorting',
        labelText: 'Сортировка', placeholder: 'Нет сортировки', dataList: dataSorting,
        multiple: false
    });
}

function renderActiveFilter() {
    set_options({FilterId: formFilterYearsID, setList: activeDataYears ? activeDataYears: []});
    set_options({FilterId: formFilterGenresID, setList: activeDataGenres ? activeDataGenres: []});
    set_options({FilterId: formFilterCountriesID, setList: activeDataCountries ? activeDataCountries: []});
    set_options({FilterId: formFilterDirectorsID, setList: activeDataDirectors ? activeDataDirectors: []});
    set_options({FilterId: formFilterSortingID, setValue: activeDataSorted, multiple: false});
}

renderFilter();
renderActiveFilter();

const btnFilterVisibleID = "#btn-filters-visible";
const filterVisibleID = "#filters-visible";

const btnFilterVisible = document.querySelector(btnFilterVisibleID);
const filterVisible = document.querySelector(filterVisibleID);

btnFilterVisible.addEventListener('click', function () {
    console.log("click")
    const active = filterVisible.classList.contains('filters-show');
    if (active) {
        filterVisible.classList.remove('filters-show');
        filterVisible.classList.add('filters-hidden');
        btnFilterVisible.innerHTML = `<i class="bi bi-plus-circle fs-4"></i>`;
    } else {
        filterVisible.classList.add('filters-show');
        filterVisible.classList.remove('filters-hidden');
        btnFilterVisible.innerHTML = `<i class="bi bi-dash-circle fs-4"></i>`;
    }
});