document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");
    const uploadMessage = document.getElementById("uploadMessage");

    const askBtn = document.getElementById("askBtn");
    const questionInput = document.getElementById("questionInput");
    const answerOutput = document.getElementById("answerOutput");

    uploadBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) {
            uploadMessage.textContent = "Please select a PDF to upload.";
            return;
        }

        uploadMessage.textContent = "Uploading and processing...";

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (res.ok) {
                uploadMessage.textContent = data.message;
            } else {
                uploadMessage.textContent = `Error: ${data.error}`;
            }
        } catch (err) {
            uploadMessage.textContent = `Upload failed: ${err}`;
        }
    });

    askBtn.addEventListener("click", async () => {
        const question = questionInput.value.trim();
        if (!question) {
            answerOutput.textContent = "Please enter a question.";
            return;
        }

        answerOutput.textContent = "Thinking...";

        try {
            const res = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            const data = await res.json();
            if (res.ok) {
                answerOutput.textContent = data.answer;
            } else {
                answerOutput.textContent = `Error: ${data.error}`;
            }
        } catch (err) {
            answerOutput.textContent = `Request failed: ${err}`;
        }
    });
});