$('.form').find('input, textarea').on('keyup blur focus', function (e) {
	
	var $this = $(this),
	label = $this.prev('label');
	
	if (e.type === 'keyup') {
		if ($this.val() === '') {
			label.removeClass('active highlight');
			} else {
			label.addClass('active highlight');
		}
		} else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
		}   
		} else if (e.type === 'focus') {
		
		if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
		} 
		else if( $this.val() !== '' ) {
		    label.addClass('highlight');
		}
	}
	
});

$('.tab a').on('click', function (e) {
	
	e.preventDefault();
	
	$(this).parent().addClass('active');
	$(this).parent().siblings().removeClass('active');
	
	target = $(this).attr('href');
	
	$('.tab-content > div').not(target).hide();
	
	$(target).fadeIn(600);
	
});


const logInBtn = document.getElementById('logInBtn');
logInBtn.addEventListener('click', async function(event) {
	event.preventDefault();
	
	const form = document.getElementById('logInForm');
	const formData = new FormData(form);
	const response = await fetch('/logIn', {
		method: 'POST',
		body: formData
	});
	
	if (response.ok) {
		const serverResponse = await response.json();
		if (serverResponse.message === 'Logged in successfully') {
			window.location.href = "/";
		} 
	}
	else {
		alert('Invalid email or password');
		;
	}
});

const signUpBtn = document.getElementById('signUpBtn');
signUpBtn.addEventListener('click', async function(event) {
	event.preventDefault();
	
	const form = document.getElementById('signUpForm');
	const formData = new FormData(form);
	const response = await fetch('/signUp', {
		method: 'POST',
		body: formData
	});
	
	if (response.ok) {
		const serverResponse = await response.json();
		if (serverResponse.message === 'Sign up successfully') {
			window.location.href = "/";
		} 
	}
	else {
		alert('Заповніть всі необхідні форми коректними значеннями');
		;
	}
});


