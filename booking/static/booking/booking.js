document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("myForm");
    form.addEventListener("submit", function (event) {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        let isChecked = false;

        checkboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                isChecked = true;
            }
        });

        if (!isChecked) {
            event.preventDefault();
            alert("Please select at least one checkbox.");
        }
    });
});
