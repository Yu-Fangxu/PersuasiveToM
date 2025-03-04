model=$1
cot=$2
# Create a folder to contain the model output
mkdir -p ./logs/$model

# First set of evaluations
nohup python evaluation/evaluate.py --dataset desire_er --model $model  > ./logs/$model/desire_er.log 2>&1 

nohup python evaluation/evaluate.py --dataset belief_er --model $model  > ./logs/$model/belief_er.log 2>&1 

nohup python evaluation/evaluate.py --dataset intent_er --model $model  > ./logs/$model/intent_er.log 2>&1 

nohup python evaluation/evaluate.py --dataset intent_ee --model $model  > ./logs/$model/intent_ee.log 2>&1 

nohup python evaluation/evaluate.py --dataset belief_ee --model $model  > ./logs/$model/belief_ee.log 2>&1 

nohup python evaluation/evaluate.py --dataset desire_ee --model $model   > ./logs/$model/desire_ee.log 2>&1 

# Fourth set of evaluations
nohup python evaluation/evaluate.py --dataset behavior_qa --model $model  > ./logs/$model/behavior_qa.log 2>&1 

nohup python evaluation/evaluate.py --dataset judge_qa --model $model  > ./logs/$model/judge_qa.log 2>&1 

