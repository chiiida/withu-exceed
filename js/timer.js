let quoteDay = {
    normal: ["Every man has his secret sorrows which the world knows not; and often times we call a man cold when he is only sad.” ― Henry Wadsworth Longfellow",
            "I didn’t want to wake up. I was having a much better time asleep. And that’s really sad. It was almost like a reverse nightmare, like when you wake up from a nightmare you’re so relieved. I woke up into a nightmare.” – Ned Vizzini, It’s Kind of a Funny Story",
            "There are wounds that never show on the body that are deeper and more hurtful than anything that bleeds.” ― Laurell K. Hamilton, Mistral’s Kiss",
            "Whenever you read a cancer booklet or website or whatever, they always list depression among the side effects of cancer. But, in fact, depression is not a side effect of cancer. Depression is a side effect of dying.” – John Green, The Fault in Our Stars",
            "That’s the thing about depression: A human being can survive almost anything, as long as she sees the end in sight. But depression is so insidious, and it compounds daily, that it’s impossible to ever see the end.” – Elizabeth Wurtzel, Prozac Nation",
            "“Try to understand the blackness, lethargy, hopelessness, and loneliness they’re going through. Be there for them when they come through the other side. It’s hard to be a friend to someone who’s depressed, but it is one of the kindest, noblest, and best things you will ever do.” ― Stephen Fry",
            "“Some friends don’t understand this. They don’t understand how desperate I am to have someone say, I love you and I support you just the way you are because you’re wonderful just the way you are. They don’t understand that I can’t remember anyone ever saying that to me.",
            "I am so demanding and difficult for my friends because I want to crumble and fall apart before them so that they will love me even though I am no fun, lying in bed, crying all the time, not moving. Depression is all about If you loved me you would.” – Elizabeth Wurtzel, Prozac Nation",
            "“There is no point treating a depressed person as though she were just feeling sad, saying, ‘There now, hang on, you’ll get over it.’ Sadness is more or less like a head cold – with patience, it passes. Depression is like cancer.” ― Barbara Kingsolver, The Bean Trees",
            "“Noble deeds and hot baths are the best cures for depression.” ― Dodie Smith, I Capture the Castle",
            "“When you’re surrounded by all these people, it can be lonelier than when you’re by yourself. You can be in a huge crowd, but if you don’t feel like you can trust anyone or talk to anybody, you feel like you’re really alone.” ― Fiona Apple",
            "“The worst type of crying wasn’t the kind everyone could see–the wailing on street corners, the tearing at clothes. No, the worst kind happened when your soul wept and no matter what you did, there was no way to comfort it.",
            "“Do you not see how necessary a world of pains and troubles is to school an intelligence and make it a soul?” ― John Keats, Letters of John Keates",
            "“Mental pain is less dramatic than physical pain, but it is more common and also more hard to bear. The frequent attempt to conceal mental pain increases the burden: it is easier to say “My tooth is aching” than to say “My heart is broken.” ― C.S. Lewis, The Problem of Pain",
            "“I don’t want any more of this try, try again stuff. I just want out. I’ve had it. I am so tired. I am twenty and I am already exhausted.” ― Elizabeth Wurtzel, Prozac Nation",
            "“Because wherever I sat—on the deck of a ship or at a street café in Paris or Bangkok—I would be sitting under the same glass bell jar, stewing in my own sour air.” ― Sylvia Plath, The Bell Jar",
            ],
}

const URL = 'https://exceed.superposition.pknn.dev';

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function giveQuote(count) {
    console.log(quoteDay)
    i = getRandomInt(16)
    if (count == 0) {
        document.getElementById('quote').innerText = quoteDay.normal[i];
    }
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
        if (count == 0) {
            giveQuote(count)
        }
        count++
        putAlert(true)
        setTimeout(() => putAlert(false), 10000);
    } else {
        count = 0;
    }
}

var hr = document.getElementById("hour");
var min = document.getElementById("min");
var count = 0;

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