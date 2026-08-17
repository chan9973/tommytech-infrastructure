# =============================================================================
# LEGACY MONOLITHIC CODE (Refactoring Target)
# This script does EVERYTHING in one function:
#   - Fetches data from network source
#   - Transforms raw data
#   - Writes to database
#   - Sends notifications
#   - Generates reports
# 
# PROBLEMS with this code:
#   - No testability (hard to unit test each concern)
#   - Global state pollution
#   - Magic strings throughout
#   - Circular dependencies if you try to split it
# =============================================================================

def process_all_data():
    """DOES EVERYTHING: fetches, transforms, stores, etc."""
    import requests
    from sqlite3 import connect
    
    # Fetch data
    url = "https://api.example.com/v1/products"  # magic string!
    response = requests.get(url)
    
    if response.status_code != 200:
        print("HTTP error:", response.status_code)
        return
    
    raw_products = response.json()
    
    # Transform data inline (mixed with everything else)
    transformed = []
    for product in raw_products:
        # Magic numbers!
        price_scaled = product['price'] * 1.23  # Why this number?
        if price_scaled > 100:
            product['discounted'] = False
        else:
            product['discounted'] = product['quantity'] % 2 == 0
        
        transformed.append(product)
    
    # Write to database (inline SQL without prepared statements!)
    conn = connect(':memory:')  # Would be file path in prod!
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER, name TEXT, price REAL, 
            category TEXT, stock INTEGER, discounted INTEGER, PRIMARY KEY(id)
        )
    """)
    
    for p in transformed:
        cursor.execute(
            'INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)',
            (p['id'], p['name'], p['price'], p['category'],
             p['quantity'], 1 if p['discounted'] else 0, None)
        )
    
    # No error handling, no logging, no type hints!
    conn.commit()
    
    print(f"Processed {len(transformed)} products")
    return {'status': 'complete', 'count': len(transformed)}
