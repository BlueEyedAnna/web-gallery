let arts_count = parseInt(document.getElementById('arts_count').innerHTML);
let filters = [];
let check_boxes = $('input[type=checkbox]');
let arts = $('.filtering');


filtering = function () {
    let classes = $(this).closest('div')[0].children[0].innerText;
    let showing = false;

    filters.forEach(flt => {
        if (classes.includes(flt)) {
            showing = true;
        }
    });

    if (showing) {
        $(this).show();
    } else {
        $(this).hide();
    }
};

check_boxes.click(function () {
    let is_checked = $(this).is(":checked");
    let flt = $(this).closest('div')[0].children[1].children[0].innerText;

    if (is_checked) {
        filters.push(flt)
    } else {
        filters.splice(filters.indexOf(flt), 1);
    }

    if (filters.length === 0){
        $('.filtering').show();
        return;
    }

    arts.each(filtering);
});


// for (let i = 0; i < arts_count; i++) {
//     arts[i] = []
//
//     for (let j = 0; j <= 20; j++) {
//         let ph = document.getElementById((i * 100 + j).toString())
//
//         if (ph != null) {
//             arts[i].push(ph)
//         }
//     }
// }

// for (let i = 0; i < arts_count; i++) {
//     if (arts[i].length > 0) {
//         arts[i][0].style.display = "block";
//     }
// }
//
// for (let i = 0; i < arts_count; i++) {
//     if (arts[i].length > 0) {
//         setInterval(() => {
//             for (let j = 0; j < arts[i].length; j++) {
//                 if (arts[i][j].style.display === "block") {
//                     if (j !== arts[i].length - 1) {
//                         // console.log(j + ' ' + (j + 1) + '\n')
//                         arts[i][j].style.display = "none";
//                         arts[i][j + 1].style.display = "block";
//                     } else {
//                         // console.log(j + ' 0' + '\n')
//                         arts[i][j].style.display = "none";
//                         arts[i][0].style.display = "block";
//                     }
//                     break;
//                 }
//             }
//         }, 3000)
//     }
// }

