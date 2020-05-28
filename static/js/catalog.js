const images = {};
const sectionTemplate = `
<div id="section-{{label}}" class="section block">
    <div class="label block" style="background-color: {{color}}">{{label}}</div>
    {{{imagesDiv}}}
</div>
`;

const imagesTemplate = `
<div id="images-{{id}}" class="images">
</div>
`;

const imgTemplate = `
<div class="entry block">
    <img class="img" src="data:image/png;base64, {{base64}}" width="93" height="93"/>
    <button class="delete-button block" value="{{id}}">Delete</button>
</div>
`;

function updateImages() {
    $.ajax({
        url: "/api/images",
        type: "GET",
        dataType: "json",
        success: function (data) {
            
            const doom = $("#content");
            doom.children().remove();

            for (const value of data) {

                const label = value.label;
                const imagesid = "#images-" + label;
                if($(imagesid).length === 0){
                    const sectionid = "#section-" + label;
                    const imagesDiv = Mustache.render(imagesTemplate, {id: label});
                    const sectionDiv = Mustache.render(sectionTemplate, {
                        imagesDiv: imagesDiv,
                        label: label,
                        color: stringToColor(label)
                    });
                    console.log(sectionDiv);
                    const sectionObj = $.parseHTML(sectionDiv);
                    doom.append(sectionObj);
                }

                const obj = $.parseHTML(Mustache.render(imgTemplate, value));
                $(imagesid).append(obj);
            }

            // delete action
            $(".delete-button").click(function () {
                const id = $(this).val();

                $.ajax({
                    url: "/api/images/delete/" + id,
                    type: "GET",
                    dataType: "text",
                    success: function (data) {
                        // alert(data);
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