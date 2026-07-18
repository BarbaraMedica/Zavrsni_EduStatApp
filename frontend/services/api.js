const API_URL = "http://127.0.0.1:5000";

export async function predict(data) {

    const response = await fetch(`${API_URL}/predict`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    return await response.json();
}