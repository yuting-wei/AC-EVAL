import argparse


def parse_args():
    # Set up argparse to parse command line arguments
    parser = argparse.ArgumentParser(description="Evaluate model performance")
    parser.add_argument(
        "--data_dir", type=str, default="data/test", help="Path to the data directory"
    )
    parser.add_argument(
        "--models", type=str, required=True, help="List of models, separated by commas"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["zero-shot", "zero-shot-cot", "few-shot", "few-shot-cot"],
        default="zero-shot",
        help="Evaluation mode",
    )
    parser.add_argument("--times", type=int, default=1, help="Number of evaluations")

    return parser.parse_args()
