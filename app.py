from flask import Flask, request, render_template
import time
app = Flask(__name__)
current_bpm = 120  # Default BPM
taps = []  # Declare taps here, outside of any functions

@app.route('/')
def index():
    return render_template('index.html', bpm=current_bpm)

@app.route('/tap', methods=['POST'])
def tap():
    global current_bpm, taps
    current_time = time.time()

    # Reset taps if there's a significant delay from the last tap
    if taps and current_time - taps[-1] > 2:  # 2 seconds delay threshold
        taps = []

    taps.append(current_time)
    if len(taps) > 1:
        intervals = [taps[i] - taps[i-1] for i in range(1, len(taps))]
        avg_interval = sum(intervals) / len(intervals)
        calculated_bpm = 60 / avg_interval
        current_bpm = calculated_bpm  # Update the current_bpm variable
        with open('bpm.txt', 'w') as f:
            f.write(str(current_bpm))
    return '', 204

@app.route('/set_bpm', methods=['POST'])
def set_bpm():
    global current_bpm
    try:
        bpm_value = float(request.form['bpm'])
        current_bpm = bpm_value
        with open('bpm.txt', 'w') as f:
            f.write(str(current_bpm))
    except ValueError:
        pass  # Handle invalid BPM value
    return '', 204

@app.route('/get_bpm')
def get_bpm():
    global current_bpm
    return {'bpm': current_bpm}


if __name__ == '__main__':
    app.run(port=5000, debug=True)