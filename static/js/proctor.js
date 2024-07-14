ques=0;
document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video');
    const questionInput = document.getElementById('question');
    const answerInput = document.getElementById('answer');
    const start = document.getElementById('start-button');

    let stream = null;
    let intervalId = null;
    // Start button click event handler
    start.addEventListener('click', function() {
        
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
            start.textContent = 'Start';
        } else {
            startCapture();
            start.textContent = 'Stop';
        }
    });

    // Function to start video capture
    function startCapture() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (mediaStream) {
                stream = mediaStream;
                video.srcObject = mediaStream;
                video.onloadedmetadata = function (e) {
                    video.play();
                };
                intervalId = setInterval(function() {
                    takeSnapshot();
                }, 5000);  // Capture photo every 5 seconds
            })
            .catch(function (err) {
                console.error('Error accessing webcam:', err);
            });
    }

    // Function to capture and send snapshot to server
    function takeSnapshot() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL('image/jpeg');

        // Send dataURL to Flask server (replace with your Flask server endpoint)
        sendToServer(dataURL);
    }

    // Placeholder function to send data to server
    function sendToServer(dataURL) {
        // Example: Send dataURL to Flask server using fetch API
        fetch('/upload_photo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: questionInput.value,
                answer: answerInput.value,
                photo: dataURL
            })
        })
        .then(response => {
            if (response.ok) {
                console.log('Photo uploaded successfully.');
            } else {
                console.error('Failed to upload photo.');
            }
        })
        .catch(error => {
            console.error('Error uploading photo:', error);
        });
    }
});
/*-------------------------------------------------------------------- */
//  when the pop comes to start the test

document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('popup');
    const subject_block = document.getElementById('get_subject_block');
    const mainContent = document.getElementById('main-content');
    const startButton = document.getElementById('start-button');
    const cancelButton = document.getElementById('cancel-button');
    const input_subject_Button = document.getElementById('input_subject_btn');
    const loader = document.getElementById('loading');

 
    input_subject_Button.addEventListener( 'click' , function(){
        sendSubject();
        subject_block.style.display = 'none';
        loader.style.display = 'flex';
    })

    startButton.addEventListener('click', function() {
        popup.style.display = 'none';
        mainContent.style.display = 'block';
    });

    cancelButton.addEventListener('click', function() {
        window.location.href = '/';
    });


    startButton.addEventListener('click', function() {
        fetch('/get_next_question')
            .then(response => response.json())
            .then(data => {
                const questionContainer = document.getElementById('question');
                questionContainer.innerText = data.question;
            })
            .catch(error => console.error('Error:', error));
    });
});


/***************************************************/

//  when the pop comes to exit the test

document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('popup-close');
    const mainContent = document.getElementById('main-content');
    const exitbtn = document.getElementById('exit');
    const cancelButton = document.getElementById('stay');
    
    const endbtn = document.getElementById('end');

    endbtn.addEventListener('click', function() {
        popup.style.display = 'flex';
        // mainContent.style.display = 'none';
    });

    cancelButton.addEventListener('click', function() {
        popup.style.display="none";
    });

    exitbtn.addEventListener('click',function(){
        window.location.href = '/';
    });
});

//---------------------------------------------------------------------------

// rendering next question

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.getElementById('nextButton');
    const startButton = document.getElementById('start-button');
    const text = document.getElementById('answer');


    // startButton.addEventListener('click', function() {
    //     fetch('/get_next_question')
    //         .then(response => response.json())
    //         .then(data => {
    //             const questionContainer = document.getElementById('question');
    //             questionContainer.innerText = data.question;
    //         })
    //         .catch(error => console.error('Error:', error));
    // });

    nextButton.addEventListener('click',function(){
        sendText();

        if(nextButton.textContent=="Submit")
            {
                window.location.href = '/stats';
            }
        else
        {fetch('/get_next_question')
            .then(response => response.json())
            .then(data => {

                if(ques==4)
                    {
                        nextButton.textContent="Submit";
                    }
                const questionContainer = document.getElementById('question');

                questionContainer.innerText = data.question;
            })
            .catch(error => console.error('Error:', error));
        ques++;
    
        text.value="";}
    })
    
});

// sending current answer
function sendText() {
    const text = document.getElementById('answer').value;

    fetch('/getanswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
 
//  sending the subject to llm file
function sendSubject(){
    
    const popup = document.getElementById('popup');
    const subject_block = document.getElementById('get_subject_block');
    const mainContent = document.getElementById('main-content');
    const startButton = document.getElementById('start-button');
    const cancelButton = document.getElementById('cancel-button');
    const input_subject_Button = document.getElementById('input_subject_btn');
    const loader = document.getElementById('loading');
    const text = document.getElementById('input_subject').value;

    fetch('/getsubject', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    fetch('/getques', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        popup.style.display='flex';
        loader.style.display='none';
    })
    .catch((error) => {
        console.error('Error:', error);
    });


   
}