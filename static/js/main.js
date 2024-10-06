// Main Javascript File for the kanban board

// Just fetch some of the stuff from the html page so this file can manipulate them
const popupOverlay = document.getElementById('popup-overlay');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('closePopup');
const emailInput = document.getElementById('kanbanName');
const listPopup = document.getElementById('popup-overlay-list');
const closeListPopup = document.getElementById('closeListPopup');
let selectedList = "";

let isModalOpen = false;

// Function to drag the container
const dragElement = (element, container) => {
  let posX = 0, posY = 0, mouseX = 0, mouseY = 0;

  element.onmousedown = dragMouseDown;

  function dragMouseDown(e) {
    if (isModalOpen) {
      return;
    }

    if (e.target.tagName.toLowerCase() === 'p') {
      e.stopPropagation();
      return;
    }

      e.preventDefault();
      mouseX = e.clientX;
      mouseY = e.clientY;

      elementX = element.offsetLeft;
      elementY = element.offsetTop;

      document.onmouseup = closeDragElement;
      document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e.preventDefault();

        const deltaX = e.clientX - mouseX;
        const deltaY = e.clientY - mouseY;

        element.style.left = (elementX + deltaX) + "px";
        element.style.top = (elementY + deltaY) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
};

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
  ev.preventPropagation();
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }

function createElement({ 
    tagName = 'div', 
    id = '', 
    className = '', 
    attributes = {}, 
    children = [] 
}) {
    const element = document.createElement(tagName);
    
    if (id) element.id = id;
    if (className) element.className = className;

    for (let key in attributes) {
        element.setAttribute(key, attributes[key]);
    }

    children.forEach(child => {
        if (typeof child === 'string') {
            element.appendChild(document.createTextNode(child));
        } else if (child instanceof HTMLElement) {
            element.appendChild(child);
        }
    });

    return element;
}


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

// Just selects which board we are using for the 
// lists, will be used with python later
function selectTheList(id) {
  selectedList = id;
  console.log('blah');
  loadListFromPython();
}

function destroyElement(element, parent) {
  console.log(element);
  const anotherthing = element.parentElement.id;
  const item = element.id;
  const userid = document.getElementById('user_id').value;
  console.log(item, anotherthing, userid)
  json_data = {SelectedList: selectedList, currentList: anotherthing, UserId: userid, item: item};
  makeApiRequest('/list-api/v1/removeitem', 'POST', 'application/json', json_data);
  element.remove();
}

function loadListFromPython() {
  (async function(){
    const boardContainer = document.getElementById('board-container');
    const user = document.getElementById('user_id').value;
    let stufftosend = [selectedList, user];
    const lists = JSON.parse(await makeApiRequest('/list-api/v1/get-list', 'POST', 'text/plain', stufftosend));
    console.log(lists);

    boardContainer.innerHTML = "";
    const newListButton = createElement({
      tagName: 'button',
      id: 'newList',
      className: 'newList',
      attributes: {onclick: 'openListPopup()', style: 'position: absolute;'},
      children: ['New List']
    });

    boardContainer.appendChild(newListButton);
      
    // Loop through the Kanban board object
    Object.entries(lists).forEach(([listName, items]) => {
      // Create a list element for each list
      const listElement = createElement({
        tagName: 'div',
        id: listName,
        className: 'list-container',
        attributes: {
          ondragover: 'allowDrop(event)',
          ondrop: 'drop(event)',
          style: 'position: absolute; border: solid black 2px;'  // Ensure absolute positioning
        }
    });

      // Create a header for the list name
      const headerElement = createElement({
          tagName: 'h2',
          className: 'header',
          attributes: {style: 'cursor: move;'},
          children: [listName, ' ', createElement({tagName: 'button', id: 'destroybutton', attributes: {onclick: 'destroyElement(this.parentNode.parentNode)'}, children: ['x']})]
      });
      listElement.appendChild(headerElement); // Append header to the list
      // Loop through items in the list

      items.forEach(item => {
          // Create a list item element for each task
          const itemElement = createElement({
              tagName: 'p',
              id: item,
              attributes: {draggable: 'true', ondragstart: 'drag(event)'},
              children: [item, ' ', createElement({tagName: 'button', id: 'destroybutton', attributes: {onclick: 'destroyElement(this.parentElement)'}, children: ['x']})]
          });
          listElement.appendChild(itemElement);
      });
      const newItemButton = createElement({
        tagName: 'button',
        id: 'newItemButton',
        className: 'newItemButton',
        attributes: {onclick: 'openItemPopup(this.parentElement.id)', style: 'position: absolute; bottom: 0; width: 100%;'},
        children: ['New Item']
      });
      listElement.appendChild(newItemButton);
      boardContainer.appendChild(listElement);
      dragElement(listElement);
    });
  })();
}

