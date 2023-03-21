// const rowCount = value.split(/\r\n|\r|\n/).length;
// const targetTextarea = document.querySelector('#summary');

// if(rowCount < 4)
//     targetTextarea.style.height="100px"; //특정 줄 수 보다 작아지면 height가 이것보다 작아지지 않았으면 한다
// else
//     targetTextarea.style.height= (rowCount * 25) 



// const textarea = useRef();

// const handResizeHeight = () => {
//     textarea.current.style.height = 'auto';
//     textarea.current.style.height = textarea.current.scrollHeight + 'px';
// }



var textarea = document.getElementById("summary");

function resizeTextarea() {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";    
}

window.onload = function() {
    resizeTextarea();
}

textarea.addEventListener("input", function() {
    resizeTextarea();
  });
