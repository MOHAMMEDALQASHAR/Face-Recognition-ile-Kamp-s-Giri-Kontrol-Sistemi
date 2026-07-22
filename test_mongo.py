"""
Test MongoDB Adapter functionality
"""

import sys
from db_adapter import MongoDatabaseAdapter, MongoCollectionAdapter

def main():
    print("Testing MongoDatabaseAdapter...")
    try:
        db_adapter = MongoDatabaseAdapter("mongo_config.json")
        students_col = db_adapter.collection("students")
        
        # Test inserting a student
        student_id = "TEST12345"
        students_col.document(student_id).set({
            "name": "Test Student",
            "student_id": student_id,
            "embedding": [0.1, 0.2, 0.3]
        })
        print("[OK] Successfully inserted student record into MongoDB")
        
        # Test retrieving student
        doc = students_col.document(student_id).get()
        if doc.exists:
            print(f"[OK] Retrieved student: {doc.to_dict()}")
        else:
            print("[FAIL] Student record not found")
            
        # Test deleting student
        students_col.document(student_id).delete()
        print("[OK] Successfully cleaned up test student record from MongoDB")
        
        print("\nAll MongoDB adapter tests passed!")
        
    except Exception as e:
        print(f"[Error] MongoDB adapter test failed: {e}")

if __name__ == "__main__":
    main()
