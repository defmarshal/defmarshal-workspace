Provider finish_reason: content_filter
# JAWS: Enhancing Long-term Rollout of Neural Operators via Spatially-Adaptive Jacobian Regularization

Imagine you're building a digital twin of Earth's climate. You train a neural network to predict weather patterns, and it works beautifully—for a few days. But after a week, the forecasts go off the rails, predicting hurricanes in deserts and sunshine in monsoons. Why? Because small errors compound, like a tiny lie that becomes an unbelievable story after many retellings. Now, a new technique called **JAWS** (Jacobian-Adaptive Weighted Smoothing) gives these AI weather prophets a much longer leash—by teaching them to stay grounded in reality, step after step.

## The Problem: Error Explosion in Long Rollouts

Neural operators—AI models that simulate physical systems—are revolutionizing fields from climate science to aerospace. Instead of solving complex differential equations, they learn from data and can simulate much faster. But there's a catch: when you chain many predictions together (an "autoregressive rollout"), tiny inaccuracies at each step accumulate, often growing exponentially. After a few dozen steps, the simulation diverges completely from true physics. It's like a photocopier making copies of copies—the image degrades with each generation.

## The Insight: Tame the Jacobian

The root cause? The model's Jacobian matrix—the set of partial derivatives that describes how small changes in input propagate to output. If the Jacobian has eigenvalues > 1, errors amplify. JAWS addresses this by adding a **spatially-adaptive Jacobian regularization** during training.

What does that mean in plain English? JAWS tells the neural operator: "Hey, be careful! Don't let errors grow too fast in any region of your input space." It does this adaptively: some parts of the state (like stable atmospheric layers) can tolerate a bit of error; others (like thunder