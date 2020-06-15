const pageData = {
    image: null,
    imageType: null,
    box: null
};

let isMouseDown = false;

function updateCanvas() {
    const canvas = document.getElementById('imgCanvas');
    const ctx = canvas.getContext("2d");

    const box = pageData.box;
    if(img != null) {
        ctx.drawImage(img, 0, 0, imgSize.w, imgSize.h, 0, 0, canvas.width, canvas.height);
        if(box != null) {
            ctx.lineWidth = 4;
            ctx.strokeStyle = box.color;
            ctx.strokeRect(box.x, box.y, box.w, box.h);
        }
    }
    console.log(pageData.box);
}

window.onload = function() {
    $("#imageUpload").change(updateImage);

    $("#delete-button").click(function() {
        pageData.box = null;
        $("#guess").html("");
        updateCanvas();
    });

    $("#send-button").click(function() {
        if(pageData.image === null) {
            alert("You need to load image first!");
            return;
        }

        if(pageData.box === null) {
            alert("Please part of and image for recognition!");
            return;
        }
        
        pageData.box = {
            x: Math.round(pageData.box.x / imgSize.k),
            y: Math.round(pageData.box.y / imgSize.k),
            w: Math.round(pageData.box.w / imgSize.k),
            h: Math.round(pageData.box.h / imgSize.k),
        };

        $.ajax({
            url: "/api/recognize",
            type: "POST",
            data: JSON.stringify(pageData),
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                console.log(data);
                $("#guess").html(data.label);
            }
        });
        
        pageData.box = null;
    });

    $("#imgCanvas").mouseup(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        isMouseDown = false;
        const box = pageData.box;
        if(box != null) {
            const item = box;
            if(item.w < 0) {
                item.x = item.x + item.w;
                item.w = -item.w;
            }

            if(item.h < 0) {
                item.y = item.y + item.h;
                item.h = -item.h;
            }

            box.x = Math.round(box.x);
            box.y = Math.round(box.y);
            box.h = Math.round(box.h);
            box.w = Math.round(box.w);
            updateCanvas();
        }

    }).mousedown(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        isMouseDown = true;
        pageData.box = {
            color: getRandomColor(),
            x: cords.x,
            y: cords.y,
            w: 0,
            h: 0
        };
        updateCanvas();

    }).mousemove(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        const box = pageData.box;
        if(box != null && isMouseDown) {
            box.w = cords.x - box.x;
            box.h = cords.y - box.y;
            updateCanvas();
        }
    });
};
