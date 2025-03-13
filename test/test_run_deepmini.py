from datetime import datetime

from src.models.Deepmini import run_test_evaluation

if __name__ == "__main__":
    print("Running test evaluation...")
    for res in run_test_evaluation():
        print(str(res))
        print(datetime.now())


