import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from baml_client.async_client import b as stream_baml_client
from src.config.loader import load_config
from loguru import logger


async def run_verification():
    try:
        logger.info("Loading config and setting up environment...")
        config = load_config()

        # Setup Env Vars for BAML (matching main.py logic)
        os.environ["MODEL_NAME"] = config.model.model_name
        os.environ["MODEL_BASE_URL"] = config.model.base_url
        os.environ["MODEL_API_KEY"] = config.model.api_key

        if config.judge_model:
            os.environ["JUDGE_MODEL_NAME"] = config.judge_model.model_name
            os.environ["JUDGE_MODEL_BASE_URL"] = config.judge_model.base_url
            os.environ["JUDGE_MODEL_API_KEY"] = config.judge_model.api_key
        else:
            os.environ["JUDGE_MODEL_NAME"] = config.model.model_name
            os.environ["JUDGE_MODEL_BASE_URL"] = config.model.base_url
            os.environ["JUDGE_MODEL_API_KEY"] = config.model.api_key

        print("\n=== Testing Generation ===")
        try:
            prompt = "What is the capital of France?"
            print(f"Prompt: {prompt}")
            res = await stream_baml_client.Generate(prompt)
            print(f"Result: {res}")
        except Exception as e:
            print(f"❌ Generation Failed: {e}")

        print("\n=== Testing AnswerCorrectness ===")
        try:
            pred = "Paris"
            gt = "The capital of France is Paris."
            print(f"Pred: {pred}, GT: {gt}")
            score = await stream_baml_client.AnswerCorrectness(
                prediction=pred, ground_truth=gt
            )
            print(f"Score: {score}")
        except Exception as e:
            print(f"❌ Correctness Failed: {e}")

        print("\n=== Testing AnswerRelevance ===")
        try:
            query = "What is capital of France?"
            pred = "The capital is Paris."
            print(f"Query: {query}, Pred: {pred}")
            score = await stream_baml_client.AnswerRelevance(
                query=query, prediction=pred
            )
            print(f"Score: {score}")
        except Exception as e:
            print(f"❌ Relevance Failed: {e}")

        print("\n=== Testing ResponseGroundedness ===")
        try:
            ctx = "Paris is the capital of France. It has a population of 2 million."
            pred = "Paris is the capital of France."
            print(f"Context: {ctx}, Pred: {pred}")
            score = await stream_baml_client.ResponseGroundedness(
                context=ctx, prediction=pred
            )
            print(f"Score: {score}")
        except Exception as e:
            print(f"❌ Groundedness Failed: {e}")

    except Exception as e:
        logger.exception(f"Setup failed: {e}")


if __name__ == "__main__":
    asyncio.run(run_verification())
