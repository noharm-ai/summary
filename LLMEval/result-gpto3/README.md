## Diagnosis Summary Evaluation

| F1 Score o3* | F1 Score 4o** | Model               | Correctness***  | Completeness***  |
|-------------:|--------------:|---------------------|----------------:|-----------------:|
| 0.903-0.905  | 0.790-0.843   | GPT o3              |
| 0.890-0.890  |               | Opus 4.1            |
| 0.885-0.904  | 0.755-0.812   | GPT o1              |
| 0.868-0.868  | 0.776-0.809   | Opus 4              | 0.79            | 0.87
| 0.864-0.869  | 0.727-0.781   | Sonnet 3.5 v2       | 0.79            | 0.88
| 0.860-0.870  | 0.763-0.774   | GPT o4-mini         |
| 0.859-0.888  | 0.830-0.834   | Sonnet 4            | 0.85            | 0.94
| 0.852-0.861  | 0.726-0.791   | Sonnet 3.5 v1       | 0.88            | 0.84
| 0.842        | 0.842         | Human Physician     |
| 0.830-0.845  | 0.762-0.810   | Sonnet 3.7          | 0.88            | 0.90
| 0.829-0.836  | 0.749-0.772   | GPT 4.1             |
| 0.819-0.830  | 0.692-0.752   | Llama 4 Mav 402B    | 0.85            | 0.90
| 0.816-0.849  | 0.684-0.727   | GPT 4o              |
| 0.813-0.818  | 0.708-0.764   | Llama 3.1 405B      |
| 0.775-0.783  | 0.674-0.735   | Llama 4 Scout 109B  | 0.74            | 0.84
| 0.748-0.764  | 0.683-0.716   | Amazon Nova Premier | 0.79            | 0.82
| 0.726-0.742  | 0.610-0.628   | Llama 3.3 70B       | 0.53            | 0.72
| 0.717-0.721  | 0.641-0.657   | Llama 3.1 70B       | 0.56            | 0.60
| 0.696-0.707  | 0.624-0.657   | Amazon Nova Pro     | 0.53            | 0.75
| 0.642-0.679  | 0.621-0.637   | Sabia 3             |
| 0.633-0.765  | 0.638-0.643   | GPT 3.5 T           |
| 0.630-0.646  | 0.573-0.597   | Mistral Large 24    | 0.53            | 0.76
| 0.603-0.618  | 0.649-0.670   | DeepSeek R1         | 0.68            | 0.84
| 0.586-0.605  | 0.600-0.634   | Sabia 3.1           |


\*  using our eval script and GPT-o3 zero-shot as a judge (worst and best model evaluation)

\**  using our eval script and GPT-4o few-shot as a judge (worst and best model evaluation)

\*** using [AWS Bedrock Evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html) w/ Sonnet 3.5 v2 as a judge