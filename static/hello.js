$(document).ready(function () {
    $("#btnSearch").click(function () {
        let url = "camera.html?";
        let selected = document.querySelector('input[name=choice]:checked');
        if(selected)
            url = url + "choice=" + selected.value;
        window.location = url;
    });
});

