const accuracy = document.querySelector('.accuracy');
const accuracyB = document.querySelector('.accuracyB');
const time = document.querySelector('.time');
const timeB = document.querySelector('.timeB');

accuracyB.addEventListener('click',()=>{
    accuracy.style.display='none'
    time.style.display='block'
})

timeB.addEventListener('click',()=>{
    accuracy.style.display='block'
    time.style.display='none'
})

const Sortmodal = document.querySelector('.Sortmodal');
const Sort = document.querySelector('.Sort')
const Sx = document.querySelector('.Sortx');

Sort.addEventListener('click',()=>{
    Sortmodal.style.display='block';
})

Sx.addEventListener('click',()=>{
    Sortmodal.style.display='none';
})