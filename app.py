from flask import Flask,render_template,request,jsonify
import base64,os
from datetime import datetime
from face_dtect import count_faces
from llm import askQA , insert_subject
from answerfile import reset,insert,getans,getEvaluation

ques_index=0
app  = Flask(__name__)


@app.route("/")
def hello():
    global ques_index
    ques_index=0
    reset()
    return render_template("home.html")


@app.route("/proctor")
def helloproctor():
    return render_template("proctor.html")

@app.route("/stats")
def showstats():
    return render_template("stats.html")

@app.route("/getstats",methods=['GET'])
def givestats():
    answer = getans()
    return jsonify(answer)


@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.get_json()
    photo_data_url = data.get('photo')
    

    # Check if photo_data_url is not None and is a base64 encoded string
    if photo_data_url and photo_data_url.startswith('data:image/jpeg;base64,'):
        # Extract base64 encoded image data
        img_data = photo_data_url.split(',')[1]

        # Decode base64 data
        try:
            img_binary = base64.b64decode(img_data)
        except Exception as e:
            return jsonify({'error': 'Failed to decode image data'}), 400
        
        if count_faces(img_binary) == 1:
            return jsonify({'message': 'Anomaly detected', }), 200

        # Specify the directory where you want to save the image
        save_dir = 'save_images'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f'uploaded_image_{timestamp}.jpg'
        try:
            with open(os.path.join(save_dir, filename), 'wb') as f:
                f.write(img_binary)
        except Exception as e:
            return jsonify({'error': 'Failed to save image file'}), 500

        return jsonify({'message': 'Photo uploaded and saved successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid photo data URL'}), 400
    

@app.route('/get_next_question')
def get_next_question():
    global ques_index
    question = askQA(ques_index)
    ques_index = ques_index + 1
    return jsonify({"question": question})

@app.route('/getanswer', methods=['POST'])
def receive_text():
    data = request.get_json()
    text = data.get('text')
    insert(text)
    print(getans())
    return jsonify({'message': 'Text received successfully!'})


@app.route('/getsubject', methods=['POST'])
def receive_subject():
    data = request.get_json()
    text = data.get('text')
    insert_subject(text)
    print("this is the subject  -> " , text)
    return jsonify({'message': 'Text received successfully!'})

@app.route('/getresult')
def results():
    data = getEvaluation()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)