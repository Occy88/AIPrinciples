//  SCRAPER FOR:
// https://journeesrdciteo.com/live/?e=QEE6EO7IFD#!whoswho
// INSTRUCTIONS FOR USE:
// 1. OPEN WEBSITE
// 2. OPEN CONSOLE (fn f12 or right click inspect element -> console tab)
// 3. PASTE THIS FILE INTO CONSOLE
// 4. PASTE: putUsers()
// 5. PRESS UP BUTTON ON KEYBOARD AND PRESS ENTER
// 6. CONTINUE UNTILL LAST PAGE REACHED.


let b = document.getElementsByClassName('page-btn')[8]

let csv = ''

function putUsers() {
    for (let u of Array.prototype.slice.call(getUsers()).slice(0, -1)) {
        let name = getName(u)
        let company = getCompany(u)
        let work = getWork(u)
        console.log(name)
        console.log(work)
        console.log('-------------')

        csv += name + ',' + company + ',' + work + '\n'
    }
    b.click()
}


function getUsers() {
    return document.getElementsByClassName('userinfo-wrapper')
}

function getCompany(u) {
    return u.getElementsByTagName('span')[1].textContent
}

function getName(user) {
    return user.firstElementChild.textContent
}

function getWork(u) {
    return u.getElementsByTagName('span')[3].textContent
}
