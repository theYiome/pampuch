const images = {};
const imgTemplate = `
<div class="entry block">
    <div class="label block">{{label}}</div>
    <div class="img block"><img src="data:image/png;base64, {{base64}}" alt="{{label}} width="80" height="80""/></div>
    <button class="delete-button block" value="{{id}}">Usuń</button>
</div>
`;

function updateImages() {
    $.ajax({
        url: "/api/images",
        type: "GET",
        dataType: "json",
        success: function (data) {

            const doom = $("#images");
            doom.children().remove();

            for (const x of data) {
                const element = $.parseHTML(Mustache.render(imgTemplate, x));
                doom.append(element);
            }

            // delete action
            $(".delete-button").click(function () {
                const id = $(this).val();

                $.ajax({
                    url: "/api/delete/" + id,
                    type: "POST",
                    dataType: "text",
                    success: function (data) {
                        alert(data);
                        updateImages();
                    },
                    error: function (xhr, status, error) {
                        alert("Image could not be deleted :-(");
                    }
                });
            });
        },
        error: function (xhr, status, error) {
            const code = parseInt(xhr.status);
            console.log(code);
            console.log(status);
            console.log(error);
        }
    });
}

updateImages();