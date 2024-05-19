from flask import Flask, render_template, request
from analyze import Probability, P_or_N, Clean_Text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html') 

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    Clean = Clean_Text(text)
    probabilities = Probability(text)
    print(probabilities)
    for key in probabilities:
        probabilities[key] = str(probabilities[key]) + '%'
    Clasification = P_or_N(Clean)
    data = {
        'probabilities': probabilities,
        'Clasification': Clasification
    }
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('result.html', text=text, probabilities=probabilities, Clasification=Clasification
                           , labels=labels, values=values)

if __name__ == '__main__':
    app.run(debug=True)

