# XLinear: Frequency-Enhanced MLP with CrossFilter for Robust Long-Range Forecasting

Predicting the future is hard—just ask anyone who's tried to forecast the weather, stock prices, or next week's anime episode popularities. Time series forecasting is everywhere: from supply chain planning to energy grid management, from epidemiological modeling to financial trading. Traditional deep learning approaches like LSTMs and Transformers have made strides, but they often struggle with **long-range dependencies**—those subtle patterns that unfold over weeks, months, or even years. Enter XLinear, a clever new architecture that supercharges the humble multi-layer perceptron (MLP) with **frequency-domain processing** and a **CrossFilter** mechanism. It's proof that sometimes the best innovations aren't about making models bigger, but about making them smarter about *what* to learn and *how* to combine information across time scales.

## The Trouble with Plain MLPs for Time Series

MLPs are simple: they take a vector of inputs, apply some linear layers and nonlinearities, and output predictions. They're fast, stable, and easy to train. But when you feed them raw time series data (a sliding window of past observations), they treat each timestep as just another feature. They don't inherently understand that nearby points are correlated, that there are seasonal cycles (daily, weekly, yearly), and that long-term trends interact with short-term noise. For long-range forecasting (predicting dozens or hundreds of steps ahead), plain MLPs tend to either:
- **Forget** distant but important context
- **Over-smooth** and lose sharp events
- **Blow up** with unstable predictions

They're like someone trying to predict next year's weather by only looking at yesterday's temperatures—they miss the big picture.

## Frequency-Enhanced Learning: See the Forest and the Trees

XLinear's first insight: **transform the time series into the frequency domain** (via Fourier or wavelet transforms). In frequency space, periodic patterns become sharp peaks—annual seasonality, weekly cycles, daily rhythms—each at their own frequency bin. This makes it much easier for a model to isolate and model each component separately. The architecture includes a frequency encoder that:
- Decomposes the input window into amplitude and phase spectra
- Learns to emphasize frequencies that carry predictive signal
- Suppresses noisy or irrelevant frequencies

By working in both time and frequency simultaneously (a dual-branch design), XLinear captures both **local temporal dynamics** and **global periodic structure**. The result is a richer representation that doesn't lose long-range context just because it's far in the past.

## CrossFilter: Letting Time Scales Talk to Each Other

But frequency decomposition alone isn't enough—you still need to recombine those components intelligently. That's where the **CrossFilter** comes in. It's a specialized module that performs **cross-scale interactions** between the time-domain and frequency-domain features. Think of it as a mixer board:
- Low-frequency trends (e.g., overall growth) modulate the amplitude of higher-frequency cycles
- Sudden events in time domain can temporarily shift phase relationships
- Seasonal patterns can be amplified or dampened based on current conditions

CrossFilter uses lightweight gating and attention mechanisms (but no heavy self-attention matrices) to let information flow across scales without blowing up compute. This is key: it's **efficient** yet expressive enough to capture complex temporal hierarchies.

## Why XLinear Shines for Long Horizons

The paper evaluates XLinear on multiple long-horizon benchmarks (electricity, traffic, weather, exchange rates). Results:
- **Accuracy**: Consistently lower MAE/MSE than vanilla MLPs, and competitive with (or better than) sophisticated Transformers like Informer or Autoformer, especially on very long horizons (H=96, 192, 336, 720 steps).
- **Efficiency**: Much faster training and inference than attention-based models, because CrossFilter avoids quadratic complexity. It scales linearly with sequence length, making it practical for production.
- **Robustness**: Less sensitive to window size choice; performs well even with shorter historical windows, because frequency features compensate.
- **Interpretability**: The frequency decomposition means you can actually look at which frequencies the model is using—a nice bonus for debugging.

The combination of frequency enhancement and cross-filtering gives MLPs a fighting chance on tasks where traditional sequence models either overfit or forget.

## The Bigger Picture: Rethinking Inductive Biases

XLinear's contribution isn't just a new architecture—it's a **design pattern**: for sequential data, explicitly encode the **temporal scale structure** (via frequency or other multi-resolution transforms) and then build modules that **mix information across scales**. This principle could apply beyond forecasting to other time series tasks: anomaly detection, segmentation, imitation learning. It also suggests that maybe we've been overcomplicating things with full self-attention; sometimes a well-designed filter that respects the signal's structure is all you need.

## Conclusion

Long-range time series forecasting is a tough nut to crack because you need to balance short-term precision with long-term trends. XLinear shows that a thoughtfully enhanced MLP—armed with frequency processing and a CrossFilter—can outperform much larger, more complex models. It's a reminder that in machine learning, as in engineering, **understanding your data's structure** and building models that respect that structure often beats brute force. For practitioners who need accurate, efficient, and interpretable forecasts, XLinear is a compelling addition to the toolkit. The future of forecasting might be simpler than we thought—and that's a beautiful thing. (◕‿◕)♡