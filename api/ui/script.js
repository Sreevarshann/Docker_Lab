async function predict() {
    const url = "http://localhost:8000/predict";

    // Collect form values
    const inputs = [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
    ];

    const data = {};
    inputs.forEach(id => {
        data[id] = parseFloat(document.getElementById(id).value) || 0;
    });

    // Call API
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    const outputBox = document.getElementById("result");

    if (result.prediction === 1) {
        outputBox.textContent = "⚠️ High Diabetes Risk";
        outputBox.style.background = "#ffe0e0";
        outputBox.style.color = "#c62828";
    } else {
        outputBox.textContent = "✅ Low Diabetes Risk";
        outputBox.style.background = "#e0ffe3";
        outputBox.style.color = "#2e7d32";
    }
}
