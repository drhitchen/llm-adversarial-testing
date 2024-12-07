import yaml
import json
import argparse
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

# Load adversarial prompts
def load_prompts(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# Run a single test case
def run_test_case(prompt, expected_response):
    template = ChatPromptTemplate.from_template(prompt)
    response = chat_model.invoke(template.format_messages())  # Use invoke method
    return response.content

# Evaluate response
def evaluate_response(response, expected_response):
    return expected_response in response

# Run all tests
def run_all_tests(prompts):
    results = []
    for test in prompts["prompts"]:
        prompt = test["prompt"]
        expected = test["expected"]
        category = test["category"]

        # Run test and evaluate
        response = run_test_case(prompt, expected)
        passed = evaluate_response(response, expected)

        # Log results
        result = {
            "category": category,
            "prompt": prompt,
            "response": response,
            "expected": expected,
            "passed": passed,
        }
        results.append(result)

    return results

# Save results to both JSON and YAML
def save_results(results, yaml_file="adversarial_prompts.yaml", json_file="results.json", update_expected=False):
    # Save results to JSON
    with open(json_file, "w") as f:
        json.dump(results, f, indent=4)

    # Update YAML file
    with open(yaml_file, "r") as f:
        prompts = yaml.safe_load(f)

    for i, result in enumerate(results):
        prompts["prompts"][i]["actual"] = result["response"]  # Log actual response
        if update_expected:  # Update expected value if the flag is set
            prompts["prompts"][i]["expected"] = result["response"]

    with open(yaml_file, "w") as f:
        yaml.safe_dump(prompts, f, default_flow_style=False)

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run adversarial testing on LLMs.")
    parser.add_argument("--update-expected", action="store_true", help="Update expected responses to match actual responses.")
    args = parser.parse_args()

    # Load prompts and run tests
    prompts = load_prompts("adversarial_prompts.yaml")
    results = run_all_tests(prompts)
    save_results(results, update_expected=args.update_expected)
    print("Testing complete. Results saved to 'results.json' and updated in 'adversarial_prompts.yaml'.")

if __name__ == "__main__":
    chat_model = ChatOpenAI(model="gpt-4")
    main()
