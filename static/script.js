document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const predictBtn = document.getElementById('predict-btn');
    const resetBtn = document.getElementById('reset-btn');
    const resultContainer = document.getElementById('result-container');
    const resultText = document.getElementById('result-text');
    const barFill = document.getElementById('bar-fill');
    const confidenceText = document.getElementById('confidence-text');

    let currentFile = null;

    // Trigger file input
    uploadArea.addEventListener('click', () => fileInput.click());

    // Handle file selection
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and drop support
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#ccc';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ccc';
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    function handleFile(file) {
        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadArea.style.display = 'none';
            previewContainer.style.display = 'block';
            resultContainer.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    // Predict
    predictBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        predictBtn.textContent = 'Analyzing...';
        predictBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showResult(data);
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during prediction.');
        } finally {
            predictBtn.textContent = 'Analyze Tomato';
            predictBtn.disabled = false;
        }
    });

    function showResult(data) {
        resultContainer.style.display = 'block';
        resultText.textContent = data.class;

        // Color coding
        resultText.className = ''; // Reset classes
        if (data.class === 'Ripe') resultText.classList.add('result-ripe');
        else if (data.class === 'Unripe') resultText.classList.add('result-unripe');
        else resultText.classList.add('result-reject');

        const confidentPercent = (data.confidence * 100).toFixed(1);
        confidenceText.textContent = `Confidence: ${confidentPercent}%`;

        // Animate bar
        setTimeout(() => {
            barFill.style.width = `${confidentPercent}%`;
            // Color bar based on class
            if (data.class === 'Unripe') barFill.style.backgroundColor = '#32cd32';
            else barFill.style.backgroundColor = '#ff6347';
        }, 100);
    }

    // Reset
    resetBtn.addEventListener('click', () => {
        currentFile = null;
        fileInput.value = '';
        uploadArea.style.display = 'block';
        previewContainer.style.display = 'none';
        resultContainer.style.display = 'none';
        barFill.style.width = '0%';
    });
});
