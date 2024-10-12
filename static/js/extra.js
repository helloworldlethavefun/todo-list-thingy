// extra javascript shit I don't wanna cram into the main file

function toggledark() {
	if (document.body.className == 'dark-mode') {
		document.body.className = "";
	}

	else {
		document.body.className = "dark-mode";
	}
}