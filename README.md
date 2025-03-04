# PersuasiveToM: A Benchmark for Evaluating Machine Theory of Mind in Persuasive Dialogues

We study the theory of mind (ToM) in persuasive dialogues. Specifically, we evaluate ToM reasoning and ToM applications. ToM reasoning evaluates the ability of LLMs for understanding mental states (belief, desire, intention) for both persuaders and perusadees. ToM application evaluates the ability of LLMs for applying the understanding of mental states for persuasion.

More details can be found in our paper:
Fangxu Yu, Lai Jiang, Shenyi Huang, Zhen Wu, Xinyu Dai, "[PersuasiveToM: A Benchmark for Evaluating Machine Theory of Mind in Persuasive Dialogues](https://arxiv.org/abs/2502.21017)" 

## PersuasiveToM

![plot](./assets/main_arch.png)

As illustrated in the above diagram, our EACL framework includes two steps: 
1. **Representation Learning**: composed of utterance representation learning and emotion anchor learning, which aims to guide LM to learn separable utterance representations.
2. **Emotion Anchor Adaptation**: is proposed to improve the classification ability of emotion anchors.

## Code
**1) Download this GitHub**
```
git clone https://github.com/Yu-Fangxu/EACL.git
```

**2) Setup Environment**

We recommend creating a new environment:
```bash
conda create -n EACL python==3.10
conda activate EACL
```

Then install all the dependencies:
```
pip install -r requirements.txt
```

**3) Run Command for EACL**

```
bash run.sh IEMOCAP|MELD|EmoryNLP 'princeton-nlp/sup-simcse-roberta-large'|'YuxinJiang/sup-promcse-roberta-large'|'microsoft/deberta-large'
```

You could choose one dataset from IEMOCAP | MELD | EmoryNLP, and choose one base model from SimCSE | PromCSE | Deberta

<br> **If you find our repository helpful to your research, please consider citing:** <br>
```
@article{yu2024emotion,
  title={Emotion-Anchored Contrastive Learning Framework for Emotion Recognition in Conversation},
  author={Yu, Fangxu and Guo, Junjie and Wu, Zhen and Dai, Xinyu},
  journal={arXiv preprint arXiv:2403.20289},
  year={2024}
}
```
