## **Train TabICL model**

Import required packages and additionally split train into `train` and `validation` splits. You will be using `validation` split later for hyperparameter tuning. 

><code-in-title>Code-in</code-in-title>
>```python
>import torch
>import pandas as pd
>from tabicl import TabICLClassifier
>from sklearn.model_selection import train_test_split
>from sklearn.metrics import classification_report
>
># load train embeddings
>train_emb = torch.load("train.pt")
>X_train_val = pd.DataFrame({k: v.numpy() for k, v in train_emb.items()}).T
>
># load test embeddings
>test_emb = torch.load("test.pt")
>X_test = pd.DataFrame({k: v.numpy() for k, v in test_emb.items()}).T
>```
{: .code-in}

> ## Prepare train and validation splits
> 1. Split the train into **training** and **validation** subsets:  
>    - Use `sklearn.model_selection.train_test_split` for a random split.  
>    - Alternatively, use `sklearn.model_selection.GroupShuffleSplit` with the `groups` parameter set to `X_train_val["bgc"]` to ensure that entries from the same biosynthetic gene cluster (BGC) are kept in the same split, maintaining a balanced class distribution.  
> 2. Extract the corresponding labels for each split to create `y_train` and `y_val` sets.  
> 3. Verify that the number of samples in `X_train`, `X_val`, `y_train`, and `y_val` are consistent.
>
{: .hands_on}

> ## Pitfall #2: Data Leakage
> **Data leakage** occurs when information (samples) from the validation or test set present in the training process. In our case, leakage could happen if protein sequences from the same **BGC class** are present in both the training and validation splits. This leads to overly optimistic results, as the model indirectly "sees" validation data during training.  
> 
> **How to avoid it:**  
> - Use `GroupShuffleSplit` with the `bgc` column as the grouping variable to ensure that all sequences from the same BGC remain in a single split.  
> - Always double-check splits to confirm no overlap of BGC identifiers between training and validation datasets.  
>
> For more information about pitfalls in machine learning applications in genomics, please read this [article](https://www.nature.com/articles/s41576-021-00434-9)
> 
{: .tip}

The code below will automatically download the pre-trained checkpoint from the Hugging Face Hub on first use and choose a GPU if available:

```python
clf = TabICLClassifier(device="cuda:0")
# clf = TabICLClassifier() # to train on CPU
```

TabICL offers a set of hyperparameters to tune which can be checked using `.get_params` method.

```python
clf.get_params()

{'allow_auto_download': True,
 'average_logits': True,
 'batch_size': 8,
 'checkpoint_version': 'tabicl-classifier-v1.1-0506.ckpt',
 'class_shift': True,
 'device': 'cuda:0',
 'feat_shuffle_method': 'latin',
 'inference_config': None,
 'model_path': None,
 'n_estimators': 32,
 'n_jobs': None,
 'norm_methods': None,
 'outlier_threshold': 4.0,
 'random_state': 42,
 'softmax_temperature': 0.9,
 'use_amp': True,
 'use_hierarchical': True,
 'verbose': False}
```

However, TabICL can produce good predictions without hyperparameter tuning, unlike classical methods that require extensive tuning for optimal performance. 

> ## Train TabICL with the default hyperparameters
> 1. Train the classifier with the default parameters.
> 2. Make predictions on the validation set.
> 3. Generate the classification report using `sklearn.metrics.classification_report` or compute any additional metrics from `sklearn.metrics`. You can also save the report for later inspection. 
> 
>> ## Solution
>> ```python
>> clf.fit(X_train, y_train)
>> val_pred = clf.predict(X_val)
>> 
>> report = classification_report(y_val, val_pred, output_dict=True)
>> report = pd.DataFrame(report).transpose()
>> report.reset_index(inplace=True)
>> ```
> {: .solution}
>
{: .hands_on}

> ## Train TabICL with hyperparameter tuning
> 1. Experiment with different values for `n_estimators` (*e.g.*, [50, 100, 150]) and observe their effect on the classifier’s performance.  
> 2. Use `GridSearchCV` with `cv=10` to identify the optimal number of `n_estimators`.  
> 3. Evaluate the tuned model and generate performance reports for both the validation and test sets.  
> 4. *(Optional)* Visualize the results to compare model performance across different hyperparameter settings.  
>
{: .hands_on}

> ## Train TabICL with additional classes
> 1. Retrain the classifier using the more granular labels from the `class` column.  
> 2. Compare the model’s average performance when trained on `simple_class` vs. `class` to evaluate the impact of increased class granularity.  
> 3. *(Optional)* Tune hyperparameters to determine whether the overall performance improves.  
>
{: .hands_on}

Save the trained model using `joblib` library. You may choose other techniques of storing model, *e.g.* `pickle`.

```python
import joblib

joblib.dump(clf, "model.joblib")
```

Congratulations! You have learned how to set up the simple ML project. 
