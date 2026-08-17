"""
Resilient JSON Batch Processor v2.0
====================================
Author: Tommy Chan - Ipoh, Malaysia
"""

import json
import time
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

try:
    from pydantic import BaseModel, field_validator, ConfigDict
except ImportError:
    def field_validator(*args, **kwargs):
        return lambda f: f
    class BaseModel: pass


# CONFIGURATION
LOG_DIR = Path(__file__).parent / 'logs'
BATCH_FILE = Path(__file__).parent / 'batch_input.json'
DQL_FILE = Path(__file__).parent / 'dead_letter_queue.json'

RETRY_MAX_ATTEMPTS = 3
RETRY_BASE_DELAY = 2.0


class OrderRecord(BaseModel):
    """Type-safe order record."""
    model_config = ConfigDict(from_attributes=True, extra='forbid')
    order_id: int
    product_name: str
    quantity: int
    price: float
    customer_email: str

    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @classmethod
    def validate_quantity(cls, v):
        if v < 0 or v > 1000:
            raise ValueError('Quantity must be between 0 and 1000')
        return v


def calculate_delay(attempt):
    """Exponential backoff with jitter."""
    delay = min(RETRY_BASE_DELAY * (2 ** attempt), 30.0)
    return delay + random.uniform(0, delay * 0.1)


def simulate_failure(rate=0.2):
    """Simulate transient failures for testing."""
    return random.random() < rate


def write_to_dql(record_raw, error_msg, index):
    """Write failed record to dead letter queue."""
    entry = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'record_index': index,
        'error_type': type(error_msg).__name__,
        'error_message': error_msg,
        'record_data': record_raw
    }

    dq_path = DQL_FILE.with_suffix('.json')
    with open(dq_path, 'w', encoding='utf-8') as f:
        json.dump([entry], f, indent=2)


def process_record(record_raw, index):
    """Process single record with retry logic."""
    attempt = 0
    
    while attempt < RETRY_MAX_ATTEMPTS:
        try:
            order = OrderRecord(**record_raw)

            if simulate_failure():
                delay = calculate_delay(attempt - 1) if attempt > 0 else 0.5
                print('    Simulated failure for order ' + str(order.order_id) + '. Retrying in {:.1f}s...'.format(delay))
                time.sleep(delay)
                attempt += 1
                continue

            # Success!
            return {
                'success': True,
                'index': index,
                'message': 'Processed order ' + str(order.order_id),
                'data': order.model_dump()
            }

        except Exception as e:
            attempt += 1
            if attempt >= RETRY_MAX_ATTEMPTS:
                error_msg = str(e)
                write_to_dql(record_raw, error_msg, index)
                return {
                    'success': False,
                    'index': index,
                    'message': 'Failed after {} attempts'.format(attempt),
                    'error': error_msg,
                    'retry_count': attempt
                }

    # Safety fallback
    order_key = record_raw.get('order_id') or str(index)
    return {
        'success': False, 
        'index': index, 
        'error': 'Max retries exceeded', 
        'message': order_key
    }


def load_batch_data():
    """Load or create sample data."""
    BATCH_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not BATCH_FILE.exists():
        print('Creating sample batch data...')
        records = [
            {'order_id': 1001, 'product_name': 'Widget A', 'quantity': 50, 'price': 25.99, 'customer_email': 'alice@example.com'},
            {'order_id': 1002, 'product_name': 'Gadget B', 'quantity': 30, 'price': 49.99, 'customer_email': 'bob@example.com'},
            {'order_id': 1003, 'product_name': 'SuperThing', 'quantity': 10, 'price': 199.50, 'customer_email': 'carol@example.com'},
            {'order_id': 8004, 'product_name': 'MegaBox', 'quantity': 100, 'price': -5.00, 'customer_email': 'dave@example.com'}
        ]
        with open(BATCH_FILE, 'w') as f:
            json.dump(records, f, indent=2)
        return records

    with open(BATCH_FILE, 'r') as f:
        return json.load(f)


def process_batch():
    """Main processing loop."""
    print('')
    print('=' * 60)
    print(' RESILIENT JSON BATCH PROCESSOR')
    print('=' * 60)
    print('')

    records = load_batch_data()
    
    print('Processing {} records...'.format(len(records)))
    print('')

    success_count = 0
    failed_count = 0

    for i, record in enumerate(records, start=1):
        print('[{}/{}] Processing record {}...'.format(i, len(records), i))
        
        result = process_record(record, i - 1)
        
        if result['success']:
            print('      SUCCESS: ' + str(result['message']))
            success_count += 1
        else:
            print("      FAILED: " + str(result['message']))
            failed_count += 1

    # Summary
    total = len(records)
    with open(BATCH_FILE.parent / 'summary.txt', 'w') as f:
        f.write('=' * 60 + '\n')
        f.write('BATCH PROCESSING SUMMARY\n')
        f.write('=' * 60 + '\n\n')
        f.write('Total Records:     ' + str(total) + '\n')
        f.write('Successful:        ' + str(success_count) + '\n')
        f.write('Failed:            ' + str(failed_count) + '\n')
        if total > 0:
            rate = (success_count / total) * 100
            f.write('Success Rate:      {:.1f}%\n'.format(rate))
        else:
            f.write('Success Rate:      N/A\n')
        f.write('=' * 60 + '\n')

    print('')
    print('=== Summary ===')
    if total > 0:
        print('Successful: {}/{}'.format(success_count, total))
        print('Failed:      {}/{}'.format(failed_count, total))


if __name__ == '__main__':
    # Clear DQL before running
    import os
    if DQL_FILE.exists():
        os.unlink(DQL_FILE)
    
    process_batch()
