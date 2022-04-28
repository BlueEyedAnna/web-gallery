let exhibitions_count = parseInt(document.getElementById('exhibitions_count').innerHTML)
let exhibitions = {}

for (let i = 0; i < exhibitions_count; i++) {
    exhibitions[i] = []

    for (let j = 0; j <= 20; j++) {
        let ph = document.getElementById((i * 100 + j).toString())

        if (ph != null) {
            exhibitions[i].push(ph)
        }
    }
}

for (let i = 0; i < exhibitions_count; i++) {
    if (exhibitions[i].length > 0) {
        exhibitions[i][0].style.display = "block";
    }
}

for (let i = 0; i < exhibitions_count; i++) {
    if (exhibitions[i].length > 0) {
        setInterval(() => {
            for (let j = 0; j < exhibitions[i].length; j++) {
                if (exhibitions[i][j].style.display === "block") {
                    if (j !== exhibitions[i].length - 1) {
                        // console.log(j + ' ' + (j + 1) + '\n')
                        exhibitions[i][j].style.display = "none";
                        exhibitions[i][j + 1].style.display = "block";
                    } else {
                        // console.log(j + ' 0' + '\n')
                        exhibitions[i][j].style.display = "none";
                        exhibitions[i][0].style.display = "block";
                    }
                    break;
                }
            }
        }, 3000)
    }
}