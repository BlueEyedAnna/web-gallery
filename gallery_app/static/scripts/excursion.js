let excursions_count = parseInt(document.getElementById('excursions_count').innerHTML)
let excursions = {}

for (let i = 0; i < excursions_count; i++) {
    excursions[i] = []

    for (let j = 0; j <= 20; j++) {
        let ph = document.getElementById((i * 100 + j).toString())

        if (ph != null) {
            excursions[i].push(ph)
        }
    }
}

for (let i = 0; i < excursions_count; i++) {
    if (excursions[i].length > 0) {
        excursions[i][0].style.display = "block";
    }
}

for (let i = 0; i < excursions_count; i++) {
    if (excursions[i].length > 0) {
        setInterval(() => {
            for (let j = 0; j < excursions[i].length; j++) {
                if (excursions[i][j].style.display === "block") {
                    if (j !== excursions[i].length - 1) {
                        // console.log(j + ' ' + (j + 1) + '\n')
                        excursions[i][j].style.display = "none";
                        excursions[i][j + 1].style.display = "block";
                    } else {
                        // console.log(j + ' 0' + '\n')
                        excursions[i][j].style.display = "none";
                        excursions[i][0].style.display = "block";
                    }
                    break;
                }
            }
        }, 3000)
    }
}