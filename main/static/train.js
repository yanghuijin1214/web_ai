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

const labeltitle1 = document.querySelector('#labeltitle1');
const labeled1 = document.querySelector('.labeled1');
const labeltitle2 = document.querySelector('#labeltitle2');
const labeled2 = document.querySelector('.labeled2');
const Allb = document.querySelector('#Allb');
const Allimages = document.querySelector('.Allimages');
const Allimagestitle = document.querySelector('#Allimagestitle');
const L1B = document.querySelector('#L1B');
const L2B = document.querySelector('#L2B');

const imgbutton = document.querySelector('.imgbutton');
const imgx = document.querySelector('.imgx');
const select = document.querySelector('#select');

Allb.addEventListener('click', () => {
    labeltitle1.style.display = 'block';
    labeled1.style.display = 'block';
    labeltitle2.style.display = 'block';
    labeled2.style.display = 'block';
    Allimages.style.display = 'block';
    Allimagestitle.style.display = 'block';

})

L1B.addEventListener('click', () => {
    labeltitle1.style.display = 'block';
    labeled1.style.display = 'block';
    labeltitle2.style.display = 'none';
    labeled2.style.display = 'none';
    Allimages.style.display = 'none';
    Allimagestitle.style.display = 'none';
})

L2B.addEventListener('click', () => {
    labeltitle1.style.display = 'none';
    labeled1.style.display = 'none';
    labeltitle2.style.display = 'block';
    labeled2.style.display = 'block';
    Allimages.style.display = 'none';
    Allimagestitle.style.display = 'none';
})