function newItemOnList(parent) {
  const userid = document.getElementById('user_id').value;
  const listToAddTo = document.getElementById(currentListId);
  const item = document.getElementById('itemName').value;
  const listItem = createElement({
    tagName: 'p',
    id: item,
    attributes: {draggable: 'true', ondragstart: 'drag(event)'},
    children: [item, ' ', createElement({tagName: 'button', id: 'destroybutton', attributes: {onclick: 'destroyElement(this.parentElement)'}, children: ['x']})]
  });
  listToAddTo.appendChild(listItem);
  json_data = {SelectedList: selectedList, currentList: currentListId, UserId: userid, item: item};
  makeApiRequest('/list-api/v1/additem', 'POST', 'application/json', json_data);
  closeItemPopupFunc();
}

// Create a list on the board 
function createBoardList() {
  if (selectedList == "") {
    alert('there is no list selected');
    closeListPopupFunc();
    return 'no';
  }
  const boardContainer = document.getElementById('board-container');
  const listInput = document.getElementById('listName').value;
  const userid = document.getElementById('user_id').value;
  const list = createElement({
    tagName: 'div',
    id: listInput,
    className: 'list-container draggable',
    attributes: {
      ondragover: 'allowDrop(event)',
      ondrop: 'drop(event)'
    },
    children: [
      createElement({
      tagName: 'div',
      id: 'header',
      className: 'header',
      attributes: {style: 'cursor: move;'},
      children: [
        createElement({
          tagName: 'h2',
          children: [listInput]
        })
      ]
    }),
    createElement({
      tagName: 'div',
      id: 'listItems',
      class: 'listItems',
    }),
    createElement({
      tagName: 'button',
      id: 'newItemButton',
      classname: 'newItemButton',
      attributes: {onclick: 'openItemPopup(this.parentElement.id)', style: 'position: absolute; bottom: 0; width: 100%;'},
      children: ['New Item']
    })
    ]
    
  })
  
  boardContainer.appendChild(list);
  closeListPopupFunc();
  json_data = {ListName: listInput, SelectedList: selectedList, UserId: userid};
  makeApiRequest('/list-api/v1/create-list', 'POST', "application/json", json_data);
};

// Function to open the popup
function openPopup() {
    document.getElementById('popup-overlay').style.display = 'block';
    isModalOpen = true;
};

// open the popup for creating a new list
function openListPopup() {
    document.getElementById('popup-overlay-list').style.display = 'block';
    isModalOpen = true;
}

let currentListId = null;

function openItemPopup(listId) {
  console.log(listId);
  currentListId = listId;  // Store the ID of the list to which the new item will be added
  document.getElementById('popup-overlay-item').style.display = 'block';
  isModalOpen = true;
}

// Function to close the popup
function closePopupFunc() {
    document.getElementById('popup-overlay').style.display = 'none';
    isModalOpen = false;
}

// close the popup after creating list
function closeListPopupFunc() {
    document.getElementById('popup-overlay-list').style.display = 'none';
    isModalOpen = false;
}

// close the popup after adding an item to the list
function closeItemPopupFunc() {
  document.getElementById('popup-overlay-item').style.display = 'none';
  isModalOpen = false;
}

// Take the name the user submitted then create that todolist file
function submitName() {
    const name = kanbanName.value;
    createboard(name);
    closePopupFunc();
}

async function makeApiRequest(url, requestType = 'GET', contentType = null, content = null) {
    return new Promise((resolve, reject) => {
        var xhttp = new XMLHttpRequest();
        
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4) {  // Ensure request is complete
                if (this.status === 200) {
                    console.log('Request success, 200');
                    resolve(this.responseText);  // Resolve the Promise with the response
                } else if (this.status === 204) {
                    console.log('Request success, 204');
                    resolve(null);  // Resolve with null for 204 No Content
                } else {
                    reject(`Request failed with status ${this.status}`);  // Reject the Promise on failure
                }
            }
        };

        xhttp.open(requestType, 'http://127.0.0.1' + url, true);

        // Set default content-type if none provided
        if (contentType === null) {
            xhttp.setRequestHeader("Content-Type", "text/plain");
        }

        if (content === null) {
            xhttp.send();  // No content to send
        } else {
            content = JSON.stringify(content);
            xhttp.setRequestHeader("Content-Type", contentType);
            xhttp.send(content);  // Send with content
        }
    });
}


// allows dropping on an element
function allowDrop(ev) {
  ev.preventDefault();
}

// actually drags stuff
function drag(ev) {
  ev.dataTransfer.setData("Text", ev.target.id);
}

// drops the element into the parent element
function drop(ev) {
  let data = ev.dataTransfer.getData("Text");
  ev.target.appendChild(document.getElementById(data));
  ev.preventDefault();
}