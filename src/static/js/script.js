function Mudarestado(el, el2) {
    var display = document.getElementById(el).style.display;
    if(display == "none"){
        document.getElementById(el).style.display = 'block';
    } else {
        document.getElementById(el).style.display = 'none';
    }
}



function marcarSelecionado(categoria) {
    console.log(categoria)
    let div = document.getElementsByClassName(categoria)[0];
    console.log(div)
    div.style.backgroundColor = 'rgb(252,205,48)';
    div.style.color = 'rgb(20,20,20)';
}
