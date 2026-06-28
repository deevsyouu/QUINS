import json
import os
from datetime import datetime

class MockDocumentReference:
    def __init__(self, doc_id, data):
        self.id = doc_id
        self._data = data

    def get(self):
        return MockDocumentSnapshot(self.id, self._data)

class MockDocumentSnapshot:
    def __init__(self, doc_id, data):
        self.id = doc_id
        self._data = data
        self.exists = data is not None

    def to_dict(self):
        return self._data

class MockCollectionReference:
    def __init__(self, name):
        self.name = name
        self.file_path = f"mock_{name}.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def _read_data(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_data(self, data):
        try:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error writing to mock db: {e}")

    def add(self, document_data):
        data = self._read_data()
        doc_id = str(len(data) + 1)
        
        # Convert datetime objects and other complex types to string for JSON compatibility
        processed_data = {}
        for k, v in document_data.items():
            if hasattr(v, 'isoformat'):
                processed_data[k] = v.isoformat()
            else:
                processed_data[k] = v
        processed_data['id'] = doc_id
        data.append(processed_data)
        self._write_data(data)
        return doc_id, MockDocumentReference(doc_id, processed_data)

    def stream(self):
        data = self._read_data()
        return [MockDocumentSnapshot(item.get('id', 'anonymous'), item) for item in data]

    def order_by(self, field, direction="ASCENDING"):
        class MockQuery:
            def __init__(self, collection, f, d):
                self.collection = collection
                self.field = f
                self.direction = d
            def stream(self):
                data = self.collection._read_data()
                reverse = (self.direction == "DESCENDING" or self.direction == "desc")
                try:
                    data.sort(key=lambda x: x.get(self.field, ""), reverse=reverse)
                except Exception:
                    pass
                return [MockDocumentSnapshot(item.get('id', 'anonymous'), item) for item in data]
        return MockQuery(self, field, direction)

class MockDb:
    def __init__(self):
        self.collections = {}

    def collection(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollectionReference(name)
        return self.collections[name]

_mock_db = MockDb()

def get_mock_db():
    return _mock_db
