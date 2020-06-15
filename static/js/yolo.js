const pageData = {
    image: null,
    imageType: null,
};

let boxes = [];

function updateCanvas() {
    const canvas = document.getElementById('imgCanvas');
    const ctx = canvas.getContext("2d");

    ctx.drawImage(img, 0, 0, imgSize.w, imgSize.h, 0, 0, canvas.width, canvas.height);
    for(const box of boxes) {
        ctx.lineWidth = 6;
        ctx.strokeStyle = box.color;
        ctx.strokeRect(box.x, box.y, box.w, box.h);
        
        function drawStroked(text, x, y) {
            ctx.font = "18px Verdana";
            ctx.strokeStyle = 'black';
            ctx.lineWidth = 5;
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

        // MOCKED DATA
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
        //         x: item.left * imgSize.k,
        //         y: item.top * imgSize.k,
        //         w: (item.right - item.left) * imgSize.k,
        //         h: (item.bottom - item.top) * imgSize.k,
        //         label: item.label + " " + item.accurancy.toFixed(2) + "%",
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
                        x: item.left * imgSize.k,
                        y: item.top * imgSize.k,
                        w: (item.right - item.left) * imgSize.k,
                        h: (item.bottom - item.top) * imgSize.k,
                        label: item.label + " " + item.accurancy.toFixed(2) + "%",
                        color: getRandomColor()
                    };
                    boxes.push(entry);
                }
                updateCanvas();
            }
        });
    });
};