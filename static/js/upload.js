const imgName = document.querySelector('#img-name')
const wrapper = document.querySelector('.wrapper')
const imgCancle = document.querySelector('#img-cancle')
const defaultBtn = document.querySelector('#default-btn')
const customtBtn = document.querySelector('#custom-btn')
const img = document.querySelector('img')
let deleteExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\}\,\$\=\!\-\#\(\)\.\%\+\~\_]+$/;
function defaultBtnActive() {
    defaultBtn.click();
}
defaultBtn.addEventListener("change",function (){
    const file = this.files[0];
    if (file){
        const reader = new FileReader();
        reader.onload = function () {
            const result = reader.result;
            img.src = result;
            img.style = ''
            wrapper.classList.add("active");
        }
        imgCancle.addEventListener("click", function(){
            img.src = "";
            wrapper.classList.remove("active");

        });
        reader.readAsDataURL(file)
    }
    if(this.value){
        let valueStore = this.value.match(deleteExp);
        imgName.textContent =valueStore;
    }
});




// $('#fileup').change(function(){
// //here we take the file extension and set an array of valid extensions
//     var res=$('#fileup').val();
//     var arr = res.split("\\");
//     var filename=arr.slice(-1)[0];
//     filextension=filename.split(".");
//     filext="."+filextension.slice(-1)[0];
//     valid=[".jpg",".png",".jpeg",".bmp"];
// //if file is not valid we show the error icon, the red alert, and hide the submit button
//     if (valid.indexOf(filext.toLowerCase())==-1){
//         $( ".imgupload" ).hide("slow");
//         $( ".imgupload.ok" ).hide("slow");
//         $( ".imgupload.stop" ).show("slow");
//
//         $('#namefile').css({"color":"red","font-weight":700});
//         $('#namefile').html("File "+filename+" is not  pic!");
//
//         $( "#submitbtn" ).hide();
//         $( "#fakebtn" ).show();
//     }else{
//         //if file is valid we show the green alert and show the valid submit
//         $( ".imgupload" ).hide("slow");
//         $( ".imgupload.stop" ).hide("slow");
//         $( ".imgupload.ok" ).show("slow");
//
//         $('#namefile').css({"color":"green","font-weight":700});
//         $('#namefile').html(filename);
//
//         $( "#submitbtn" ).show();
//         $( "#fakebtn" ).hide();
//     }
// });