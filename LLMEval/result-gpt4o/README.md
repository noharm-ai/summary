## Diagnosis Summary Evaluation

| F1 Score* | Model                | Correctness**  | Completeness**  |
|-----------|----------------------|---------------:|----------------:|
| 0.869     | GPT o1-preview       |
|           | Sonnet 3.7           | 0.88          | 0.90
| 0.842     | Human Physician      |
| 0.827     | Sonnet 3.5           | 0.88          | 0.84
|           | Sonnet 4             | 0.85          | 0.94
|           | Llama 4 Mav 17b      | 0.85          | 0.90
|           | Opus 4               | 0.79          | 0.87
|           | Nova Premier         | 0.79          | 0.82
|           | Llama 4 Scout 17b    | 0.74          | 0.84
| 0.800     | GPT4o                |
|           | DeepSeek R1          | 0.68          | 0.84
| 0.785     | DeepSeek V3          |
|           | Llama 3.3 70B        | 0.53          | 0.72
| 0.774     | Llama 3.1 405B       |
|           | Mistral Large 24     | 0.53          | 0.76
|           | Amazon Nova Pro      | 0.53          | 0.75
| 0.768     | Palm 2               |
| 0.764     | GPT 4.6              |
| 0.740     | GPT 3                |
| 0.726     | Llama 3              |
| 0.670     | Gemini Pro           |
| 0.666     | MariTalk 2           |
| 0.624     | MariTalk 2.5 Medium  |
| 0.571     | MariTalk 1           |

\*  using out eval script and GPT-4o as a judge

\** using [AWS Bedrock Evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html) w/ Sonnet 3.5 as a judge
