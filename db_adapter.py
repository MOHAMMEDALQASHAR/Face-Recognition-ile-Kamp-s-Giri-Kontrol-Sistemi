"""
MongoDB Database Adapter for Face Attendance System
Provides a clean Firestore-compatible wrapper over PyMongo with graceful local fallback.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError


class MongoDocumentAdapter:
    def __init__(self, collection, doc_id: str, data: Optional[Dict] = None):
        self.collection = collection
        self.doc_id = str(doc_id)
        self._cached_data = data
        self.id = self.doc_id

    @property
    def exists(self) -> bool:
        if self.collection.is_fallback:
            return self.doc_id in self.collection.fallback_store or any(
                v.get('student_id') == self.doc_id for v in self.collection.fallback_store.values()
            )
        try:
            doc = self.collection.find_one({'_doc_id': self.doc_id})
            if doc is None and 'student_id' in (self._cached_data or {}):
                doc = self.collection.find_one({'student_id': self.doc_id})
            return doc is not None
        except Exception as e:
            print(f"[MongoDB Error] {e}")
            return False

    def get(self):
        if self.collection.is_fallback:
            if self.doc_id in self.collection.fallback_store:
                self._cached_data = self.collection.fallback_store[self.doc_id]
            else:
                for v in self.collection.fallback_store.values():
                    if v.get('student_id') == self.doc_id:
                        self._cached_data = v
                        break
            return self

        try:
            doc = self.collection.find_one({'_doc_id': self.doc_id})
            if doc is None:
                doc = self.collection.find_one({'student_id': self.doc_id})
            if doc:
                self._cached_data = doc
        except Exception as e:
            print(f"[MongoDB Error] {e}")
        return self

    def to_dict(self) -> Dict:
        if self._cached_data is None:
            self.get()
        if not self._cached_data:
            return {}
        data = dict(self._cached_data)
        data.pop('_id', None)
        data.pop('_doc_id', None)
        return data

    def set(self, data: Dict):
        doc_data = dict(data)
        doc_data['_doc_id'] = self.doc_id
        if 'student_id' not in doc_data:
            doc_data['student_id'] = self.doc_id

        if self.collection.is_fallback:
            self.collection.fallback_store[self.doc_id] = doc_data
            self._cached_data = doc_data
            return

        try:
            self.collection.update_one(
                {'_doc_id': self.doc_id},
                {'$set': doc_data},
                upsert=True
            )
            self._cached_data = doc_data
        except Exception as e:
            print(f"[MongoDB Error] Failed set: {e}")

    def delete(self):
        if self.collection.is_fallback:
            self.collection.fallback_store.pop(self.doc_id, None)
            to_remove = [k for k, v in self.collection.fallback_store.items() if v.get('student_id') == self.doc_id]
            for k in to_remove:
                self.collection.fallback_store.pop(k, None)
            return

        try:
            self.collection.delete_one({'_doc_id': self.doc_id})
            self.collection.delete_one({'student_id': self.doc_id})
        except Exception as e:
            print(f"[MongoDB Error] Failed delete: {e}")

    @property
    def reference(self):
        return self


class MongoQueryAdapter:
    def __init__(self, collection, filters: Optional[Dict] = None):
        self.collection = collection
        self.filters = filters or {}

    def where(self, field: str, op: str, value: Any):
        new_filters = dict(self.filters)
        if op in ('==', '='):
            new_filters[field] = value
        elif op == '>':
            new_filters[field] = {'$gt': value}
        elif op == '<':
            new_filters[field] = {'$lt': value}
        elif op == '>=':
            new_filters[field] = {'$gte': value}
        elif op == '<=':
            new_filters[field] = {'$lte': value}
        elif op == 'in':
            new_filters[field] = {'$in': value}
        return MongoQueryAdapter(self.collection, new_filters)

    def stream(self) -> List[MongoDocumentAdapter]:
        if self.collection.is_fallback:
            results = []
            for doc_id, doc in list(self.collection.fallback_store.items()):
                match = True
                for k, v in self.filters.items():
                    if isinstance(v, dict):
                        if '$gt' in v and not (doc.get(k) > v['$gt']):
                            match = False
                        if '$lt' in v and not (doc.get(k) < v['$lt']):
                            match = False
                    elif doc.get(k) != v:
                        match = False
                if match:
                    results.append(MongoDocumentAdapter(self.collection, doc_id, doc))
            return results

        try:
            cursor = self.collection.find(self.filters)
            results = []
            for doc in cursor:
                doc_id = doc.get('_doc_id') or str(doc.get('student_id', doc.get('_id')))
                results.append(MongoDocumentAdapter(self.collection, doc_id, doc))
            return results
        except Exception as e:
            print(f"[MongoDB Error] Query failed: {e}")
            return []


class MongoCollectionAdapter:
    def __init__(self, db, name: str, is_fallback: bool = False, fallback_store: Optional[Dict] = None):
        self.db = db
        self.name = name
        self.is_fallback = is_fallback
        self.fallback_store = fallback_store if fallback_store is not None else {}
        if not is_fallback and db is not None:
            self.collection = db[name]
        else:
            self.collection = None

    def document(self, doc_id: str) -> MongoDocumentAdapter:
        return MongoDocumentAdapter(self, str(doc_id))

    def add(self, data: Dict):
        doc_data = dict(data)
        doc_id = doc_data.get('student_id') or f"id_{time.time_ns()}"
        doc_data['_doc_id'] = doc_id

        if self.is_fallback:
            self.fallback_store[doc_id] = doc_data
            return MongoDocumentAdapter(self, doc_id, doc_data)

        try:
            res = self.collection.insert_one(doc_data)
            return MongoDocumentAdapter(self, doc_id, doc_data)
        except Exception as e:
            print(f"[MongoDB Error] Add failed: {e}")
            return MongoDocumentAdapter(self, doc_id, doc_data)

    def stream(self) -> List[MongoDocumentAdapter]:
        return MongoQueryAdapter(self).stream()

    def where(self, field: str, op: str, value: Any) -> MongoQueryAdapter:
        return MongoQueryAdapter(self).where(field, op, value)

    def find_one(self, filter_dict: Dict):
        if self.is_fallback:
            for doc in self.fallback_store.values():
                match = True
                for k, v in filter_dict.items():
                    if doc.get(k) != v:
                        match = False
                        break
                if match:
                    return doc
            return None
        return self.collection.find_one(filter_dict)

    def find(self, filter_dict: Dict):
        if self.is_fallback:
            res = []
            for doc in self.fallback_store.values():
                match = True
                for k, v in filter_dict.items():
                    if doc.get(k) != v:
                        match = False
                        break
                if match:
                    res.append(doc)
            return res
        return self.collection.find(filter_dict)

    def delete_one(self, filter_dict: Dict):
        if self.is_fallback:
            for k, v in list(self.fallback_store.items()):
                match = True
                for fk, fv in filter_dict.items():
                    if v.get(fk) != fv:
                        match = False
                        break
                if match:
                    del self.fallback_store[k]
                    break
            return
        return self.collection.delete_one(filter_dict)

    def update_one(self, filter_dict: Dict, update_dict: Dict, upsert: bool = False):
        if self.is_fallback:
            set_data = update_dict.get('$set', {})
            doc_id = set_data.get('_doc_id') or filter_dict.get('_doc_id') or f"id_{time.time_ns()}"
            existing = self.fallback_store.get(doc_id, {})
            existing.update(set_data)
            self.fallback_store[doc_id] = existing
            return
        return self.collection.update_one(filter_dict, update_dict, upsert=upsert)


class MongoDatabaseAdapter:
    """
    Main MongoDB adapter connecting to MongoDB database with graceful fallback
    """
    _fallback_db_stores = {}

    def __init__(self, config_path: str = "mongo_config.json"):
        connection_string = "mongodb://localhost:27017/"
        db_name = "face_attendance_db"
        self.is_fallback = False

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    connection_string = cfg.get("connection_string", connection_string)
                    db_name = cfg.get("database_name", db_name)
            except Exception as e:
                print(f"[MongoDB] Warning: Failed to read {config_path}: {e}")

        print(f"[MongoDB] Attempting connection to: {connection_string} (DB: {db_name})...")
        try:
            client = MongoClient(connection_string, serverSelectionTimeoutMS=2000)
            # Test connection
            client.admin.command('ping')
            self.client = client
            self.db = self.client[db_name]
            print(f"[MongoDB Success] Successfully connected to MongoDB database '{db_name}'!")
        except Exception as e:
            print(f"[MongoDB Warning] Could not connect to MongoDB server: {e}")
            print(f"[MongoDB Notice] System running in Mongo Memory Mode (Fallback).")
            print(f"[MongoDB Notice] To connect to MongoDB Atlas or local MongoDB, edit 'mongo_config.json'.")
            self.is_fallback = True
            self.db = None

    def collection(self, name: str) -> MongoCollectionAdapter:
        if self.is_fallback:
            if name not in MongoDatabaseAdapter._fallback_db_stores:
                MongoDatabaseAdapter._fallback_db_stores[name] = {}
            return MongoCollectionAdapter(
                db=None,
                name=name,
                is_fallback=True,
                fallback_store=MongoDatabaseAdapter._fallback_db_stores[name]
            )
        return MongoCollectionAdapter(self.db, name)


SERVER_TIMESTAMP = datetime.now
