new Kinobox('.kinobox_player', {
    search: {
        kinopoisk: '{{movie.kinopoisk_id}}',
        // imdb: 'tt0816692',
        // title: 'Интерстеллар'
    },
    menu: {
        default: false,
        mobile: 'menuButton',
        format: '{N} :: {T} ({Q})',
        limit: 5,
        open: false,
    },
    players: {
        // alloha: {
        //     enable: true,
        //     position: 1,
        //     token: '{token}'
        // },
        // kodik: {
        //     enable: true,
        //     position: 2,
        //     token: '{token}'
        // },
        videocdn: {
            enable: true,
            position: 1,
            token: '{token}'
        },
        // collaps: {
        //     enable: true,
        //     position: 4,
        //     token: '{token}'
        // },
    },
    params: {
        all: {
            poster: 'https://example.org/poster.jpg',
        },
        // alloha: {
        //     autoplay: 0
        // },
        // kodik: {
        //     hide_selectors: true
        // },
        videocdn: {
            hide_selectors: true
        },
        // collaps: {
        //     hide_selectors: true
        // },
    },
    hide: [],
    order: ['kodik', 'alloha', 'videocdn', 'collaps'],
}).init();