function padzero(num) {
    if (num < 10) { num = "0" + num; }
    else { num = num.toString(); }
    return num;
}

function createSel(max, sel) {
    for (var i = 0; i < max; i++) {
        var opt = document.createElement("option");
        i = padzero(i);
        opt.value = i;
        opt.innerHTML = i;
        sel.appendChild(opt);
    }
}

var hr = document.getElementById("hour");
var min = document.getElementById("min");

createSel(23, hr)
createSel(59, min)

hour = 0;
minute = 0;
nowHr = 0;
nowMin = 0;

function setTime() {
    hour = parseInt($("#hour").children("option:selected").val());
    minute = parseInt($("#min").children("option:selected").val());
}

function tryText() {
    if ((hour == nowHr) && (minute == nowMin)) {
        console.log("afdf")
    }
}

setInterval(() => {
    today = new Date();
    nowHr = today.getHours();
    nowMin = today.getMinutes();

    tryText()
}, 1000)