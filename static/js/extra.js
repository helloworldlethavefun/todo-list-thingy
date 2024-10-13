// extra javascript shit I don't wanna cram into the main file



function toggledark() {
	if (document.body.className == 'dark-mode') {
		document.body.className = "";
<<<<<<< HEAD
		localStorage.setItem('darkmode', true);
=======
		localStorage.setItem('darkmode', False);
>>>>>>> 3b4e6c9b91193852ded3e985588e3da264054e72
	}

	else {
		document.body.className = "dark-mode";
<<<<<<< HEAD
		localStorage.setItem('darkmode', true);
=======
		localStorage.setItem('darkmode', True);
>>>>>>> 3b4e6c9b91193852ded3e985588e3da264054e72
	}
}
