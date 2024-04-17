/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

// Wait for the deviceready event before using any of Cordova's device APIs.
// See https://cordova.apache.org/docs/en/latest/cordova/events/events.html#deviceready
document.addEventListener('deviceready', onDeviceReady, false);

function onDeviceReady() {
    // Cordova is now initialized. Have fun!

    console.log('Running cordova-' + cordova.platformId + '@' + cordova.version);
    document.getElementById('deviceready').classList.add('ready');
}


const matrixContainer = document.querySelector('.matrix-container');
const ledMatrix = [
  [78, 77, 76, 75, 74, 73, 72],
  [64, 65, 66, 67, 68, 69, 70],
  [62, 61, 60, 59, 58, 57, 56],
  [48, 49, 50, 51, 52, 53, 54],
  [46, 45, 44, 43, 42, 41, 40],
  [32, 33, 34, 35, 36, 37, 38],
  [30, 29, 28, 27, 26, 25, 24],
  [16, 17, 18, 19, 20, 21, 22],
  [14, 13, 12, 11, 10, 9, 8],
  [0, 1, 2, 3, 4, 5, 6]
];

// Function to convert hex to RGB
function hexToRgb(hex) {
    var r = parseInt(hex.slice(1, 3), 16),
        g = parseInt(hex.slice(3, 5), 16),
        b = parseInt(hex.slice(5, 7), 16);
    return `${r},${g},${b}`;
}

// Existing LED toggle function adjusted to include dynamic background color change
ledMatrix.forEach(row => {
    row.forEach(led => {
        const ledDiv = document.createElement('div');
        ledDiv.className = 'led';
        ledDiv.id = `led-${led}`;
        ledDiv.textContent = led;
        ledDiv.style.backgroundColor = 'white'; // Initial background color
        ledDiv.style.color = 'red'; // Initial font color

        let isLedOn = false; // Track the LED state

        const toggleLED = () => {
            const colorPicker = document.getElementById('colorPicker');
            const colorHex = colorPicker.value;
            const colorRgb = hexToRgb(colorHex); // Get RGB color from picker
            if (!isLedOn) {
                const urlOn = `http://192.168.0.222:8080/led/on/${led}/${colorRgb}`;
                fetch(urlOn).catch(error => {
                    console.error(`Error turning on LED ${led}:`, error);
                });
                ledDiv.style.backgroundColor = colorHex; // Change background color to selected color
                ledDiv.style.color = 'blue'; // Change font color for better visibility
                isLedOn = true;
            } else {
                const urlOff = `http://192.168.0.222:8080/led/off/${led}`;
                fetch(urlOff).catch(error => {
                    console.error(`Error turning off LED ${led}:`, error);
                });
                ledDiv.style.backgroundColor = 'white'; // Revert background color
                ledDiv.style.color = 'red'; // Revert font color
                isLedOn = false;
            }
        };

        // Toggle LED on click
        ledDiv.addEventListener('click', toggleLED);

        // Toggle LED on touch (suitable for mobile devices)
        ledDiv.addEventListener('touchstart', (event) => {
            event.preventDefault(); // Prevent the default touch behavior
            toggleLED();
        });

        matrixContainer.appendChild(ledDiv);
    });
});


function turnLedOn() {
    const ledId = document.getElementById('ledIdOn').value;
    const color = document.getElementById('colorOn').value;
    fetch(`http://192.168.0.222:8080/led/on/${ledId}/${color}`)
        .then(response => response.json())
        .then(data => displayMessage(data.message))
        .catch(error => console.error('Error:', error));
}

function turnLedOff() {
    const ledId = document.getElementById('ledIdOff').value;
    fetch(`http://192.168.0.222:8080/led/off/${ledId}`)
        .then(response => response.json())
        .then(data => displayMessage(data.message))
        .catch(error => console.error('Error:', error));
}

function turnAllLedsOn() {
    const color = document.getElementById('allColorOn').value;
    fetch(`http://192.168.0.222:8080/leds/on/${color}`)
        .then(response => response.json())
        .then(data => displayMessage(data.message))
        .catch(error => console.error('Error:', error));
}

function turnAllLedsOff() {
    fetch('http://192.168.0.222:8080/leds/off')
        .then(response => response.json())
        .then(data => displayMessage(data.message))
        .catch(error => console.error('Error:', error));
}

function displayLetter() {
    const character = document.getElementById('character').value;
    const color = document.getElementById('letterColor').value;
    fetch(`http://192.168.0.222:8080/led/display_letter/${character}/${color}`)
        .then(response => response.json())
        .then(data => displayMessage(data.message))
        .catch(error => console.error('Error:', error));
}

function displaySentence() {
    const sentence = encodeURIComponent(document.getElementById('sentence').value);
    const color = document.getElementById('sentenceColor').value;
    const delay = document.getElementById('delay').value;
    fetch(`http://192.168.0.222:8080/led/display_sentence?sentence=${sentence}&color=${color}&delay=${delay}`)
        .then(response => response.json())
        .then(data => displayMessage(data.message))
        .catch(error => console.error('Error:', error));
}

function displayMessage(message) {
    document.getElementById('responseMessage').innerText = message;
}

// Function to send a GET request
function sendGetRequest() {
const url = "http://192.168.0.222:8080/led/display_letter/a/155,255,125"; // Replace YOUR_URL_HERE with your target URL

fetch(url)
    .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // or .text() if the response is not in JSON format || ERROR
    })
    .then(data => console.log(data))
    .catch(error => console.error('There was a problem with your fetch operation:', error));
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "flex";
    evt.currentTarget.className += " active";
}
  
// Get the element with id="defaultOpen" and click on it
document.addEventListener('DOMContentLoaded', () => {
document.getElementById("defaultOpen").click();
});