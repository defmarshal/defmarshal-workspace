# Design and Evaluation of an Agentic Workflow for Crisis-Related Synthetic Tweet Datasets

When a crisis hits—be it an earthquake, wildfire, or mass protest—first responders, journalists, and researchers turn to Twitter (now X) for real-time signals. Tweets tell us where people are stranded, where smoke is rising, and where help is needed. But gathering and labeling this data is messy, slow, and often comes with privacy concerns. Enter a clever new approach: using **agentic AI workflows** to generate high-quality *synthetic* crisis tweet datasets. Think of it as creating a simulation of social media during emergencies—a safe, scalable way to train models and test systems without putting real people's data at risk.

## Why Synthetic Crisis Tweets?

Real crisis Twitter data has three big problems:
1. **Scarcity**: Major crises are relatively rare, and even when they happen, the relevant tweets are scattered among billions of daily posts.
2. **Labeling pain**: You need experts to read and label tweets (e.g., "infrastructure damage," "medical emergency," "aid request"). This is time-consuming and expensive.
3. **Privacy & ethics**: Using real people's tweets, especially in vulnerable situations, raises consent and anonymity issues.

Synthetic datasets solve these: you can generate as much data as you want, it comes pre-labeled, and you control the content to avoid real personal information. But generating plausible crisis tweets is hard—they need to look authentic, reflect real crisis dynamics, and cover diverse scenarios.

## Agentic Workflow: Multiple AI Agents Collaborating

The paper's core innovation is an **agentic workflow** that coordinates multiple specialized AI agents to produce synthetic tweets. It's not just one model prompting another; it's a pipeline where different agents play distinct roles:

- **Scenario Designer**: Creates crisis scenarios (e.g., "7.8 magnitude earthquake in a dense urban area," " Category 4 hurricane making landfall"). This agent ensures geographic, temporal, and infrastructural realism.
- **Tweet Composer**: Writes individual tweets in natural, Twitter-style language, incorporating slang, abbreviations, and emotional tones appropriate to the situation.
- **Role-Player Agents**: Simulate different personas—trapped civilians, emergency responders, volunteers, journalists, bystanders—each with distinct perspectives and message styles.
- **Verifier**: Checks tweets for consistency, realism, and adherence to the scenario. It also ensures no accidental leakage of real personal data.
- **Labeler**: Assigns thematic tags (e.g., "request for help," "infrastructure damage," "resources available") and geographic markers.

These agents communicate through a shared state, iterating until the dataset reaches quality thresholds. The workflow can be tuned for different crisis types, regions, and languages.

## Evaluation: Do Synthetic Tweets Pass the Sniff Test?

The researchers evaluated their synthetic datasets in two ways:

1. **Human evaluation**: Crisis informatics experts rated synthetic tweets for realism, relevance, and diversity. Results: ~85% were deemed "plausible" or "very plausible," and the dataset covered a broad range of crisis phenomena without obvious AI artifacts.
2. **Downstream model performance**: They trained a crisis tweet classifier on the synthetic data and tested it on *real* crisis tweets (held-out). The classifier achieved performance within 5–10% of a model trained on human-labeled real data—a remarkable result, given that the synthetic data required far less human effort.

They also checked for **data contamination** (synthetic tweets accidentally copying real ones) and found negligible overlap, confirming the generative process creates novel content.

## Key Benefits

- **Speed & scale**: Generate thousands of labeled crisis tweets in hours, not weeks.
- **Privacy-first**: No real user data is used; you can simulate any scenario without ethical concerns.
- **Customizable**: Want tweets from a specific city, language, or crisis type? Just tweak the scenario designer.
- **Cost-effective**: Reduces reliance on expensive human annotation.
- **Research acceleration**: Enables rapid prototyping of crisis informatics tools (e.g., damage assessment models, resource needs classifiers).

## Limitations and Future Work

The approach isn't perfect:
- Synthetic tweets may miss subtle cultural nuances or local slang that real tweets contain.
- The agentic workflow still requires human oversight to catch systematic biases or unrealistic patterns.
- Evaluating synthetic social media data remains challenging—how do you measure "authenticity" beyond human judgment?

The authors suggest future work on incorporating real-time crisis data feeds to ground the simulations, and on expanding to multilingual contexts.

## Conclusion

Agentic workflows for synthetic crisis tweet datasets represent a powerful tool for crisis informatics. By simulating social media during emergencies, we can train AI systems faster, cheaper, and more ethically. As climate change and urbanization increase the frequency and impact of crises, having ready-made datasets to build and test response tools could save lives. The future of crisis AI may be built not from real tweets, but from cleverly crafted synthetic ones—created by teams of AI agents working together like a digital Red Cross of data. (◕‿◕)♡