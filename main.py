"""
LazyEval - Automated Evaluation Platform for Language Models

Main entry point for running evaluations.
Run with: uv run main.py
"""

import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

from src.config.loader import load_config
from src.datasets.agriculture import AgricultureDatasetLoader
from src.evaluation.runner import EvaluationRunner
from src.integrations.json_export import JSONExporter
from src.integrations.langfuse_client import LangfuseExporter
from src.models.client import ModelClient


def setup_logging(log_dir: str):
    """
    Configure loguru logger for file and console output.
    
    Args:
        log_dir: Directory to save log files
    """
    # Create log directory
    Path(log_dir).mkdir(exist_ok=True, parents=True)
    
    # Remove default handler
    logger.remove()
    
    # Add console handler (INFO level)
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )
    
    # Add file handler (DEBUG level)
    logger.add(
        f"{log_dir}/lazyeval_{{time:YYYYMMDD_HHmmss}}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days"
    )
    
    logger.info("Logging configured")


def main():
    """Main execution flow for LazyEval platform."""
    
    try:
        # Load configuration
        logger.info("=" * 60)
        logger.info("LazyEval - Automated Model Evaluation Platform")
        logger.info("=" * 60)
        
        config = load_config()
        
        # Setup logging first (so we can configure it from config)
        setup_logging(config.output.log_dir)
        
        # Initialize components
        logger.info("Initializing components...")
        dataset_loader = AgricultureDatasetLoader(config.dataset, config.evaluation)
        model_client = ModelClient(config.model)
        eval_runner = EvaluationRunner(dataset_loader, model_client, config.evaluation)
        
        # Run evaluation
        logger.info("=" * 60)
        logger.info("Starting Evaluation")
        logger.info("=" * 60)
        
        results = eval_runner.run()
        
        if not results:
            logger.warning("No results generated. Evaluation may have failed or dataset was empty.")
            return
        
        # Export to JSON backup
        logger.info("=" * 60)
        logger.info("Saving JSON Backup")
        logger.info("=" * 60)
        
        json_exporter = JSONExporter(config.output.results_dir)
        json_file = json_exporter.export_results(results)
        
        # Export to Langfuse
        logger.info("=" * 60)
        logger.info("Exporting to Langfuse")
        logger.info("=" * 60)
        
        try:
            langfuse_exporter = LangfuseExporter(config.langfuse)
            run_name = f"agriculture_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            langfuse_exporter.export_results(results, run_name)
            logger.info(f"Langfuse run: {run_name}")
            logger.info(f"Check Langfuse dashboard at {config.langfuse.host} for LLM-as-Judge results")
        except Exception as e:
            logger.error(f"Failed to export to Langfuse: {e}")
            run_name = "EXPORT_FAILED"
        
        # Summary
        logger.info("=" * 60)
        logger.info("Evaluation Complete!")
        logger.info("=" * 60)
        logger.info(f"Total items processed: {len(results)}")
        logger.info(f"Average latency: {sum(r.latency_ms for r in results) / len(results):.2f}ms")
        logger.info(f"JSON backup: {json_file}")
        logger.info(f"Langfuse run: {run_name}")
        logger.info(f"Check Langfuse dashboard at {config.langfuse.host} for LLM-as-Judge results")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.exception(f"Fatal error during evaluation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
