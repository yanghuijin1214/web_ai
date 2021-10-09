const Importmodal = document.querySelector('.Importmodal');
const Import = document.querySelector('.Import');
const Ix = document.querySelector('.Importx');

const Sortmodal = document.querySelector('.Sortmodal');
const Sort = document.querySelector('.Sort');
const Sx = document.querySelector('.Sortx');

Import.addEventListener('click',()=>{
    Importmodal.style.display='block';
    if (Sortmodal.style.display='block')
        Sortmodal.style.display='none';
})

Ix.addEventListener('click',()=>{
    Importmodal.style.display='none';
})

Sort.addEventListener('click',()=>{
    Sortmodal.style.display='block';
    if (Importmodal.style.display='block')
        Importmodal.style.display='none';
})

Sx.addEventListener('click',()=>{
    Sortmodal.style.display='none';
})

function changeValue(obj){
    document.imageForm.submit();
}