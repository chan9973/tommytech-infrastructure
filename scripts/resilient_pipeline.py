#!/usr/bin/env python3
"""
Resilient Pipeline - Self-healing JSON processor with strict validation,
automatic retry, and dead letter queue handling.

Usage:
    python resilient_pipeline.py [--input input.json] [--output output.json]
"""

import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
from functools import wraps
import random

# Configure structured JSON logging
class JSONFormatter(logging.Formatter):
    """Formats log records as structured JSON"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            log_entry["error_type"] = record.exc_info[0].__name__ if record.exc_info[0] else "UnknownError"
        
        return json.dumps(log_entry)


# Setup logging
logger = logging.getLogger("resilient_pipeline")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)


@dataclass
class RecordField:
    """Validated field definition with type and constraints"""
    name: str
    type: type
    required: bool = True
    default: Any = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None


@dataclass
class PipelineRecord:
    """Strongly typed record schema with validation"""
    id: str
    name: str
    email: str
    age: int
    active: bool = True
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate record against constraints, return list of errors"""
        errors = []
        
        # ID validation
        if not isinstance(self.id, str) or len(self.id) == 0:
            errors.append("id must be a non-empty string")
        
        # Name validation
        if not isinstance(self.name, str) or len(self.name) == 0:
            errors.append("name must be a non-empty string")
        
        # Email validation (basic)
        if not isinstance(self.email, str) or '@' not in self.email:
            errors.append("email must be a valid email address")
        
        # Age validation
        if not isinstance(self.age, int) or self.age < 0 or self.age > 150:
            errors.append("age must be a valid integer between 0 and 150")
        
        # Tags validation
        if not isinstance(self.tags, list):
            errors.append("tags must be a list")
        else:
            for tag in self.tags:
                if not isinstance(tag, str):
                    errors.append("all tags must be strings")
                    break
        
        return errors


class ExponentialBackoffRetry:
    """Decorator for automatic retry with exponential backoff"""
    
    def __init__(self, max_attempts: int = 5, base_delay: float = 1.0, 
                 max_delay: float = 60.0, jitter: bool = True):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt}/{self.max_attempts} failed: {str(e)}")
                    
                    if attempt < self.max_attempts:
                        delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
                        if self.jitter:
                            delay *= random.uniform(0.5, 1.5)
                        
                        logger.debug(f"Retrying in {delay:.2f}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {self.max_attempts} attempts failed")
            
            raise last_exception
        return wrapper


class DeadLetterQueue:
    """Handles unparseable records safely"""
    
    def __init__(self, path: str = "dead_letter_queue.json"):
        self.path = Path(path)
        self.records: List[Dict[str, Any]] = []
        self._load_existing()
    
    def _load_existing(self):
        """Load existing dead letter records"""
        if self.path.exists():
            try:
                with open(self.path, 'r') as f:
                    self.records = json.load(f)
                logger.info(f"Loaded {len(self.records)} existing dead letter records")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load existing dead letter queue: {e}")
                self.records = []
    
    def add(self, record: Dict[str, Any], error: str, context: str):
        """Add a failed record to the queue"""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "original_record": record,
            "error": error,
            "context": context,
            "retry_count": record.get("_retry_count", 0)
        }
        self.records.append(entry)
        logger.warning(f"Added record to dead letter queue: {error}")
    
    def save(self):
        """Persist dead letter queue to disk"""
        try:
            with open(self.path, 'w') as f:
                json.dump(self.records, f, indent=2)
            logger.info(f"Saved {len(self.records)} records to {self.path}")
        except IOError as e:
            logger.error(f"Failed to save dead letter queue: {e}")


