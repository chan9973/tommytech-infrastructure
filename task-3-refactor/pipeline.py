# =============================================================================
# Pipeline Orchestrator (Main entry point)
# Coordinates fetch → transform → store workflow with error handling
# =============================================================================

from typing import List, Dict, Any, Optional
import json
from datetime import datetime


class PipelineError(Exception):
    """Custom exception for pipeline failures."""
    def __init__(self, message: str, context: Optional[Dict] = None):
        self.message = message
        self.context = context or {}
        super().__init__(f"{message} {'Context: ' + json.dumps(self.context) if self.context else ''}")


class Pipeline:
    """
    Orchestrates the complete ETL pipeline.
    
    Architecture:
        1. DataSource (fetcher) → 2. DataTransformer → 3. Storage
    
    Dependencies are injected, enabling easy swapping for testing.
    """
    
    def __init__(
        self,
        data_source,
        storage_backend,
        enable_logging: bool = True,
        transformer_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize pipeline with injectable dependencies.
        
        Args:
            data_source: DataSource implementation (MockNetworkData, etc.)
            storage_backend: Storage implementation (InMemoryStorage, etc.)
            enable_logging: Enable debug logging
            transformer_config: Configuration dict for DataTransformer
        """
        self.data_source = data_source
        self.storage = storage_backend
        
        # Initialize transformer with defaults or config
        from transformer import DataTransformer  # Local import for circular deps
        self.transformer = DataTransformer(**(transformer_config or {}))
        
        self.enable_logging = enable_logging
    
    def process(self) -> Dict[str, Any]:
        """Execute full pipeline: fetch → transform → store.
        
        Returns:
            Pipeline execution result with statistics
        """
        if self.enable_logging:
            print('[' + datetime.now().isoformat()[:19] + '] Starting pipeline...')
        
        try:
            # Step 1: Fetch data
            raw_data = self.data_source.fetch()
            
            source_name = self.data_source.name()
            if self.enable_logging:
                print('✓ Fetched ' + str(len(raw_data)) + ' records from [' + source_name + ']')
            
            # Step 2: Transform data
            transformed = self.transformer.transform(raw_data)
            
            if self.enable_logging:
                valid_count = len([r for r in transformed if r.get('status') == 'success'])
                print('✓ Transformed' + str(len(transformed))+'records ('+str(valid_count)+'valid, '+str(len(transformed)-valid_count)+'rejected)')
            
            # Step 3: Store data
            saved_count = self.storage.save_all(transformed)
            
            if self.enable_logging:
                print('✓ Saved ' + str(saved_count) + ' records to storage')
            
            # Step 4: Validate counts match
            if saved_count != len(transformed):
                warning_count = len(transformed) - saved_count
                print('⚠ Warning: Not all transformed records were saved ('+str(warning_count)+'lost)')
            
            result = {
                'status': 'success',
                'source': source_name,
                'records_fetched': len(raw_data),
                'records_transformed': len(transformed),
                'records_saved': saved_count,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            error_details = {
                'message': str(e),
                'source': self.data_source.name(),
                'transformer_config': {
                    'price_multiplier': getattr(self.transformer, 'price_multiplier', None)
                },
                'file_path': self.storage.name()
            }
            
            raise PipelineError(
                f"Pipeline failed: {''.join(e.args)}",
                context=error_details if hasattr(e, 'context') else None
            ) from e


def run_pipeline():
    """Run default pipeline with mock data source and in-memory storage."""
    from fetcher import MockNetworkData
    from storage import InMemoryStorage
    
    pipeline = Pipeline(
        data_source=MockNetworkData(),
        storage_backend=InMemoryStorage()
    )
    
    result = pipeline.process()
    print('')
    print('=== Pipeline Execution Summary ===')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run_pipeline()
