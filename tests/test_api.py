"""Test API endpoints."""
import json


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'version' in data


def test_api_index(client):
    """Test the API index endpoint."""
    response = client.get('/api/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'version' in data


def test_get_examples(client):
    """Test getting all examples."""
    response = client.get('/api/examples')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)


def test_get_example_by_id(client):
    """Test getting a specific example."""
    response = client.get('/api/examples/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['id'] == 1


def test_create_example(client):
    """Test creating a new example."""
    new_example = {
        'name': 'Test Example',
        'description': 'This is a test'
    }
    response = client.post(
        '/api/examples',
        data=json.dumps(new_example),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['name'] == 'Test Example'


def test_create_example_missing_fields(client):
    """Test creating an example with missing fields."""
    incomplete_example = {
        'name': 'Test Example'
        # Missing 'description' field
    }
    response = client.post(
        '/api/examples',
        data=json.dumps(incomplete_example),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


def test_update_example(client):
    """Test updating an example."""
    updated_data = {
        'name': 'Updated Name',
        'description': 'Updated description'
    }
    response = client.put(
        '/api/examples/1',
        data=json.dumps(updated_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['name'] == 'Updated Name'


def test_delete_example(client):
    """Test deleting an example."""
    response = client.delete('/api/examples/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_echo_endpoint(client):
    """Test the echo endpoint."""
    test_data = {'message': 'Hello, World!'}
    response = client.post(
        '/api/echo',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['echo'] == test_data


def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['status'] == 404
    assert 'error' in data
