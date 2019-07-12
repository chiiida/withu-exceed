let quoteDay = {
    normal: ["Every man has his secret sorrows which the world knows not; and often times we call a man cold when he is only sad.” ― Henry Wadsworth Longfellow",
            "I didn’t want to wake up. I was having a much better time asleep. And that’s really sad. It was almost like a reverse nightmare, like when you wake up from a nightmare you’re so relieved. I woke up into a nightmare.” – Ned Vizzini, It’s Kind of a Funny Story",
            "There are wounds that never show on the body that are deeper and more hurtful than anything that bleeds.” ― Laurell K. Hamilton, Mistral’s Kiss",
            ],
    danger: ["Whenever you read a cancer booklet or website or whatever, they always list depression among the side effects of cancer. But, in fact, depression is not a side effect of cancer. Depression is a side effect of dying.” – John Green, The Fault in Our Stars",
            "That’s the thing about depression: A human being can survive almost anything, as long as she sees the end in sight. But depression is so insidious, and it compounds daily, that it’s impossible to ever see the end.” – Elizabeth Wurtzel, Prozac Nation",
            ],
}

const URL = 'https://exceed.superposition.pknn.dev';

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function giveQuote() {
    i = getRandomInt(2)
    v = getRandomInt(2)
    document.getElementById('quote').innerText = quoteDay.normal[i];
    //$('#quote').append(quoteDay.normal[i])
}

function putAlert(status) {
    fetch(URL + '/data/withu/alert', {
        method: 'PUT',
        body: JSON.stringify({
            "value" : status
        }),
        headers:{
          'Content-Type': 'application/json'
        }
      }).then(res => res.json())
      .then(response => console.log('Success:', JSON.stringify(response)))
      .catch(error => console.error('Error:', error));
}

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

function setTime() {
    hour = parseInt($("#hour").children("option:selected").val());
    minute = parseInt($("#min").children("option:selected").val());
}

function alertQuote() {
    if ((hour == nowHr) && (minute == nowMin)) {
        giveQuote()
        putAlert(true)
        setTimeout(() => putAlert(false), 10000);
    }
}

var hr = document.getElementById("hour");
var min = document.getElementById("min");

createSel(24, hr)
createSel(60, min)

hour = 0;
minute = 0;
nowHr = 0;
nowMin = 0;

setInterval(() => {
    today = new Date();
    nowHr = today.getHours();
    nowMin = today.getMinutes();
    alertQuote()
}, 1000)