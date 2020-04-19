const pageData = {
    image: undefined,
    rects: undefined
}

window.onload = function() {
    const input = document.getElementById('imageUpload');
    input.addEventListener('change', updateImage, false);
}

function updateImage(event) {
    const canvas = document.getElementById('imgCanvas')
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    imageFile = event.target.files[0];
    const url = URL.createObjectURL(imageFile);
    const img = new Image();
    img.onload = function() {
        ctx.drawImage(img, 20, 20);    
    }
    img.src = url;
    console.log(imageFile);

    const fileReader = new FileReader();
    fileReader.onload = function(e) {
        const data = new Uint8Array(e.target.result);

        pageData.image = base64encode(data);
        pageData.rects = [
            {
                x: 50,
                y: 32,
                w: 109,
                h: 123
            },
            {
                x: 321,
                y: 54,
                w: 768,
                h: 232
            },
        ];
        console.log(pageData)
    };
    fileReader.readAsArrayBuffer(imageFile);
    // console.log(imageData)
    // console.log(JSON.stringify(imageData))
}