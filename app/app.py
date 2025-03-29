from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database" for storing tasks
tasks = {}

@app.route('/')
def home():
    return "Welcome to the To-Do List App!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task_id = len(tasks) + 1
    task_data = request.json.get('task', '')
    tasks[task_id] = {'id': task_id, 'task': task_data}
    return jsonify({'message': 'Task added successfully!', 'task': tasks[task_id]}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': f'Task {task_id} deleted successfully!'})
    else:
        return jsonify({'error': 'Task not found!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