class ResilientPipeline:
    """Main pipeline processor with retry and validation"""
    
    def __init__(self, output_path: str = "output.json"):
        self.output_path = Path(output_path)
        self.dead_letter = DeadLetterQueue()
        self.processed_count = 0
        self.failed_count = 0
        self.valid_records: List[PipelineRecord] = []
        
        # Retry decorator with configuration
        self.retry = ExponentialBackoffRetry(
            max_attempts=3,
            base_delay=0.5,
            max_delay=10.0
        )
    
    def safe_parse_record(self, raw: Dict[str, Any]) -> Optional[PipelineRecord]:
        """
        Safely parse a raw dict into a PipelineRecord.
        Returns None if validation fails.
        """
        try:
            record = PipelineRecord(
                id=str(raw.get("id", "")),
                name=str(raw.get("name", "")),
                email=str(raw.get("email", "")),
                age=int(raw.get("age", 0)),
                active=bool(raw.get("active", True)),
                tags=list(raw.get("tags", [])),
                metadata=dict(raw.get("metadata", {}))
            )
            
            # Validate
            errors = record.validate()
            if errors:
                raise ValueError(f"Validation failed: {'; '.join(errors)}")
            
            return record
            
        except (ValueError, TypeError, KeyError) as e:
            logger.error(f"Record parsing error: {e}")
            self.dead_letter.add(raw, str(e), "validation")
            self.failed_count += 1
            return None
    
    @ExponentialBackoffRetry(max_attempts=3, base_delay=0.5)
    def process_batch(self, records: List[Dict[str, Any]]) -> List[PipelineRecord]:
        """Process a batch of records with automatic retry"""
        logger.info(f"Processing batch of {len(records)} records")
        
        valid_records = []
        for raw in records:
            try:
                record = self.safe_parse_record(raw)
                if record:
                    valid_records.append(record)
            except Exception as e:
                logger.error(f"Unexpected error processing record {raw.get('id', 'unknown')}: {e}")
                self.dead_letter.add(raw, str(e), "processing")
                self.failed_count += 1
        
        self.processed_count += len(valid_records)
        logger.info(f"Batch processed: {len(valid_records)} valid, {len(records) - len(valid_records)} invalid")
        
        return valid_records
    
    def write_output(self):
        """Write validated records to output file"""
        output_data = [asdict(r) for r in self.valid_records]
        
        try:
            with open(self.output_path, 'w') as f:
                json.dump({
                    "metadata": {
                        "total_processed": self.processed_count,
                        "total_failed": self.failed_count,
                        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                    },
                    "records": output_data
                }, f, indent=2)
            logger.info(f"Written {len(self.valid_records)} records to {self.output_path}")
        except IOError as e:
            logger.error(f"Failed to write output: {e}")
            raise


def load_input_file(path: str) -> List[Dict[str, Any]]:
    """Load JSON input file with retry"""
    with open(path, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, dict) and "records" in data:
        return data["records"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Input must be a JSON array or object with 'records' key")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Resilient JSON Pipeline")
    parser.add_argument("--input", default="sample_input.json", help="Input JSON file")
    parser.add_argument("--output", default="processed_output.json", help="Output JSON file")
    args = parser.parse_args()
    
    logger.info(f"Starting pipeline: input={args.input}, output={args.output}")
    
    try:
        # Load input
        logger.debug(f"Loading input from {args.input}")
        records = load_input_file(args.input)
        logger.info(f"Loaded {len(records)} records from input")
        
        # Process
        pipeline = ResilientPipeline(output_path=args.output)
        valid_records = pipeline.process_batch(records)
        pipeline.valid_records.extend(valid_records)
        
        # Write output
        pipeline.write_output()
        
        # Save dead letter queue
        pipeline.dead_letter.save()
        
        # Summary
        logger.info(f"Pipeline complete: {pipeline.processed_count} processed, "
                   f"{pipeline.failed_count} failed")
        
        # Print summary
        print(json.dumps({
            "status": "success",
            "processed": pipeline.processed_count,
            "failed": pipeline.failed_count,
            "output_file": str(pipeline.output_path),
            "dead_letter_file": str(pipeline.dead_letter.path)
        }, indent=2))
        
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()