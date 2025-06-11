export function createModal({modalId, callback}) {
    const existingModal = document.getElementById(modalId);
    if (existingModal) {
        existingModal.remove();
    }

    return new Promise((resolve) => {
        const modalHTML = document.createElement('div');
        modalHTML.innerHTML = `
            <div class="modal fade" id="${modalId}" tabindex="-1" aria-labelledby="${modalId}Label">
                <div class="modal-dialog modal-lg modal-dialog-scrollable">
                    <div class="modal-content bg-dark text-white">
                        <div class="modal-body">
                            <form onsubmit="return false;">
                              <div class="row">
                                <div class="col-12">
                                  <div class="mb-3">
                                    <div class="input-group mb-3">
                                      <span class="input-group-text"><i class="bi bi-search fs-5"></i></span>
                                      <input id="modal-search-input" class="form-control" type="search" placeholder="Поиск" autocomplete="off">
                                      
                                    </div>
                                  </div>
                                </div>
                                <div class="col-12">
                                  <div id="loading-spinner" class="d-flex justify-content-center d-none mb-2">
                                    <div class="spinner-border text-success" role="status">
                                      <span class="visually-hidden">Loading...</span>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </form>
                            <div id="searchedList" class="row searched-list"></div>
                        </div>
                        <div class="modal-footer d-none" id="all-search-result"></div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modalHTML);

        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();

        const input = document.getElementById('modal-search-input');
        const searchedList = document.getElementById('searchedList');
        const loadingSpinner = document.getElementById('loading-spinner');
        const allSearchResult = document.getElementById('all-search-result');

        input.addEventListener('input', debounce(async function () {
        // input.addEventListener('input', async function () {
            const query = input.value.trim();
            if (query.length === 0) {
                searchedList.innerHTML = '';
            } else {
                if (query.length >= 3) {
                    loadingSpinner.classList.remove('d-none');

                    const url = `/api/movie/search/?query=${encodeURIComponent(query)}`;
                    const response = await apiFetch({method: 'GET', url: url})
                    if (response) {
                        console.log("response", response.objects);
                        console.log("response", response.pagination);
                        searchedList.innerHTML = '';
                        if (response.pagination.items === 0){
                            console.log("response", 0);
                            allSearchResult.classList.add('d-none');
                            searchedList.innerHTML = notSearchResult();
                        } else if (response.pagination.items > 0 && response.pagination.items <= 5) {
                            allSearchResult.classList.add('d-none');
                            searchedList.innerHTML = response.objects.map(movie => createSearchMovie(movie)).join('');
                        } else {
                            allSearchResult.classList.remove('d-none');
                            const first5 = Object.entries(response.objects).slice(0, 5);
                            const first5Obj = Object.fromEntries(first5);
                            searchedList.innerHTML = first5Obj.objects.map(movie => createSearchMovie(movie)).join('');
                            allSearchResult.innerHTML = manySearchResult(response.pagination.items);
                        }
                        loadingSpinner.classList.add('d-none');
                        console.log("finish render");
                    }
                } else {
                    allSearchResult.classList.add('d-none');
                    loadingSpinner.classList.add('d-none');
                    searchedList.innerHTML = '';
                }
            }
        }, 500));
        resolve();
    });
}

function createSearchMovie(movie) {
    return `
        <div class="search-card search-card-shadow mb-2">
            <a href="/film/${movie.slug}" class="text-decoration-none text-reset d-block p-2 rounded card-hover">
              <div class="d-flex mb-1 mt-1 align-items-start">
                <div class="search-card-image me-2">
                  <img class="search-card-img" src="${movie.poster_url}" alt="${movie.name_ru}">
                </div>
                <div class="flex-grow-1">
                  <div class="d-flex">
                    <div class="me-auto">
                      <h5 class="card-title mb-1">${movie.name_ru}</h5>
                      <div class="card-text mb-1">
                        <i class="bi bi-calendar3 icon-color"></i> ${movie.year}
                      </div>
                    </div>
                    <div class="text-end">
                      <div class="card-text">
                        <i class="bi bi-star-fill icon-color"></i> ${movie.rating_imdb}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </a>
        </div>
    `
}

function notSearchResult() {
    return `
        <div class="alert alert-dark" role="alert">
            Не найдено совпадений!
        </div>
    `
}

function manySearchResult(count) {
    return `
        <div class="d-flex">
          <div class="p-2 flex-grow-1">Найдено совпадений: ${count}</div>
          <div class="p-2">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Все совпадения</button>
          </div>
        </div>
    `
}

async function apiFetch({method, url, data = {}}) {
    return await fetch(url, {
        method: method,
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Response:', data);
        return data;
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}

function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}