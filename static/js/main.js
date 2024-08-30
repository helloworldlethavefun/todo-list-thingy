// Main Javascript File

// Just fetch some of the stuff from the html page so this file can manipulate them
const popupOverlay = document.getElementById('popup-overlay');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('closePopup');
const emailInput = document.getElementById('kanbanName');
let selectedList = "";
// fucntion used to create a kanban board
// use ajax async reqeusts to send the listname to the api endpoint
function createboard(kanbanName) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.status == 204) {
      console.log('request sent');
      window.location.reload();
    }
  };
  xhttp.open("POST", "/list-api/v1/create-board", true);
  xhttp.setRequestHeader("Content-type", "text/plain");
  xhttp.send(kanbanName);
}

function selectTheList(id) {
  selectedList = id;
  console.log(selectedList);
};

function createBoardList(listname) {
  const list = document.createElement('div');
  // list.id = listname;
  console.log(listname);
};

// Function to open the popup
function openPopup() {
    popupOverlay.style.display = 'block';
};


//function openListPopup() {
//    popup-overlay-list.style.display = 'block';
//};

// Function to close the popup
function closePopupFunc() {
    popupOverlay.style.display = 'none';
}

// If the user clicks on the x close the popup
closePopup.addEventListener('click', closePopupFunc);

// Close the popup when clicking outside the popup content
popupOverlay.addEventListener('click', function (event) {
if (event.target === popupOverlay) {
    closePopupFunc();
  }
});

// Take the name the user submitted then create that todolist file
function submitName() {
    const name = kanbanName.value;
    createboard(name);
    closePopupFunc();
}

function makeApiRequest(url, requestType, header=null content=null) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.status == 204) {
            console.log('Request success, 204')
          }
        };
        xhttp.open(requestType, 'http://127.0.0.1' + url, true);
        if (headers != null) {
          xhttp.setRequestHeader("Content-Type", "text/plain");
        };
        if (content == null) {
          xhttp.send()
        }; else {
          xhttp.send(content)
        };
      };
