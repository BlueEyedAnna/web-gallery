let btn = document.getElementById("loginBtn");
let check_login = false;

if (btn.value !== "Выйти") {
    document.getElementById("check_login").hidden = true;
    document.getElementById("is_valid").hidden = true;
}

let form = document.getElementById("form");
btn = document.getElementById("submitBtn");
let regbtn = document.getElementById("reg");
let regdiv1 = document.getElementById("checkon");
let regdiv2 = document.getElementById("checkoff");

regbtn.onclick = function () {
    if (btn.value === "Войти") {
        form.action = "/registration";
        btn.value = "Зарегестрироваться";
        regdiv1.style.display = "block";
        regdiv2.style.display = "none";
        regbtn.textContent = "Вход"
        document.getElementById("userPasswordCheck").required = true;
        btn.disabled = true;
        document.getElementById("modal_title").innerText = "Регистрация";
    } else {
        form.action = "/login";
        btn.value = "Войти";
        regdiv1.style.display = "none";
        regdiv2.style.display = "block";
        regbtn.textContent = "Регистрация"
        document.getElementById("userPasswordCheck").required = false;
        btn.disabled = false;
        document.getElementById("userPasswordCheck").value = "";
        document.getElementById("modal_title").innerText = "Авторизация";
    }
    document.getElementById("check_login").hidden = true;
    document.getElementById("is_valid").hidden = true;
}

let password = document.getElementById("userPassword");
let passwordCheck = document.getElementById("userPasswordCheck");

passwordCheck.onkeyup = function () {
    if (regbtn.textContent === "Вход") {
        if (password.value !== passwordCheck.value) {
            passwordCheck.style.borderColor = "red";
            btn.disabled = true;
        } else {
            passwordCheck.style.borderColor = "green";
            btn.disabled = false;
        }
    } else {
        btn.disabled = false;
    }
}

password.onkeyup = function () {
    if (regbtn.textContent === "Вход") {
        if (password.value !== passwordCheck.value) {
            btn.disabled = true;
        } else {
            btn.disabled = check_login;
        }
    } else {
        btn.disabled = false;
    }
}

document.getElementById("userLogin").onblur = function () {
    let url = "http://" + window.location.hostname + ":5000/check_login/" + document.getElementById("userLogin").value;

    $.ajax({
        type: 'GET',
        async: false,
        url: url,
        success: function (data) {
            if (btn.value !== "Войти") {
                if (data.toString() === "true") {
                    check_login = true;
                    document.getElementById("check_login").hidden = false;
                    btn.disabled = true;
                } else {
                    check_login = false;
                    document.getElementById("check_login").hidden = true;
                    btn.disabled = password.value !== passwordCheck.value;
                }
            }
        }
    });
}

$('#submitBtn').click(function () {
    if (btn.value === "Войти") {
        let valid = true;
        let url = "http://" + window.location.hostname + ":5000/login_user/" + document.getElementById("userLogin").value + "&" + document.getElementById("userPassword").value;

        $.ajax({
            type: 'GET',
            async: false,
            url: url,
            success: function (res) {
                valid = (res.toString() === "true");
                if (!valid) {
                    document.getElementById("is_valid").hidden = false;
                }
            }
        });

        if (!valid) {
            return false;
        }
    }
});