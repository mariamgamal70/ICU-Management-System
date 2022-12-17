let userselect=document.getElementById('userchoice'); //select itself
let patientform=document.getElementById('patient'); //patientformdiv
let doctorform=document.getElementById('doctorform');
let nurseform=document.getElementById('nurseform');
let adminform=document.getElementById('adminform');
let receptionistform=document.getElementById('receptionistform');
let staffselectdiv=document.getElementById('staff');
let staffselect=document.getElementById('staffchoice');
let staffform=document.getElementById('staff2');

function checkstaffchangevalue(){
    if (this.value=='Doctor'){
        doctorform.style.display='block'
        nurseform.style.display='none';
        adminform.style.display='none';
        receptionistform.style.display='none';
    }
    else if(this.value=='Nurse'){
        doctorform.style.display='none'
        nurseform.style.display='block';
        adminform.style.display='none';
        receptionistform.style.display='none';
    }
    else if(this.value=='Admin'){
        doctorform.style.display='none'
        nurseform.style.display='none';
        adminform.style.display='block';
        receptionistform.style.display='none';
    }
    else{
        doctorform.style.display='none'
        nurseform.style.display='none';
        adminform.style.display='none';
        receptionistform.style.display='block';
    }
}

function checkuserchangevalue(){
    if (this.value=='Patient'){
        patientform.style.display='block';
        staffselectdiv.style.display='none';
    }
    else {
        patientform.style.display='none';
        staffselectdiv.style.display='block';
        staffselect.addEventListener('change',checkstaffchangevalue);
    }
}
userselect.addEventListener('change',checkuserchangevalue);