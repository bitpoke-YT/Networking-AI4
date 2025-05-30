from flask import Flask, render_template, request, jsonify, abort
import json
import uuid  # For generating unique breach IDs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/breaches', methods=['GET'])
def get_breaches():
    search = request.args.get('search', '').lower()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    with open('breaches.json', 'r') as f:
        breaches = json.load(f)
    
    filtered = []
    for breach in breaches:
        if (search in breach['service_name'].lower() or
            search in breach['email'].lower()):
            filtered.append(breach)
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]
    
    return jsonify({
        'breaches': paginated,
        'total': len(filtered),
        'page': page,
        'per_page': per_page,
        'pages': (len(filtered) + per_page - 1) // per_page
    })

@app.route('/api/breaches', methods=['POST'])
def add_breach():
    # Validate and parse the incoming JSON data
    try:
        data = request.get_json()
        if not data:
            abort(400, 'No data provided')
        
        required_fields = ['service_name', 'email', 'password', 'paste_date']
        for field in required_fields:
            if field not in data:
                abort(400, f'Missing required field: {field}')
        
        # Default risk_level if not provided
        data['risk_level'] = data.get('risk_level', 'Medium')
        
        # Generate a unique ID for the new breach
        data['id'] = str(uuid.uuid4())
        
        with open('breaches.json', 'r+') as f:
            breaches = json.load(f)
            breaches.append(data)
            f.seek(0)
            json.dump(breaches, f, indent=2, ensure_ascii=False)
        
        return jsonify({'success': True, 'message': 'Breach added successfully'}), 201
    
    except json.JSONDecodeError:
        abort(400, 'Invalid JSON provided')
    except Exception as e:
        abort(500, f'Server error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True, port=3333, host='0.0.0.0')