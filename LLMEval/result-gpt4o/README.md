## Diagnosis Summary Evaluation

| F1 Score* | Model                | Correctness**  | Completeness**  |
|-----------|----------------------|---------------:|----------------:|
| 0.863     | Sonnet 3.5           | 0.88          | 0.84
| 0.842     | Human Physician      |
| 0.830     | Sonnet 4             | 0.85          | 0.94
| 0.809     | Opus 4               | 0.79          | 0.87
| 0.790-0.843     | GPT o3               |
| 0.779     | Llama 3.1 405B       |
| 0.763-0.774     | GPT o4-mini          |
| 0.762-0.801     | Sonnet 3.7           | 0.88          | 0.90
| 0.755-0.812     | GPT o1               |
| 0.755     | DeepSeek V3          |
| 0.739     | GPT 4.6              |
| 0.716     | Amazon Nova Premier  | 0.79          | 0.82
| 0.692     | Llama 4 Mav 402B     | 0.85          | 0.90
| 0.684     | GPT 4o               |
| 0.674     | Llama 4 Scout 109B   | 0.74          | 0.84
| 0.670     | DeepSeek R1          | 0.68          | 0.84
| 0.667     | GPT 3                |
| 0.657     | Llama 3 70B          | 0.56          | 0.60
| 0.656     | Palm 2               |
| 0.653     | Gemini Pro           |
| 0.628     | Llama 3.3 70B        | 0.53          | 0.72
| 0.624     | Amazon Nova Pro      | 0.53          | 0.75
| 0.615     | MariTalk 2           |
| 0.613     | MariTalk 2.5 Medium  |
| 0.597     | Mistral Large 24     | 0.53          | 0.76
| 0.569     | MariTalk 1           |

\*  using our eval script and GPT-4o as a judge

\** using [AWS Bedrock Evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html) w/ Sonnet 3.5 v2 as a judge
