// extra javascript shit I don't wanna cram into the main file



function toggledark() {
	if (document.body.className == 'dark-mode') {
		document.body.className = "";
		localStorage.setItem('darkmode', false);
	}

	else {
		document.body.className = "dark-mode";
		localStorage.setItem('darkmode', true);
	}
}