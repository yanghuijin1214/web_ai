const labeltitle1 = document.querySelector('#labeltitle1');
const labeled1 = document.querySelector('.labeled1');
const labeltitle2 = document.querySelector('#labeltitle2');
const labeled2 = document.querySelector('.labeled2');
const unlabeltitle = document.querySelector('#unlabeltitle');
const unlabel = document.querySelector('.unlabel');
const Allb = document.querySelector('#Allb');
const L1B = document.querySelector('#L1B');
const L2B = document.querySelector('#L2B');
const UnlabelB = document.querySelector('#UnlabelB');

const imgbutton = document.querySelector('.imgbutton');
const imgx = document.querySelector('.imgx');
const select = document.querySelector('#select');

Allb.addEventListener('click', () => {
    labeltitle1.style.display = 'block';
    labeled1.style.display = 'block';
    labeltitle2.style.display = 'block';
    labeled2.style.display = 'block';
    unlabeltitle.style.display = 'block';
    unlabel.style.display = 'block';

})

L1B.addEventListener('click', () => {
    labeltitle1.style.display = 'block';
    labeled1.style.display = 'block';
    labeltitle2.style.display = 'none';
    labeled2.style.display = 'none';
    unlabeltitle.style.display = 'none';
    unlabel.style.display = 'none';
})

L2B.addEventListener('click', () => {
    labeltitle1.style.display = 'none';
    labeled1.style.display = 'none';
    labeltitle2.style.display = 'block';
    labeled2.style.display = 'block';
    unlabeltitle.style.display = 'none';
    unlabel.style.display = 'none';
})

UnlabelB.addEventListener('click', () => {
    labeltitle1.style.display = 'none';
    labeled1.style.display = 'none';
    labeltitle2.style.display = 'none';
    labeled2.style.display = 'none';
    unlabeltitle.style.display = 'block';
    unlabel.style.display = 'block';
})


const Importmodal = document.querySelector('.Importmodal');
const Import = document.querySelector('.Import');
const Ix = document.querySelector('.Importx');

const Sortmodal = document.querySelector('.Sortmodal');
const Sort = document.querySelector('.Sort');
const Sx = document.querySelector('.Sortx');

const trainB = document.querySelector('.trainB');
const yes = document.querySelector('.yes');
const no = document.querySelector('.no');
const Trainmodal1 = document.querySelector('.Trainmodal1');
const Trainmodal2 = document.querySelector('.Trainmodal2');
const Trainmodal2x = document.querySelector('.Trainmodal2x');
const Trainmodal3 = document.querySelector('.Trainmodal3');
const Trainmodal3x = document.querySelector('.Trainmodal3x');
const back = document.querySelector('.back');
const ok = document.querySelector('.ok');

Import.addEventListener('click', () => {
    Importmodal.style.display = 'block';
    if (Sortmodal.style.display = 'block')
        Sortmodal.style.display = 'none';
})

Import.addEventListener('click', () => {
    Importmodal.style.display = 'block';
    if (Sortmodal.style.display = 'block')
        Sortmodal.style.display = 'none';
})

Ix.addEventListener('click', () => {
    Importmodal.style.display = 'none';
})

Sort.addEventListener('click', () => {
    Sortmodal.style.display = 'block';
    if (Importmodal.style.display = 'block')
        Importmodal.style.display = 'none';
})

Sx.addEventListener('click', () => {
    Sortmodal.style.display = 'none';
})

trainB.addEventListener('click', () => {
    Trainmodal1.style.visibility = 'visible';
    back.style.visibility='visible';
})

yes.addEventListener('click', () => {
    var queryString=$("form[name=Train]").serialize();
    console.log(queryString);
    Trainmodal2.style.visibility = 'visible';
    setTimeout(function(){
        var j=$.ajax({
            type:"POST",
            url:"/train/",
            cache:false,
            data:queryString,
            async:false,
            dataType:'json',
            error:function(){
                alert("Ajax post request to the following script failed : /train/");
            },
            success:function(){
                window.location.href='/train/'; //train페이지로 넘어가기
            }
        })
    },0);
})


no.addEventListener('click', () => {
    Trainmodal1.style.visibility = 'hidden';
    back.style.visibility='hidden';
})

Trainmodal2x.addEventListener('click', () => {
    Trainmodal2.style.visibility = 'hidden';
    Trainmodal1.style.visibility = 'hidden';
    back.style.visibility='hidden';
})

Trainmodal3x.addEventListener('click', () => {
    Trainmodal3.style.visibility = 'hidden';
    Trainmodal2.style.visibility = 'hidden';
    Trainmodal1.style.visibility = 'hidden';
    back.style.visibility='hidden';
})

ok.addEventListener('click', () => {
    Trainmodal3.style.visibility = 'hidden';
    Trainmodal2.style.visibility = 'hidden';
    Trainmodal1.style.visibility = 'hidden';
    back.style.visibility='hidden';
})

function changeValue(obj) {
    document.imageForm.submit();
}

function press1(f) {
    if (f.keyCode == 13) {
        label1.submit
    }
}

function press2(f) {
    if (f.keyCode == 13) {
        label2.submit
    }
}