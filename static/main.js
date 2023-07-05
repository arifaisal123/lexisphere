$("#contactForm").on("submit", (event) => {
    const name = $("#name").val();
    const email = $("#email").val();
    const message = $("#message").val();

    if (name === "") {
        $("#nameError").css("display", "initial");
        event.preventDefault();
    } else {
        $("#nameError").css("display", "none");
    }

    if (!validateEmail(email)) {
        $("#emailError").css("display", "initial");
        event.preventDefault();
    } else {
        $("#emailError").css("display", "none");
    }

    if (message === "") {
        $("#messageError").css("display", "initial");
        event.preventDefault();
    } else {
        $("#messageError").css("display", "none");
    }
});

function validateEmail(emailid) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(emailid);
}