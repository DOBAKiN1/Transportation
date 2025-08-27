try {
	const requestBtn = document.getElementById('submitRequestBtn');
	requestBtn.addEventListener('click', async function(event) {
		var weight = document.getElementById('weight').value;
		var cargoInformation = document.getElementById('cargoInformation').value;
		var size = document.getElementById('size').value;
		
		if (!weight || !cargoInformation || !size) {
			alert("Заповніть всі обов'язкові поля коректними значеннями");
		}
		else
		{
			event.preventDefault();
			
			const form = document.getElementById('requestForm');
			const formData = new FormData(form);
			const response = await fetch('/request', {
				method: 'POST',
				body: formData
			});
			
			if (response.ok) {
				const serverResponse = await response.json();
				if (serverResponse.message === 'Sended successfully') {
					alert("Запит додано");
					window.location.href = "http://127.0.0.1:5000/account";
				} 
			}
			else {
				console.error('Invalid sending');
				;
			}
		}
	});
	} catch (error) {
	
}

try {
	const driverAccept = document.getElementById('driverAcceptBtn');
	driverAccept.addEventListener('click', async function(event) {
		event.preventDefault();
		
		const form = document.getElementById('driverAcceptForm');
		const formData = new FormData(form);
		const response = await fetch('/driverAccept', {
			method: 'POST',
			body: formData
		});
		
		if (response.ok) {
			const serverResponse = await response.json();
			if (serverResponse.message === 'Accept successfully') {
				window.location.href = "http://127.0.0.1:5000/account";
			} 
		}
		else {
			console.error('Invalid sending');
			;
		}
		
	});
	} catch (error) {
	
}

try {
	const driverConfirm = document.getElementById('driverConfirmBtn');
	driverConfirm.addEventListener('click', async function(event) {
		event.preventDefault();
		
		const form = document.getElementById('driverConfirmForm');
		const response = await fetch('/driverConfirm', {
			method: 'POST',
		});
		
		if (response.ok) {
			const serverResponse = await response.json();
			if (serverResponse.message === 'Confirm successfully') {
				window.location.href = "http://127.0.0.1:5000/account";
			} 
		}
		else {
			console.error('Invalid sending');
			;
		}
		
	});
	} catch (error) {
	
}


try {
    const getReport = document.getElementById('getReportBtn');
    getReport.addEventListener('click', async function(event) {
        event.preventDefault();
        
        const form = document.getElementById('getReportForm');
        const response = await fetch('/getReport', {
            method: 'POST',
		});
        
        if (response.ok) {
            const blob = await response.blob(); 
            const url = window.URL.createObjectURL(blob);
            
            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = 'report.pdf'; 
            downloadLink.click(); 
			} else {
            console.error('Invalid sending');
		}
	});
	} catch (error) {
	
}


try {
    const addDriver = document.getElementById('addDriverBtn');
    addDriver.addEventListener('click', async function(event) {
        event.preventDefault();
        
        const form = document.getElementById('addDriverForm');
		const formData = new FormData(form);
        const response = await fetch('/addDriver', {
            method: 'POST',
			body: formData
		});
        
		if (response.ok) {
			const serverResponse = await response.json();
			if (serverResponse.message === 'Done successfully') {
				alert("Клієнт перетворений у водія");
			} 
		}
		else  {
			const serverResponse = await response.json();
			if (serverResponse.message === 'Client not found'){
				alert("Клієнта не знайдено");
			}
			else{
				alert("Щось пішло не так");
			}
			;
		}
		
		
	});
	} catch (error) {
	
}


