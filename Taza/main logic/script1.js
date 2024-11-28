<script>
    const loginForm = document.getElementById("loginForm");
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();
    const role = document.getElementById("role").value;
    if (role === "farmer") {
        window.location.href = "farmer-dashboard.html";
        } else if (role === "agribusiness") {
        window.location.href = "agribusiness-dashboard.html";
        } else if (role === "vendor") {
        window.location.href = "vendor-dashboard.html";
        }
    });
</script>
