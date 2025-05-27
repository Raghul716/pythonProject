function startVoiceCommand() {
    fetch("/voice-command")
        .then(response => response.json())
        .then(data => {
            document.getElementById("status").innerText = 
                `Status: ${data.status}, Track: ${data.track || 'N/A'}`;
        });
}
