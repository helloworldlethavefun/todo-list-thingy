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


function toggledarkboard() {
	const boardContainer = document.getElementById('board-container');
	if (boardContainer.className == 'board-container-dark') {
		boardContainer.className = "board-container";
		localStorage.setItem('darkmode', false);
	}

	else {
		boardContainer.className = "board-container-dark";
		localStorage.setItem('darkmode', true);
	}
}