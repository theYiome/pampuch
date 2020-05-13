const pageData = {
    image: null,
    imageType: null,
    rects: null
};

let imgSize = {
    k: null,
    w: null,
    h: null
};

let img = null;

window.onload = function() {
    $("#imageUpload").change(updateImage);
    $("#send-button").click(function() {
        if(pageData.image === null) {
            alert("You need to load image and categorize it first!");
            return;
        } else if(pageData.rects === null || pageData.rects.length) {
            alert("Please pick and label some images!");
            return;
        } else {
            $.ajax({
                url: "/api/save",
                type: "POST",
                data: JSON.stringify(pageData),
                contentType: "application/json",
                dataType: "json",
                success: function(data) {
                    console.log(data);
                }
            });
        }
    });

    $("#imgCanvas").mouseup(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        console.log(cords);
    }).mousedown(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        console.log(cords);
    }).mousemove(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        console.log(cords);
    });
};

function updateImage(event) {
    const canvas = document.getElementById('imgCanvas');
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    imageFile = event.target.files[0];
    console.log(imageFile)

    pageData.imageType = imageFile.type;

    const url = URL.createObjectURL(imageFile);
    img = new Image();
    img.onload = function() {
        imgSize.w = this.width;
        imgSize.h = this.height;
        imgSize.k = 900 / imgSize.w;
        console.log(imgSize);
        const cnv = $("#imgCanvas");
        cnv.width(imgSize.w);
        cnv.height(imgSize.h);

        ctx.drawImage(img, 0, 0, imgSize.w, imgSize.h, 0, 0, canvas.width, canvas.height);
    };
    img.src = url;

    const fileReader = new FileReader();
    fileReader.onload = function(e) {
        const data = new Uint8Array(e.target.result);
        pageData.image = base64encode(data);
    };
    fileReader.readAsArrayBuffer(imageFile);
}

