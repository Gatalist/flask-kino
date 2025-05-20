const allTab = document.getElementById('player-tabs');
const activeTab = allTab.querySelector('.nav-link.active');

function getPlayerTab(activeTab) {
    // console.log('activeTab:', activeTab);
    const activeTabId = activeTab.getAttribute('id');        // Новый активный таб
    console.log('Активен таб:', activeTabId);
    const movieKinopoiskId = activeTab.dataset.moviekinopoiskid;
    console.log('movieKinopoiskId:', movieKinopoiskId);
    const playerName = activeTabId.split('-')[0];
    console.log('playerName:', playerName);
    const tabPlayer = '.' + playerName + '-player';
    console.log('tabPlayer:', tabPlayer);
    console.log('--------------------');
    // return {
    //     movieKinopoiskId: movieKinopoiskId,
    //     playerName: playerName,
    //     tabPlayer: tabPlayer
    // }
    play(tabPlayer, movieKinopoiskId);
}

getPlayerTab(activeTab);

document.addEventListener('DOMContentLoaded', function () {
  const tabElList = allTab.querySelectorAll('button[data-bs-toggle="tab"]');
  tabElList.forEach(function (tabEl) {
    tabEl.addEventListener('shown.bs.tab', function (event) {
      getPlayerTab(tabEl);
    });
  });
});

function play(container, movieKinopoiskId) {
    new Kinobox(container, {

        search: {
            kinopoisk: movieKinopoiskId,
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
                autoplay: 0,
                hide_selectors: true
            },
            // collaps: {
            //     hide_selectors: true
            // },
        },
        hide: ['kodik', 'alloha', 'collaps'],
        order: ['videocdn'],
    }).init();
}

// class Player{
//     allohaPlayer= {
//         enable: true,
//         position: 1,
//         token: '{token}'
//     }
//     videocdnPlayer = {
//         enable: true,
//         position: 1,
//         token: '{token}'
//     }
//     collapsPlayer = {
//         enable: true,
//         position: 4,
//         token: '{token}'
//     }
//
//     constructor(
//         container,
//         movieKinopoiskId,
//         playersName,
//         token,
//     ) {
//         this.container = container;
//         this.kinopoiskId = movieKinopoiskId;
//         this.playersName = playersName;
//         this.token = token;
//     }
//
//     init(){
//         new Kinobox('.cdn_player', {
//             search: {
//                 kinopoisk: '{{movie.kinopoisk_id}}',
//             },
//             menu: {
//                 default: false,
//                 mobile: 'menuButton',
//                 format: '{N} :: {T} ({Q})',
//                 limit: 5,
//                 open: false,
//             },
//             players: {
//                 // alloha: {
//                 //     enable: true,
//                 //     position: 1,
//                 //     token: '{token}'
//                 // },
//                 videocdn: {
//                     enable: true,
//                     position: 1,
//                     token: '{token}'
//                 },
//                 // collaps: {
//                 //     enable: true,
//                 //     position: 4,
//                 //     token: '{token}'
//                 // },
//             },
//             params: {
//                 all: {
//                     poster: 'https://example.org/poster.jpg',
//                 },
//                 // alloha: {
//                 //     autoplay: 0
//                 // },
//                 // kodik: {
//                 //     hide_selectors: true
//                 // },
//                 videocdn: {
//                     autoplay: 0,
//                     hide_selectors: true
//                 },
//                 // collaps: {
//                 //     hide_selectors: true
//                 // },
//             },
//             hide: ['kodik', 'alloha', 'collaps'],
//             order: ['videocdn'],
//         }).init();
//     }
// }

// new Kinobox('.cdn_player', {
//
//         search: {
//             kinopoisk: '{{movie.kinopoisk_id}}',
//         },
//         menu: {
//             default: false,
//             mobile: 'menuButton',
//             format: '{N} :: {T} ({Q})',
//             limit: 5,
//             open: false,
//         },
//         players: {
//             // alloha: {
//             //     enable: true,
//             //     position: 1,
//             //     token: '{token}'
//             // },
//             videocdn: {
//                 enable: true,
//                 position: 1,
//                 token: '{token}'
//             },
//             // collaps: {
//             //     enable: true,
//             //     position: 4,
//             //     token: '{token}'
//             // },
//         },
//         params: {
//             all: {
//                 poster: 'https://example.org/poster.jpg',
//             },
//             // alloha: {
//             //     autoplay: 0
//             // },
//             // kodik: {
//             //     hide_selectors: true
//             // },
//             videocdn: {
//                 autoplay: 0,
//                 hide_selectors: true
//             },
//             // collaps: {
//             //     hide_selectors: true
//             // },
//         },
//         hide: ['kodik', 'alloha', 'collaps'],
//         order: ['videocdn'],
//     }).init();