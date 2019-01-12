$(document).ready(function () {
    $("#btnSearch").click(function () {
        let url = "camera?";
        let selected = document.querySelector('input[name=filter]:checked');
        if(selected)
            url = url + "filter=" + selected.value;
        window.location = url;
    });

    $("#btnModel").click(function () {
        let url = "camera?filter=Harr Cascades&";
        let selected = document.querySelector('input[name=model]:checked');
        if(selected)
            url = url + "model=" + selected.value;
        window.location = url;
    });

    $("#btnModels").click(function () {
        let url = "models";
        window.location = url;
    });

    $("#btnMailSettings").click(function () {
        let url = "settings/mail";
        window.location = url;
    });
});

