document.getElementById("checkBtn").addEventListener("click", () => {
    const inputText = document.getElementById("inputText").value;
    fetch("/check_plagiarism", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `text=${encodeURIComponent(inputText)}`,
    })
        .then((response) => response.json())
        .then((data) => {
            document.getElementById("plagiarismPercentage").textContent = data.plagiarism_percentage.toFixed(2);
            document.getElementById("uniquePercentage").textContent = data.unique_percentage.toFixed(2);

            const plagiarizedList = document.getElementById("plagiarizedSentences");
            const uniqueList = document.getElementById("uniqueSentences");
            plagiarizedList.innerHTML = "";
            uniqueList.innerHTML = "";

            data.plagiarized_sentences.forEach(([sentence, similarity]) => {
                const li = document.createElement("li");
                li.textContent = `${sentence} (Similarity: ${(similarity * 100).toFixed(2)}%)`;
                plagiarizedList.appendChild(li);
            });

            data.unique_sentences.forEach((sentence) => {
                const li = document.createElement("li");
                li.textContent = sentence;
                uniqueList.appendChild(li);
            });
        });
});

document.getElementById("removeBtn").addEventListener("click", () => {
    const inputText = document.getElementById("inputText").value;
    fetch("/remove_plagiarism", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `text=${encodeURIComponent(inputText)}`,
    })
        .then((response) => response.json())
        .then((data) => {
            document.getElementById("rewrittenTextSection").style.display = "block";
            document.getElementById("rewrittenText").textContent = data.rewritten_text;
        });
});
