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

function renderInputs() {
    const inputs = $(".inputs");
    inputs.children().remove();
    boxArray.forEach(function(item, index) {
        const str = `
            <div class="entry">
                <div class="field block" style="background-color: {{color}}"></div>
                <div class="input-box">
                    <input class="field block input-label" type="text" placeholder="label" value="{{value}}" id="{{id}}"/>
                    <button class="field block" onclick="deleteInput({{id}})" type="button">Delete box</button>
                </div>
            </div>
        `;
        const element = $.parseHTML(Mustache.render(str, {color: item.color, id: index, value: item.label}));
        inputs.append(element);
    });

    $(".input-label").change(function() {
        labelsArr = [];
        $(".input-label").each(function() {
            labelsArr.push($(this).val());
        });

        for(let i = 0; i < boxArray.length; i++) {
            boxArray[i].label = labelsArr[i];
        }
    });
}

function deleteInput(id) {
    console.log(id);
    boxArray.splice(id, 1);
    renderInputs();
    updateCanvas();
}

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
        }

        if(boxArray.length == 0) {
            alert("Please pick and label some images!");
            return;
        }
        
        pageData.rects = [];
        boxArray.forEach(function(item, index) {
            if(item.w < 0) {
                item.x = item.x + item.w;
                item.w = -item.w;
            }

            if(item.h < 0) {
                item.y = item.y + item.h;
                item.h = -item.h;
            }

            const rect = {
                x: Math.round(item.x),
                y: Math.round(item.y),
                w: Math.round(item.w),
                h: Math.round(item.h),
                label: item.label,
            };
            pageData.rects.push(rect);
        });
        
        $.ajax({
            url: "/api/save",
            type: "POST",
            data: JSON.stringify(pageData),
            contentType: "application/json",
            success: function(data) {
                console.log(data);
                boxArray.length = 0;
                updateCanvas();
                renderInputs();
                alert("All labels are saved successfully!")
            },
            error: function(xhr, status, error) {
                const code = parseInt(xhr.status);
                console.log(code);
                console.log(status);
                console.log(error);
            }
        });
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
        renderInputs();
    }).mousedown(function(evt) {
        let offset = $(this).offset();
        let cords = {
            x: evt.pageX - offset.left,
            y: evt.pageY - offset.top,
        };
        mouseContext.isDown = true;
        mouseContext.currentRec = {
            color: getRandomColor(),
            label: "",
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

