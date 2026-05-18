const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "/login-page";
}


window.onload = () => {

    loadHistory();
    loadTickets();
};



async function loadHistory() {

    const chatBox =
        document.getElementById("chat-box");

    const historyList =
        document.getElementById("history-list");

    historyList.innerHTML = "";

    chatBox.innerHTML = "";

    const response = await fetch(
        "/history",
        {
            headers: {
                "Authorization":
                    `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    data.forEach(chat => {

        historyList.innerHTML += `

            <div class="history-item">

                <div class="history-text">
                    ${chat.user_message}
                </div>

                <button
                    class="delete-btn"
                    onclick="deleteChat(${chat.id})"
                >
                    ✕
                </button>

            </div>
        `;

        chatBox.innerHTML += `

            <div class="message user">
                ${chat.user_message}
            </div>

            <div class="message ai">
                ${chat.ai_response}
            </div>
        `;
    });

    chatBox.scrollTop =
        chatBox.scrollHeight;
}

//Send Message

async function sendMessage() {

    const promptInput =
        document.getElementById("prompt");

    const message =
        promptInput.value;

    if (message.trim() === "") {
        return;
    }

    const chatBox =
        document.getElementById("chat-box");

    chatBox.innerHTML += `

        <div class="message user">
            ${message}
        </div>
    `;

    promptInput.value = "";

    chatBox.innerHTML += `

        <div class="message ai" id="loading">
            AI is typing...
        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;

    try {

        const screenshotName =
            await uploadScreenshot();

        const response = await fetch(
            "/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({
                    message: message,
                    screenshot: screenshotName
                })
            }
        );

        const data =
            await response.json();

        document.getElementById(
            "loading"
        ).remove();

        chatBox.innerHTML += `

            <div class="message ai">
                ${data.response}
            </div>
        `;

        chatBox.scrollTop =
            chatBox.scrollHeight;

        loadHistory();

    } catch (error) {

        document.getElementById(
            "loading"
        ).remove();

        chatBox.innerHTML += `

            <div class="message ai">
                Error getting AI response
            </div>
        `;
    }
}



async function uploadScreenshot() {

    const fileInput =
        document.getElementById(
            "screenshot"
        );

    const file =
        fileInput.files[0];

    if (!file) {
        return null;
    }

    const formData =
        new FormData();

    formData.append("file", file);

    const response = await fetch(
        "/upload-screenshot",
        {
            method: "POST",
            body: formData
        }
    );

    const data =
        await response.json();

    return data.filename;
}



document.getElementById(
    "prompt"
).addEventListener(
    "keypress",
    function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


// DELETE CHAT


async function deleteChat(chatId) {

    await fetch(
        `/delete-chat/${chatId}`,
        {
            method: "DELETE"
        }
    );

    loadHistory();
}



function logout() {

    localStorage.removeItem(
        "token"
    );

    window.location.href =
        "/login-page";
}



async function getSystemInfo() {

    const response =
        await fetch("/system-info");

    const data =
        await response.json();

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    chatBox.innerHTML += `
        <div class="message ai">

            <h3>System Diagnostics</h3>

            <p><b>OS:</b> ${data.os}</p>

            <p><b>Processor:</b> ${data.processor}</p>

            <p><b>CPU Usage:</b> ${data.cpu_usage}%</p>

            <p><b>RAM Usage:</b> ${data.ram_usage}%</p>

            <p><b>Disk Usage:</b> ${data.disk_usage}%</p>

        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;
}

// TICKET MODAL


function openTicketModal() {

    document.getElementById(
        "ticket-modal"
    ).style.display = "flex";
}


async function createTicket() {

    const title =
        document.getElementById(
            "ticket-title"
        ).value;

    const description =
        document.getElementById(
            "ticket-description"
        ).value;

    const priority =
        document.getElementById(
            "ticket-priority"
        ).value;

    const response = await fetch(
        "/create-ticket",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",

                "Authorization":
                    `Bearer ${token}`
            },

            body: JSON.stringify({
                title,
                description,
                priority
            })
        }
    );

    const data =
        await response.json();

    alert(data.message);

    document.getElementById(
        "ticket-modal"
    ).style.display = "none";

    loadTickets();
}


async function loadTickets() {

    const response = await fetch(
        "/tickets",
        {
            headers: {
                "Authorization":
                    `Bearer ${token}`
            }
        }
    );

    const data =
        await response.json();

    const ticketList =
        document.getElementById(
            "ticket-list"
        );

    ticketList.innerHTML = "";

    data.forEach(ticket => {

        ticketList.innerHTML += `

            <div class="ticket-item">

                <div class="ticket-top">

                    <h4>
                        ${ticket.title}
                    </h4>

                    <button
                        class="ticket-delete-btn"
                        onclick="deleteTicket(${ticket.id})"
                    >
                        ✕
                    </button>

                </div>

                <p>
                    ${ticket.priority}
                </p>

                <span class="ticket-status">
                    ${ticket.status}
                </span>

                ${ticket.status !== "Closed"
                ?
                `
                    <button
                        class="close-ticket-btn"
                        onclick="closeTicket(${ticket.id})"
                    >
                        Close Ticket
                    </button>
                    `
                :
                ""
            }

            </div>
        `;
    });
}


async function closeTicket(ticketId) {

    await fetch(
        `/close-ticket/${ticketId}`,
        {
            method: "PUT"
        }
    );

    loadTickets();
}


async function deleteTicket(ticketId) {

    await fetch(
        `/delete-ticket/${ticketId}`,
        {
            method: "DELETE"
        }
    );

    loadTickets();
}




