import json
import argparse
from openai import OpenAI
import openai
from vllm import LLM, SamplingParams
from tqdm import tqdm
import csv
import os
# Load the JSON file

letters = ["A", "B", "C", "D", "E", "F"]

def evaluate(args, client, problem):
  if args.cot == True:
    system_prompt = """Here is a persuasive dialogue. There are two agents, the persuader and the persuadee. The persuader is trying to persuade the persuadee to do something. Think step by step to answer the question."""
  else:
    system_prompt = f"Here is a persuasive dialogue. There are two agents, the persuader and the persuadee. The persuader is trying to persuade the persuadee to do something. Please answer the following questions using \"A\", \"B\", \"C\", \"D\", \"E\", \"F\" without any explanation."
  dialogue = problem['dialogue']
  question = problem['question']
  choices = problem['choices']
  answerKey = problem['answerKey']
  if args.cot == True:
    shot = """\n
    Ending with "The answer is \"A\", \"B\", \"C\", \"D\", \"E\", \"F\"." 
    For example, if the most likely answer option is 'A. considering', then end your response with 'The answer is A'. 
    """
    user_prompt = shot + "\nDialogue History:\n" + dialogue + "\nQuestion:\n" + question + "\nChoices:"
  else:
    user_prompt = "\nDialogue History:\n" + dialogue + "\nQuestion:\n" + question + "\nChoices:"
  answer_set = []
  for i, choice in enumerate(choices):
    answer_set.append(f"{letters[i]}. {choice}")

  for i, choice in enumerate(choices):
    user_prompt += f"\n{letters[i]}. {choice}"
  if args.cot == False:
    user_prompt += "\nAnswer:"
  else:
    user_prompt += """\nAnswer: Let's think step by step."""
  if "o1" in args.model or "gemma" in args.model:
    messages = [{"role": "user", "content": system_prompt + "\n" + user_prompt}]
    # print(messages)
  else:
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
  while True:
    response = client.chat.completions.create(
      model=args.model,
      messages=messages,
      temperature=0.7,
      max_tokens=500
    )
    # print(response.choices[0].message.content)
    # print(response)
    intent = response.choices[0].message.content
    print(intent)

    if args.cot != True:
      intent = intent.replace("\"", ".").replace("*", ".").replace(":", ".").replace(".", ".").replace("-", ".").replace(",", ".").split(".")[0].strip().split("\n")[0]
      # print(intent)
    else:
      try:
        if "The answer is" in intent:
          intent = intent.split("The answer is")[1].replace("\"", "").replace("*", "").replace(":", "").replace(".", "").replace("-", "").replace(",", "").strip().split(" ")[0]
        elif "the answer is" in intent:
          intent = intent.split("the answer is")[1].replace("\"", "").replace("*", "").replace(":", "").replace(".", "").replace("-", "").replace(",", "").strip().split(" ")[0]
        else:
          for a in answer_set:
            if a.lower() in intent.lower():
              intent = intent.replace("\"", "").replace("*", "").replace(":", "").replace(".", "").replace("-", "").replace(",", "").strip().split(" ")[0]
  
      except:
        intent = "Z"
      
    if intent in letters:
      break
    # else:
    # break
  return intent


def options():
    parser = argparse.ArgumentParser()
    ## setting
    parser.add_argument("--dataset", type=str, default="behavior_qa")
    parser.add_argument("--model", type=str, choices=
                        ["meta-llama/Llama-3.1-8B-Instruct", "yi-lightning", 
                         "Qwen/Qwen2.5-7B-Instruct", "google/gemma-2-9b-it", "deepseek-chat",
                         "THUDM/glm-4-9b-chat", "internlm/internlm2_5-7b-chat", "mistralai/Mixtral-8x7B-Instruct-v0.1", "gpt-4o-mini",
                        "gpt-4o-2024-08-06", "o1-mini"])
    parser.add_argument("--cot", type=bool, default=False)
    args = parser.parse_args()
    return args

args = options()

def main():
    args = options()
    # device = "cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu"
    with open(f'./data/{args.dataset}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    if "deepseek" in args.model:
      API_BASE="https://api.deepseek.com/v1"
      API_KEY="sk-169c9341b3b948f987ef8b9a6d5fa3b0"

    else:
      API_BASE = "http://localhost:8000/v1"
      API_KEY = "token-abc123"

    if "gpt-4o" in args.model or "o1" in args.model:
      API_BASE = "https://api.vveai.com/v1/"
      API_KEY = ""
      openai.default_headers = {"x-foo": "true"}
    client = OpenAI(
      api_key=API_KEY,
      base_url=API_BASE
    )
    if not args.cot:
      file_path = f'./outputs/{args.model}/{args.dataset}.csv'
    else:
      file_path = f'./outputs/{args.model}/{args.dataset}_cot.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file)
      writer.writerow(['dialogue_id', 'labels', 'predictions'])
    answers = []
    correct = 0
    incorrect = 0


    for problem in tqdm(data):
      intent = evaluate(args, client, problem)
      dialogue_id = problem['dialogue_id']
      answers.append([dialogue_id, problem['answerKey'], intent])
      if intent == problem['answerKey']:
          correct += 1
      else:
          incorrect += 1
      print(f"Accuracy: {correct / (correct + incorrect)}")
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(answers)

if __name__ == "__main__":
    main()
