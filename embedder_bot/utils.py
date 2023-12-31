from typing import List, Optional

def find_one(query: dict, items: List[dict]) -> Optional[dict]:
    """Search through a list of dicts and return the first dict with a given value"""
    
    for item in items:
        if item | query:
            return item 
    
    return None