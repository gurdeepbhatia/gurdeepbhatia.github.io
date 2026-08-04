const status = document.getElementById("status");
const fileStatus = document.getElementById("fileStatus");
const dailyBtn = document.getElementById("dailyBtn");
const marketBtn = document.getElementById("marketBtn");
let uploadedFile = null;

// Fetch and display version on page load
async function fetchVersion() {
    try {
        const response = await fetch('/api/version');
        const data = await response.json();
        const versionElement = document.getElementById('versionNumber');
        if (versionElement && data.version) {
            versionElement.innerText = data.version;
        }
    } catch (e) {
        console.error('Failed to fetch version:', e);
    }
}

// Load version when page loads
document.addEventListener('DOMContentLoaded', fetchVersion);

function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) {
        fileStatus.innerText = "";
        fileStatus.style.color = "";
        dailyBtn.disabled = true;
        marketBtn.disabled = true;
        uploadedFile = null;
        return;
    }

    // Validate file type
    if (!file.name.endsWith('.csv')) {
        fileStatus.innerText = "Error: Please upload a CSV file.";
        fileStatus.style.color = "red";
        dailyBtn.disabled = true;
        marketBtn.disabled = true;
        uploadedFile = null;
        return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        fileStatus.innerText = "Error: File size exceeds 10MB.";
        fileStatus.style.color = "red";
        dailyBtn.disabled = true;
        marketBtn.disabled = true;
        uploadedFile = null;
        return;
    }

    uploadedFile = file;
    fileStatus.innerText = `File "${file.name}" selected (${(file.size / 1024).toFixed(2)} KB)`;
    fileStatus.style.color = "green";
    dailyBtn.disabled = false;
    marketBtn.disabled = false;
}

async function prepareChart(chartType) {

    if (!uploadedFile) {
        status.innerText = "Error: Please upload a CSV file first.";
        status.style.color = "red";
        return;
    }

    status.innerText = "Preparing chart...";
    status.style.color = "";

    try {
        const formData = new FormData();
        formData.append('file', uploadedFile);

        const response = await fetch(`/prepare-chart/${chartType}`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            status.style.color = "green";
            // Display message with filepath if available
            if (result.filepath) {
                status.innerText = `${result.message}\nFile saved at: ${result.filepath}`;
            } else {
                status.innerText = result.message;
            }
        } else {
            status.style.color = "red";
            status.innerText = result.message;
        }

    } catch (e) {
        status.innerText = "Unable to contact server.";
        status.style.color = "red";
    }

}