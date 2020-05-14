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

const mouseContext = {
    isDown: false,
    currentRec: null,
};

const boxArray = [];

function updateCanvas() {
    const canvas = document.getElementById('imgCanvas');
    const ctx = canvas.getContext("2d");

    if(img != null) {
        ctx.lineWidth = 4;
        ctx.drawImage(img, 0, 0, imgSize.w, imgSize.h, 0, 0, canvas.width, canvas.height);
        boxArray.forEach(function(item, index) {
            const box = item;
            ctx.strokeStyle = box.color;
            ctx.strokeRect(box.x, box.y, box.w, box.h);
        });

        if(mouseContext.currentRec != null) {
            const box = mouseContext.currentRec;
            ctx.strokeStyle = box.color;
            ctx.strokeRect(box.x, box.y, box.w, box.h);
        }
    }
}

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
        boxArray.push(mouseContext.currentRec);
        mouseContext.isDown = false;
        mouseContext.currentRec = null;
        console.log(cords);
        updateCanvas();
    }).mousedown(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        mouseContext.isDown = true;
        mouseContext.currentRec = {
            color: "#" + Math.floor(Math.random()*16777215).toString(16),
            label: "label",
            x: cords.x,
            y: cords.y,
            w: 0,
            h: 0
        };
        console.log(cords);
        updateCanvas();
    }).mousemove(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        if(mouseContext.currentRec != null && mouseContext.isDown) {
            mouseContext.currentRec.w = cords.x - mouseContext.currentRec.x;
            mouseContext.currentRec.h = cords.y - mouseContext.currentRec.y;
            updateCanvas();
        }
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

