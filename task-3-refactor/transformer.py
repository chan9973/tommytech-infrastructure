# =============================================================================
# Data Transformer Module (Data Transformer)
# Applies business logic to transform raw data into processed format
# =============================================================================

from typing import List, Dict, Any


class DataTransformer:
    """
    Transforms raw product data into enriched records.
    
    Features:
        - Price scaling and validation
        - Discount flag calculation
        - Category normalization
    """
    
    def __init__(
        self,
        price_multiplier: float = 1.0,
        min_quantity: int = 0,
        max_quantity: int = 1000,
        discount_threshold: float = 100.0
    ):
        """
        Initialize transformer configuration.
        
        Args:
            price_multiplier: Scale factor for prices (default: 1.0)
            min_quantity: Minimum allowed quantity
            max_quantity: Maximum allowed quantity  
            discount_threshold: Price above which no discount applies
        """
        self.price_multiplier = price_multiplier
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.discount_threshold = discount_threshold
    
    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform raw data into enriched records.
        
        Args:
            raw_data: List of raw product dictionaries from datasource
            
        Returns:
            List of transformed and enriched product records
        """
        transformed = []
        
        for idx, raw_item in enumerate(raw_data):
            # Normalize and enrich each item
            record = self._enrich_item(raw_item, idx)
            transformed.append(record)
        
        return transformed
    
    def _enrich_item(self, raw_item: Dict[str, Any], idx: int) -> Dict[str, Any]:
        """Enrich single item with metadata."""
        # Copy raw fields
        record = {
            'source_index': idx,
            **raw_item
        }
        
        # Validate and scale price
        try:
            price = float(raw_item.get('price', 0)) * self.price_multiplier
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid price for item {idx}: {e}") from e
        
        if price < 0:
            raise ValueError(f"Negative price detected: {price}")
        
        record['processed_price'] = round(price, 2)
        
        # Calculate discount eligibility
        quantity = raw_item.get('quantity', 0)
        
        if not self.min_quantity <= quantity <= self.max_quantity:
            record['status'] = 'rejected'
            record['reason'] = f"Quantity {quantity} outside bounds [{self.min_quantity}, {self.max_quantity}]"
        elif price > self.discount_threshold:
            record['discounted'] = False
            record['reason'] = 'Above threshold'
        elif quantity % 2 == 0:
            record['discounted'] = True
            record['reason'] = 'Eligible discount'
        else:
            record['discounted'] = False
            record['reason'] = 'No discount applied'
        
        # Normalize category (lowercase, remove extra spaces)
        cat = raw_item.get('category', '')
        record['processed_category'] = ' '.join(
            part.lower() for part in str(cat).strip().split()
        )
        
        return record
