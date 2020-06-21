let clock = {
    data: {
        time: '',
        date: ''
    }
};

let week = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];

setInterval(updateTime, 1000);
updateTime();

function updateTime() {
    let cd = new Date();

    clock.time = zeroPadding(
        cd.getHours(), 2) + ':' +
        zeroPadding(cd.getMinutes(), 2) + ':' +
        zeroPadding(cd.getSeconds(), 2);

    clock.date = zeroPadding(
        week[cd.getDay()] + '  ' +
        zeroPadding(cd.getDate(), 2) + '-' +
        zeroPadding(cd.getMonth()+1, 2) + '-' +
        cd.getFullYear(), 0);

    document.getElementsByClassName("date")[0].innerHTML = clock.date;
    document.getElementsByClassName("time")[0].innerHTML = clock.time;
}

function zeroPadding(num, digit) {
    let zero = '';
    for(let i = 0; i < digit; i++) {
        zero += '0';
    }
    return (zero + num).slice(-digit);
}