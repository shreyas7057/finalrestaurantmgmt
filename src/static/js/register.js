// when there is error in username or email then submit btn is disable
const submitBtn = document.querySelector('.submit-btn');


// for username validation
const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');

// when username is available this msg will be shown by using this queryselector
const usernamesuccessOutput = document.querySelector('.usernamesuccessOutput');

// get what user is typing by this eventlistener
usernameField.addEventListener('keyup',(e)=>{

    console.log('7777777',7777777);

    const usernameVal = e.target.value;
    // console.log('username',usernameVal);

    // if available disp msg available
    usernamesuccessOutput.style.display = 'block';
    usernamesuccessOutput.textContent = `Checking ${usernameVal}`;


    // when user deletes invalid username or press backspace then invalid goes then error also goes 
    usernameField.classList.remove('is-invalid');
    feedBackArea.style.display='none';

    // fetch api call
    if(usernameVal.length>0) {

        fetch("/authentication/validate-username",{
            body:JSON.stringify({'username':usernameVal}),
            method:'POST',
        }).then(res=>res.json()).then(data=>{
            // console.log('data',data);

            usernamesuccessOutput.style.display = 'none';

            if(data.username_error) {
                usernameField.classList.add('is-invalid');

                feedBackArea.style.display='block';
                
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`
                submitBtn.setAttribute('disabled','disabled');
                submitBtn.disabled = true;
            }
            else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }

});



// for email validation
const emailField = document.querySelector('#emailField');
const emailfeedBackArea = document.querySelector('.emailfeedBackArea');


emailField.addEventListener('keyup',(e)=>{


    console.log('7777777',7777777);

    const emailVal = e.target.value;
    // console.log('email',emailVal);


    // when user deletes invalid username or press backspace then invalid goes then error also goes 
    emailField.classList.remove('is-invalid');
    emailfeedBackArea.style.display='none';

    // fetch api call
    if(emailVal.length>0) {

        fetch("/authentication/validate-email",{
            body:JSON.stringify({'email':emailVal}),
            method:'POST',
        }).then(res=>res.json()).then(data=>{
            // console.log('data',data);

            if(data.email_error) {
                // here btn will be disable of submit
                submitBtn.setAttribute('disabled','disabled');
                submitBtn.disabled = true;
                emailField.classList.add('is-invalid');

                emailfeedBackArea.style.display='block';
                
                emailfeedBackArea.innerHTML=`<p>${data.email_error}</p>`

            }else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }

});


// for toggle button::: show password button
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');


const handleToggleInput= (e) => {
    if(showPasswordToggle.textContent==='SHOW') {
        showPasswordToggle.textContent = "HIDE";

        // showing the characters in password field

        passwordField.setAttribute("type","text");

    }
    else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type","password");
    }

}


showPasswordToggle.addEventListener('click',handleToggleInput);