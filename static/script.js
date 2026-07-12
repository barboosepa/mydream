const stories = [
    {
        title: "გაზაფხული",
        text: "გაზაფხული ყოველთვის თავიდან დაწყების იმედს მაძლევს. როცა ხეები ისევ მწვანდება, მგონია, რომ ადამიანსაც შეუძლია თავიდან დაიწყოს.",
        writer: "ნინო მაისურაძე",
        description: "ნინო 18 წლისაა. მას უყვარს მოკლე მოთხრობების წერა ადამიანურ ურთიერთობებსა და ყოველდღიურ ცხოვრებაზე."
    },

    {
        title: "ოცნება",
        text: "ყველას აქვს ერთი პატარა ოცნება, რომელსაც გულში მალავს. მთავარია, არასოდეს შეწყვიტო მისი სჯეროდეს.",
        writer: "ლუკა კაპანაძე",
        description: "ლუკა 19 წლისაა. ის წერს თანამედროვე ქართულ პროზასა და ფსიქოლოგიურ მოთხრობებს."
    },

    {
        title: "წვიმიანი დღე",
        text: "წვიმის ხმა ყოველთვის სიმშვიდეს მგვრის. თითქოს მთელი ქალაქი ცოტა ხნით ჩერდება და საკუთარ ფიქრებთან მარტო რჩება.",
        writer: "მარიამ გიორგაძე",
        description: "მარიამი 17 წლისაა. ის წერს ლექსებსა და მცირე ესეებს სიყვარულისა და ბუნების შესახებ."
    }
];

let currentStory = stories[0];

function changeStory() {
    const randomNumber = Math.floor(Math.random() * stories.length);

    currentStory = stories[randomNumber];

    document.getElementById("storyTitle").textContent =
        currentStory.title;

    document.getElementById("storyText").textContent =
        currentStory.text;

    document.getElementById("storyWriter").textContent =
        currentStory.writer;

    document.getElementById("storyWriterInfo").style.display =
        "none";
}

function showStoryWriter() {
    document.getElementById("storyWriterName").textContent =
        currentStory.writer;

    document.getElementById("storyWriterDescription").textContent =
        currentStory.description;

    document.getElementById("storyWriterInfo").style.display =
        "block";
}

function hideStoryWriter() {
    document.getElementById("storyWriterInfo").style.display =
        "none";
}

function openWriter(writer) {
    const writerName = document.getElementById("writerName");
    const writerDescription =
        document.getElementById("writerDescription");
    const writerText = document.getElementById("writerText");
    const writerDetails = document.getElementById("writerDetails");

    if (writer === "nino") {
        writerName.textContent = "ნინო მაისურაძე";

        writerDescription.textContent =
            "ნინო 18 წლისაა. მას უყვარს მოკლე მოთხრობების წერა ადამიანურ ურთიერთობებსა და ყოველდღიურ ცხოვრებაზე.";

        writerText.textContent =
            "გაზაფხული ყოველთვის თავიდან დაწყების იმედს მაძლევს. როცა ხეები ისევ მწვანდება, მგონია, რომ ადამიანსაც შეუძლია თავიდან დაიწყოს.";
    }

    if (writer === "luka") {
        writerName.textContent = "ლუკა კაპანაძე";

        writerDescription.textContent =
            "ლუკა 19 წლისაა. ის წერს თანამედროვე ქართულ პროზასა და ფსიქოლოგიურ მოთხრობებს.";

        writerText.textContent =
            "ყველას აქვს ერთი პატარა ოცნება, რომელსაც გულში მალავს. მთავარია, არასოდეს შეწყვიტო მისი სჯეროდეს.";
    }

    if (writer === "mariam") {
        writerName.textContent = "მარიამ გიორგაძე";

        writerDescription.textContent =
            "მარიამი 17 წლისაა. ის წერს ლექსებსა და მცირე ესეებს სიყვარულისა და ბუნების შესახებ.";

        writerText.textContent =
            "წვიმის ხმა ყოველთვის სიმშვიდეს მგვრის. თითქოს მთელი ქალაქი ცოტა ხნით ჩერდება და საკუთარ ფიქრებთან მარტო რჩება.";
    }

    writerDetails.style.display = "block";
}

function closeWriter() {
    document.getElementById("writerDetails").style.display = "none";
}