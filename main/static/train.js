const Importmodal = document.querySelector('.Importmodal');
const Import = document.querySelector('.Import')
const Ix = document.querySelector('.Importx');

const Sortmodal = document.querySelector('.Sortmodal');
const Sort = document.querySelector('.Sort')
const Sx = document.querySelector('.Sortx');


Import.addEventListener('click',()=>{
    Importmodal.style.display='block';
})

Ix.addEventListener('click',()=>{
    Importmodal.style.display='none';
})

Sort.addEventListener('click',()=>{
    Sortmodal.style.display='block';
})

Sx.addEventListener('click',()=>{
    Sortmodal.style.display='none';
})