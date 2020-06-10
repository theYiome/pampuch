const pageData = {
    image: null,
    imageType: null,
};

let imgSize = {
    k: null,
    w: null,
    h: null
};

let boxes = [];

let img = null;

function updateCanvas() {
    const canvas = document.getElementById('imgCanvas');
    const ctx = canvas.getContext("2d");

    ctx.drawImage(img, 0, 0, imgSize.w, imgSize.h, 0, 0, canvas.width, canvas.height);
    for(const box of boxes) {
        ctx.lineWidth = 6;
        ctx.strokeStyle = box.color;
        ctx.strokeRect(box.x, box.y, box.w, box.h);
        
        function drawStroked(text, x, y) {
            ctx.font = "24px Verdana";
            ctx.strokeStyle = 'black';
            ctx.lineWidth = 8;
            ctx.strokeText(text, x, y);
            ctx.fillStyle = 'white';
            ctx.fillText(text, x, y);
        }

        drawStroked(box.label, box.x, box.y - 12);
    }
}

window.onload = function() {
    $("#imageUpload").change(updateImage);

    $("#send-button").click(function() {
        if(pageData.image === null) {
            alert("You need to load image first!");
            return;
        }

        // data = [
        //     {
        //         "label": "cat",
        //         "accurancy": 5.2,
        //         "left": 300,
        //         "top": 700,
        //         "right": 700,
        //         "bottom": 900
        //     },
        //     {
        //         "label": "dog",
        //         "accurancy": 92.3,
        //         "left": 200,
        //         "top": 200,
        //         "right": 350,
        //         "bottom": 500
        //     }
        // ];

        // boxes = [];

        // for(const item of data) {
        //     const entry = {
        //         x: item.left,
        //         y: item.top,
        //         w: item.right - item.left,
        //         h: item.bottom - item.top,
        //         label: item.label + " " + item.accurancy + "%",
        //         color: getRandomColor()
        //     };
        //     boxes.push(entry);
        // }
        // updateCanvas();
        $.ajax({
            url: "/api/yolo",
            type: "POST",
            data: JSON.stringify(pageData),
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                console.log(data);

                boxes = [];

                for(const item of data) {
                    const entry = {
                        x: item.left,
                        y: item.top,
                        w: item.right - item.left,
                        h: item.bottom - item.top,
                        label: item.label + " " + Math.round(item.accurancy) + "%",
                        color: getRandomColor()
                    };
                    boxes.push(entry);
                }
                updateCanvas();
            }
        });
    });
};

function updateImage(event) {
    const canvas = document.getElementById('imgCanvas');
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    imageFile = event.target.files[0];
    pageData.imageType = imageFile.type;
    boxes = [];

    const url = URL.createObjectURL(imageFile);
    img = new Image();
    img.onload = function() {
        imgSize.w = this.width;
        imgSize.h = this.height;
        imgSize.k = 900 / imgSize.w;
        console.log(imgSize);
        const cnv = $("#imgCanvas");
        canvas.width = imgSize.w;
        canvas.height = imgSize.h;
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

