const pageData = {
    image: undefined,
    imageType: undefined,
    rects: undefined
}

window.onload = function() {
    const input = document.getElementById('imageUpload');
    input.addEventListener('change', updateImage, false);
}

function updateImage(event) {
    const canvas = document.getElementById('imgCanvas');
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    imageFile = event.target.files[0];
    console.log(imageFile)

    pageData.imageType = imageFile.type;

    const url = URL.createObjectURL(imageFile);
    const img = new Image();
    img.onload = function() {
        ctx.drawImage(img, 20, 20);    
    }
    img.src = url;

    const fileReader = new FileReader();
    fileReader.onload = function(e) {
        const data = new Uint8Array(e.target.result);
        pageData.image = base64encode(data);

        pageData.rects = [
            {
                label: "cat",
                x: 50,
                y: 32,
                w: 109,
                h: 123
            },
            {
                label: "cucumber",
                x: 321,
                y: 54,
                w: 768,
                h: 232
            },
        ];

        onPostSuccess = function(data) {
            console.log(data);
        }

        $.ajax({
            url: "/api/save",
            type: "POST",
            data: JSON.stringify(pageData),
            contentType: "application/json",
            dataType: "json",
            success: onPostSuccess
        });
    };
    fileReader.readAsArrayBuffer(imageFile);
}